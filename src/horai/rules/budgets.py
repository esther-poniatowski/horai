"""
Time consumed and remaining work of an item.

The remaining work of an item is its budget less the time spent since that budget was set, and zero
once the budget is consumed. The budget was set at the start of the cycle that the item records, or
at the date of its last decision entry that renewed or reduced it. A consumed budget calls for a
checkpoint decision, and the tasks of the item leave the candidates of the selection until then.

An item carried into a new cycle keeps its budget until a decision entry renews or reduces it. The
item counts as carried when time was spent on it before its cycle started, and no such decision is
dated on or after the last of that time. Its budget then counts from its last earlier decision, or
else from the first time spent on it, so that the time of the earlier cycle is not forgotten.

Classes
-------
BudgetStatus
    The time consumed and the remaining work of one item.

Functions
---------
budget_status(plan, item, work) -> BudgetStatus
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from datetime import date, timedelta

from ..domain.records import Item, Plan
from .time_spent import Span, time_on


@dataclass(frozen=True)
class BudgetStatus:
    """The time consumed and the remaining work of one item.

    Attributes
    ----------
    consumed : timedelta
        Time spent on the item and on its tasks, over its whole life.
    since : date | None
        Date at which the budget in force was set, or None when no date is known.
    remaining : timedelta | None
        Budget less the time spent since `since`, floored at zero; None without a budget.
    exhausted : bool
        Whether the budget in force is consumed, which calls for a checkpoint decision.
    undefined : str | None
        Reason for which the status cannot be computed, such as an excluded cycle.
    carried : bool
        Whether the item was carried into its cycle without a decision entry on its budget.
    """

    consumed: timedelta
    since: date | None
    remaining: timedelta | None
    exhausted: bool
    undefined: str | None = None
    carried: bool = False


def budget_status(plan: Plan, item: Item, work: Sequence[Span]) -> BudgetStatus:
    """Compute the time consumed and the remaining work of `item` from the spans of work."""
    identifiers = {item.id, *(task.id for task in item.tasks)}
    consumed = time_on(work, identifiers)
    if item.cycle is not None and item.cycle in plan.excluded:
        return BudgetStatus(
            consumed, None, None, False, f"its cycle {item.cycle} is excluded as invalid"
        )
    decisions = [
        entry.date
        for entry in plan.decisions
        if entry.milestone == item.id and entry.checkpoint_decision in ("renew", "reduce")
    ]
    start = (
        plan.cycles[item.cycle].start
        if item.cycle is not None and item.cycle in plan.cycles
        else None
    )
    before = sorted(
        span.start.date()
        for span in work
        if span.task in identifiers and start is not None and span.start.date() < start
    )
    carried = bool(before) and not any(day >= before[-1] for day in decisions)
    if carried:
        since: date | None = max(decisions) if decisions else before[0]
    else:
        dates = [day for day in (start, *decisions) if day is not None]
        since = max(dates) if dates else None
    budget = item.planned_budget
    if budget is None:
        return BudgetStatus(consumed, since, None, False, carried=carried)
    spent = time_on(work, identifiers, since)
    remaining = max(budget - spent, timedelta(0))
    return BudgetStatus(consumed, since, remaining, spent >= budget, carried=carried)
