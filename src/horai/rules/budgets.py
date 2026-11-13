"""
Time consumed and remaining work of an item.

The remaining work of an item is its budget less the time spent since that budget was set, and zero
once the budget is consumed. The budget was set at the start of the cycle that the item records, or
at the date of its last decision entry that renewed or reduced it. A consumed budget calls for a
checkpoint decision, and the tasks of the item leave the candidates of the selection until then.

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
    """

    consumed: timedelta
    since: date | None
    remaining: timedelta | None
    exhausted: bool
    undefined: str | None = None


def budget_status(plan: Plan, item: Item, work: Sequence[Span]) -> BudgetStatus:
    """Compute the time consumed and the remaining work of `item` from the spans of work."""
    identifiers = {item.id, *(task.id for task in item.tasks)}
    consumed = time_on(work, identifiers)
    if item.cycle is not None and item.cycle in plan.excluded:
        return BudgetStatus(
            consumed, None, None, False, f"its cycle {item.cycle} is excluded as invalid"
        )
    dates = []
    if item.cycle is not None and item.cycle in plan.cycles:
        dates.append(plan.cycles[item.cycle].start)
    dates += [
        entry.date
        for entry in plan.decisions
        if entry.milestone == item.id and entry.decision in ("renew", "reduce")
    ]
    since = max(dates) if dates else None
    budget = item.planned_budget
    if budget is None:
        return BudgetStatus(consumed, since, None, False)
    spent = time_on(work, identifiers, since)
    remaining = max(budget - spent, timedelta(0))
    return BudgetStatus(consumed, since, remaining, spent >= budget)
