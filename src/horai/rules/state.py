"""
The commitment state of a task, computed from its parent and from the week of its commitment.

The rule is stated in the kernel note on commitment states (anchor ``^state-rule``):

1. a task is in the state ``week`` when its ``committed_week`` is the date of the review that opened
   the current week, the latest week of the calendar;
2. otherwise, in the state ``cycle`` when its parent is selected for the current cycle, or is a
   standing parent;
3. otherwise, in the state ``backlog``.

Functions
---------
current_cycle(plan, day) -> Cycle | None
current_week(plan, day) -> Week | None
task_state(plan, item, task, day) -> str
"""

from __future__ import annotations

from datetime import date
from typing import Literal

from ..domain.records import Cycle, Item, Plan, Task, Week

State = Literal["backlog", "cycle", "week"]


def current_cycle(plan: Plan, day: date) -> Cycle | None:
    """Return the cycle that contains `day`, or None."""
    for cycle in plan.cycles.values():
        if cycle.contains(day):
            return cycle
    return None


def current_week(plan: Plan, day: date) -> Week | None:
    """Return the latest week opened on or before `day`, or None."""
    opened = [week_day for week_day in plan.weeks if week_day <= day]
    return plan.weeks[max(opened)] if opened else None


def task_state(plan: Plan, item: Item | None, task: Task, day: date) -> State:
    """Return the commitment state of `task`, held by `item`, on `day`.

    A task of the holding file has no parent, and its `item` is None.
    """
    week = current_week(plan, day)
    if week is not None and task.committed_week == week.opened:
        return "week"
    if item is not None:
        if item.kind == "standing":
            return "cycle"
        cycle = current_cycle(plan, day)
        if cycle is not None and item.cycle == cycle.id:
            return "cycle"
    return "backlog"
