"""Tests of the typical week, of the departures of single dates, and of their checks."""

from __future__ import annotations

import dataclasses
from datetime import date, time, timedelta
from pathlib import Path

import pytest
from conftest import DAY

from horai.domain.records import (
    Absence,
    Allocation,
    Appointment,
    Deadline,
    Block,
    DayChange,
    PartyRef,
    Plan,
    Stage,
    Stream,
    Task,
)
from horai.io.loader import load_plan
from horai.rules.calendar_checks import plannable_hours
from horai.io.schemas import SchemaSet
from horai.rules.calendar import calendar_day, week_calendar
from horai.rules.checks import check_plan
from horai.rules.selection import select
from horai.rules.stages import missing_stages
from horai.rules.state import current_week, task_state

FRIDAY = date(2026, 11, 13)
DAY_REVIEW = date(2026, 11, 9)


def _rules(plan: Plan) -> set[str]:
    return {issue.rule for issue in check_plan(plan, DAY)}


def _change(plan: Plan, day: date, change: DayChange) -> None:
    plan.dates[day] = change


def _typical_day(plan: Plan, weekday: str, **changes) -> None:
    week = plan.typical_week
    assert week is not None
    day = dataclasses.replace(week.days[weekday], **changes)
    plan.typical_week = dataclasses.replace(week, days={**week.days, weekday: day})


# --- Calendar -------------------------------------------------------------------------------------


def test_typical_week_gives_the_calendar_and_its_capacity(plan: Plan) -> None:
    friday = calendar_day(plan, FRIDAY)
    assert [(e.kind, e.start) for e in friday.entries] == [
        ("block", time(9)),
        ("appointment", time(10)),
        ("block", time(13, 30)),
    ]
    assert plan.typical_week is not None
    assert plan.typical_week.capacity == timedelta(hours=33, minutes=30)
    assert plan.typical_week.minimum_span == timedelta(hours=3)


def test_dated_appointment_joins_its_date(plan: Plan) -> None:
    thursday = calendar_day(plan, date(2026, 11, 12))
    assert [e.appointment.id for e in thursday.entries if e.appointment] == [
        "supervision-2026-11-12"
    ]


def test_cancelled_and_moved_recurring_appointments(plan: Plan) -> None:
    _change(plan, FRIDAY, DayChange(cancelled=("lab-meeting",)))
    assert not [e for e in calendar_day(plan, FRIDAY).entries if e.kind == "appointment"]
    _change(plan, FRIDAY, DayChange(moved={"lab-meeting": (time(15), None)}))
    moved = [e for e in calendar_day(plan, FRIDAY).entries if e.kind == "appointment"]
    assert [(e.start, e.length) for e in moved] == [(time(15), timedelta(hours=1))]


def test_unavailable_day_and_replaced_blocks(plan: Plan) -> None:
    plan.absences = (Absence(date(2026, 11, 10), date(2026, 11, 10), "conference"),)
    _change(
        plan, date(2026, 11, 11), DayChange(blocks=(Block(time(14), timedelta(hours=2), "tools"),))
    )
    days = week_calendar(plan, date(2026, 11, 9))
    assert days[1].unavailable and days[1].reason == "conference" and not days[1].entries
    assert [(e.start, e.stream) for e in days[2].blocks()] == [(time(14), "tools")]


def test_change_recorded_ahead_does_not_start_a_week(plan: Plan) -> None:
    _change(plan, date(2026, 11, 20), DayChange(cancelled=("lab-meeting",)))
    assert not [e for e in calendar_day(plan, date(2026, 11, 20)).entries if e.appointment]
    assert check_plan(plan, DAY) == []
    postponed = date(2026, 11, 16)
    item = plan.items["ctx-population-fit"]
    assert current_week(plan, postponed) == date(2026, 11, 9)
    assert task_state(plan, item, item.tasks[0], postponed) == "week"


def test_absence_covers_a_range_of_dates(plan: Plan) -> None:
    plan.absences = (Absence(date(2026, 12, 1), date(2026, 12, 21), "travel"),)
    assert (
        all(calendar_day(plan, date(2026, 12, d)).unavailable for d in (1, 10, 21))
        and not calendar_day(plan, date(2026, 12, 22)).unavailable
    )
    plan.absences = (Absence(date(2026, 12, 21), date(2026, 12, 1)),)
    assert "calendar/absence" in _rules(plan)


# --- Checks of the calendar -----------------------------------------------------------------------


def test_block_outside_the_spans_and_overlapping_an_appointment(plan: Plan) -> None:
    _typical_day(
        plan,
        "fri",
        blocks=(
            Block(time(9), timedelta(hours=2), "inquiry"),
            Block(time(18), timedelta(hours=1), "training"),
        ),
    )
    assert {"calendar/outside-spans", "calendar/overlap"} <= _rules(plan)


def test_inverted_and_overlapping_spans(plan: Plan) -> None:
    _typical_day(plan, "tue", spans=((600, 540), (540, 780), (720, 900)))
    messages = [i.message for i in check_plan(plan, DAY) if i.rule == "calendar/span"]
    assert any("end after it starts" in m for m in messages) and any(
        "overlap" in m for m in messages
    )


def test_planned_block_outside_the_hours_of_high_energy(plan: Plan) -> None:
    _typical_day(plan, "thu", blocks=(Block(time(14), timedelta(hours=2), "inquiry"),))
    issues = [i for i in check_plan(plan, DAY) if i.rule == "calendar/energy"]
    assert [i.severity for i in issues] == ["warning"]


def test_appointment_may_name_any_stream_of_the_profile(plan: Plan) -> None:
    talk = Appointment("talk", time(15), timedelta(minutes=30), "inquiry", PartyRef(name="team"))
    _typical_day(plan, "fri", appointed=(talk,))
    assert "reference/stream" not in _rules(plan)
    _typical_day(plan, "fri", appointed=(dataclasses.replace(talk, stream="absent"),))
    assert "reference/stream" in _rules(plan)


def test_date_cancels_a_known_appointment(plan: Plan) -> None:
    _change(plan, FRIDAY, DayChange(cancelled=("absent-meeting",)))
    assert "reference/appointment" in _rules(plan)


def test_task_prepares_a_known_appointment(plan: Plan) -> None:
    task = dataclasses.replace(plan.loose[0], prepares="lab-meeting")
    plan.loose = (task, *plan.loose[1:])
    assert check_plan(plan, DAY) == []
    plan.loose = (dataclasses.replace(task, prepares="absent"), *plan.loose[1:])
    assert "reference/appointment" in _rules(plan)


# --- Profile and types of deliverable -------------------------------------------------------------


def _stream(plan: Plan, stream: Stream) -> None:
    assert plan.profile is not None
    plan.profile = dataclasses.replace(
        plan.profile, streams={**plan.profile.streams, stream.id: stream}
    )


def test_reserve_per_event_names_known_appointments(plan: Plan) -> None:
    per_event = Allocation("reserve", "at_most", timedelta(hours=2), "event", ("lab-meeting",))
    _stream(plan, Stream("tools", "builds the tools", ("means",), "demand", per_event))
    assert "profile/allocation" not in _rules(plan)
    absent = dataclasses.replace(per_event, events=("absent-meeting",))
    _stream(plan, Stream("tools", "builds the tools", ("means",), "demand", absent))
    assert "profile/allocation" in _rules(plan)


def test_shares_beyond_the_plannable_time(plan: Plan) -> None:
    _stream(
        plan, Stream("tools", "builds", ("means",), "demand", Allocation("share", "exact", 0.6))
    )
    assert "profile/allocation" in _rules(plan)


def test_blocks_against_the_allocation(plan: Plan) -> None:
    inquiry = Stream(
        "inquiry", "advances", ("results",), "selection", Allocation("share", "exact", 0.3)
    )
    _stream(plan, inquiry)
    messages = [i.message for i in check_plan(plan, DAY) if i.rule == "calendar/allocation"]
    assert len(messages) == 1 and "inquiry" in messages[0] and "51.3%" in messages[0]
    requests = Allocation("reserve", "exact", timedelta(hours=2))
    _stream(plan, Stream("requests", "answers", ("coordination",), "arrival", requests))
    assert sum("requests" in i.message for i in check_plan(plan, DAY)) == 1


def test_each_arrival_stream_is_held_by_its_own_blocks(plan: Plan) -> None:
    reserve = Allocation("reserve", "at_least", timedelta(minutes=30))
    _stream(plan, Stream("incidents", "repairs incidents", ("integrity",), "arrival", reserve))
    messages = [i.message for i in check_plan(plan, DAY) if i.rule == "calendar/allocation"]
    assert any("incidents 0.0 h, for a reserve of 0.5 h" in m for m in messages)
    assert not any("stream requests" in m for m in messages)


def test_request_window_serves_hand_offs_of_any_stream(plan: Plan) -> None:
    item = plan.items["ctx-population-fit"]
    tasks = tuple(
        dataclasses.replace(t, hands_off=True) if t.id == "fit-gating-model" else t
        for t in item.tasks
    )
    plan.items[item.id] = dataclasses.replace(item, tasks=tasks)
    reply = Task("reply-to-editor", "Reply", None, stream="requests", committed_week=DAY_REVIEW)
    plan.loose = (*plan.loose, reply)
    window = calendar_day(plan, date(2026, 11, 9)).blocks()[1]
    assert (window.start, window.stream) == (time(12, 30), "requests")
    tiers = select(plan, DAY, "requests", ()).tiers
    assert [[c.task.id for c in tier] for tier in tiers] == [
        ["reply-to-editor"],
        ["fit-gating-model"],
    ]
    assert "fit-gating-model" not in {
        c.task.id for t in select(plan, DAY, "training", ()).tiers for c in t
    }


def test_deliverable_takes_the_defaults_of_its_type(plan: Plan) -> None:
    deliverable = plan.deliverables["ctx-geometry"]
    assert plan.phase_of(deliverable) == "validation"
    assert plan.stages_of(deliverable)[0] == Stage("argument-plan", "validation")
    own = (Stage("draft", "delivery"),)
    bare = dataclasses.replace(deliverable, phase=None, stages=own)
    assert plan.phase_of(bare) == "exploration" and plan.stages_of(bare) == own
    plan.deliverables["ctx-geometry"] = dataclasses.replace(deliverable, type="book")
    assert "reference/type" in _rules(plan)


def test_stage_takes_its_own_defaults_before_those_of_its_type(plan: Plan) -> None:
    deliverable = plan.deliverables["ctx-geometry"]
    stages = {stage.id: stage for stage in plan.stages_of(deliverable)}
    assert plan.stage_defaults(deliverable, stages["submission"])[0] == "routine"
    assert plan.stage_defaults(deliverable, stages["draft"])[0] == "exploratory"


def test_missing_stages_follow_the_phase_of_the_deliverable(plan: Plan) -> None:
    missing = missing_stages(plan)
    assert [(m.name, m.predictability, m.stream) for m in missing] == [
        ("ctx-geometry-argument-plan", "exploratory", "inquiry")
    ]
    delivery = dataclasses.replace(plan.deliverables["ctx-geometry"], phase="delivery")
    plan.deliverables["ctx-geometry"] = delivery
    assert len(missing_stages(plan)) == 5
    held = dataclasses.replace(plan.items["ctx-rank-bound"], stage="draft")
    plan.items["ctx-rank-bound"] = held
    assert "ctx-geometry-draft" not in {m.name for m in missing_stages(plan)}
    assert "identifier/stage" in _rules(plan)
    plan.items["ctx-rank-bound"] = dataclasses.replace(held, stage="absent")
    assert "reference/stage" in _rules(plan)


def test_appointment_every_two_weeks_and_in_month(plan: Plan) -> None:
    lab = plan.typical_week.days["fri"].appointed[0] if plan.typical_week else None
    assert lab is not None
    fortnightly = dataclasses.replace(lab, first=date(2026, 11, 6), every_weeks=2)
    _typical_day(plan, "fri", appointed=(fortnightly,))
    assert [
        d
        for d in (6, 13, 20, 27)
        if any(e.appointment for e in calendar_day(plan, date(2026, 11, d)).entries)
    ] == [6, 20]
    last = dataclasses.replace(lab, in_month=(1, -1))
    _typical_day(plan, "fri", appointed=(last,))
    assert [
        d
        for d in (6, 13, 20, 27)
        if any(e.appointment for e in calendar_day(plan, date(2026, 11, d)).entries)
    ] == [6, 27]
    wrong = dataclasses.replace(lab, first=date(2026, 11, 5), every_weeks=2)
    _typical_day(plan, "fri", appointed=(wrong,))
    assert "calendar/recurrence" in _rules(plan)


def test_fortnightly_appointment_counts_half_its_time(plan: Plan) -> None:
    before = plannable_hours(plan)
    assert before is not None and plan.typical_week is not None
    lab = plan.typical_week.days["fri"].appointed[0]
    _typical_day(plan, "fri", appointed=(dataclasses.replace(lab, first=FRIDAY, every_weeks=2),))
    assert plannable_hours(plan) == pytest.approx(before + 0.5)


def test_unplaced_appointment_of_a_longer_period(plan: Plan) -> None:
    assert plan.typical_week is not None
    unplaced = plan.typical_week.unplaced[0]
    every_two = dataclasses.replace(unplaced, every_weeks=2, first=date(2026, 11, 2))
    plan.typical_week = dataclasses.replace(plan.typical_week, unplaced=(every_two,))
    assert every_two.period_of(DAY) == (date(2026, 11, 2), date(2026, 11, 15))
    placing = plan.dates.pop(date(2026, 11, 12))
    assert "calendar/unplaced" in _rules(plan)
    _change(plan, date(2026, 11, 3), placing)
    assert "calendar/unplaced" not in _rules(plan)
    monthly = dataclasses.replace(unplaced, every_weeks=None)
    assert monthly.period_of(DAY) == (date(2026, 11, 1), date(2026, 11, 30))


# --- Unknown record types ------------------------------------------------------------------------


def test_unknown_record_type_is_reported(plan_folder: Path, schemas: SchemaSet) -> None:
    stray = plan_folder / "stray"
    stray.mkdir()
    (stray / "typo.yml").write_text("_schema: horai:milstone@1\ntitle: Typo\n")
    (stray / "horai.yml").write_text("_schema: horai:configuration@1\nplan: .\n")
    _, issues = load_plan(plan_folder, schemas, roots=[stray], base=plan_folder)
    assert [(i.rule, i.path) for i in issues] == [("schema/unknown", "stray/typo.yml")]


# --- Parties, unplaced appointments and single blocks -------------------------------------------


def test_undeclared_party_and_occasional_party(plan: Plan) -> None:
    occasional = Appointment(
        "tea", time(14, 30), timedelta(minutes=30), "meetings", PartyRef(name="Jane")
    )
    _typical_day(plan, "tue", appointed=(occasional,))
    assert "reference/party" not in _rules(plan)
    typo = dataclasses.replace(occasional, party=PartyRef(id="supervisr"))
    _typical_day(plan, "tue", appointed=(typo,))
    assert "reference/party" in _rules(plan)


def test_party_of_a_deadline_is_declared(plan: Plan) -> None:
    deliverable = plan.deliverables["ctx-geometry"]
    due = Deadline(date(2027, 3, 1), "hard", PartyRef(id="journl"))
    plan.deliverables["ctx-geometry"] = dataclasses.replace(deliverable, deadline=due)
    assert ("reference/party", "ctx-geometry") in {
        (i.rule, i.record) for i in check_plan(plan, DAY)
    }


def test_derived_deliverable_names_an_original(plan: Plan) -> None:
    article = plan.deliverables["ctx-geometry"]
    talk = dataclasses.replace(article, id="ctx-talk", type="poster", derived_from="ctx-geometry")
    plan.deliverables["ctx-talk"] = talk
    assert "reference/derived" not in _rules(plan) and "reference/missing" not in _rules(plan)
    plan.deliverables["ctx-poster"] = dataclasses.replace(
        talk, id="ctx-poster", derived_from="ctx-talk"
    )
    assert "reference/derived" in _rules(plan)


def test_started_week_must_place_the_unplaced_appointment(plan: Plan) -> None:
    change = plan.dates[date(2026, 11, 12)]
    unplaced = dataclasses.replace(change.appointments[0], places=None)
    _change(plan, date(2026, 11, 12), dataclasses.replace(change, appointments=(unplaced,)))
    issues = [i for i in check_plan(plan, DAY) if i.rule == "calendar/unplaced"]
    assert [i.severity for i in issues] == ["warning"]


def test_ended_week_is_not_checked_for_placements(plan: Plan) -> None:
    placing = plan.dates.pop(date(2026, 11, 12))
    assert "calendar/unplaced" in _rules(plan)
    plan.reviews = (*plan.reviews, date(2026, 11, 16))
    _change(plan, date(2026, 11, 19), placing)
    later = date(2026, 11, 17)
    assert "calendar/unplaced" not in {i.rule for i in check_plan(plan, later)}


def test_preparation_needs_blocks_of_its_stream(plan: Plan) -> None:
    preparation = Task(
        "prepare-supervision",
        "Prepare the supervision meeting",
        None,
        stream="meetings",
        committed_week=date(2026, 11, 9),
        budget=timedelta(hours=2),
        prepares="supervision-2026-11-12",
    )
    plan.loose = (*plan.loose, preparation)
    issues = [i for i in check_plan(plan, DAY) if i.rule == "calendar/preparation"]
    assert [i.severity for i in issues] == ["warning"]
    assert "0.0 h, for 2.0 h of preparation" in issues[0].message
    block = Block(time(14), timedelta(hours=2), "meetings")
    _change(plan, FRIDAY, DayChange(added_blocks=(block,)))
    assert check_plan(plan, DAY) == []
    offered = select(plan, DAY, calendar_day(plan, FRIDAY).blocks()[-1].stream, ())
    assert [[c.task.id for c in tier] for tier in offered.tiers] == [["prepare-supervision"]]
    plan.loose = (*plan.loose[:-1], dataclasses.replace(preparation, budget=timedelta(hours=4)))
    assert {"calendar/preparation", "calendar/allocation"} <= _rules(plan)


def test_added_and_removed_blocks(plan: Plan) -> None:
    added = Block(time(14), timedelta(hours=1), "meetings")
    _change(plan, FRIDAY, DayChange(removed_blocks=(time(13, 30),), added_blocks=(added,)))
    blocks = [(e.start, e.stream) for e in calendar_day(plan, FRIDAY).blocks()]
    assert blocks == [(time(9), "inquiry"), (time(14), "meetings")]
    assert check_plan(plan, DAY) == []
    _change(plan, FRIDAY, DayChange(removed_blocks=(time(15),)))
    assert "reference/block" in _rules(plan)
