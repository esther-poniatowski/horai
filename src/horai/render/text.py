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

from ..domain.records import WEEKDAYS, Appointment, Block, Plan, Task, Window
from ..domain.time import format_duration
from ..issues import Issue
from ..rules.budgets import budget_status
from ..rules.selection import Selection
from ..rules.state import current_cycle, current_week, task_state
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
    if selection.marked is not None:
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
            rank = f", rank {candidate.item.rank}" if candidate.item.rank is not None else ""
            risk = ", riskiest" if candidate.task.risk else ""
            lines.append(
                f"  {number}. {candidate.task.title} [{candidate.task.id}] "
                f"— {candidate.item.title}{rank}{risk}{tied}"
            )
    lines += [f"  note: {note}" for note in selection.notes]
    return "\n".join(lines)


def _calendar(plan: Plan, opened: date) -> list[str]:
    """List, day by day, the blocks, windows and appointments of the week opened on `opened`."""
    week = plan.weeks.get(opened)
    template = plan.template
    blocks: Sequence[Block] = (
        week.blocks if week and week.blocks is not None else template.blocks if template else ()
    )
    windows: Sequence[Window] = (
        week.windows if week and week.windows is not None else template.windows if template else ()
    )
    appointed = template.appointed if template else ()
    days = [opened + timedelta(days=offset) for offset in range(7)]
    lines = []
    for day in days:
        weekday = WEEKDAYS[day.weekday()]
        slots: list[tuple[str, str]] = []
        slots += [
            (f"{b.start:%H:%M}", f"block {b.stream} {format_duration(b.length)}")
            for b in blocks
            if b.day == weekday
        ]
        slots += [
            (f"{w.start:%H:%M}", f"window {format_duration(w.length)}")
            for w in windows
            if w.day == weekday
        ]
        slots += [
            (f"{a.start:%H:%M}", f"appointed {a.stream} {format_duration(a.length)} with {a.party}")
            for a in appointed
            if a.day == weekday
        ]
        dated: list[Appointment] = [a for a in plan.appointments.values() if a.date == day]
        slots += [
            (f"{a.start:%H:%M}", f"appointment {a.title} ({a.stream}, {a.party})") for a in dated
        ]
        if slots:
            lines.append(
                f"  {weekday} {day}: " + "; ".join(f"{hour} {what}" for hour, what in sorted(slots))
            )
    return lines


def _mark(task: Task, day: date) -> str:
    """Return the mark of a task on `day`: done, main objective, marked for the day, or none."""
    if not task.is_open:
        return "x"
    if task.today == day:
        return "main" if task.main else "today"
    return " "


def _committed(plan: Plan, day: date, work: Sequence[Span]) -> list[str]:
    """List the tasks in the state week, by stream, each item with its remaining work."""
    streams = plan.profile.streams if plan.profile else {}
    lines = []
    for stream_id in sorted({item.stream for item in plan.items.values()}):
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
            for task in committed:
                waits = f" (waits, follow-up {task.waiting})" if task.waiting is not None else ""
                rows.append(f"      [{_mark(task, day)}] {task.title} [{task.id}]{waits}")
        if rows:
            name = streams[stream_id].name if stream_id in streams else stream_id
            lines += [f"  {stream_id} {name}:", *rows]
    return lines


def _follow_ups(plan: Plan, end: date) -> list[str]:
    """List the follow-ups of open tasks that fall on or before `end`."""
    due = sorted(
        (
            (task.waiting, task)
            for _, task in plan.tasks()
            if isinstance(task.waiting, date) and task.is_open and task.waiting <= end
        ),
        key=lambda pair: pair[0],
    )
    return [f"  {when}: {task.title} [{task.id}]" for when, task in due] or ["  none"]


def _overhead(plan: Plan, opened: date, work: Sequence[Span]) -> list[str]:
    """State the time spent on the planning acts of the week, against the overhead budget."""
    parent = next((item for item in plan.items.values() if item.overhead), None)
    if parent is None or plan.profile is None:
        return []
    spent = time_on(
        work, {parent.id, *(t.id for t in parent.tasks)}, opened, opened + timedelta(days=6)
    )
    budget = plan.profile.overhead_budget
    over = " (over budget)" if spent > budget else ""
    return [f"Overhead of the method: {format_duration(spent)} of {format_duration(budget)}{over}"]


def render_week(plan: Plan, day: date, work: Sequence[Span]) -> str:
    """Write the week view: the calendar, the committed tasks by stream, and the follow-ups due."""
    week = current_week(plan, day)
    if week is None:
        return "No week is opened: a weekly review opens one in calendar/weeks/."
    cycle = current_cycle(plan, day)
    cycle_text = f" · cycle {cycle.id} until {cycle.end}" if cycle else " · no current cycle"
    lines = [f"Week opened {week.opened}{cycle_text}", "Calendar:", *_calendar(plan, week.opened)]
    lines += ["Committed tasks:", *_committed(plan, day, work)]
    lines += ["Follow-ups due:", *_follow_ups(plan, week.opened + timedelta(days=6))]
    lines += _overhead(plan, week.opened, work)
    running = [span for span in work if span.running]
    if running:
        lines.append(f"Running: {running[-1].task} since {running[-1].start:%H:%M}")
    return "\n".join(lines)
