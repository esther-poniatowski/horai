"""
The checks of the calendar: the typical week, and the departures recorded for single dates.

The typical week is checked against the allocation of the profile. The current week, which runs
from the last weekly review held, is checked for what exists only in that week: the placement of
its unplaced appointments, and the blocks that hold the preparation of its appointments.

Functions
---------
check_calendar(plan) -> Iterator[Issue]
    Run every check of the calendar.
"""

from __future__ import annotations

from collections import Counter
from collections.abc import Iterator, Sequence
from datetime import date, time, timedelta

from ..domain.records import (
    WEEKDAYS,
    Allocation,
    Appointment,
    Block,
    DayChange,
    Plan,
    TypicalDay,
)
from ..domain.time import minute_of_day
from ..issues import Issue, Severity
from .calendar import calendar_day, week_calendar
from .state import current_week

TYPICAL_WEEK = "settings/typical-week.yml"

Interval = tuple[int, int]


def _interval(start: time, length: timedelta) -> Interval:
    """Return the bounds of an entry, in minutes after midnight."""
    begin = minute_of_day(start)
    return begin, begin + int(length.total_seconds() // 60)


def _within(interval: Interval, spans: Sequence[Interval]) -> bool:
    """Whether an interval lies inside one of the spans."""
    return any(start <= interval[0] and interval[1] <= end for start, end in spans)


def _overlaps(intervals: Sequence[tuple[Interval, str]]) -> list[tuple[str, str]]:
    """Return the pairs of labelled intervals that overlap."""
    ordered = sorted(intervals)
    return [
        (ordered[i][1], ordered[i + 1][1])
        for i in range(len(ordered) - 1)
        if ordered[i + 1][0][0] < ordered[i][0][1]
    ]


def _stream_issues(plan: Plan, stream: str, where: str, path: str) -> Iterator[Issue]:
    """A block or an appointment names a stream of the profile."""
    if plan.profile is not None and stream not in plan.profile.streams:
        yield Issue("reference/stream", f"{where}: no stream {stream} in the profile", path)


def _entries(
    blocks: Sequence[Block], appointments: Sequence[Appointment]
) -> list[tuple[Interval, str]]:
    """Label each entry of a day with its interval."""
    return [
        (_interval(b.start, b.length), f"block {b.stream} at {b.start:%H:%M}") for b in blocks
    ] + [(_interval(a.start, a.length), f"appointment {a.id}") for a in appointments]


def _check_typical_day(plan: Plan, weekday: str, day: TypicalDay) -> Iterator[Issue]:
    """The spans of a day are ordered and disjoint, and hold its entries without overlap."""
    for start, end in day.spans:
        if start >= end:
            yield Issue(
                "calendar/span", f"{weekday}: a span must end after it starts", TYPICAL_WEEK
            )
    for first, second in _overlaps([(span, f"span {span}") for span in day.spans]):
        yield Issue("calendar/span", f"{weekday}: {first} and {second} overlap", TYPICAL_WEEK)
    entries = _entries(day.blocks, day.appointed)
    for interval, label in entries:
        if not _within(interval, day.spans):
            message = f"{weekday}: the {label} lies outside the available spans"
            yield Issue("calendar/outside-spans", message, TYPICAL_WEEK)
    for first, second in _overlaps(entries):
        yield Issue(
            "calendar/overlap", f"{weekday}: the {first} and the {second} overlap", TYPICAL_WEEK
        )
    for block in day.blocks:
        yield from _stream_issues(plan, block.stream, weekday, TYPICAL_WEEK)
    for appointment in day.appointed:
        yield from _stream_issues(plan, appointment.stream, weekday, TYPICAL_WEEK)
        if appointment.first is not None and WEEKDAYS[appointment.first.weekday()] != weekday:
            message = f"{weekday}: the appointment {appointment.id} starts on {appointment.first}"
            yield Issue("calendar/recurrence", message + ", another weekday", TYPICAL_WEEK)


def _check_energy(plan: Plan) -> Iterator[Issue]:
    """A block of a stream of high complexity lies within the hours of high energy."""
    week = plan.typical_week
    if week is None or plan.profile is None or not plan.profile.energy:
        return
    streams = plan.profile.streams
    for weekday, day in week.days.items():
        high = plan.profile.energy.get(weekday, ())
        for block in day.blocks:
            stream = streams.get(block.stream)
            if stream is None or stream.complexity != "high":
                continue
            if not _within(_interval(block.start, block.length), high):
                message = (
                    f"{weekday}: the block {block.stream} at {block.start:%H:%M} lies outside "
                    "the hours of high energy"
                )
                yield Issue("calendar/energy", message, TYPICAL_WEEK, severity=Severity.WARNING)


def _check_change(
    plan: Plan, change: DayChange, typical_day: TypicalDay | None, where: str, path: str
) -> Iterator[Issue]:
    """A change of one date names the blocks, the appointments and the streams that exist."""
    starts = {
        b.start
        for b in (
            change.blocks
            if change.blocks is not None
            else (typical_day.blocks if typical_day else ())
        )
    }
    for start in change.removed_blocks:
        if start not in starts:
            message = f"{where}: no block starts at {start:%H:%M} to remove"
            yield Issue("reference/block", message, path)
    for block in [*(change.blocks or ()), *change.added_blocks]:
        yield from _stream_issues(plan, block.stream, where, path)
    unplaced = {u.id for u in plan.typical_week.unplaced} if plan.typical_week else set()
    for appointment in change.appointments:
        yield from _stream_issues(plan, appointment.stream, where, path)
        if appointment.places is not None and appointment.places not in unplaced:
            message = f"{where}: no unplaced appointment {appointment.places} to place"
            yield Issue("reference/appointment", message, path)


def dates_path(day: date) -> str:
    """Return the path of the file of the calendar of dates that holds the month of `day`."""
    return f"calendar/dates/{day:%Y-%m}.yml"


def _check_dates(plan: Plan) -> Iterator[Issue]:
    """A departure names the recurring appointments, the blocks and the streams that exist, and an
    absence ends on or after its first date."""
    typical = plan.typical_week
    for day, change in sorted(plan.dates.items()):
        path, where = dates_path(day), f"{day}"
        weekday = WEEKDAYS[day.weekday()]
        typical_day = typical.days.get(weekday) if typical else None
        recurring = {a.id for a in typical_day.appointed} if typical_day else set()
        for name in [*change.cancelled, *change.moved]:
            if name not in recurring:
                message = f"{where}: no recurring appointment {name} on a {weekday}"
                yield Issue("reference/appointment", message, path)
        yield from _check_change(plan, change, typical_day, where, path)
    for absence in plan.absences:
        if absence.end < absence.start:
            message = f"the absence from {absence.start} ends on {absence.end}, before it starts"
            yield Issue("calendar/absence", message, dates_path(absence.start))


def _placed(plan: Plan, first: date, last: date) -> Counter[str]:
    """Count the placements of each unplaced appointment on the available dates of a range."""
    calendars = [
        calendar_day(plan, first + timedelta(days=offset))
        for offset in range((last - first).days + 1)
    ]
    return Counter(
        entry.appointment.places
        for calendar in calendars
        for entry in calendar.entries
        if entry.appointment is not None and entry.appointment.places
    )


def _check_placements(plan: Plan, day: date) -> Iterator[Issue]:
    """Each unplaced appointment is placed as often as the typical week states, in each period.

    A period of one week is the current week, which covers seven dates from its review; a longer
    period is checked in the week in which it ends. A week whose dates are all unavailable is not
    checked, and an ended week never is.
    """
    typical, week = plan.typical_week, current_week(plan, day)
    if typical is None or not typical.unplaced or week is None:
        return
    end = week + timedelta(days=6)
    if all(calendar.unavailable or not calendar.spans for calendar in week_calendar(plan, week)):
        return
    for unplaced in typical.unplaced:
        period = unplaced.period_of(week) or (week, end)
        if period[1] > end:
            continue
        count = _placed(plan, *period)[unplaced.id]
        if count < unplaced.times:
            message = (
                f"the period from {period[0]} to {period[1]} places {unplaced.id} {count} "
                f"time(s), of {unplaced.times}"
            )
            yield Issue("calendar/unplaced", message, dates_path(week), severity=Severity.WARNING)


def _preparation_amount(plan: Plan, stream: str | None, appointment: str) -> Allocation | None:
    """Return the reserve per event of `stream` that covers `appointment`, or None."""
    declared = plan.profile.streams.get(stream) if plan.profile and stream else None
    allocation = declared.allocation if declared else None
    if allocation is None or allocation.mode != "reserve" or allocation.per != "event":
        return None
    if allocation.events and appointment not in allocation.events:
        return None
    return allocation


def _block_hours(plan: Plan, starts_on: date) -> dict[str, float]:
    """Return the hours of the blocks of each stream in the calendar of a week."""
    placed: dict[str, float] = {}
    for calendar in week_calendar(plan, starts_on):
        for block in calendar.blocks():
            assert block.stream is not None
            placed[block.stream] = placed.get(block.stream, 0.0) + _hours(block.length)
    return placed


def _check_preparations(plan: Plan, day: date) -> Iterator[Issue]:
    """The blocks of the current week hold the preparations committed for it.

    A preparation task takes its budget, or else the reserve per event of its stream, and a budget
    outside the bound of that reserve is reported. The blocks of the stream over the seven dates of
    the week must sum to at least the budgets of its preparation tasks.
    """
    week = current_week(plan, day)
    if week is None:
        return
    path = dates_path(week)
    needed: dict[str, float] = {}
    for item, task in plan.tasks():
        stream = plan.stream_of(item, task)
        if task.prepares is None or task.committed_week != week or stream is None:
            continue
        allocation = _preparation_amount(plan, stream, task.prepares)
        if allocation is None:
            continue
        assert isinstance(allocation.amount, timedelta)
        budget = task.budget or allocation.amount
        if {
            "exact": budget != allocation.amount,
            "at_least": budget < allocation.amount,
            "at_most": budget > allocation.amount,
        }[allocation.bound]:
            bound = allocation.bound.replace("_", " ")
            message = (
                f"the preparation {task.id} has a budget of {_hours(budget):.1f} h, for a "
                f"reserve of {_hours(allocation.amount):.1f} h per event ({bound})"
            )
            yield Issue("calendar/allocation", message, path, severity=Severity.WARNING)
        needed[stream] = needed.get(stream, 0.0) + _hours(budget)
    placed = _block_hours(plan, week)
    for stream, want in sorted(needed.items()):
        have = placed.get(stream, 0.0)
        if have < want:
            message = (
                f"the blocks of the week of {week} give the stream {stream} {have:.1f} h, "
                f"for {want:.1f} h of preparation"
            )
            yield Issue("calendar/preparation", message, path, severity=Severity.WARNING)


def appointment_ids(plan: Plan) -> list[str]:
    """Return the identifiers of the appointments: a recurring one once, a dated one as stated.

    A recurring appointment held on several weekdays keeps one identifier across them.
    """
    recurring = sorted(
        {
            a.id
            for day in (plan.typical_week.days if plan.typical_week else {}).values()
            for a in day.appointed
        }
    )
    dated = [a.id for change in plan.dates.values() for a in change.appointments]
    return recurring + dated


def check_calendar(plan: Plan, day: date) -> Iterator[Issue]:
    """Run every check of the calendar, as it stands on `day`."""
    if plan.typical_week is not None:
        for weekday, typical_day in plan.typical_week.days.items():
            yield from _check_typical_day(plan, weekday, typical_day)
        for unplaced in plan.typical_week.unplaced:
            yield from _stream_issues(plan, unplaced.stream, unplaced.id, TYPICAL_WEEK)
    yield from _check_energy(plan)
    yield from _check_dates(plan)
    yield from _check_placements(plan, day)
    yield from _check_preparations(plan, day)
    yield from check_allocation(plan)


def _hours(length: timedelta) -> float:
    return length / timedelta(hours=1)


def _reserved(plan: Plan, days_with_spans: int) -> float:
    """Return the hours of a typical week held by the reserves per week and per day."""
    assert plan.profile is not None
    total = 0.0
    for stream in plan.profile.streams.values():
        allocation = stream.allocation
        if allocation is None or allocation.mode != "reserve":
            continue
        assert isinstance(allocation.amount, timedelta)
        if allocation.per == "week":
            total += _hours(allocation.amount)
        elif allocation.per == "day":
            total += _hours(allocation.amount) * days_with_spans
    return total


def plannable_hours(plan: Plan) -> float | None:
    """Return the hours of a typical week left to the shares, or None without stated spans.

    The available spans, less the mean weekly time of the recurring and the unplaced appointments,
    less the reserves per
    week and per day. A reserve per event depends on the preparation tasks of a week, and a reserve
    per cycle on the length of a cycle, so neither is removed from a typical week.
    """
    week = plan.typical_week
    if week is None or not week.days or plan.profile is None:
        return None
    appointed = sum(
        _hours(a.length) * a.weekly_share for day in week.days.values() for a in day.appointed
    )
    unplaced = sum(_hours(u.length) * u.weekly_share for u in week.unplaced)
    days = sum(1 for day in week.days.values() if day.spans)
    return _hours(week.capacity) - appointed - unplaced - _reserved(plan, days)


def _placed_hours(plan: Plan) -> dict[str, float]:
    """Return the hours of the blocks of each stream in the typical week."""
    assert plan.typical_week is not None
    hours: dict[str, float] = {}
    for day in plan.typical_week.days.values():
        for block in day.blocks:
            hours[block.stream] = hours.get(block.stream, 0.0) + _hours(block.length)
    return hours


def _measure(
    allocation: Allocation, have: float, remainder: float, days: int, tolerance: float
) -> tuple[float, float, float, str]:
    """Return the measured value, the amount, the admitted slack and the text of a comparison."""
    if allocation.mode == "share":
        assert isinstance(allocation.amount, float)
        value = have / remainder
        share = f"{allocation.amount:.0%}"
        shown = f"{value:.1%} of the plannable {remainder:.1f} h, for a share of {share}"
        return value, allocation.amount, tolerance, shown
    assert isinstance(allocation.amount, timedelta)
    want = _hours(allocation.amount) * (days if allocation.per == "day" else 1)
    return have, want, tolerance * remainder, f"{have:.1f} h, for a reserve of {want:.1f} h"


def check_allocation(plan: Plan) -> Iterator[Issue]:
    """The blocks of the typical week give each stream the time that its allocation states.

    A share is compared with the hours of the stream over the plannable hours, a reserve per week
    or per day with the hours of the stream; the reserve of a stream triggered by arrival is held by
    its blocks, the request windows. An exact amount is met within `allocation_tolerance` of the
    plannable hours. A reserve per event or per cycle is not compared.
    """
    remainder = plannable_hours(plan)
    if remainder is None or remainder <= 0:
        return
    assert plan.profile is not None and plan.typical_week is not None
    placed = _placed_hours(plan)
    tolerance = plan.profile.allocation_tolerance
    days = sum(1 for day in plan.typical_week.days.values() if day.spans)
    for stream in plan.profile.streams.values():
        allocation = stream.allocation
        if allocation is None or allocation.per in ("event", "cycle"):
            continue
        value, want, slack, shown = _measure(
            allocation, placed.get(stream.id, 0.0), remainder, days, tolerance
        )
        failed = {
            "exact": abs(value - want) > slack,
            "at_least": value < want,
            "at_most": value > want,
        }[allocation.bound]
        if failed:
            bound = allocation.bound.replace("_", " ")
            message = f"the blocks give the stream {stream.id} {shown} ({bound})"
            yield Issue("calendar/allocation", message, TYPICAL_WEEK, severity=Severity.WARNING)
