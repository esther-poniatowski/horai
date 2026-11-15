"""
Rendering of the results of horai as plain text.

Functions
---------
render_issues(issues) -> str
render_selection(selection, stream) -> str
render_week(plan, day, work) -> str
"""

from __future__ import annotations

import math
from collections.abc import Sequence
from datetime import date, timedelta

from ..domain.records import WEEKDAYS, Plan, Task
from ..domain.time import format_duration
from ..issues import Issue
from ..rules.budgets import budget_status
from ..rules.calendar import Entry, week_calendar
from ..rules.selection import Selection
from ..rules.state import current_cycle, current_week, is_open_on, task_state
from ..rules.time_spent import Span, time_on


def render_issues(issues: Sequence[Issue]) -> str:
    """Write one line per issue, then a count by severity."""
    lines = [
        f"{issue.severity} {issue.rule} {issue.location()}: {issue.message}" for issue in issues
    ]
    errors = sum(issue.severity == "error" for issue in issues)
    lines.append(f"{errors} error(s), {len(issues) - errors} warning(s)")
    return "\n".join(lines)


def render_selection(selection: Selection, stream: str | None) -> str:
    """Write the tiers of the selection, numbered, with the notes of the rule."""
    if selection.marked_task is not None and selection.marked is None:
        task = selection.marked_task
        header = f"Next, for the non-negotiable task {task.action} [{task.id}]:"
    elif selection.marked is not None:
        header = (
            f"Next, for the non-negotiable item {selection.marked.title} [{selection.marked.id}]:"
        )
    else:
        header = f"Next, in the stream {stream}:"
    lines = [header]
    if not selection.tiers:
        lines.append("  no candidate")
    for number, tier in enumerate(selection.tiers, start=1):
        tied = " (tied)" if len(tier) > 1 else ""
        for candidate in tier:
            item, task = candidate.item, candidate.task
            parent = item.title if item is not None else "loose task"
            rank = f", rank {item.rank}" if item is not None and item.rank is not None else ""
            risk = ", riskiest" if task.riskiest else ""
            if task.importance:
                risk += f", {task.importance}"
            lines.append(f"  {number}. {task.action} [{task.id}] — {parent}{rank}{risk}{tied}")
    lines += [f"  note: {note}" for note in selection.notes]
    return "\n".join(lines)


def _entry(entry: Entry) -> str:
    """Write one entry of the calendar: its hour, its kind, and what it holds."""
    length = format_duration(entry.length)
    if entry.kind == "block":
        return f"{entry.start:%H:%M} block {entry.stream} {length}"
    assert entry.appointment is not None
    title = entry.appointment.title or entry.appointment.id
    party = entry.appointment.party
    return f"{entry.start:%H:%M} appointment {title} ({entry.stream}, {party}) {length}"


def _calendar(plan: Plan, starts_on: date) -> list[str]:
    """List, day by day, the entries of the week that starts on `starts_on`."""
    lines = []
    for calendar in week_calendar(plan, starts_on):
        weekday = WEEKDAYS[calendar.day.weekday()]
        if calendar.unavailable:
            reason = f": {calendar.reason}" if calendar.reason else ""
            lines.append(f"  {weekday} {calendar.day}: unavailable{reason}")
        elif calendar.entries:
            lines.append(
                f"  {weekday} {calendar.day}: " + "; ".join(_entry(e) for e in calendar.entries)
            )
    return lines


def _mark(plan: Plan, task: Task, day: date) -> str:
    """Return the mark of a task on `day`: done, main objective, marked for the day, or none."""
    if not is_open_on(plan, task, day):
        return "x"
    if task.marked_for == day:
        return "main" if task.main_objective else "today"
    return " "


def _task_row(plan: Plan, task: Task, day: date, indent: str) -> str:
    """Write one committed task, with its mark of the day and its wait."""
    waits = (
        f" (waits, follow-up {task.follow_up})"
        if task.follow_up is not None
        else f" (awaits {task.awaits})" if task.awaits is not None else ""
    )
    return f"{indent}[{_mark(plan, task, day)}] {task.action} [{task.id}]{waits}"


def _committed(plan: Plan, day: date, work: Sequence[Span]) -> list[str]:
    """List the tasks in the state week, by stream, each item with its remaining work."""
    streams = plan.profile.streams if plan.profile else {}
    lines = []
    named = {item.stream for item in plan.items.values()} | {
        task.stream for task in plan.loose if task.stream
    }
    for stream_id in sorted(named):
        rows = []
        items = sorted(
            (i for i in plan.items.values() if i.stream == stream_id),
            key=lambda i: (i.rank if i.rank is not None else math.inf, i.id),
        )
        for item in items:
            committed = [t for t in item.tasks if task_state(plan, item, t, day) == "week"]
            if not committed:
                continue
            remaining = budget_status(plan, item, work).remaining
            budget = f", remaining {format_duration(remaining)}" if remaining is not None else ""
            rows.append(f"    {item.title} [{item.id}]{budget}")
            rows += [_task_row(plan, task, day, "      ") for task in committed]
        loose = [
            task
            for task in plan.loose
            if task.stream == stream_id and task_state(plan, None, task, day) == "week"
        ]
        if loose:
            rows.append("    loose tasks")
            rows += [_task_row(plan, task, day, "      ") for task in loose]
        if rows:
            described = f": {streams[stream_id].description}" if stream_id in streams else ""
            lines += [f"  {stream_id}{described}", *rows]
    return lines


def _follow_ups(plan: Plan, end: date) -> list[str]:
    """List the follow-ups of open tasks that fall on or before `end`."""
    due = sorted(
        (
            (task.follow_up, task)
            for _, task in plan.tasks()
            if task.follow_up is not None and task.is_open and task.follow_up <= end
        ),
        key=lambda pair: pair[0],
    )
    return [f"  {when}: {task.action} [{task.id}]" for when, task in due] or ["  none"]


def _reserves(plan: Plan, starts_on: date, work: Sequence[Span]) -> list[str]:
    """State, for each stream with a reserve per week, the time spent on it during the week."""
    if plan.profile is None:
        return []
    lines = []
    for stream in plan.profile.streams.values():
        allocation = stream.allocation
        if allocation is None or allocation.mode != "reserve" or allocation.per != "week":
            continue
        assert isinstance(allocation.amount, timedelta)
        names = {
            name
            for item, task in plan.tasks()
            if plan.stream_of(item, task) == stream.id
            for name in (task.id, item.id if item else task.id)
        }
        spent = time_on(work, names, starts_on, starts_on + timedelta(days=6))
        amount = format_duration(allocation.amount)
        bound = allocation.bound.replace("_", " ")
        beyond = (
            " (beyond the reserve)"
            if allocation.bound == "at_most" and spent > allocation.amount
            else ""
        )
        lines.append(f"  {stream.id}: {format_duration(spent)}, {bound} {amount}{beyond}")
    return ["Reserves of the week:", *lines] if lines else []


def render_week(plan: Plan, day: date, work: Sequence[Span]) -> str:
    """Write the week view: the calendar, the committed tasks by stream, and the follow-ups due."""
    week = current_week(plan, day)
    if week is None:
        return "No week has started: log a weekly review in log/reviews/."
    cycle = current_cycle(plan, day)
    cycle_text = f" · cycle {cycle.id} until {cycle.end}" if cycle else " · no current cycle"
    lines = [f"Week of {week}{cycle_text}", "Calendar:", *_calendar(plan, week)]
    lines += ["Committed tasks:", *_committed(plan, day, work)]
    lines += ["Follow-ups due:", *_follow_ups(plan, week + timedelta(days=6))]
    lines += _reserves(plan, week, work)
    running = [span for span in work if span.running]
    if running:
        lines.append(f"Running: {running[-1].task} since {running[-1].start:%H:%M}")
    return "\n".join(lines)
