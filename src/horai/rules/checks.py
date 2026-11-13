"""
The checks across records, which the schemas of single files cannot express.

Each check returns the issues that it finds. A reference to a record excluded as invalid is
reported as excluded rather than missing, since its file exists but could not be read.

Functions
---------
check_plan(plan, day) -> list[Issue]
    Run every check on the plan, as it stands on `day`.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from collections.abc import Iterator
from datetime import date

from ..domain.records import Plan, Task
from ..issues import Issue, Severity
from .state import current_cycle


def _issue(
    plan: Plan, rule: str, message: str, record: str, severity: Severity = Severity.ERROR
) -> Issue:
    """Build an issue located at the file of `record`."""
    return Issue(rule, message, plan.sources.get(record, ""), record, severity)


def _missing(plan: Plan, kind: str, target: str, record: str) -> Issue:
    """Report a reference to a record that is absent, or excluded as invalid."""
    if target in plan.excluded:
        return _issue(
            plan, "reference/excluded", f"the {kind} {target} is excluded as invalid", record
        )
    return _issue(plan, "reference/missing", f"no {kind} named {target}", record)


def _all_tasks(plan: Plan) -> list[Task]:
    """Return the tasks held by items and by the holding file."""
    return [task for _, task in plan.tasks()] + list(plan.holding)


def check_identifiers(plan: Plan) -> Iterator[Issue]:
    """An identifier names one record or one task in the whole plan."""
    names = (
        list(plan.purposes)
        + list(plan.deliverables)
        + list(plan.items)
        + list(plan.appointments)
        + [task.id for task in _all_tasks(plan)]
    )
    for name, count in Counter(names).items():
        if count > 1:
            yield _issue(
                plan,
                "identifier/duplicate",
                f"the identifier {name} names {count} records; change the title of all but one",
                name,
            )


def _check_hierarchy(plan: Plan) -> Iterator[Issue]:
    """A deliverable names its purpose; an item, its deliverable, stream, cycle and dependencies."""
    streams = plan.profile.streams if plan.profile else {}
    for deliverable in plan.deliverables.values():
        if deliverable.purpose not in plan.purposes:
            yield _missing(plan, "purpose", deliverable.purpose, deliverable.id)
    for item in plan.items.values():
        if item.deliverable is not None and item.deliverable not in plan.deliverables:
            yield _missing(plan, "deliverable", item.deliverable, item.id)
        if plan.profile and item.stream not in streams:
            message = f"no stream {item.stream} in the profile"
            yield _issue(plan, "reference/stream", message, item.id)
        if item.cycle is not None and item.cycle not in plan.cycles:
            yield _missing(plan, "cycle", item.cycle, item.id)
        for dependency in item.depends_on:
            if dependency not in plan.items:
                yield _missing(plan, "milestone", dependency, item.id)


def _check_tasks(plan: Plan) -> Iterator[Issue]:
    """A task names predecessors of its own parent, and an opened week."""
    for item in plan.items.values():
        siblings = {task.id for task in item.tasks}
        for task in item.tasks:
            for predecessor in task.depends_on:
                if predecessor not in siblings:
                    message = f"the predecessor {predecessor} is not a task of {item.id}"
                    yield _issue(plan, "reference/task", message, task.id)
            if task.committed_week is not None and task.committed_week not in plan.weeks:
                message = f"no week opened on {task.committed_week}"
                yield _issue(plan, "reference/week", message, task.id)


def _check_calendar(plan: Plan) -> Iterator[Issue]:
    """An appointment names a stream of the regime appointed; a block names a stream."""
    if plan.profile is None:
        return
    streams = plan.profile.streams
    for appointment in plan.appointments.values():
        stream = streams.get(appointment.stream)
        if stream is None or stream.regime != "appointed":
            message = f"the stream {appointment.stream} is not a stream of the regime appointed"
            yield _issue(plan, "reference/stream", message, appointment.id)
    for block in plan.template.blocks if plan.template else ():
        if block.stream not in streams:
            message = f"no stream {block.stream} in the profile"
            yield Issue("reference/stream", message, "calendar/week-template.yml")


def _check_clock_tasks(plan: Plan) -> Iterator[Issue]:
    """A clock entry names a task or a parent of the plan."""
    known = {task.id for task in _all_tasks(plan)} | set(plan.items)
    for entry in plan.clock:
        if entry.task is not None and entry.task not in known:
            message = f"the clock entry of {entry.at.isoformat()} names no task {entry.task}"
            yield Issue("reference/task", message, f"log/clock/{entry.at:%Y-%m}.yml")


def check_references(plan: Plan) -> Iterator[Issue]:
    """Every reference names an existing record."""
    yield from _check_hierarchy(plan)
    yield from _check_tasks(plan)
    yield from _check_calendar(plan)
    yield from _check_clock_tasks(plan)


def check_marks(plan: Plan) -> Iterator[Issue]:
    """At most one item bears the non-negotiable mark, and each day bears its permitted marks."""
    marked = [item.id for item in plan.items.values() if item.non_negotiable] + [
        task.id for _, task in plan.tasks() if task.non_negotiable
    ]
    if len(marked) > 1:
        for name in marked:
            yield _issue(
                plan,
                "mark/non-negotiable",
                f"{len(marked)} items bear the non-negotiable mark, and at most one may: "
                + ", ".join(marked),
                name,
            )
    limit = plan.profile.daily_marks if plan.profile else 3
    per_day: dict[date, list[Task]] = defaultdict(list)
    for task in _all_tasks(plan):
        if task.today is not None:
            per_day[task.today].append(task)
    for day, tasks in sorted(per_day.items()):
        if len(tasks) > limit:
            yield _issue(
                plan,
                "mark/today",
                f"{len(tasks)} tasks are marked for {day}, more than daily_marks = {limit}",
                tasks[0].id,
            )
        if sum(task.main for task in tasks) > 1:
            yield _issue(
                plan, "mark/main", f"more than one main objective is marked for {day}", tasks[0].id
            )


def check_selection(plan: Plan, day: date) -> Iterator[Issue]:
    """A selected item states its budget and, under ordinal valuation, its rank."""
    ordinal = plan.profile is not None and plan.profile.valuation == "ordinal"
    cycle = current_cycle(plan, day)
    for item in plan.items.values():
        if item.kind == "standing":
            if ordinal and item.rank is None:
                yield _issue(
                    plan,
                    "field/rank",
                    "a standing parent is ranked at each cycle planning",
                    item.id,
                )
            continue
        if cycle is None or item.cycle != cycle.id or not item.is_open:
            continue
        if item.budget is None:
            yield _issue(
                plan,
                "field/budget",
                f"selected for the cycle {cycle.id}, the item states no budget",
                item.id,
            )
        if ordinal and item.rank is None:
            yield _issue(
                plan,
                "field/rank",
                f"selected for the cycle {cycle.id}, the item states no rank",
                item.id,
            )


def check_holding(plan: Plan) -> Iterator[Issue]:
    """A task of the holding file bears the date of its entry."""
    for task in plan.holding:
        if task.held is None:
            yield Issue(
                "field/held",
                "a task of the holding file states the date held",
                "capture/holding.yml",
                task.id,
            )


def check_clock(plan: Plan) -> Iterator[Issue]:
    """A stop closes a running span."""
    running = False
    for entry in sorted(plan.clock, key=lambda e: e.at):
        if entry.event == "stop" and not running:
            yield Issue(
                "clock/stop",
                f"the stop of {entry.at.isoformat()} closes no running task",
                f"log/clock/{entry.at:%Y-%m}.yml",
                severity=Severity.WARNING,
            )
        running = entry.event == "start"


def check_plan(plan: Plan, day: date) -> list[Issue]:
    """Run every check on the plan, as it stands on `day`."""
    return [
        *check_identifiers(plan),
        *check_references(plan),
        *check_marks(plan),
        *check_selection(plan, day),
        *check_holding(plan),
        *check_clock(plan),
    ]
