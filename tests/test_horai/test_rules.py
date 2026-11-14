"""Tests of the rules: state, time spent, budgets, selection and checks."""

from __future__ import annotations

import dataclasses
from datetime import date, datetime, timedelta, timezone

from conftest import DAY

from horai.domain.records import ClockEntry, Cycle, DecisionEntry, Item, Plan, Task
from horai.rules.budgets import budget_status
from horai.rules.checks import check_plan
from horai.rules.selection import select
from horai.rules.state import is_open_on, task_state
from horai.rules.time_spent import spans, time_by_task_and_day

TZ = timezone(timedelta(hours=1))


def _at(day: int, hour: int, minute: int = 0) -> datetime:
    return datetime(2026, 11, day, hour, minute, tzinfo=TZ)


def _replace_item(plan: Plan, identifier: str, **changes) -> None:
    plan.items[identifier] = dataclasses.replace(plan.items[identifier], **changes)


def _replace_task(plan: Plan, identifier: str, **changes) -> None:
    item, task = plan.find_task(identifier)
    tasks = tuple(
        dataclasses.replace(t, **changes) if t.id == identifier else t for t in item.tasks
    )
    _replace_item(plan, item.id, tasks=tasks)


def _located_on(plan: Plan, day: date) -> set[tuple[str, str]]:
    return {(issue.rule, issue.record) for issue in check_plan(plan, day)}


# --- State ----------------------------------------------------------------------------------------


def test_state_follows_the_week_and_the_cycle(plan: Plan) -> None:
    item = plan.items["ctx-population-fit"]
    states = {task.id: task_state(plan, item, task, DAY) for task in item.tasks}
    assert states == {
        "fit-gating-model": "week",
        "compare-geometries": "week",
        "write-methods-paragraph": "cycle",
    }
    assert task_state(plan, None, plan.holding[0], DAY) == "backlog"


def test_week_ends_at_the_next_review_held(plan: Plan) -> None:
    item = plan.items["ctx-population-fit"]
    late = date(2026, 11, 17)
    assert task_state(plan, item, item.tasks[0], late) == "week"
    assert ("review/overdue", "") in _located_on(plan, late)
    plan.reviews = (*plan.reviews, date(2026, 11, 16))
    assert task_state(plan, item, item.tasks[0], late) == "cycle"
    assert ("review/overdue", "") not in _located_on(plan, late)


def test_loose_task_waits_in_the_backlog_until_committed(plan: Plan) -> None:
    committed = next(task for task in plan.loose if task.id == "chapter-3-exercises")
    assert task_state(plan, None, committed, DAY) == "week"
    task = dataclasses.replace(committed, committed_week=None)
    assert task_state(plan, None, task, DAY) == "backlog"
    assert task_state(plan, None, dataclasses.replace(task, stream=None), DAY) == "backlog"


def test_recurring_task_reopens_with_its_period(plan: Plan) -> None:
    tasks = {task.id: task for task in plan.loose}
    weekly = dataclasses.replace(tasks["weekly-review"], completed=date(2026, 11, 9))
    assert task_state(plan, None, weekly, DAY) == "week" and not is_open_on(plan, weekly, DAY)
    plan.reviews = (*plan.reviews, date(2026, 11, 16))
    assert is_open_on(plan, weekly, date(2026, 11, 16))
    daily = dataclasses.replace(tasks["daily-planning"], completed=date(2026, 11, 12))
    assert is_open_on(plan, daily, DAY) and not is_open_on(plan, daily, date(2026, 11, 12))
    per_cycle = dataclasses.replace(tasks["cycle-planning"], completed=date(2026, 12, 8))
    assert not is_open_on(plan, per_cycle, date(2026, 12, 9))
    plan.cycles["2026-c7"] = Cycle("2026-c7", date(2026, 12, 14), date(2027, 1, 22))
    assert is_open_on(plan, per_cycle, date(2026, 12, 14))


# --- Time spent -----------------------------------------------------------------------------------


def test_spans_close_on_the_next_entry_and_run_until_now() -> None:
    entries = [
        ClockEntry(_at(13, 9), "start", "a"),
        ClockEntry(_at(13, 10), "start", "b"),
        ClockEntry(_at(13, 11), "stop"),
        ClockEntry(_at(13, 14), "start", "c"),
    ]
    work = spans(entries, now=_at(13, 14, 30))
    assert [(s.task, s.end - s.start, s.running) for s in work] == [
        ("a", timedelta(hours=1), False),
        ("b", timedelta(hours=1), False),
        ("c", timedelta(minutes=30), True),
    ]
    assert len(spans(entries)) == 2


def test_span_across_midnight_is_split_by_day() -> None:
    work = spans([ClockEntry(_at(12, 23), "start", "a"), ClockEntry(_at(13, 1), "stop")])
    totals = time_by_task_and_day(work)
    assert totals == {
        ("a", date(2026, 11, 12)): timedelta(hours=1),
        ("a", date(2026, 11, 13)): timedelta(hours=1),
    }


# --- Budgets --------------------------------------------------------------------------------------


def test_remaining_work_is_the_budget_less_the_time_since_it_was_set(plan: Plan) -> None:
    status = budget_status(plan, plan.items["ctx-population-fit"], spans(plan.clock))
    assert status.consumed == timedelta(hours=1, minutes=45)
    assert status.since == date(2026, 11, 2)
    assert status.remaining == timedelta(hours=10, minutes=15) and not status.exhausted


def test_renewal_resets_the_count(plan: Plan) -> None:
    plan.decisions = (DecisionEntry(date(2026, 11, 13), "ctx-population-fit", "renew", "new fact"),)
    status = budget_status(plan, plan.items["ctx-population-fit"], spans(plan.clock))
    assert status.since == date(2026, 11, 13) and status.remaining == timedelta(hours=12)


def test_consumed_budget_is_exhausted(plan: Plan) -> None:
    _replace_item(plan, "ctx-rank-bound", budget=timedelta(hours=1))
    status = budget_status(plan, plan.items["ctx-rank-bound"], spans(plan.clock))
    assert status.exhausted and status.remaining == timedelta(0)


def test_carried_item_keeps_its_budget_until_a_decision(plan: Plan) -> None:
    cycle = plan.cycles["2026-c6"]
    plan.cycles["2026-c6"] = dataclasses.replace(cycle, start=date(2026, 11, 13))
    item = plan.items["ctx-population-fit"]
    status = budget_status(plan, item, spans(plan.clock))
    assert status.carried and status.since == date(2026, 11, 12)
    assert status.remaining == timedelta(hours=10, minutes=15)
    assert ("budget/carried", item.id) in _located(plan)
    selection = select(plan, DAY, "inquiry", spans(plan.clock))
    assert any("carried into its cycle" in note for note in selection.notes)
    plan.decisions = (DecisionEntry(date(2026, 11, 12), item.id, "renew", "new fact"),)
    status = budget_status(plan, item, spans(plan.clock))
    assert not status.carried and status.remaining == timedelta(hours=12)
    assert ("budget/carried", item.id) not in _located(plan)


def test_excluded_cycle_makes_the_status_undefined(plan: Plan) -> None:
    plan.excluded.add("2026-c6")
    assert budget_status(plan, plan.items["ctx-population-fit"], ()).undefined


# --- Selection ------------------------------------------------------------------------------------


def _first_tier_ids(plan: Plan, stream: str | None = "inquiry") -> list[str]:
    selection = select(plan, DAY, stream, spans(plan.clock))
    return [[c.task.id for c in tier] for tier in selection.tiers]


def test_selection_orders_by_rank_and_excludes_waits_and_open_predecessors(plan: Plan) -> None:
    assert _first_tier_ids(plan) == [["fit-gating-model"], ["prove-rank-bound"], ["simulate-noise"]]


def test_completed_predecessor_releases_its_successor(plan: Plan) -> None:
    _replace_task(plan, "fit-gating-model", completed=DAY)
    assert _first_tier_ids(plan)[0] == ["compare-geometries"]


def test_unranked_items_tie_after_the_ranked_ones(plan: Plan) -> None:
    _replace_item(plan, "ctx-rank-bound", rank=None)
    _replace_item(plan, "gating-under-noise", rank=None)
    assert _first_tier_ids(plan) == [["fit-gating-model"], ["prove-rank-bound", "simulate-noise"]]


def test_exhausted_budget_leaves_the_candidates(plan: Plan) -> None:
    _replace_item(plan, "ctx-rank-bound", budget=timedelta(hours=1))
    selection = select(plan, DAY, "inquiry", spans(plan.clock))
    assert "prove-rank-bound" not in {c.task.id for tier in selection.tiers for c in tier}
    assert any("awaits a checkpoint" in note for note in selection.notes)


def test_non_negotiable_item_takes_every_stream(plan: Plan) -> None:
    _replace_item(plan, "gating-under-noise", non_negotiable=DAY)
    selection = select(plan, DAY, "training", spans(plan.clock))
    assert selection.marked is not None and _first_tier_ids(plan, "training") == [
        ["simulate-noise"]
    ]


def test_mark_on_a_closed_item_is_ignored_and_reported(plan: Plan) -> None:
    _replace_item(plan, "gating-under-noise", non_negotiable=DAY, status="done")
    selection = select(plan, DAY, "training", spans(plan.clock))
    assert selection.marked is None and _first_tier_ids(plan, "training") == [
        ["chapter-3-exercises"]
    ]
    assert "mark/closed" in _rules(plan)


def test_selection_admits_loose_tasks(plan: Plan) -> None:
    assert _first_tier_ids(plan, "training") == [["chapter-3-exercises"]]


# --- Checks ---------------------------------------------------------------------------------------


def _rules(plan: Plan) -> set[str]:
    return {issue.rule for issue in check_plan(plan, DAY)}


def _located(plan: Plan) -> set[tuple[str, str]]:
    return _located_on(plan, DAY)


def test_custom_rule_reopens_after_its_periods(plan: Plan) -> None:
    review = dataclasses.replace(plan.loose[0], recurs="P2C", completed=date(2026, 11, 3))
    plan.cycles["2026-c7"] = Cycle("2026-c7", date(2026, 12, 14), date(2027, 1, 22))
    assert not is_open_on(plan, review, date(2026, 12, 20))
    plan.cycles["2026-c8"] = Cycle("2026-c8", date(2027, 1, 25), date(2027, 3, 5))
    assert is_open_on(plan, review, date(2027, 1, 25))
    quarterly = dataclasses.replace(review, recurs="P3M", completed=date(2026, 11, 20))
    assert not is_open_on(plan, quarterly, date(2027, 1, 31))
    assert is_open_on(plan, quarterly, date(2027, 2, 1))


def test_named_rule_of_the_profile(plan: Plan) -> None:
    assert plan.profile is not None
    plan.profile = dataclasses.replace(plan.profile, recurrences={"fortnightly": "P2W"})
    task = dataclasses.replace(plan.loose[0], recurs="fortnightly", completed=date(2026, 11, 9))
    plan.loose = (*plan.loose[1:], task)
    plan.reviews = (*plan.reviews, date(2026, 11, 16))
    assert not is_open_on(plan, task, date(2026, 11, 16))
    plan.reviews = (*plan.reviews, date(2026, 11, 23))
    assert is_open_on(plan, task, date(2026, 11, 23))
    assert "reference/recurrence" not in _rules(plan)
    plan.loose = (*plan.loose[:-1], dataclasses.replace(task, recurs="biweekly"))
    assert "reference/recurrence" in _rules(plan)


def test_stream_with_committed_work_states_an_allocation(plan: Plan) -> None:
    _replace_item(plan, "ctx-population-fit", stream="upkeep")
    assert ("profile/allocation", "upkeep") in _located(plan)


def test_fixture_passes_every_check(plan: Plan) -> None:
    assert check_plan(plan, DAY) == []


def test_duplicate_identifier(plan: Plan) -> None:
    plan.holding = (Task("prove-rank-bound", "duplicate", None, held_since=DAY),)
    assert "identifier/duplicate" in _rules(plan)


def test_missing_and_excluded_references(plan: Plan) -> None:
    _replace_item(plan, "ctx-rank-bound", deliverable="absent", cycle="2026-c5")
    plan.excluded.add("2026-c5")
    assert {"reference/missing", "reference/excluded"} <= _rules(plan)


def test_second_non_negotiable_mark(plan: Plan) -> None:
    _replace_item(plan, "gating-under-noise", non_negotiable=DAY)
    _replace_task(plan, "prove-rank-bound", non_negotiable=DAY)
    assert "mark/non-negotiable" in _rules(plan)


def test_too_many_marks_for_one_day(plan: Plan) -> None:
    for identifier in ["compare-geometries", "prove-rank-bound", "simulate-noise"]:
        _replace_task(plan, identifier, marked_for=DAY, main_objective=True)
    assert {"mark/marked-for", "mark/main"} <= _rules(plan)


def test_selected_item_needs_a_budget_and_a_rank(plan: Plan) -> None:
    _replace_item(plan, "ctx-rank-bound", budget=None, rank=None)
    issues = [(i.rule, i.record) for i in check_plan(plan, DAY)]
    assert ("field/budget", "ctx-rank-bound") in issues and (
        "field/rank",
        "ctx-rank-bound",
    ) in issues


def test_held_task_needs_its_date_and_stop_needs_a_start(plan: Plan) -> None:
    plan.holding = (Task("loose-task", "loose", None),)
    plan.clock = plan.clock + (ClockEntry(_at(13, 20), "stop"),)
    assert {"field/held-since", "clock/stop"} <= _rules(plan)


def test_item_appears_in_an_unknown_stream(plan: Plan) -> None:
    plan.items["stray"] = Item("stray", "milestone", "Stray", "absent", rank=1)
    assert "reference/stream" in _rules(plan)
    plan.items.pop("stray")
    plan.loose = plan.loose + (Task("stray-task", "Stray", None, stream="absent"),)
    assert "reference/stream" in _rules(plan)


# --- Estimates and overhead -------------------------------------------------------------------------


def test_three_durations_give_a_pert_budget(plan: Plan) -> None:
    estimate = (timedelta(hours=4), timedelta(hours=5), timedelta(hours=12))
    _replace_item(plan, "ctx-rank-bound", budget=None, estimate=estimate)
    item = plan.items["ctx-rank-bound"]
    assert item.planned_budget == timedelta(hours=6)
    assert budget_status(plan, item, spans(plan.clock)).remaining == timedelta(hours=4, minutes=17)
    assert check_plan(plan, DAY) == []


def test_estimate_defects(plan: Plan) -> None:
    disordered = (timedelta(hours=5), timedelta(hours=4), timedelta(hours=12))
    _replace_item(plan, "ctx-rank-bound", estimate=disordered)
    _replace_item(plan, "gating-under-noise", estimate=(timedelta(hours=1),) * 3)
    messages = [i.message for i in check_plan(plan, DAY) if i.rule == "field/estimate"]
    assert len(messages) == 4  # rank bound: budget and order; question: budget and exploratory
    assert any("either a budget" in m for m in messages) and any("appetite" in m for m in messages)


def _loose(plan: Plan, task: Task) -> None:
    plan.loose = plan.loose + (task,)


def test_urgent_loose_task_precedes_the_milestones(plan: Plan) -> None:
    urgent = Task(
        "answer-referee",
        "Answer the referee",
        None,
        stream="inquiry",
        committed_week=date(2026, 11, 9),
        importance="high",
        scheduled=DAY,
    )
    later = dataclasses.replace(urgent, id="tidy-figures", title="Tidy", importance="low")
    _loose(plan, urgent)
    _loose(plan, later)
    tiers = _first_tier_ids(plan)
    assert tiers[0] == ["answer-referee"] and tiers[-1] == ["tidy-figures"]


def test_milestone_without_deliverable_serves_its_stream(plan: Plan) -> None:
    _replace_item(plan, "gating-under-noise", deliverable=None)
    assert check_plan(plan, DAY) == []
    assert "simulate-noise" in {t for tier in _first_tier_ids(plan) for t in tier}


# --- Order within a parent and dependencies across parents ------------------------------------------


def test_quadrant_orders_the_tasks_of_one_parent(plan: Plan) -> None:
    _replace_task(plan, "fit-gating-model", riskiest=False)
    _replace_task(plan, "compare-geometries", depends_on=())
    _replace_task(plan, "fit-gating-model", importance="low", scheduled=DAY)
    _replace_task(plan, "compare-geometries", importance="highest")
    tiers = _first_tier_ids(plan)
    assert tiers[:2] == [["compare-geometries"], ["fit-gating-model"]]
    _replace_task(plan, "fit-gating-model", importance="high")
    assert _first_tier_ids(plan)[:2] == [["fit-gating-model"], ["compare-geometries"]]


def test_dependency_across_parents(plan: Plan) -> None:
    _replace_task(plan, "prove-rank-bound", depends_on=("simulate-noise",))
    assert "prove-rank-bound" not in {t for tier in _first_tier_ids(plan) for t in tier}
    assert check_plan(plan, DAY) == []
    _replace_task(plan, "simulate-noise", completed=DAY)
    assert "prove-rank-bound" in {t for tier in _first_tier_ids(plan) for t in tier}


def test_dependency_cycle_and_missing_predecessor(plan: Plan) -> None:
    _replace_task(plan, "prove-rank-bound", depends_on=("simulate-noise",))
    _replace_task(plan, "simulate-noise", depends_on=("prove-rank-bound", "absent-task"))
    assert {"reference/cycle", "reference/task"} <= _rules(plan)
