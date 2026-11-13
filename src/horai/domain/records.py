"""
Typed records of a plan, built from validated files.

Each class mirrors one record of the specification. A record is built only from a file that its
schema has validated, so the constructors trust the shape of their input and convert its notations.

Classes
-------
Stream, Profile, Availability
    Configuration of the kernel for one agent.
Task, Item, Purpose, Deliverable
    The hierarchy of work: an item is a milestone, a question or a standing parent.
Block, Window, AppointedBlock, WeekTemplate, Cycle, Week, Appointment
    The calendar.
ClockEntry, DecisionEntry, DeviationEntry
    The entries of the logs.
Plan
    All the records of one plan, indexed by identifier.
"""

# The specification names the identifier of a record `id`, and fixes the fields of each record.
# pylint: disable=disallowed-name,too-many-instance-attributes

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, time, timedelta
import re
from typing import Any, Literal

from .time import parse_date, parse_duration, parse_time, parse_timestamp, pert

ItemKind = Literal["milestone", "question", "standing"]

DEFAULT_DAILY_MARKS = 3
DEFAULT_OVERHEAD_BUDGET = timedelta(minutes=105)

_ISO_DATE = re.compile(r"\d{4}-\d{2}-\d{2}")


def _date_or_none(value: str | None) -> date | None:
    return parse_date(value) if value else None


def _duration_or_none(value: str | None) -> timedelta | None:
    return parse_duration(value) if value else None


def _estimate(data: dict[str, str] | None) -> tuple[timedelta, timedelta, timedelta] | None:
    """Return the three durations of an estimate, or None."""
    if data is None:
        return None
    return (
        parse_duration(data["optimistic"]),
        parse_duration(data["probable"]),
        parse_duration(data["pessimistic"]),
    )


# --- Configuration --------------------------------------------------------------------------------


@dataclass(frozen=True)
class Stream:
    """A class of work declared by the profile, with one role and one regime."""

    id: str
    name: str
    role: str
    regime: str
    capacity: dict[str, Any]

    @classmethod
    def from_data(cls, data: dict[str, Any]) -> Stream:
        """Build a stream from one entry of the field `streams` of a profile."""
        return cls(data["id"], data["name"], data["role"], data["regime"], dict(data["capacity"]))


@dataclass(frozen=True)
class Profile:
    """The configuration of the kernel for one domain."""

    name: str
    streams: dict[str, Stream]
    options: dict[str, dict[str, Any]]
    valuation: str
    parameters: dict[str, Any]

    @classmethod
    def from_data(cls, data: dict[str, Any]) -> Profile:
        """Build a profile from a validated `profile.yml`."""
        streams = [Stream.from_data(entry) for entry in data["streams"]]
        overrides = {name: entry["value"] for name, entry in data.get("parameters", {}).items()}
        return cls(
            name=data["name"],
            streams={stream.id: stream for stream in streams},
            options=dict(data.get("options", {})),
            valuation=data["valuation"]["scale"],
            parameters=overrides,
        )

    @property
    def daily_marks(self) -> int:
        """Maximum number of tasks marked for one day."""
        return int(self.parameters.get("daily_marks", DEFAULT_DAILY_MARKS))

    @property
    def overhead_budget(self) -> timedelta:
        """Weekly budget of the planning acts, as an ISO 8601 duration when overridden."""
        value = self.parameters.get("overhead_budget")
        return parse_duration(value) if isinstance(value, str) else DEFAULT_OVERHEAD_BUDGET


@dataclass(frozen=True)
class Availability:
    """The working time of the agent."""

    median: timedelta
    low: timedelta
    predictable: bool
    minimum_block: timedelta
    energy: str

    @classmethod
    def from_data(cls, data: dict[str, Any]) -> Availability:
        """Build the availability from a validated `availability.yml`."""
        return cls(
            median=parse_duration(data["capacity"]["median"]),
            low=parse_duration(data["capacity"]["low"]),
            predictable=data["predictable"],
            minimum_block=parse_duration(data["minimum_block"]),
            energy=data["energy"],
        )


# --- Hierarchy of work ----------------------------------------------------------------------------


@dataclass(frozen=True)
class Task:
    """A task, held in the file of its parent or in the holding file.

    The attribute `parent` is the identifier of the record that holds the task, or None for a task
    of the holding file. The mark `today` is split into its date and the flag of the main objective.
    """

    id: str
    title: str
    parent: str | None
    committed_week: date | None = None
    origin: str = "chosen"
    budget: timedelta | None = None
    today: date | None = None
    main: bool = False
    completed: date | None = None
    held: date | None = None
    depends_on: tuple[str, ...] = ()
    scheduled: date | None = None
    waiting: date | str | None = None
    releases: bool = False
    risk: bool = False
    importance: str | None = None
    steps: tuple[tuple[str, bool], ...] = ()
    request_kind: str | None = None
    prepares: str | None = None
    verifies: str | None = None
    non_negotiable: date | None = None

    @classmethod
    def from_data(cls, data: dict[str, Any], parent: str | None) -> Task:
        """Build a task from one entry of a validated list of tasks."""
        today, main = None, False
        if "today" in data:
            day, _, flag = data["today"].partition(" ")
            today, main = parse_date(day), flag == "main"
        waiting: date | str | None = data.get("waiting")
        if isinstance(waiting, str) and _ISO_DATE.fullmatch(waiting):
            waiting = parse_date(waiting)
        return cls(
            id=data["id"],
            title=data["title"],
            parent=parent,
            committed_week=_date_or_none(data.get("committed_week")),
            origin=data.get("origin", "chosen"),
            budget=_duration_or_none(data.get("budget")),
            today=today,
            main=main,
            completed=_date_or_none(data.get("completed")),
            held=_date_or_none(data.get("held")),
            depends_on=tuple(data.get("depends_on", ())),
            scheduled=_date_or_none(data.get("scheduled")),
            waiting=waiting,
            releases=data.get("releases", False),
            risk=data.get("risk", False),
            importance=data.get("importance"),
            steps=tuple((step["title"], step.get("done", False)) for step in data.get("steps", ())),
            request_kind=data.get("request_kind"),
            prepares=data.get("prepares"),
            verifies=data.get("verifies"),
            non_negotiable=_date_or_none(data.get("non_negotiable")),
        )

    @property
    def is_open(self) -> bool:
        """Whether the task is not completed."""
        return self.completed is None


@dataclass(frozen=True)
class Item:
    """A parent of level 3: a milestone, a question or a standing parent.

    The selection rule counts a question and a standing parent as milestones, so one class holds
    the three kinds. Fields that a kind lacks keep their default.
    """

    id: str
    kind: ItemKind
    title: str
    stream: str
    tasks: tuple[Task, ...] = ()
    deliverable: str | None = None
    status: str = "open"
    variance: str | None = None
    budget: timedelta | None = None
    cycle: str | None = None
    rank: int | None = None
    origin: str = "chosen"
    non_negotiable: date | None = None
    depends_on: tuple[str, ...] = ()
    estimate: tuple[timedelta, timedelta, timedelta] | None = None
    overhead: bool = False

    @classmethod
    def from_data(cls, identifier: str, kind: ItemKind, data: dict[str, Any]) -> Item:
        """Build an item from a validated file of the folder of its kind."""
        tasks = tuple(Task.from_data(entry, identifier) for entry in data.get("tasks", ()))
        return cls(
            id=identifier,
            kind=kind,
            title=data["title"],
            stream=data["stream"],
            tasks=tasks,
            deliverable=data.get("deliverable"),
            status=data.get("status", "open"),
            variance=data.get("variance"),
            budget=_duration_or_none(data.get("budget")),
            cycle=data.get("cycle"),
            rank=data.get("rank"),
            origin=data.get("origin", "chosen"),
            non_negotiable=_date_or_none(data.get("non_negotiable")),
            depends_on=tuple(data.get("depends_on", ())),
            estimate=_estimate(data.get("estimate")),
            overhead=data.get("overhead", False),
        )

    @property
    def planned_budget(self) -> timedelta | None:
        """Return the authored budget, or else the PERT value of the three durations, or None."""
        if self.budget is not None or self.estimate is None:
            return self.budget
        return pert(*self.estimate)

    @property
    def is_open(self) -> bool:
        """Whether the item is still open; a standing parent is always open."""
        return self.status == "open"


@dataclass(frozen=True)
class Purpose:
    """A purpose, spanning the strategic horizon."""

    id: str
    title: str
    deadline: date | None = None


@dataclass(frozen=True)
class Deliverable:
    """A result handed to the world or to a party."""

    id: str
    title: str
    purpose: str
    phase: str
    status: str
    deadline: date | None = None


# --- Calendar -------------------------------------------------------------------------------------

WEEKDAYS = ("mon", "tue", "wed", "thu", "fri", "sat", "sun")


@dataclass(frozen=True)
class Block:
    """A block of a week: one stream for one contiguous span of a day."""

    day: str
    start: time
    length: timedelta
    stream: str

    @classmethod
    def from_data(cls, data: dict[str, Any]) -> Block:
        """Build a block from a validated entry of a template or of a week."""
        return cls(
            data["day"], parse_time(data["start"]), parse_duration(data["length"]), data["stream"]
        )


@dataclass(frozen=True)
class Window:
    """A short slot between two blocks, for requests and releasing tasks."""

    day: str
    start: time
    length: timedelta

    @classmethod
    def from_data(cls, data: dict[str, Any]) -> Window:
        """Build a window from a validated entry of a template or of a week."""
        return cls(data["day"], parse_time(data["start"]), parse_duration(data["length"]))


@dataclass(frozen=True)
class AppointedBlock:
    """A recurring block fixed by a party, placed in the week template."""

    day: str
    start: time
    length: timedelta
    stream: str
    party: str


@dataclass(frozen=True)
class WeekTemplate:
    """The placement of the capacity, from which each week may depart."""

    blocks: tuple[Block, ...]
    windows: tuple[Window, ...] = ()
    appointed: tuple[AppointedBlock, ...] = ()

    @classmethod
    def from_data(cls, data: dict[str, Any]) -> WeekTemplate:
        """Build the template from a validated `calendar/week-template.yml`."""
        appointed = tuple(
            AppointedBlock(
                e["day"],
                parse_time(e["start"]),
                parse_duration(e["length"]),
                e["stream"],
                e["party"],
            )
            for e in data.get("appointed", ())
        )
        return cls(
            blocks=tuple(Block.from_data(e) for e in data["blocks"]),
            windows=tuple(Window.from_data(e) for e in data.get("windows", ())),
            appointed=appointed,
        )


@dataclass(frozen=True)
class Cycle:
    """A cycle of the plan, ending with its cool-down."""

    id: str
    start: date
    end: date
    cool_down: tuple[date, date] | None = None

    def contains(self, day: date) -> bool:
        """Whether a day falls within the cycle."""
        return self.start <= day <= self.end


@dataclass(frozen=True)
class Week:
    """A week, opened by a weekly review, with its departures from the template."""

    opened: date
    blocks: tuple[Block, ...] | None = None
    windows: tuple[Window, ...] | None = None


@dataclass(frozen=True)
class Appointment:
    """A dated block fixed by a party."""

    id: str
    title: str
    date: date
    start: time
    length: timedelta
    stream: str
    party: str
    cap: timedelta | None = None


# --- Logs -----------------------------------------------------------------------------------------


@dataclass(frozen=True)
class ClockEntry:
    """A mark of the start or the stop of work, written by the tool."""

    at: datetime
    event: Literal["start", "stop"]
    task: str | None = None
    assigned: bool = False

    @classmethod
    def from_data(cls, data: dict[str, Any]) -> ClockEntry:
        """Build a clock entry from a validated entry of a clock log."""
        return cls(
            parse_timestamp(data["at"]),
            data["event"],
            data.get("task"),
            data.get("assigned", False),
        )


@dataclass(frozen=True)
class DecisionEntry:
    """The decision taken at a checkpoint or at the completion of an item."""

    date: date
    milestone: str
    decision: str
    rationale: str | None = None


@dataclass(frozen=True)
class DeviationEntry:
    """A deviation from a policy, recorded at a weekly review."""

    date: date
    policy: str
    deviation: str
    cycle: str | None = None


# --- Plan -----------------------------------------------------------------------------------------


@dataclass
class Plan:
    """All the records of one plan, indexed by identifier.

    Attributes
    ----------
    sources : dict[str, str]
        For each identifier of a record or of a task, the path of its file, relative to the plan.
    excluded : set[str]
        Identifiers of the records whose file failed its validation. A computation that needs one
        of them is reported as undefined instead of being computed on a partial plan.
    """

    profile: Profile | None = None
    availability: Availability | None = None
    template: WeekTemplate | None = None
    purposes: dict[str, Purpose] = field(default_factory=dict)
    deliverables: dict[str, Deliverable] = field(default_factory=dict)
    items: dict[str, Item] = field(default_factory=dict)
    holding: tuple[Task, ...] = ()
    archive: tuple[Task, ...] = ()
    inbox: tuple[str, ...] = ()
    ideas: tuple[str, ...] = ()
    cycles: dict[str, Cycle] = field(default_factory=dict)
    weeks: dict[date, Week] = field(default_factory=dict)
    appointments: dict[str, Appointment] = field(default_factory=dict)
    clock: tuple[ClockEntry, ...] = ()
    decisions: tuple[DecisionEntry, ...] = ()
    deviations: tuple[DeviationEntry, ...] = ()
    sources: dict[str, str] = field(default_factory=dict)
    excluded: set[str] = field(default_factory=set)

    def tasks(self) -> list[tuple[Item, Task]]:
        """Return every task held by an item, with its item."""
        return [(item, task) for item in self.items.values() for task in item.tasks]

    def find_task(self, identifier: str) -> tuple[Item, Task] | None:
        """Return the task of this identifier with its item, or None."""
        for item, task in self.tasks():
            if task.id == identifier:
                return item, task
        return None
