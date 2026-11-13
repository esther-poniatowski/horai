"""
Issues: the defects that `horai check` reports in the records of a plan.

An issue names the rule that it breaks, the file and the record concerned, and a message. Its
severity decides the exit status of the check: an error fails it, a warning does not.

Classes
-------
Severity
    Severity of an issue.
Issue
    One defect found in the records of a plan.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class Severity(StrEnum):
    """Severity of an issue."""

    ERROR = "error"
    WARNING = "warning"


@dataclass(frozen=True)
class Issue:
    """One defect found in the records of a plan.

    Attributes
    ----------
    rule : str
        Identifier of the broken rule, in the form ``area/kind``, such as ``schema/invalid``.
    message : str
        Statement of the defect, naming the value at fault.
    path : str
        Path of the file concerned, relative to the plan; empty for a defect of the whole plan.
    record : str
        Identifier of the record or of the task concerned, when one is concerned.
    severity : Severity
        Severity of the issue.
    """

    rule: str
    message: str
    path: str = ""
    record: str = ""
    severity: Severity = Severity.ERROR

    def location(self) -> str:
        """Return the file and the record concerned, in the form ``path#record``."""
        return self.path + (f"#{self.record}" if self.record else "")
