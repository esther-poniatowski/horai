"""
The time spent on each task, computed from the clock entries and stored nowhere.

A ``start`` opens a span on its task, which the next clock entry closes, whether a ``stop`` or the
``start`` of another task. A span still open at the time of the computation runs until that time.
A span that crosses midnight is split between its days, in the time zone of its start.

Classes
-------
Span
    A period of work on one task.

Functions
---------
spans(entries, now) -> list[Span]
time_by_task_and_day(spans) -> dict[tuple[str, date], timedelta]
time_on(spans, identifiers, since) -> timedelta
"""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import date, datetime, timedelta

from ..domain.records import ClockEntry


@dataclass(frozen=True)
class Span:
    """A period of work on one task, or on a parent for work without a task."""

    task: str
    start: datetime
    end: datetime
    running: bool = False
    assigned: bool = False


def spans(entries: Iterable[ClockEntry], now: datetime | None = None) -> list[Span]:
    """Pair the clock entries into spans of work.

    Parameters
    ----------
    entries : Iterable[ClockEntry]
        The clock entries, in any order.
    now : datetime | None
        End of a span still open; without it, an open span is left out.

    Returns
    -------
    list[Span]
        The spans, in order of start.
    """
    ordered = sorted(entries, key=lambda entry: entry.at)
    result = []
    for index, entry in enumerate(ordered):
        if entry.event != "start" or entry.task is None:
            continue
        if index + 1 < len(ordered):
            result.append(
                Span(entry.task, entry.at, ordered[index + 1].at, assigned=entry.assigned)
            )
        elif now is not None and now > entry.at:
            result.append(Span(entry.task, entry.at, now, running=True, assigned=entry.assigned))
    return result


def _split_by_day(span: Span) -> list[tuple[date, timedelta]]:
    """Split a span at each midnight, in the time zone of its start."""
    parts, cursor = [], span.start
    while cursor < span.end:
        midnight = datetime.combine(
            cursor.date() + timedelta(days=1), datetime.min.time(), cursor.tzinfo
        )
        end = min(midnight, span.end)
        parts.append((cursor.date(), end - cursor))
        cursor = end
    return parts


def time_by_task_and_day(work: Iterable[Span]) -> dict[tuple[str, date], timedelta]:
    """Sum the spans per task and per day."""
    totals: dict[tuple[str, date], timedelta] = defaultdict(timedelta)
    for span in work:
        for day, length in _split_by_day(span):
            totals[(span.task, day)] += length
    return dict(totals)


def time_on(
    work: Iterable[Span],
    identifiers: set[str],
    since: date | None = None,
    until: date | None = None,
) -> timedelta:
    """Sum the time spent on the tasks or parents in `identifiers`, from `since` to `until`."""
    total = timedelta(0)
    for span in work:
        if span.task in identifiers:
            for day, length in _split_by_day(span):
                if (since is None or day >= since) and (until is None or day <= until):
                    total += length
    return total
