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
from graphlib import CycleError, TopologicalSorter

from ..domain.records import Deliverable, Item, Plan, Purpose, Task
from ..issues import Issue, Severity
from .budgets import budget_status
from .calendar_checks import appointment_ids, check_calendar
from .stages import check_stages
from .state import current_cycle, current_week, recurrence_rule, task_state
from .time_spent import spans


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
    """Return the tasks of the items, the loose tasks, and the tasks of the holding file."""
    return [task for _, task in plan.tasks()] + list(plan.holding)


def check_identifiers(plan: Plan) -> Iterator[Issue]:
    """An identifier names one record or one task in the whole plan."""
    names = (
        list(plan.purposes)
        + list(plan.deliverables)
        + list(plan.items)
        + appointment_ids(plan)
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
    types = plan.profile.deliverable_types if plan.profile else {}
    for deliverable in plan.deliverables.values():
        if deliverable.purpose not in plan.purposes:
            yield _missing(plan, "purpose", deliverable.purpose, deliverable.id)
        if plan.profile and deliverable.type not in types:
            message = f"no type of deliverable {deliverable.type} in the profile"
            yield _issue(plan, "reference/type", message, deliverable.id)
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
    for task in plan.loose:
        if plan.profile and task.stream not in streams:
            message = f"no stream {task.stream} in the profile"
            yield _issue(plan, "reference/stream", message, task.id)


def _check_tasks(plan: Plan) -> Iterator[Issue]:
    """A task names existing predecessors without a cycle, a recorded week and an appointment."""
    graph = {task.id: set(task.depends_on) for task in _all_tasks(plan)}
    appointments = set(appointment_ids(plan))
    for _, task in plan.tasks():
        if task.prepares is not None and task.prepares not in appointments:
            message = f"no appointment {task.prepares} for {task.id} to prepare"
            yield _issue(plan, "reference/appointment", message, task.id)
        for predecessor in task.depends_on:
            if predecessor not in graph:
                message = f"no task named {predecessor} precedes {task.id}"
                yield _issue(plan, "reference/task", message, task.id)
        if task.committed_week is not None and task.committed_week not in plan.reviews:
            message = f"no weekly review is logged on {task.committed_week}"
            yield _issue(plan, "reference/week", message, task.id)
    try:
        TopologicalSorter({k: v & graph.keys() for k, v in graph.items()}).prepare()
    except CycleError as error:
        cycle = list(dict.fromkeys(error.args[1]))
        message = "the dependencies form a cycle: " + " -> ".join(cycle)
        yield _issue(plan, "reference/cycle", message, cycle[0])


def check_profile(plan: Plan) -> Iterator[Issue]:
    """The events of a reserve name appointments, and the shares fit in the plannable time."""
    if plan.profile is None:
        return
    known = set(appointment_ids(plan))
    if plan.typical_week is not None:
        known |= {unplaced.id for unplaced in plan.typical_week.unplaced}
    shares = 0.0
    for stream in plan.profile.streams.values():
        allocation = stream.allocation
        if allocation is None:
            continue
        for event in allocation.events:
            if event not in known:
                message = (
                    f"the stream {stream.id} reserves time for {event}, which no appointment names"
                )
                yield Issue("profile/allocation", message, "settings/profile.yml", stream.id)
        if allocation.mode == "share" and allocation.bound in ("exact", "at_least"):
            assert isinstance(allocation.amount, float)
            shares += allocation.amount
    if shares > 1:
        message = f"the exact and minimum shares sum to {shares:.0%}, more than the plannable time"
        yield Issue("profile/allocation", message, "settings/profile.yml")


def _check_parties(plan: Plan) -> Iterator[Issue]:
    """A party named by its identifier is declared in the file of the parties."""
    named: list[tuple[str, str]] = []
    week = plan.typical_week
    if week is not None:
        named += [(str(u.party), u.id) for u in week.unplaced if u.party.id]
        named += [
            (str(a.party), a.id) for day in week.days.values() for a in day.appointed if a.party.id
        ]
    named += [
        (str(a.party), a.id)
        for change in plan.dates.values()
        for a in change.appointments
        if a.party.id
    ]
    named += [
        (str(d.accountable_to), d.id)
        for d in plan.deliverables.values()
        if d.accountable_to is not None and d.accountable_to.id
    ]
    levels: list[Purpose | Deliverable | Item] = [
        *plan.purposes.values(),
        *plan.deliverables.values(),
        *plan.items.values(),
    ]
    named += [
        (str(level.deadline.party), level.id)
        for level in levels
        if level.deadline is not None
        and level.deadline.party is not None
        and level.deadline.party.id
    ]
    for party, record in named:
        if party not in plan.parties:
            message = (
                f"{record} names the party {party}, which settings/parties.yml does not declare; "
                "an occasional party is written {name: ...}"
            )
            yield Issue(
                "reference/party", message, plan.sources.get(record, "settings/parties.yml"), record
            )


def _check_clock_tasks(plan: Plan) -> Iterator[Issue]:
    """A clock entry names a task, a milestone or a question, or an appointment."""
    known = {task.id for task in _all_tasks(plan)} | set(plan.items) | set(appointment_ids(plan))
    for entry in plan.clock:
        if entry.task is not None and entry.task not in known:
            message = f"the clock entry of {entry.at.isoformat()} names no task {entry.task}"
            yield Issue("reference/task", message, f"log/clock/{entry.at:%Y-%m}.yml")


def _check_derived(plan: Plan) -> Iterator[Issue]:
    """A derived deliverable names another deliverable, which is derived from none."""
    for deliverable in plan.deliverables.values():
        source = deliverable.derived_from
        if source is None:
            continue
        if source == deliverable.id or source not in plan.deliverables:
            yield _missing(plan, "deliverable", source, deliverable.id)
        elif plan.deliverables[source].derived_from is not None:
            message = f"the source {source} is itself derived; name the original deliverable"
            yield _issue(plan, "reference/derived", message, deliverable.id)


def check_references(plan: Plan) -> Iterator[Issue]:
    """Every reference names an existing record."""
    yield from _check_hierarchy(plan)
    yield from _check_tasks(plan)
    yield from _check_parties(plan)
    yield from _check_derived(plan)
    yield from _check_clock_tasks(plan)
    yield from check_stages(plan)


def check_marks(plan: Plan) -> Iterator[Issue]:
    """At most one item bears the non-negotiable mark, and each day bears its permitted marks.

    A mark left on a closed item or a completed task is ignored by the selection, and reported.
    """
    for item in plan.items.values():
        if item.non_negotiable is not None and not item.is_open:
            message = "the item is closed and still bears the non-negotiable mark; remove the mark"
            yield _issue(plan, "mark/closed", message, item.id, Severity.WARNING)
    for parent, task in plan.tasks():
        if task.non_negotiable is not None and (
            not task.is_open or (parent is not None and not parent.is_open)
        ):
            message = f"the task {task.id} is closed and still bears the non-negotiable mark"
            yield _issue(
                plan, "mark/closed", message, parent.id if parent else task.id, Severity.WARNING
            )
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
        if task.marked_for is not None:
            per_day[task.marked_for].append(task)
    for day, tasks in sorted(per_day.items()):
        if len(tasks) > limit:
            yield _issue(
                plan,
                "mark/marked-for",
                f"{len(tasks)} tasks are marked for {day}, more than daily_marks = {limit}",
                tasks[0].id,
            )
        if sum(task.main_objective for task in tasks) > 1:
            yield _issue(
                plan, "mark/main", f"more than one main objective is marked for {day}", tasks[0].id
            )


def check_selection(plan: Plan, day: date) -> Iterator[Issue]:
    """A selected item states its budget and, when worth is ordinal, its rank.

    An item carried into the cycle needs a decision entry that renews or reduces its budget.
    """
    ordinal = plan.profile is not None and plan.profile.worth_scale == "ordinal"
    cycle = current_cycle(plan, day)
    work = spans(plan.clock)
    for item in plan.items.values():
        if cycle is None or item.cycle != cycle.id or not item.is_open:
            continue
        status = budget_status(plan, item, work)
        if status.carried:
            yield _issue(
                plan,
                "budget/carried",
                f"time was spent on the item before the cycle {cycle.id} started, and no decision "
                f"entry renews or reduces its budget, which counts from {status.since}",
                item.id,
                Severity.WARNING,
            )
        if item.planned_budget is None:
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


def check_recurrences(plan: Plan) -> Iterator[Issue]:
    """A recurring task names a default rule, a rule of the profile, or a period."""
    for task in plan.loose:
        if task.recurs is not None and recurrence_rule(plan, task.recurs) is None:
            message = (
                f"the task {task.id} recurs by the rule {task.recurs}, which is neither a default "
                "rule, a rule of the profile, nor a period such as P2W"
            )
            yield _issue(plan, "reference/recurrence", message, task.id)


def check_committed_streams(plan: Plan, day: date) -> Iterator[Issue]:
    """A stream that holds committed work states how it receives its time.

    The committed work is an open item selected for the current cycle, or a task in the state
    `week`; without an allocation, its stream receives no block and no capacity.
    """
    if plan.profile is None:
        return
    cycle = current_cycle(plan, day)
    holders: dict[str, str] = {}
    for item in plan.items.values():
        if cycle is not None and item.cycle == cycle.id and item.is_open:
            holders.setdefault(item.stream, item.id)
    for parent, task in plan.tasks():
        stream = plan.stream_of(parent, task)
        if stream is not None and task_state(plan, parent, task, day) == "week":
            holders.setdefault(stream, parent.id if parent else task.id)
    for stream, record in sorted(holders.items()):
        declared = plan.profile.streams.get(stream)
        if declared is not None and declared.allocation is None:
            message = (
                f"the stream {stream} holds committed work, such as {record}, "
                "and states no allocation, so it receives no time"
            )
            yield Issue("profile/allocation", message, "settings/profile.yml", stream)


def check_reviews(plan: Plan, day: date) -> Iterator[Issue]:
    """The last weekly review is at most seven days old, so that the week of commitment is current.

    A week of commitment lasts until the next review, so a missed review leaves the tasks of an old
    week committed.
    """
    week = current_week(plan, day)
    if week is not None and (day - week).days > 7:
        message = (
            f"the last weekly review was held on {week}, {(day - week).days} days ago; "
            "its commitments remain in force until the next review is logged"
        )
        yield Issue(
            "review/overdue", message, f"log/reviews/{week:%Y-%m}.yml", "", Severity.WARNING
        )


def check_estimates(plan: Plan) -> Iterator[Issue]:
    """Three durations replace the budget of a routine item, in increasing order."""
    for item in plan.items.values():
        if item.estimate is None:
            continue
        if item.budget is not None:
            yield _issue(
                plan, "field/estimate", "an item states either a budget or three durations", item.id
            )
        if item.predictability == "exploratory":
            message = "an exploratory item receives an appetite, not three durations"
            yield _issue(plan, "field/estimate", message, item.id)
        optimistic, probable, pessimistic = item.estimate
        if not optimistic <= probable <= pessimistic:
            message = "the durations must increase from optimistic to pessimistic"
            yield _issue(plan, "field/estimate", message, item.id)


def check_holding(plan: Plan) -> Iterator[Issue]:
    """A task of the holding file bears the date of its entry."""
    for task in plan.holding:
        if task.held_since is None:
            yield Issue(
                "field/held-since",
                "a task of the holding file states the date from which it is held",
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
        *check_profile(plan),
        *check_references(plan),
        *check_calendar(plan, day),
        *check_marks(plan),
        *check_selection(plan, day),
        *check_reviews(plan, day),
        *check_committed_streams(plan, day),
        *check_recurrences(plan),
        *check_estimates(plan),
        *check_holding(plan),
        *check_clock(plan),
    ]
