"""Tests of the command-line interface against the conventions of the workspace."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from typer.testing import CliRunner

from horai import __version__
from horai.cli import app

runner = CliRunner()
DAY = ["--date", "2026-11-13"]


@pytest.mark.parametrize("flag", ["-v", "--version"])
def test_version_prints_and_exits_zero(flag: str) -> None:
    result = runner.invoke(app, [flag])
    assert result.exit_code == 0
    assert result.stdout.strip() == __version__


def test_info_exits_zero() -> None:
    assert runner.invoke(app, ["info"]).exit_code == 0


@pytest.mark.parametrize("arguments", [["--bogus"], ["info", "--bogus"], ["unknown"]])
def test_usage_error_exits_two(arguments: list[str]) -> None:
    assert runner.invoke(app, arguments).exit_code == 2


def test_check_passes_on_the_fixture(plan_folder: Path) -> None:
    result = runner.invoke(app, ["check", "--root", str(plan_folder), *DAY])
    assert result.exit_code == 0, result.stdout
    assert "0 error(s)" in result.stdout


def test_check_fails_with_status_one_and_reports_json(plan_folder: Path) -> None:
    path = plan_folder / "plan" / "deliverables" / "ctx-geometry.yml"
    path.write_text(path.read_text().replace("purpose: thesis", "purpose: absent"))
    result = runner.invoke(app, ["check", "--root", str(plan_folder), "--format", "json", *DAY])
    assert result.exit_code == 1
    issues = json.loads(result.stdout)
    assert [(i["rule"], i["record"]) for i in issues] == [("reference/missing", "ctx-geometry")]


def test_wrong_configuration_exits_two(plan_folder: Path) -> None:
    result = runner.invoke(app, ["check", "--config", str(plan_folder / "absent.yml")])
    assert result.exit_code == 2


def test_next_prints_the_tiers(plan_folder: Path) -> None:
    result = runner.invoke(app, ["next", "--stream", "inquiry", "--root", str(plan_folder), *DAY])
    assert result.exit_code == 0
    assert result.stdout.index("fit-gating-model") < result.stdout.index("prove-rank-bound")


def test_next_rejects_an_unknown_stream(plan_folder: Path) -> None:
    assert (
        runner.invoke(
            app, ["next", "--stream", "absent", "--root", str(plan_folder), *DAY]
        ).exit_code
        == 2
    )


def test_view_week(plan_folder: Path) -> None:
    result = runner.invoke(app, ["view", "week", "--root", str(plan_folder), *DAY])
    assert result.exit_code == 0
    assert "Week of 2026-11-09" in result.stdout and "remaining PT10H15M" in result.stdout
    assert "planning: PT45M, at most PT1H45M" in result.stdout


def test_start_and_stop_append_clock_entries(plan_folder: Path) -> None:
    root = ["--root", str(plan_folder)]
    first = runner.invoke(app, ["start", "simulate-noise", "--at", "2026-11-13T15:00+01:00", *root])
    again = runner.invoke(app, ["start", "simulate-noise", "--at", "2026-11-13T15:05+01:00", *root])
    stop = runner.invoke(app, ["stop", "--at", "2026-11-13T16:00+01:00", *root])
    idle = runner.invoke(app, ["stop", *root])
    assert [r.exit_code for r in (first, again, stop, idle)] == [0, 0, 0, 0]
    assert "already running" in again.stdout and "no task is running" in idle.stdout
    text = (plan_folder / "log" / "clock" / "2026-11.yml").read_text()
    assert text.endswith(
        "  - {at: 2026-11-13T15:00+01:00, event: start, task: simulate-noise}\n"
        "  - {at: 2026-11-13T16:00+01:00, event: stop}\n"
    )
    assert runner.invoke(app, ["check", *root, *DAY]).exit_code == 0


def test_start_creates_the_file_of_a_new_month(plan_folder: Path) -> None:
    result = runner.invoke(
        app,
        ["start", "simulate-noise", "--at", "2026-12-01T09:00+01:00", "--root", str(plan_folder)],
    )
    assert result.exit_code == 0
    assert (
        (plan_folder / "log" / "clock" / "2026-12.yml")
        .read_text()
        .startswith("_schema: horai:clock-log@1\n")
    )


def test_start_rejects_unknown_or_completed_tasks(plan_folder: Path) -> None:
    root = ["--root", str(plan_folder)]
    assert runner.invoke(app, ["start", "absent", *root]).exit_code == 2
    path = plan_folder / "plan" / "TODO.yml"
    path.write_text(
        path.read_text().replace(
            "action: Simulate the gated network under input noise",
            "action: Simulate the gated network under input noise\n        completed: 2026-11-12",
        )
    )
    assert runner.invoke(app, ["start", "simulate-noise", *root]).exit_code == 2


def test_start_refuses_a_clock_file_not_ending_with_its_entries(plan_folder: Path) -> None:
    path = plan_folder / "log" / "clock" / "2026-11.yml"
    path.write_text(path.read_text().replace("month: 2026-11\n", "") + "month: 2026-11\n")
    before = path.read_text()
    result = runner.invoke(
        app,
        ["start", "simulate-noise", "--at", "2026-11-13T15:00+01:00", "--root", str(plan_folder)],
    )
    assert result.exit_code == 2 and path.read_text() == before


def test_stages_creates_the_missing_milestones(plan_folder: Path) -> None:
    root = ["--root", str(plan_folder)]
    listed = runner.invoke(app, ["stages", "--dry-run", *root])
    assert listed.exit_code == 0 and "missing ctx-geometry-argument-plan (inquiry)" in listed.stdout
    created = runner.invoke(app, ["stages", *root])
    assert created.exit_code == 0, created.stdout
    path = plan_folder / "plan" / "TODO.yml"
    assert "id: ctx-geometry-argument-plan" in path.read_text()
    assert "stage: argument-plan" in path.read_text()
    assert runner.invoke(app, ["check", *root, *DAY]).exit_code == 0
    assert "no stage is missing" in runner.invoke(app, ["stages", *root]).stdout


def test_stages_append_before_a_following_key(plan_folder: Path) -> None:
    path = plan_folder / "plan" / "TODO.yml"
    text = path.read_text()
    milestones, rest = text.split("questions:", 1)
    path.write_text(milestones + "questions:" + rest)
    assert runner.invoke(app, ["stages", "--root", str(plan_folder)]).exit_code == 0
    written = path.read_text()
    assert written.index("id: ctx-geometry-argument-plan") < written.index("questions:")
    assert written.startswith("_schema: horai:actions@1\nmilestones:\n")
