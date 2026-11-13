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
