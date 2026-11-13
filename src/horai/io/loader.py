"""
Loading of the files of a plan into typed records.

Each file is parsed, checked for its `_schema`, and validated against the schema of its type, then
converted into records. A file that fails any of these steps is reported as an issue and excluded:
its identifier joins `Plan.excluded`, so that a computation that needs it reports itself undefined
instead of running on a partial plan.

Functions
---------
load_plan(folder, schemas) -> tuple[Plan, list[Issue]]
    Load every file of the plan in `folder`.
"""

from __future__ import annotations

import re
from collections.abc import Callable
from pathlib import Path
from typing import Any

import yaml

from ..domain.records import (
    Appointment,
    Availability,
    ClockEntry,
    Cycle,
    DecisionEntry,
    Deliverable,
    DeviationEntry,
    Item,
    Plan,
    Profile,
    Purpose,
    Task,
    Week,
    WeekTemplate,
    Block,
    Window,
)
from ..domain.time import parse_date, parse_duration, parse_time
from ..issues import Issue
from .schemas import SchemaSet
from .yaml_loader import load_yaml

_SLUG = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
_MONTH = re.compile(r"^\d{4}-\d{2}$")

SINGLE_FILES: dict[str, str] = {
    "profile.yml": "horai:profile@1",
    "availability.yml": "horai:availability@1",
    "calendar/week-template.yml": "horai:week-template@1",
    "capture/inbox.yml": "horai:inbox@1",
    "capture/holding.yml": "horai:holding@1",
    "capture/ideas.yml": "horai:ideas@1",
    "capture/archive.yml": "horai:archive@1",
}

FOLDERS: dict[str, str] = {
    "plan/purposes": "horai:purpose@1",
    "plan/deliverables": "horai:deliverable@1",
    "plan/milestones": "horai:milestone@1",
    "plan/questions": "horai:question@1",
    "plan/standing": "horai:standing@1",
    "calendar/cycles": "horai:cycle@1",
    "calendar/weeks": "horai:week@1",
    "calendar/appointments": "horai:appointment@1",
    "log/clock": "horai:clock-log@1",
    "log/decisions": "horai:decision-log@1",
    "log/deviations": "horai:deviation-log@1",
}

_TITLED = {
    "plan/purposes",
    "plan/deliverables",
    "plan/milestones",
    "plan/questions",
    "plan/standing",
    "calendar/appointments",
}
_LOGS = {"log/clock", "log/decisions", "log/deviations"}


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


def _deadline(data: dict[str, Any]) -> Any:
    """Return the date of the deadline of a level, or None."""
    return parse_date(data["deadline"]["date"]) if "deadline" in data else None


def _week(data: dict[str, Any]) -> Week:
    """Build a week, with its departures from the template when it states any."""
    blocks = tuple(Block.from_data(e) for e in data["blocks"]) if "blocks" in data else None
    windows = tuple(Window.from_data(e) for e in data["windows"]) if "windows" in data else None
    return Week(opened=parse_date(data["opened"]), blocks=blocks, windows=windows)


def _store(plan: Plan, folder: str, stem: str, data: dict[str, Any]) -> None:
    """Convert one validated file of a folder into records of the plan."""
    builders: dict[str, Callable[[], None]] = {
        "plan/purposes": lambda: plan.purposes.__setitem__(
            stem, Purpose(stem, data["title"], _deadline(data))
        ),
        "plan/deliverables": lambda: plan.deliverables.__setitem__(
            stem,
            Deliverable(
                stem, data["title"], data["purpose"], data["phase"], data["status"], _deadline(data)
            ),
        ),
        "plan/milestones": lambda: plan.items.__setitem__(
            stem, Item.from_data(stem, "milestone", data)
        ),
        "plan/questions": lambda: plan.items.__setitem__(
            stem, Item.from_data(stem, "question", data)
        ),
        "plan/standing": lambda: plan.items.__setitem__(
            stem, Item.from_data(stem, "standing", data)
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
        "calendar/weeks": lambda: plan.weeks.__setitem__(parse_date(data["opened"]), _week(data)),
        "calendar/appointments": lambda: plan.appointments.__setitem__(
            stem,
            Appointment(
                stem,
                data["title"],
                parse_date(data["date"]),
                parse_time(data["start"]),
                parse_duration(data["length"]),
                data["stream"],
                data["party"],
                parse_duration(data["cap"]) if "cap" in data else None,
            ),
        ),
    }
    if folder in builders:
        builders[folder]()
    elif folder == "log/clock":
        plan.clock += tuple(ClockEntry.from_data(e) for e in data["entries"])
    elif folder == "log/decisions":
        plan.decisions += tuple(
            DecisionEntry(parse_date(e["date"]), e["milestone"], e["decision"], e.get("rationale"))
            for e in data["entries"]
        )
    elif folder == "log/deviations":
        plan.deviations += tuple(
            DeviationEntry(parse_date(e["date"]), e["policy"], e["deviation"], e.get("cycle"))
            for e in data["entries"]
        )


def _store_single(plan: Plan, relative: str, data: dict[str, Any]) -> None:
    """Convert one validated single file into records of the plan."""
    if relative == "profile.yml":
        plan.profile = Profile.from_data(data)
    elif relative == "availability.yml":
        plan.availability = Availability.from_data(data)
    elif relative == "calendar/week-template.yml":
        plan.template = WeekTemplate.from_data(data)
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
    opened, month = data.get("opened"), data.get("month")
    if folder in _TITLED and not _SLUG.match(stem):
        return [Issue("identifier/form", f"the file name {stem!r} must be a slug", relative, stem)]
    if folder == "calendar/weeks" and data["opened"] != stem:
        return [
            Issue(
                "identifier/week",
                f"a week file must be named by its date {opened}",
                relative,
            )
        ]
    if folder in _LOGS and (not _MONTH.match(stem) or data["month"] != stem):
        return [
            Issue(
                "identifier/month",
                f"a log file must be named by its month {month}",
                relative,
            )
        ]
    return []


def load_plan(folder: Path, schemas: SchemaSet) -> tuple[Plan, list[Issue]]:
    """Load every file of the plan in `folder`.

    Parameters
    ----------
    folder : Path
        Folder of the plan.
    schemas : SchemaSet
        Validators of the record types.

    Returns
    -------
    tuple[Plan, list[Issue]]
        The records of the valid files, and the issues of the invalid ones.
    """
    plan, issues = Plan(), []
    for relative, schema_id in SINGLE_FILES.items():
        path = folder / relative
        if not path.is_file():
            if relative == "profile.yml":
                issues.append(
                    Issue("plan/profile-missing", "the plan has no profile.yml", relative)
                )
            continue
        data, problems = _read(path, relative, schema_id, schemas)
        issues += problems
        if data is not None:
            _store_single(plan, relative, data)
    for sub, schema_id in FOLDERS.items():
        directory = folder / sub
        if not directory.is_dir():
            continue
        for path in sorted(directory.glob("*.yml")):
            relative, stem = f"{sub}/{path.name}", path.stem
            data, problems = _read(path, relative, schema_id, schemas)
            if data is not None:
                problems += _name_issues(sub, stem, relative, data)
            issues += problems
            if problems or data is None:
                plan.excluded.add(stem)
                continue
            _store(plan, sub, stem, data)
            plan.sources[stem] = relative
            for task in data.get("tasks", ()):
                plan.sources.setdefault(task["id"], relative)
    for task in plan.holding:
        plan.sources.setdefault(task.id, "capture/holding.yml")
    return plan, issues
