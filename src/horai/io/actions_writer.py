"""
Writing of the milestone of a stage into the store of actions of a folder.

The milestone is appended to the list `milestones` of the store, which is created when absent. The
rest of the file, comments included, is left as written. The new content is parsed back, and must
hold the new milestone, before it replaces the file through a temporary file in the same folder.

Classes
-------
ActionsFileError
    A store of actions that the milestone cannot be appended to.

Functions
---------
milestone_entry(milestone, stream) -> dict
append_stage_milestone(store, milestone, stream) -> Path
"""

from __future__ import annotations

import os
import re
import tempfile
from pathlib import Path
from typing import Any

import yaml

from ..rules.stages import StageMilestone
from .yaml_loader import load_yaml

_MILESTONES = re.compile(r"^milestones:[ \t]*(\[[ \t]*\])?[ \t]*(#.*)?$", re.MULTILINE)
_TOP_KEY = re.compile(r"^[A-Za-z_][\w-]*:", re.MULTILINE)


class ActionsFileError(Exception):
    """A store of actions that the milestone cannot be appended to, with the exit status 2."""


def milestone_entry(milestone: StageMilestone, stream: str) -> dict[str, Any]:
    """Return the entry of the milestone of a stage, in the order of the form.

    Examples
    --------
    >>> from horai.domain.records import Deliverable, Stage
    >>> paper = Deliverable("ctx", "Geometry", "p", "paper", "active")
    >>> entry = milestone_entry(StageMilestone("ctx-draft", paper, Stage("draft", "delivery"),
    ...                                        "routine", "inquiry"), "inquiry")
    >>> entry["title"], entry["status"]
    ('Draft of Geometry', 'open')
    """
    stage = milestone.stage.id.replace("-", " ").capitalize()
    entry: dict[str, Any] = {
        "id": milestone.name,
        "title": f"{stage} of {milestone.deliverable.title}",
        "deliverable": milestone.deliverable.id,
        "stage": milestone.stage.id,
        "stream": stream,
        "status": "open",
    }
    if milestone.predictability is not None:
        entry["predictability"] = milestone.predictability
    return entry


def _block(entry: dict[str, Any]) -> str:
    """Write `entry` as one item of a list at the top level, indented by two spaces."""
    text = yaml.safe_dump([entry], sort_keys=False, allow_unicode=True, width=100)
    return "".join(f"  {line}\n" for line in text.splitlines())


def _appended(text: str, block: str) -> str:
    """Return `text` with `block` appended to its list `milestones`, which it creates if absent."""
    found = _MILESTONES.search(text)
    if found is None:
        return text + ("" if text.endswith("\n") or not text else "\n") + "milestones:\n" + block
    head = text[: found.start()] + "milestones:\n"
    rest = text[found.end() + 1 :] if found.end() < len(text) else ""
    following = _TOP_KEY.search(rest)
    if following is None:
        body = rest if rest.endswith("\n") or not rest else rest + "\n"
        return head + body + block
    return head + rest[: following.start()] + block + rest[following.start() :]


def append_stage_milestone(store: Path, milestone: StageMilestone, stream: str) -> Path:
    """Append the milestone of a stage to the store `store`, created when absent."""
    text = store.read_text(encoding="utf-8") if store.exists() else "_schema: horai:actions@1\n"
    content = _appended(text, _block(milestone_entry(milestone, stream)))
    data = load_yaml(content)
    names = [entry.get("id") for entry in (data or {}).get("milestones") or ()]
    if not isinstance(data, dict) or names.count(milestone.name) != 1:
        raise ActionsFileError(f"{store}: the milestone {milestone.name} cannot be appended")
    store.parent.mkdir(parents=True, exist_ok=True)
    handle, temporary = tempfile.mkstemp(dir=store.parent, suffix=".tmp")
    with os.fdopen(handle, "w", encoding="utf-8") as stream_out:
        stream_out.write(content)
    os.replace(temporary, store)
    return store
