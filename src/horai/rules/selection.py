"""
The selection rule: which task comes next.

The rule is stated in the kernel note on the selection of the next task (anchors
``^non-negotiable-key`` and ``^selection-rule``). The candidates are the open tasks in the state
``week`` of the stream of the current block, which do not wait, whose milestone has no open
dependency and no consumed budget, and whose predecessors are done. The loose tasks of the stream,
which serve no milestone, are candidates as well. While an open item or an open task is marked
non-negotiable, the candidates are its own open tasks, whatever their stream; a mark left on a
closed item or task is ignored, and the check reports it. In a request window, a block of a stream
triggered by arrival, the tasks of other streams that hand off to a party are candidates as well,
after the tasks of the stream of the window.

A loose task that is important and urgent precedes the milestones of its stream, and the other loose
tasks follow them. Among the milestones, the keys apply lexicographically, a question counting as a
milestone:

1. deadline, under the option of imposed deadlines;
2. hand-off to a party, under the option of external parties;
3. unblocking, under the option of the milestone graph;
4. worth: the rank set at the cycle planning.

Within a milestone, and among loose tasks, the quadrant, the importance and the riskiest mark order
the tasks. The result is a list of tiers: the candidates
that the keys do not separate share a tier, and the choice among them is left to the agent.

Classes
-------
Candidate, Selection

Functions
---------
marked(plan) -> tuple[Item | None, Task | None]
select(plan, day, stream, work) -> Selection
"""

from __future__ import annotations

import math
from collections.abc import Sequence
from dataclasses import dataclass, field
from datetime import date
from itertools import groupby

from ..domain.records import Item, Plan, Task
from .budgets import budget_status
from .state import is_open_on, task_state
from .time_spent import Span

IMPORTANT = {"highest", "high"}
IMPORTANT_AND_URGENT = 0
IMPORTANCE_ORDER: dict[str | None, int] = {
    "highest": 0,
    "high": 1,
    "medium": 2,
    None: 3,
    "low": 4,
    "lowest": 5,
}

_UNIMPLEMENTED_KEYS = {
    "imposed_deadlines": "the deadline key is not computed yet",
    "milestone_graph": "the unblocking key is not computed yet",
}


@dataclass(frozen=True)
class Candidate:
    """A task that may be taken next, with its item, or None for a loose task."""

    item: Item | None
    task: Task


@dataclass
class Selection:
    """The result of the selection rule.

    Attributes
    ----------
    tiers : list[list[Candidate]]
        The candidates, from the first tier to the last; the candidates of one tier are tied.
    marked : Item | None
        The item marked non-negotiable, whose tasks are the only candidates, or None.
    notes : list[str]
        Statements of what the rule excluded or could not compute.
    """

    tiers: list[list[Candidate]] = field(default_factory=list)
    marked: Item | None = None
    marked_task: Task | None = None
    notes: list[str] = field(default_factory=list)


def marked(plan: Plan) -> tuple[Item | None, Task | None]:
    """Return the open item marked non-negotiable, or the open marked task with its item.

    The item of a loose task is None. A mark on a closed item, or on a completed task or a task of
    a closed item, is ignored.

    Examples
    --------
    >>> marked(Plan())
    (None, None)
    """
    for item in plan.items.values():
        if item.non_negotiable is not None and item.is_open:
            return item, None
    for parent, task in plan.tasks():
        if task.non_negotiable is not None and task.is_open and (parent is None or parent.is_open):
            return parent, task
    return None, None


def _blocked_by_dependency(plan: Plan, item: Item) -> str | None:
    """Return the first open milestone on which `item` depends, or None."""
    for dependency in item.depends_on:
        other = plan.items.get(dependency)
        if other is None or other.is_open:
            return dependency
    return None


def _pool(
    plan: Plan, day: date, stream: str | None, selection: Selection
) -> list[tuple[Item | None, Task]]:
    """Return the tasks among which the candidates are chosen, and record the marked item."""
    marked_item, marked_task = marked(plan)
    if marked_task is not None:
        selection.marked = marked_item
        selection.marked_task = marked_task
        return [(marked_item, marked_task)]
    if marked_item is not None:
        selection.marked = marked_item
        return [(marked_item, task) for task in marked_item.tasks]
    declared = plan.profile.streams.get(stream) if plan.profile and stream else None
    window = declared is not None and declared.triggered_by == "arrival"
    return [
        (item, task)
        for item, task in plan.tasks()
        if task_state(plan, item, task, day) == "week"
        and (plan.stream_of(item, task) == stream or (window and task.hands_off))
    ]


@dataclass(frozen=True)
class _Context:
    """What the admission of a candidate reads: the plan, the work, the done tasks, the notes."""

    plan: Plan
    day: date
    work: Sequence[Span]
    done: set[str]
    notes: list[str]


def _admit(item: Item | None, task: Task, context: _Context) -> bool:
    """Whether a task of the pool is a candidate; record in `notes` why an item is excluded."""
    if not is_open_on(context.plan, task, context.day) or task.is_waiting:
        return False
    if item is None:
        return all(predecessor in context.done for predecessor in task.depends_on)
    if not item.is_open:
        return False
    plan, notes = context.plan, context.notes
    dependency = _blocked_by_dependency(plan, item)
    if dependency is not None:
        notes.append(f"{item.id}: waits for the milestone {dependency}")
        return False
    status = budget_status(plan, item, context.work)
    if status.carried:
        notes.append(
            f"{item.id}: carried into its cycle without a decision entry; "
            f"its budget counts from {status.since}"
        )
    if status.undefined:
        notes.append(f"{item.id}: the remaining work is undefined: {status.undefined}")
    elif status.exhausted:
        notes.append(f"{item.id}: the budget is consumed and awaits a checkpoint decision")
        return False
    return all(predecessor in context.done for predecessor in task.depends_on)


def quadrant(task: Task, day: date) -> int:
    """Return the quadrant of a task within its parent: 0 important and urgent, 1 important,
    2 urgent, 3 neither. A task is important at the levels highest and high, and urgent once its
    scheduled date is reached.

    Examples
    --------
    >>> task = Task("a", "A", None, importance="high", scheduled=date(2026, 11, 1))
    >>> quadrant(task, date(2026, 11, 2))
    0
    """
    important = task.importance in IMPORTANT
    urgent = task.scheduled is not None and task.scheduled <= day
    return (0 if urgent else 1) if important else (2 if urgent else 3)


def _tiers(
    candidates: list[Candidate], release_key: bool, day: date, stream: str | None
) -> list[list[Candidate]]:
    """Order the candidates by the keys, and group the tied ones into tiers.

    In a request window, the tasks of other streams that hand off to a party follow the tasks of
    the stream of the window.
    """
    releasing = (
        {c.item.id for c in candidates if c.item is not None and c.task.hands_off}
        if release_key
        else set()
    )

    def key(candidate: Candidate) -> tuple[int, int, float, int, int, int, int]:
        item, task = candidate.item, candidate.task
        if stream is not None and Plan.stream_of(item, task) != stream:
            group, rank = 3, math.inf
        elif item is None:
            group = 0 if quadrant(task, day) == IMPORTANT_AND_URGENT else 2
            rank = math.inf
        else:
            group, rank = 1, item.rank if item.rank is not None else math.inf
        return (
            group,
            0 if item is not None and item.id in releasing else 1,
            rank,
            0 if release_key and task.hands_off else 1,
            quadrant(task, day),
            IMPORTANCE_ORDER.get(task.importance, IMPORTANCE_ORDER[None]),
            0 if task.riskiest else 1,
        )

    return [list(group) for _, group in groupby(sorted(candidates, key=key), key=key)]


def select(plan: Plan, day: date, stream: str | None, work: Sequence[Span]) -> Selection:
    """Apply the selection rule on `day`, for the stream of the current block.

    Parameters
    ----------
    plan : Plan
        The records of the plan.
    day : date
        The day of the selection, which fixes the current week and cycle.
    stream : str | None
        The stream of the current block; ignored while an item is marked non-negotiable.
    work : Sequence[Span]
        The spans of work, from which the consumed budgets are computed.

    Returns
    -------
    Selection
        The candidates, in tiers.
    """
    selection = Selection()
    options = plan.profile.enabled_mechanisms if plan.profile else {}
    selection.notes += [note for name, note in _UNIMPLEMENTED_KEYS.items() if name in options]
    done = {task.id for _, task in plan.tasks() if not is_open_on(plan, task, day)}
    context = _Context(plan, day, work, done, [])
    candidates = [
        Candidate(item, task)
        for item, task in _pool(plan, day, stream, selection)
        if _admit(item, task, context)
    ]
    selection.notes += list(dict.fromkeys(context.notes))
    selection.tiers = _tiers(candidates, "external_parties" in options, day, stream)
    return selection
