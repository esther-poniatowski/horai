"""
Writing of the milestone of a stage, as a new file.

The file is created and never replaced: a stage whose milestone exists is not missing. Its test of
completion is left to the agent, behind a marked placeholder, since no stage states one. The
content is parsed back before the file is created.

Classes
-------
MilestoneFileError
    A milestone file that cannot be created.

Functions
---------
milestone_text(milestone, stream) -> str
write_stage_milestone(folder, milestone, stream) -> Path
"""

from __future__ import annotations

from pathlib import Path

import yaml

from ..rules.stages import StageMilestone
from .yaml_loader import load_yaml

PLACEHOLDER = "to state"


class MilestoneFileError(Exception):
    """A milestone file that cannot be created, reported with the exit status 2."""


def milestone_text(milestone: StageMilestone, stream: str) -> str:
    """Write the file of the milestone of a stage.

    Examples
    --------
    >>> from horai.domain.records import Deliverable, Stage
    >>> paper = Deliverable("ctx", "Geometry", "p", "paper", "active")
    >>> text = milestone_text(StageMilestone("ctx-draft", paper, Stage("draft", "delivery"),
    ...                                      "routine", "inquiry"), "inquiry")
    >>> text.splitlines()[1]
    'title: Draft of Geometry'
    """
    stage = milestone.stage.id.replace("-", " ").capitalize()
    fields = {
        "title": f"{stage} of {milestone.deliverable.title}",
        "deliverable": milestone.deliverable.id,
        "stage": milestone.stage.id,
        "stream": stream,
        "status": "open",
    }
    if milestone.predictability is not None:
        fields["predictability"] = milestone.predictability
    body = yaml.safe_dump(fields, sort_keys=False, allow_unicode=True, width=100)
    return (
        "_schema: horai:milestone@1\n"
        + body
        + "# PLACEHOLDER: the test that judges the completion of the stage.\n"
        + f"done_when: {PLACEHOLDER}\n"
    )


def write_stage_milestone(folder: Path, milestone: StageMilestone, stream: str) -> Path:
    """Create the file of the milestone of a stage in `folder`, and return its path."""
    path = folder / f"{milestone.name}.yml"
    if path.exists():
        raise MilestoneFileError(f"{path} exists already")
    text = milestone_text(milestone, stream)
    load_yaml(text)
    folder.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as handle:
        handle.write(text)
    return path
