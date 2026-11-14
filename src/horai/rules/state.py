"""
The commitment state of a task, computed from its parent and from the week of its commitment.

A week of commitment starts at a weekly review held, as the review log records it, and ends at the
next one. The rule is stated in the kernel note on commitment states (anchor ``^state-rule``):

1. a task is in the state ``week`` when its ``committed_week`` is the date of the review that
   started the current week, or when it recurs;
2. otherwise, in the state ``cycle`` when its parent is selected for the current cycle;
3. otherwise, in the state ``backlog``, which holds the loose tasks that no review has committed.

A recurring task holds the date of its last completion, and is open again from the start of its
next period: the next date for a daily task, the next week for a weekly task, the next cycle for a
task per cycle.

Functions
---------
current_cycle(plan, day) -> Cycle | None
current_week(plan, day) -> date | None
is_open_on(plan, task, day) -> bool
task_state(plan, item, task, day) -> str
"""

from __future__ import annotations

from datetime import date, timedelta
from typing import Literal

from ..domain.records import Cycle, Item, Plan, Task

State = Literal["backlog", "cycle", "week"]


def current_cycle(plan: Plan, day: date) -> Cycle | None:
    """Return the cycle that contains `day`, or None."""
    for cycle in plan.cycles.values():
        if cycle.contains(day):
            return cycle
    return None


def current_week(plan: Plan, day: date) -> date | None:
    """Return the date of the last weekly review held on or before `day`, or None.

    Examples
    --------
    >>> current_week(Plan(reviews=(date(2026, 11, 9), date(2026, 11, 17))), date(2026, 11, 16))
    datetime.date(2026, 11, 9)
    """
    held = [review for review in plan.reviews if review <= day]
    return max(held) if held else None


def is_open_on(plan: Plan, task: Task, day: date) -> bool:
    """Whether `task` is open on `day`; a recurring task reopens at the start of each period.

    The period of a weekly task starts at the current week, or on the Monday of `day` before any
    review is held; the period of a task per cycle starts with the current cycle, or on `day`
    outside any cycle.
    """
    if task.recurs is None or task.completed is None:
        return task.completed is None
    if task.recurs == "daily":
        start = day
    elif task.recurs == "weekly":
        start = current_week(plan, day) or day - timedelta(days=day.weekday())
    else:
        cycle = current_cycle(plan, day)
        start = cycle.start if cycle is not None else day
    return task.completed < start


def task_state(plan: Plan, item: Item | None, task: Task, day: date) -> State:
    """Return the commitment state of `task`, held by `item`, on `day`.

    A loose task and a task of the holding file have no parent, and their `item` is None; they are
    in the backlog until a weekly review commits them.
    """
    week = current_week(plan, day)
    if task.recurs is not None or (week is not None and task.committed_week == week):
        return "week"
    if item is None:
        return "backlog"
    cycle = current_cycle(plan, day)
    if cycle is not None and item.cycle == cycle.id:
        return "cycle"
    return "backlog"
