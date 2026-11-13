"""Tests of the notations of time and of the YAML loader with the core types."""

from __future__ import annotations

from datetime import timedelta

import pytest

from horai.domain.time import format_duration, parse_duration, parse_timestamp
from horai.io.yaml_loader import load_yaml


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("PT4H", timedelta(hours=4)),
        ("PT1H30M", timedelta(minutes=90)),
        ("PT45M", timedelta(minutes=45)),
        ("P1D", timedelta(days=1)),
        ("P1DT2H", timedelta(hours=26)),
    ],
)
def test_parse_duration(text: str, expected: timedelta) -> None:
    assert parse_duration(text) == expected


@pytest.mark.parametrize("text", ["4h", "PT", "P", "PT1.5H", "1H30M", "PTH"])
def test_parse_duration_rejects_other_forms(text: str) -> None:
    with pytest.raises(ValueError):
        parse_duration(text)


@pytest.mark.parametrize(
    "value", [timedelta(0), timedelta(minutes=5), timedelta(hours=3, minutes=7)]
)
def test_format_duration_round_trips(value: timedelta) -> None:
    assert parse_duration(format_duration(value)) == value


def test_timestamp_requires_offset() -> None:
    assert parse_timestamp("2026-11-13T09:02+01:00").utcoffset() == timedelta(hours=1)
    with pytest.raises(ValueError):
        parse_timestamp("2026-11-13T09:02")


def test_loader_keeps_dates_hours_and_words_as_strings() -> None:
    data = load_yaml(
        "day: 2026-11-13\nstart: 10:00\nanswer: no\nflag: true\ncount: 3\nshare: 0.45\nnothing:"
    )
    assert data == {
        "day": "2026-11-13",
        "start": "10:00",
        "answer": "no",
        "flag": True,
        "count": 3,
        "share": 0.45,
        "nothing": None,
    }
