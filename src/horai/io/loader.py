"""
Loading of the files of a plan into typed records.

Each file is parsed, checked for its `_schema`, and validated against the schema of its type, then
converted into records. A file that fails any of these steps is reported as an issue and excluded:
its identifier joins `Plan.excluded`, so that a computation that needs it reports itself undefined
instead of running on a partial plan. In a store of actions, an invalid milestone, question or
loose task is excluded alone, with its tasks.

Classes
-------
Discovery
    Where the distributed records are found.

Functions
---------
load_plan(folder, schemas, discovery) -> tuple[Plan, list[Issue]]
    Load every file of the plan in `folder`.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
import re
from fnmatch import fnmatch
from collections.abc import Callable, Sequence
from pathlib import Path, PurePath
from typing import Any

import yaml

from ..domain.records import (
    ItemKind,
    Absence,
    ClockEntry,
    Cycle,
    DayChange,
    Deadline,
    DecisionEntry,
    Deliverable,
    DeviationEntry,
    Item,
    Party,
    PartyRef,
    Plan,
    Profile,
    Purpose,
    Task,
    TypicalWeek,
    stages_from,
)
from ..domain.time import parse_date
from ..issues import Issue
from .config import ACTIONS_FILE, CONFIG_SCHEMA
from .schemas import SchemaSet
from .yaml_loader import load_yaml

_SLUG = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
_MONTH = re.compile(r"^\d{4}-\d{2}$")

SINGLE_FILES: dict[str, str] = {
    "settings/profile.yml": "horai:profile@1",
    "settings/parties.yml": "horai:parties@1",
    "settings/typical-week.yml": "horai:typical-week@1",
    "capture/inbox.yml": "horai:inbox@1",
    "capture/holding.yml": "horai:holding@1",
    "capture/ideas.yml": "horai:ideas@1",
    "capture/archive.yml": "horai:archive@1",
}

FOLDERS: dict[str, str] = {
    "plan/purposes": "horai:purpose@1",
    "plan/deliverables": "horai:deliverable@1",
    "calendar/cycles": "horai:cycle@1",
    "calendar/dates": "horai:dates@1",
    "log/clock": "horai:clock-log@1",
    "log/decisions": "horai:decision-log@1",
    "log/deviations": "horai:deviation-log@1",
    "log/reviews": "horai:review-log@1",
}

_TITLED = {"plan/purposes", "plan/deliverables"}
ACTIONS = "horai:actions@1"
_LOCATION = re.compile(r"^(milestones|questions|tasks)/(\d+)(/|:)")
_MONTHLY = {"calendar/dates", "log/clock", "log/decisions", "log/deviations", "log/reviews"}


def _read(
    path: Path, relative: str, schema_id: str, schemas: SchemaSet
) -> tuple[dict[str, Any] | None, list[Issue]]:
    """Parse one file and validate it; return its content, or None with the issues found."""
    try:
        data = load_yaml(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, yaml.YAMLError) as error:
        return None, [Issue("file/unreadable", f"cannot be read as YAML: {error}", relative)]
    if not isinstance(data, dict):
        return None, [Issue("file/not-a-record", "the file must hold a mapping", relative)]
    if data.get("_schema") != schema_id:
        found = data.get("_schema", "nothing")
        return None, [
            Issue("schema/type", f"the key _schema must hold {schema_id}, not {found}", relative)
        ]
    problems = [
        Issue("schema/invalid", message, relative) for message in schemas.errors(schema_id, data)
    ]
    return (None, problems) if problems else (data, [])


def _parse(path: Path, relative: str, schema_id: str) -> tuple[dict[str, Any] | None, list[Issue]]:
    """Parse one file and check its type, without validating its content."""
    try:
        data = load_yaml(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, yaml.YAMLError) as error:
        return None, [Issue("file/unreadable", f"cannot be read as YAML: {error}", relative)]
    if not isinstance(data, dict):
        return None, [Issue("file/not-a-record", "the file must hold a mapping", relative)]
    if data.get("_schema") != schema_id:
        found = data.get("_schema", "nothing")
        return None, [
            Issue("schema/type", f"the key _schema must hold {schema_id}, not {found}", relative)
        ]
    return data, []


def _entry_ids(data: dict[str, Any]) -> list[str]:
    """Return the identifiers of the items and of the tasks that a store states, valid or not."""
    names = []
    for key in ("milestones", "questions", "tasks"):
        for entry in data.get(key) or ():
            if isinstance(entry, dict) and isinstance(entry.get("id"), str):
                names.append(entry["id"])
            if key != "tasks" and isinstance(entry, dict):
                names += [
                    t["id"]
                    for t in entry.get("tasks") or ()
                    if isinstance(t, dict) and isinstance(t.get("id"), str)
                ]
    return names


def _store_actions(
    plan: Plan, data: dict[str, Any], relative: str, invalid: set[tuple[str, int]]
) -> None:
    """Convert the valid entries of a store of actions into records of the plan."""
    kinds: tuple[tuple[str, ItemKind], ...] = (
        ("milestones", "milestone"),
        ("questions", "question"),
    )
    for key, kind in kinds:
        for index, entry in enumerate(data.get(key) or ()):
            if (key, index) in invalid:
                continue
            item = Item.from_data(kind, entry)
            plan.items[item.id] = item
            plan.sources[item.id] = relative
            for task in item.tasks:
                plan.sources.setdefault(task.id, relative)
    for index, entry in enumerate(data.get("tasks") or ()):
        if ("tasks", index) in invalid:
            continue
        task = Task.from_data(entry, None)
        plan.loose += (task,)
        plan.sources.setdefault(task.id, relative)


def _deadline(data: dict[str, Any]) -> Deadline | None:
    """Return the deadline of a level, or None."""
    return Deadline.from_data(data.get("deadline"))


def _store(plan: Plan, folder: str, stem: str, data: dict[str, Any]) -> None:
    """Convert one validated file of a folder into records of the plan."""
    builders: dict[str, Callable[[], None]] = {
        "plan/purposes": lambda: plan.purposes.__setitem__(
            stem, Purpose(stem, data["title"], data.get("description"), _deadline(data))
        ),
        "plan/deliverables": lambda: plan.deliverables.__setitem__(
            stem,
            Deliverable(
                stem,
                data["title"],
                data["purpose"],
                data["type"],
                data["status"],
                data.get("phase"),
                (stages_from(data["stages"]) if "stages" in data else None),
                PartyRef.from_data(data.get("accountable_to")),
                _deadline(data),
                data.get("derived_from"),
            ),
        ),
        "calendar/cycles": lambda: plan.cycles.__setitem__(
            stem,
            Cycle(
                stem,
                parse_date(data["start"]),
                parse_date(data["end"]),
                (
                    (parse_date(data["cool_down"][0]), parse_date(data["cool_down"][1]))
                    if "cool_down" in data
                    else None
                ),
            ),
        ),
    }
    if folder in builders:
        builders[folder]()
    elif folder == "log/clock":
        plan.clock += tuple(ClockEntry.from_data(e) for e in data["entries"])
    elif folder == "log/decisions":
        plan.decisions += tuple(
            DecisionEntry(
                parse_date(e["date"]), e["milestone"], e["checkpoint_decision"], e.get("rationale")
            )
            for e in data["entries"]
        )
    elif folder == "calendar/dates":
        plan.dates.update(
            (parse_date(day), DayChange.from_data(entry))
            for day, entry in data.get("days", {}).items()
        )
        plan.absences += tuple(Absence.from_data(e) for e in data.get("unavailable", ()))
    elif folder == "log/reviews":
        plan.reviews = tuple(
            sorted({*plan.reviews, *(parse_date(e["date"]) for e in data["entries"])})
        )
    elif folder == "log/deviations":
        plan.deviations += tuple(
            DeviationEntry(parse_date(e["date"]), e["policy"], e["deviation"], e.get("cycle"))
            for e in data["entries"]
        )


def _store_single(plan: Plan, relative: str, data: dict[str, Any]) -> None:
    """Convert one validated single file into records of the plan."""
    if relative == "settings/profile.yml":
        plan.profile = Profile.from_data(data)
    elif relative == "settings/parties.yml":
        plan.parties = {entry["id"]: Party.from_data(entry) for entry in data["parties"]}
    elif relative == "settings/typical-week.yml":
        plan.typical_week = TypicalWeek.from_data(data)
    elif relative == "capture/inbox.yml":
        plan.inbox = tuple(data["entries"])
    elif relative == "capture/ideas.yml":
        plan.ideas = tuple(data["entries"])
    elif relative == "capture/holding.yml":
        plan.holding = tuple(Task.from_data(e, None) for e in data["tasks"])
    elif relative == "capture/archive.yml":
        plan.archive = tuple(Task.from_data(e, None) for e in data["tasks"])


def _name_issues(folder: str, stem: str, relative: str, data: dict[str, Any]) -> list[Issue]:
    """Check what the file layout fixes about the name of a file."""
    month = data.get("month")
    if folder in _TITLED and not _SLUG.match(stem):
        return [Issue("identifier/form", f"the file name {stem!r} must be a slug", relative, stem)]
    if folder in _MONTHLY and (not _MONTH.match(stem) or month != stem):
        return [
            Issue(
                "identifier/month",
                f"a file of a month must be named by its month {month}",
                relative,
            )
        ]
    dated = [
        *data.get("days", {}),
        *(entry["from"] for entry in data.get("unavailable", ())),
        *(entry["date"] for entry in data.get("entries", ()) if "date" in entry),
    ]
    if folder in ("calendar/dates", "log/reviews"):
        outside = [str(day) for day in dated if not str(day).startswith(f"{month}-")]
        if outside:
            listed = ", ".join(outside)
            message = f"the dates {listed} fall outside the month {month} of the file"
            return [Issue("calendar/month", message, relative)]
    return []


DISTRIBUTED: dict[str, str] = {
    schema_id: folder for folder, schema_id in FOLDERS.items() if folder in _TITLED
}
_SCHEMA_LINE = re.compile(r"^_schema:\s*['\"]?(horai:[a-z-]+@\d+)", re.MULTILINE)


def _skipped(relative: PurePath, exclude: Sequence[str]) -> bool:
    """Whether a path under a root lies in a hidden or an excluded folder.

    A pattern without a slash matches a folder name at any depth, as in `.gitignore`; a pattern
    with a slash matches a path from the root.

    Examples
    --------
    >>> _skipped(PurePath("projects/x/archive/a.yml"), ["archive"])
    True
    >>> _skipped(PurePath("utils/scripts/tests/a.yml"), ["utils/scripts/tests"])
    True
    >>> _skipped(PurePath("conferences/a.yml"), ["archive"])
    False
    """
    folders = relative.parts[:-1]
    if any(part.startswith(".") for part in folders):
        return True
    posix = relative.as_posix()
    for pattern in exclude:
        if "/" not in pattern.strip("/"):
            if any(fnmatch(part, pattern.strip("/")) for part in folders):
                return True
        elif fnmatch(posix, pattern.rstrip("/") + "/*"):
            return True
    return False


class _Loader:
    """The state of one loading: the plan built so far, its issues, and the files already read."""

    def __init__(self, schemas: SchemaSet) -> None:
        self.schemas = schemas
        self.plan = Plan()
        self.issues: list[Issue] = []
        self.loaded: set[Path] = set()

    def single_file(self, path: Path, relative: str, schema_id: str) -> None:
        """Load one central file of a single record."""
        self.loaded.add(path.resolve())
        data, problems = _read(path, relative, schema_id, self.schemas)
        self.issues += problems
        if data is not None:
            _store_single(self.plan, relative, data)

    def folder_file(self, path: Path, sub: str, relative: str) -> None:
        """Load one file of the kind that the folder `sub` holds, or record why it is excluded."""
        self.loaded.add(path.resolve())
        stem = path.stem
        data, problems = _read(path, relative, FOLDERS[sub], self.schemas)
        if data is not None:
            problems += _name_issues(sub, stem, relative, data)
        self.issues += problems
        if problems or data is None:
            self.plan.excluded.add(stem)
            return
        _store(self.plan, sub, stem, data)
        self.plan.sources[stem] = relative

    def actions_file(self, path: Path, relative: str, actions_file: str) -> None:
        """Load one store of actions, and exclude each invalid entry alone.

        An error located in one milestone, question or loose task excludes that entry; any other
        error excludes the whole store.
        """
        self.loaded.add(path.resolve())
        data, problems = _parse(path, relative, ACTIONS)
        if data is None:
            self.issues += problems
            return
        if path.name != actions_file:
            message = f"a store of actions must be named {actions_file}, the name of every store"
            self.issues.append(Issue("identifier/actions-file", message, relative))
        invalid: set[tuple[str, int]] = set()
        whole = False
        for message in self.schemas.errors(ACTIONS, data):
            self.issues.append(Issue("schema/invalid", message, relative))
            match = _LOCATION.match(message)
            if match is None:
                whole = True
            else:
                invalid.add((match.group(1), int(match.group(2))))
        if whole:
            self.plan.excluded.update(_entry_ids(data))
            return
        for key, index in invalid:
            entry = (data.get(key) or [])[index]
            self.plan.excluded.update(_entry_ids({key: [entry]}))
        _store_actions(self.plan, data, relative, invalid)

    def discover(
        self, roots: Sequence[Path], exclude: Sequence[str], base: Path, actions_file: str
    ) -> None:
        """Load the records of the hierarchy found by their `_schema` under the roots."""
        for root in roots:
            for path in sorted(root.rglob("*.yml")):
                if path.resolve() in self.loaded or _skipped(path.relative_to(root), exclude):
                    continue
                try:
                    match = _SCHEMA_LINE.search(path.read_text(encoding="utf-8")[:2048])
                except (OSError, UnicodeDecodeError):
                    continue
                if match is None:
                    continue
                relative = os.path.relpath(path, base)
                schema_id = match.group(1)
                if schema_id == CONFIG_SCHEMA:
                    continue
                if schema_id == ACTIONS:
                    self.actions_file(path, relative, actions_file)
                elif schema_id in DISTRIBUTED:
                    self.folder_file(path, DISTRIBUTED[schema_id], relative)
                elif schema_id in FOLDERS.values() or schema_id in SINGLE_FILES.values():
                    self.loaded.add(path.resolve())
                    message = f"a record {schema_id} belongs to the central folder of the plan"
                    self.issues.append(Issue("placement/central", message, relative))
                else:
                    self.loaded.add(path.resolve())
                    message = f"the record type {schema_id} is unknown to this version of horai"
                    self.issues.append(Issue("schema/unknown", message, relative))


@dataclass(frozen=True)
class Discovery:
    """Where the records of the hierarchy are found, outside the central folder of a plan.

    Attributes
    ----------
    roots : Sequence[Path]
        Folders under which the records are found by their key `_schema`.
    exclude : Sequence[str]
        Patterns of paths, relative to a root, under which no record is sought.
    base : Path | None
        Folder against which the paths of the distributed records are reported; the central
        folder by default.
    actions_file : str
        Name of the file in which each folder, the central `plan/` included, keeps its actions.
    """

    roots: Sequence[Path] = ()
    exclude: Sequence[str] = ()
    base: Path | None = None
    actions_file: str = ACTIONS_FILE


def load_plan(
    folder: Path, schemas: SchemaSet, discovery: Discovery = Discovery()
) -> tuple[Plan, list[Issue]]:
    """Load the central folder of a plan, then the records found under its roots.

    Parameters
    ----------
    folder : Path
        Central folder of the plan.
    schemas : SchemaSet
        Validators of the record types.
    discovery : Discovery
        Where the distributed records are found, and the name of the stores of actions.

    Returns
    -------
    tuple[Plan, list[Issue]]
        The records of the valid files, and the issues of the invalid ones.
    """
    loading = _Loader(schemas)
    for relative, schema_id in SINGLE_FILES.items():
        path = folder / relative
        if path.is_file():
            loading.single_file(path, relative, schema_id)
        elif relative == "settings/profile.yml":
            loading.issues.append(
                Issue("plan/profile-missing", "the plan has no settings/profile.yml", relative)
            )
    for sub in FOLDERS:
        directory = folder / sub
        if directory.is_dir():
            for path in sorted(directory.glob("*.yml")):
                loading.folder_file(path, sub, f"{sub}/{path.name}")
    name = discovery.actions_file
    central = folder / "plan" / name
    if central.is_file():
        loading.actions_file(central, f"plan/{name}", name)
    loading.discover(discovery.roots, discovery.exclude, discovery.base or folder, name)
    for task in loading.plan.holding:
        loading.plan.sources.setdefault(task.id, "capture/holding.yml")
    return loading.plan, loading.issues
