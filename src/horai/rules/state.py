"""
The commitment state of a task, computed from its parent and from the week of its commitment.

A week of commitment starts at a weekly review held, as the review log records it, and ends at the
next one. The rule is stated in the kernel note on commitment states (anchor ``^state-rule``):

1. a task is in the state ``week`` when its ``committed_week`` is the date of the review that
   started the current week, or when it recurs;
2. otherwise, in the state ``cycle`` when its parent is selected for the current cycle;
3. otherwise, in the state ``backlog``, which holds the loose tasks that no review has committed.

A recurring task holds the date of its last completion, and names its rule in `recurs`: a default
rule, ``daily``, ``weekly`` or ``cycle``, a rule named in the profile, or a period such as ``P2W``
or ``P2C``. A period counts days (D), weeks of commitment (W), months (M) or cycles (C). The task is
open again once that many periods have begun since its last completion: a period begins at each
date, at each weekly review held, on the first of each month, or at the start of each cycle.

Functions
---------
current_cycle(plan, day) -> Cycle | None
current_week(plan, day) -> date | None
recurrence_rule(plan, rule) -> tuple[int, str] | None
is_open_on(plan, task, day) -> bool
task_state(plan, item, task, day) -> str
"""

from __future__ import annotations

import re
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


DEFAULT_RULES = {"daily": "P1D", "weekly": "P1W", "cycle": "P1C"}
_PERIOD = re.compile(r"^P([1-9][0-9]*)([DWMC])$")


def recurrence_rule(plan: Plan, rule: str) -> tuple[int, str] | None:
    """Return the number and the unit of the periods of a rule, or None for an unknown rule.

    Examples
    --------
    >>> recurrence_rule(Plan(), "cycle"), recurrence_rule(Plan(), "P3M")
    ((1, 'C'), (3, 'M'))
    """
    named = plan.profile.recurrences if plan.profile else {}
    match = _PERIOD.match(DEFAULT_RULES.get(rule) or named.get(rule) or rule)
    return (int(match.group(1)), match.group(2)) if match else None


def _periods_begun(plan: Plan, unit: str, after: date, day: date) -> int:
    """Count the periods of `unit` that begin after the date `after` and on or before `day`."""
    if unit == "D":
        return (day - after).days
    if unit == "M":
        return (day.year - after.year) * 12 + day.month - after.month
    if unit == "C":
        return sum(1 for cycle in plan.cycles.values() if after < cycle.start <= day)
    if plan.reviews:
        return sum(1 for review in plan.reviews if after < review <= day)
    return (
        day - timedelta(days=day.weekday()) - (after - timedelta(days=after.weekday()))
    ).days // 7


def is_open_on(plan: Plan, task: Task, day: date) -> bool:
    """Whether `task` is open on `day`; a recurring task reopens after the periods of its rule.

    Before any review is held, a week begins on each Monday. A task whose rule is unknown stays
    open, and the check reports the rule.
    """
    if task.cancelled is not None:
        return False
    if task.recurs is None or task.completed is None:
        return task.completed is None
    rule = recurrence_rule(plan, task.recurs)
    if rule is None:
        return True
    count, unit = rule
    return _periods_begun(plan, unit, task.completed, day) >= count


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
