"""
Command-line interface of horai.

Commands
--------
check : Validate the files of a plan and the references between its records.
next : Apply the selection rule and print the candidates, in tiers.
view week : Print the view of the current week.
start : Mark the start of work on a task.
stop : Mark the stop of work.
info : Print diagnostic information.

The options ``--root`` and ``--config`` and the exit statuses follow the conventions of the command
line of the workspace: 0 on success, 1 when a check finds a problem, 2 for a wrong command line or
configuration.
"""

from __future__ import annotations

import json
import os
from datetime import date, datetime
from enum import StrEnum
from pathlib import Path

import typer

from . import __version__, info
from .domain.records import WEEKDAYS, ClockEntry, Plan
from .domain.time import parse_date, parse_timestamp
from .io.clock_writer import ClockFileError, append_clock_entry
from .io.config import Configuration, ConfigurationError, resolve_configuration
from .io.loader import load_plan
from .io.schemas import SchemaSet
from .issues import Issue, Severity
from .render.text import render_issues, render_selection, render_week
from .rules.checks import check_plan
from .rules.selection import select
from .rules.state import current_week
from .rules.time_spent import spans

app = typer.Typer(add_completion=False, no_args_is_help=True)
view_app = typer.Typer(no_args_is_help=True, help="Print a view of the plan.")
app.add_typer(view_app, name="view")

ROOT_OPTION = typer.Option(
    None, "--root", "-r", help="Folder from which the configuration is found."
)
CONFIG_OPTION = typer.Option(None, "--config", "-c", help="Configuration file of horai.")
DATE_OPTION = typer.Option(
    None, "--date", help="Day of the computation, in ISO 8601; today by default."
)


class ReportFormat(StrEnum):
    """Formats of the report of `check`."""

    TEXT = "text"
    JSON = "json"


def _fail(message: str, status: int = 2) -> typer.Exit:
    """Print `message` to the standard error, and return the exit to raise."""
    typer.echo(f"horai: {message}", err=True)
    return typer.Exit(status)


def _configure(root: Path | None, config: Path | None) -> Configuration:
    """Resolve the configuration, or exit with status 2."""
    try:
        return resolve_configuration(root, config, os.environ, Path.cwd())
    except ConfigurationError as error:
        raise _fail(str(error)) from error


def _now(configuration: Configuration) -> datetime:
    """Return the current moment, in the time zone of the configuration."""
    return datetime.now(configuration.timezone).astimezone(configuration.timezone)


def _day(value: str | None, configuration: Configuration) -> date:
    """Return the day given by --date, or today."""
    try:
        return parse_date(value) if value else _now(configuration).date()
    except ValueError as error:
        raise _fail(f"--date: {error}") from error


def _load(configuration: Configuration) -> tuple[Plan, list[Issue]]:
    """Load the plan named by the configuration."""
    return load_plan(
        configuration.plan,
        SchemaSet.load(),
        roots=configuration.roots,
        exclude=configuration.exclude,
        base=configuration.root,
    )


@app.command("check")
def cli_check(
    root: Path | None = ROOT_OPTION,
    config: Path | None = CONFIG_OPTION,
    day: str | None = DATE_OPTION,
    report: ReportFormat = typer.Option(
        ReportFormat.TEXT, "--format", help="Format of the report."
    ),
) -> None:
    """Validate the files of the plan and the references between its records."""
    configuration = _configure(root, config)
    plan, issues = _load(configuration)
    issues += check_plan(plan, _day(day, configuration))
    if report is ReportFormat.JSON:
        typer.echo(json.dumps([vars(issue) for issue in issues], indent=2, default=str))
    else:
        typer.echo(render_issues(issues))
    if any(issue.severity == Severity.ERROR for issue in issues):
        raise typer.Exit(1)


def _current_stream(plan: Plan, moment: datetime) -> str | None:
    """Return the stream of the block of the current week that holds `moment`, or None."""
    week = current_week(plan, moment.date())
    blocks = (
        week.blocks
        if week is not None and week.blocks is not None
        else (plan.template.blocks if plan.template else ())
    )
    weekday = WEEKDAYS[moment.weekday()]
    for block in blocks:
        start = datetime.combine(moment.date(), block.start, moment.tzinfo)
        if block.day == weekday and start <= moment < start + block.length:
            return block.stream
    return None


@app.command("next")
def cli_next(
    stream: str | None = typer.Option(None, "--stream", help="Stream of the current block."),
    root: Path | None = ROOT_OPTION,
    config: Path | None = CONFIG_OPTION,
    day: str | None = DATE_OPTION,
) -> None:
    """Apply the selection rule and print the candidates, in tiers."""
    configuration = _configure(root, config)
    plan, _ = _load(configuration)
    now = _now(configuration)
    on = _day(day, configuration)
    work = spans(plan.clock, now)
    if stream is None and not any(
        i.non_negotiable or any(t.non_negotiable for t in i.tasks) for i in plan.items.values()
    ):
        stream = _current_stream(plan, now)
        if stream is None:
            raise _fail("no block of the calendar holds this moment; name the stream with --stream")
    if stream is not None and plan.profile and stream not in plan.profile.streams:
        raise _fail(f"no stream {stream} in the profile")
    typer.echo(render_selection(select(plan, on, stream, work), stream))


@view_app.command("week")
def cli_view_week(
    root: Path | None = ROOT_OPTION,
    config: Path | None = CONFIG_OPTION,
    day: str | None = DATE_OPTION,
) -> None:
    """Print the view of the current week."""
    configuration = _configure(root, config)
    plan, _ = _load(configuration)
    work = spans(plan.clock, _now(configuration))
    typer.echo(render_week(plan, _day(day, configuration), work))


def _moment(at: str | None, configuration: Configuration) -> datetime:
    """Return the moment given by --at, in the configured zone when it has no offset, or now."""
    if at is None:
        return _now(configuration).replace(second=0, microsecond=0)
    try:
        moment = datetime.fromisoformat(at)
    except ValueError as error:
        raise _fail(f"--at: {error}") from error
    if moment.tzinfo is None:
        moment = (
            moment.replace(tzinfo=configuration.timezone)
            if configuration.timezone
            else moment.astimezone()
        )
    return parse_timestamp(moment.isoformat())


def _running(plan: Plan) -> str | None:
    """Return the task under way, from the last clock entry, or None."""
    entries = sorted(plan.clock, key=lambda e: e.at)
    return entries[-1].task if entries and entries[-1].event == "start" else None


AT_OPTION = typer.Option(None, "--at", help="Moment of the mark, in ISO 8601; now by default.")


@app.command("start")
def cli_start(
    task: str = typer.Argument(
        ..., help="Identifier of the task, or of a parent for work without a task."
    ),
    at: str | None = AT_OPTION,
    root: Path | None = ROOT_OPTION,
    config: Path | None = CONFIG_OPTION,
) -> None:
    """Mark the start of work on a task; the task under way stops."""
    configuration = _configure(root, config)
    plan, _ = _load(configuration)
    found = plan.find_task(task)
    if found is None and task not in plan.items:
        raise _fail(f"no task or parent named {task}")
    if found is not None and not found[1].is_open:
        raise _fail(f"the task {task} is completed")
    if _running(plan) == task:
        typer.echo(f"{task} is already running")
        return
    try:
        path = append_clock_entry(
            configuration.plan, ClockEntry(_moment(at, configuration), "start", task)
        )
    except ClockFileError as error:
        raise _fail(str(error)) from error
    typer.echo(f"started {task} ({path.relative_to(configuration.plan)})")


@app.command("stop")
def cli_stop(
    at: str | None = AT_OPTION,
    root: Path | None = ROOT_OPTION,
    config: Path | None = CONFIG_OPTION,
) -> None:
    """Mark the stop of work on the task under way."""
    configuration = _configure(root, config)
    plan, _ = _load(configuration)
    running = _running(plan)
    if running is None:
        typer.echo("no task is running")
        return
    try:
        append_clock_entry(configuration.plan, ClockEntry(_moment(at, configuration), "stop"))
    except ClockFileError as error:
        raise _fail(str(error)) from error
    typer.echo(f"stopped {running}")


@app.command("info")
def cli_info() -> None:
    """Display version and platform diagnostics."""
    typer.echo(info())


def _print_version(value: bool) -> None:
    """Print the version string and exit before any command is required."""
    if value:
        typer.echo(__version__)
        raise typer.Exit()


@app.callback()
def main_callback(  # pylint: disable=unused-argument  # typer reads the option
    version: bool = typer.Option(
        False,
        "--version",
        "-v",
        callback=_print_version,
        is_eager=True,
        help="Show the package version and exit.",
    )
) -> None:
    """Organize tasks, priorities and schedules from the YAML records of a plan."""
