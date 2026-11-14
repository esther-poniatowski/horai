"""
The stages of a deliverable that its phase has reached, and the milestones that hold them.

A type of deliverable lists its stages, each with the phase from which it exists as a milestone;
a deliverable may list its own. The milestone of a stage is named ``<deliverable>-<stage>``, and
names the stage in its field ``stage``. It takes the predictability of the stage, or else that of
the type. The decision on the stages is recorded in the decision record on request windows and
stages.

Classes
-------
StageMilestone
    A stage reached by its deliverable and held by no milestone yet.

Functions
---------
stage_milestone_id(deliverable, stage) -> str
missing_stages(plan, deliverable) -> list[StageMilestone]
check_stages(plan) -> Iterator[Issue]
"""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass

from ..domain.records import Deliverable, Plan, Stage
from ..issues import Issue

PHASES = ("exploration", "validation", "delivery")


@dataclass(frozen=True)
class StageMilestone:
    """A stage reached by its deliverable and held by no milestone yet.

    Attributes
    ----------
    name : str
        The name of the milestone to create, ``<deliverable>-<stage>``, which is its identifier.
    deliverable : Deliverable
        The deliverable of the stage.
    stage : Stage
        The stage.
    predictability : str | None
        The predictability of the stage, or else that of the type of the deliverable.
    stream : str | None
        The stream shared by the other milestones of the deliverable, or None when they share none.
    """

    name: str
    deliverable: Deliverable
    stage: Stage
    predictability: str | None
    stream: str | None


def stage_milestone_id(deliverable: str, stage: str) -> str:
    """Return the name of the milestone of a stage.

    Examples
    --------
    >>> stage_milestone_id("ctx-geometry", "draft")
    'ctx-geometry-draft'
    """
    return f"{deliverable}-{stage}"


def _reached(plan: Plan, deliverable: Deliverable) -> list[Stage]:
    """Return the stages of `deliverable` whose phase its current phase has reached."""
    phase = plan.phase_of(deliverable)
    if phase not in PHASES:
        return []
    return [
        stage
        for stage in plan.stages_of(deliverable)
        if PHASES.index(stage.phase) <= PHASES.index(phase)
    ]


def _shared_stream(plan: Plan, deliverable: str) -> str | None:
    """Return the stream of the milestones of `deliverable` when they all share one, or None."""
    streams = {item.stream for item in plan.items.values() if item.deliverable == deliverable}
    return streams.pop() if len(streams) == 1 else None


def missing_stages(plan: Plan, deliverable: str | None = None) -> list[StageMilestone]:
    """Return the stages reached by the active deliverables and held by no milestone.

    A stage is held by a milestone that names it in `stage`, or by a record, valid or excluded,
    that bears the name of its milestone. With `deliverable`, only that deliverable is examined.
    """
    missing = []
    for record in plan.deliverables.values():
        if record.status != "active" or deliverable not in (None, record.id):
            continue
        held = {
            item.stage
            for item in plan.items.values()
            if item.deliverable == record.id and item.stage
        }
        for stage in _reached(plan, record):
            name = stage_milestone_id(record.id, stage.id)
            if stage.id in held or name in plan.items or name in plan.excluded:
                continue
            predictability, _ = plan.stage_defaults(record, stage)
            missing.append(
                StageMilestone(name, record, stage, predictability, _shared_stream(plan, record.id))
            )
    return missing


def check_stages(plan: Plan) -> Iterator[Issue]:
    """A milestone that names a stage holds a stage of its deliverable, and bears its name."""
    for item in plan.items.values():
        if item.stage is None or item.deliverable not in plan.deliverables:
            continue
        deliverable = plan.deliverables[item.deliverable]
        path = plan.sources.get(item.id, "")
        if item.stage not in {stage.id for stage in plan.stages_of(deliverable)}:
            message = f"the deliverable {deliverable.id} has no stage {item.stage}"
            yield Issue("reference/stage", message, path, item.id)
        expected = stage_milestone_id(deliverable.id, item.stage)
        if item.id != expected:
            message = f"the milestone of the stage {item.stage} must be named {expected}"
            yield Issue("identifier/stage", message, path, item.id)
