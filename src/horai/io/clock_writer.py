"""
Writing of clock entries, the only records that this increment of horai writes.

An entry is appended as one line to the list `entries` of the clock file of its month, so that the
rest of the file, comments included, is left as written. The new content is parsed back before it
replaces the file, through a temporary file and a rename in the same folder.

Classes
-------
ClockFileError
    A clock file whose shape forbids an append.

Functions
---------
append_clock_entry(plan_folder, entry) -> Path
"""

from __future__ import annotations

import os
import re
import tempfile
from pathlib import Path

from ..domain.records import ClockEntry
from .yaml_loader import load_yaml

_EMPTY_LIST = re.compile(r"^entries:\s*\[\s*\]\s*$", re.MULTILINE)
_TOP_KEY = re.compile(r"^[A-Za-z_][\w-]*:", re.MULTILINE)


class ClockFileError(Exception):
    """A clock file whose shape forbids an append, reported with the exit status 2."""


def _line(entry: ClockEntry) -> str:
    """Write `entry` as one line of the list entries, in flow style."""
    moment = entry.at.isoformat(timespec="minutes")
    fields = [f"at: {moment}", f"event: {entry.event}"]
    if entry.task is not None:
        fields.append(f"task: {entry.task}")
    if entry.assigned:
        fields.append("assigned: true")
    return "  - {" + ", ".join(fields) + "}\n"


def _atomic_write(path: Path, text: str) -> None:
    """Replace `path` by `text` through a temporary file in the same folder."""
    descriptor, temporary = tempfile.mkstemp(
        dir=path.parent, prefix=f".{path.name}.", suffix=".tmp"
    )
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(text)
        os.replace(temporary, path)
    except BaseException:
        Path(temporary).unlink(missing_ok=True)
        raise


def append_clock_entry(plan_folder: Path, entry: ClockEntry) -> Path:
    """Append `entry` to the clock file of its month, and return the path of that file.

    Raises
    ------
    ClockFileError
        If the existing file does not end with its list `entries`, or if the result does not parse
        back with one more entry.
    """
    month = f"{entry.at:%Y-%m}"
    path = plan_folder / "log" / "clock" / f"{month}.yml"
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.is_file():
        text = path.read_text(encoding="utf-8")
        before = len((load_yaml(text) or {}).get("entries") or [])
        text = _EMPTY_LIST.sub("entries:", text)
        keys = _TOP_KEY.findall(text)
        if not keys or keys[-1] != "entries:":
            raise ClockFileError(f"{path}: the list entries must be the last key of the file")
        if not text.endswith("\n"):
            text += "\n"
    else:
        text, before = f"_schema: horai:clock-log@1\nmonth: {month}\nentries:\n", 0
    text += _line(entry)
    after = load_yaml(text).get("entries") or []
    if len(after) != before + 1:
        raise ClockFileError(f"{path}: the entry would not be read back as a new entry of the list")
    _atomic_write(path, text)
    return path
