"""
The calendar of a date: the typical day of its weekday, changed by the departures of the date.

The typical week states, for each weekday, the blocks and the recurring appointments; a request
window is a block of a stream triggered by arrival. The calendar of dates may change one date: it
replaces its blocks, removes or adds single blocks, cancels or moves a recurring appointment, or
adds an appointment of that date only. A range of absence makes each of its dates unavailable.
Departures are recorded as soon as they are known, for any date.

Classes
-------
Entry, CalendarDay

Functions
---------
absence_on(plan, day) -> Absence | None
calendar_day(plan, day) -> CalendarDay
week_calendar(plan, starts_on) -> list[CalendarDay]
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import date, time, timedelta
from typing import Literal

from ..domain.records import WEEKDAYS, Absence, Appointment, DayChange, Plan, TypicalDay

EntryKind = Literal["block", "appointment"]


@dataclass(frozen=True)
class Entry:
    """One entry of the calendar of a date: a block or an appointment."""

    start: time
    length: timedelta
    kind: EntryKind
    stream: str | None = None
    appointment: Appointment | None = None


@dataclass(frozen=True)
class CalendarDay:
    """The calendar of one date, in the order of the hours, with its available spans in minutes."""

    day: date
    entries: tuple[Entry, ...] = ()
    unavailable: bool = False
    reason: str | None = None
    spans: tuple[tuple[int, int], ...] = ()

    def blocks(self) -> list[Entry]:
        """Return the blocks of the date."""
        return [entry for entry in self.entries if entry.kind == "block"]


def absence_on(plan: Plan, day: date) -> Absence | None:
    """Return the absence that covers `day`, or None."""
    for absence in plan.absences:
        if absence.contains(day):
            return absence
    return None


def _recurring(typical: TypicalDay, change: DayChange | None, day: date) -> list[Appointment]:
    """Return the recurring appointments held on the date, without the cancelled, with the moved."""
    held = []
    for appointment in typical.appointed:
        if not appointment.occurs_on(day):
            continue
        if change is None:
            held.append(appointment)
            continue
        if appointment.id in change.cancelled:
            continue
        if appointment.id in change.moved:
            start, length = change.moved[appointment.id]
            appointment = replace(appointment, start=start, length=length or appointment.length)
        held.append(appointment)
    return held


def calendar_day(plan: Plan, day: date) -> CalendarDay:
    """Return the calendar of `day`.

    Examples
    --------
    >>> calendar_day(Plan(), date(2026, 11, 16)).entries
    ()
    """
    absence = absence_on(plan, day)
    if absence is not None:
        return CalendarDay(day, unavailable=True, reason=absence.reason)
    change = plan.dates.get(day)
    typical_week = plan.typical_week
    typical = (typical_week.days.get(WEEKDAYS[day.weekday()]) if typical_week else None) or (
        TypicalDay(spans=())
    )
    blocks = change.blocks if change is not None and change.blocks is not None else typical.blocks
    if change is not None:
        removed = set(change.removed_blocks)
        blocks = tuple(b for b in blocks if b.start not in removed) + change.added_blocks
    appointments = _recurring(typical, change, day) + list(change.appointments if change else ())
    entries = [Entry(b.start, b.length, "block", b.stream) for b in blocks] + [
        Entry(a.start, a.length, "appointment", a.stream, a) for a in appointments
    ]
    ordered = tuple(sorted(entries, key=lambda e: (e.start, e.kind)))
    return CalendarDay(day, ordered, spans=typical.spans)


def week_calendar(plan: Plan, starts_on: date) -> list[CalendarDay]:
    """Return the calendar of the seven dates of the week that starts on `starts_on`."""
    return [calendar_day(plan, starts_on + timedelta(days=offset)) for offset in range(7)]
