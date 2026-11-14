"""
Conversion of the ISO 8601 notations used by the records of a plan.

The records hold dates, hours of the day, timestamps and durations as strings, which their schemas
validate. This module converts them, once, into the types of the standard library.

Functions
---------
parse_duration(text) -> timedelta
    Convert an ISO 8601 duration in days, hours and minutes.
format_duration(value) -> str
    Write a duration in the notation that `parse_duration` reads.
parse_date(text) -> date
    Convert an ISO 8601 date.
parse_time(text) -> time
    Convert an hour of the day.
parse_timestamp(text) -> datetime
    Convert an ISO 8601 timestamp, which must carry its offset.
pert(optimistic, probable, pessimistic) -> timedelta
    Compute the PERT value of three durations.
parse_span(text) -> tuple[int, int]
    Convert an interval of one day into its bounds, in minutes after midnight.
minute_of_day(moment) -> int
    Return the minutes after midnight of an hour of the day.
"""

from __future__ import annotations

import re
from datetime import date, datetime, time, timedelta

_DURATION = re.compile(r"^P(?=\d|T\d)(?:(\d+)D)?(?:T(?=\d)(?:(\d+)H)?(?:(\d+)M)?)?$")


def parse_duration(text: str) -> timedelta:
    """Convert an ISO 8601 duration in days, hours and minutes.

    Parameters
    ----------
    text : str
        A duration such as ``PT4H``, ``PT1H30M`` or ``P1D``.

    Returns
    -------
    timedelta
        The duration.

    Raises
    ------
    ValueError
        If the text is not a duration of the admitted form.

    Examples
    --------
    >>> parse_duration("PT1H30M")
    datetime.timedelta(seconds=5400)
    """
    match = _DURATION.match(text)
    if match is None:
        raise ValueError(f"not an ISO 8601 duration in days, hours and minutes: {text!r}")
    days, hours, minutes = (int(group) if group else 0 for group in match.groups())
    return timedelta(days=days, hours=hours, minutes=minutes)


def format_duration(value: timedelta) -> str:
    """Write a duration in the notation that `parse_duration` reads, rounded to the minute.

    Examples
    --------
    >>> format_duration(timedelta(hours=1, minutes=45))
    'PT1H45M'
    >>> format_duration(timedelta(0))
    'PT0M'
    """
    minutes = round(value.total_seconds() / 60)
    sign = "-" if minutes < 0 else ""
    hours, minutes = divmod(abs(minutes), 60)
    parts = (f"{hours}H" if hours else "") + (f"{minutes}M" if minutes or not hours else "")
    return f"{sign}PT{parts}"


def parse_date(text: str) -> date:
    """Convert an ISO 8601 date such as ``2026-11-13``."""
    return date.fromisoformat(text)


def parse_time(text: str) -> time:
    """Convert an hour of the day such as ``09:30``."""
    return time.fromisoformat(text)


def parse_timestamp(text: str) -> datetime:
    """Convert an ISO 8601 timestamp, which must carry the offset of its time zone.

    Raises
    ------
    ValueError
        If the timestamp has no offset.

    Examples
    --------
    >>> parse_timestamp("2026-11-13T09:02+01:00").utcoffset()
    datetime.timedelta(seconds=3600)
    """
    value = datetime.fromisoformat(text)
    if value.tzinfo is None:
        raise ValueError(f"timestamp without the offset of its time zone: {text!r}")
    return value


def pert(optimistic: timedelta, probable: timedelta, pessimistic: timedelta) -> timedelta:
    """Compute the PERT value of three durations, (optimistic + 4 probable + pessimistic) / 6.

    Examples
    --------
    >>> pert(timedelta(hours=4), timedelta(hours=5), timedelta(hours=12))
    datetime.timedelta(seconds=21600)
    """
    return (optimistic + 4 * probable + pessimistic) / 6


def parse_span(text: str) -> tuple[int, int]:
    """Convert an interval of one day, such as ``08:30-12:30``, into its bounds in minutes.

    The end may be ``24:00``, the end of the day. An interval that ends before it starts is
    returned as written, and the check of the calendar reports it.

    Examples
    --------
    >>> parse_span("08:30-12:30")
    (510, 750)
    >>> parse_span("20:00-24:00")
    (1200, 1440)
    """
    start, end = text.split("-")
    bounds = []
    for part in (start, end):
        hours, minutes = part.split(":")
        bounds.append(int(hours) * 60 + int(minutes))
    return bounds[0], bounds[1]


def minute_of_day(moment: time) -> int:
    """Return the minutes after midnight of an hour of the day.

    Examples
    --------
    >>> minute_of_day(time(9, 30))
    570
    """
    return moment.hour * 60 + moment.minute
