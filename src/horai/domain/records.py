"""
Typed records of a plan, built from validated files.

Each class mirrors one record of the specification. A record is built only from a file that its
schema has validated, so the constructors trust the shape of their input and convert its notations.

Classes
-------
Allocation, Stream, Stage, DeliverableType, Profile, PartyRef, Party
    Configuration of the kernel for one agent, and the parties that it deals with.
Task, Item, Deadline, Purpose, Deliverable
    The hierarchy of work: an item is a milestone or a question; a loose task names its stream.
Block, Appointment, Unplaced, TypicalDay, TypicalWeek, Cycle, DayChange, Absence
    The calendar: the typical week, the departures of single dates, and the ranges of absence.
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
from typing import Any, Literal

from .time import parse_date, parse_duration, parse_span, parse_time, parse_timestamp, pert

ItemKind = Literal["milestone", "question"]

DEFAULT_DAILY_MARKS = 3
DEFAULT_ALLOCATION_TOLERANCE = 0.02

WEEKDAYS = ("mon", "tue", "wed", "thu", "fri", "sat", "sun")
MONTHS_PER_WEEK = 12 / 52


def _weeks(period: str | None) -> int | None:
    """Return the number of weeks of a period `P<n>W`, 1 when absent, or None for `P1M`."""
    if period is None:
        return 1
    return None if period.endswith("M") else int(period[1:-1])


def occurrence_in_month(day: date) -> tuple[int, bool]:
    """Return the rank of `day` among the dates of its weekday in its month, and whether it is
    the last of them.

    Examples
    --------
    >>> occurrence_in_month(date(2026, 11, 24))
    (4, True)
    """
    return (day.day - 1) // 7 + 1, (day + timedelta(days=7)).month != day.month


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


def _spans(texts: list[str]) -> tuple[tuple[int, int], ...]:
    return tuple(parse_span(text) for text in texts)


def _energy(data: dict[str, Any] | None) -> dict[str, tuple[tuple[int, int], ...]]:
    """Return the spans of high energy of each weekday, from one list or one list per weekday."""
    if not data:
        return {}
    high = data["high"]
    if isinstance(high, list):
        return {day: _spans(high) for day in WEEKDAYS}
    return {day: _spans(spans) for day, spans in high.items()}


@dataclass(frozen=True)
class PartyRef:
    """A party named by a record: a declared one by its identifier, an occasional one by name."""

    id: str | None = None
    name: str | None = None

    @classmethod
    def from_data(cls, data: str | dict[str, str] | None) -> PartyRef | None:
        """Build a reference from an identifier, a mapping `{name}`, or None."""
        if data is None:
            return None
        if isinstance(data, str):
            return cls(id=data)
        return cls(name=data["name"])

    def __str__(self) -> str:
        return self.id or self.name or ""


@dataclass(frozen=True)
class Allocation:
    """The time that a stream receives: a share of the plannable time, or a reserve."""

    mode: Literal["share", "reserve"]
    bound: Literal["at_least", "at_most", "exact"]
    amount: float | timedelta
    per: Literal["day", "week", "cycle", "event"] = "week"
    events: tuple[str, ...] = ()

    @classmethod
    def from_data(cls, data: dict[str, Any]) -> Allocation:
        """Build an allocation from a validated entry of a stream."""
        amount = data["amount"]
        return cls(
            mode=data["mode"],
            bound=data["bound"],
            amount=parse_duration(amount) if isinstance(amount, str) else float(amount),
            per=data.get("per", "week"),
            events=tuple(data.get("events", ())),
        )


# --- Configuration --------------------------------------------------------------------------------


@dataclass(frozen=True)
class Stream:
    """A class of work declared by the profile: what it yields, and what triggers it.

    The attribute `needs_high_energy` states whether the work of the stream is placed at the hours
    of high energy, whatever triggers it.
    """

    id: str
    description: str
    yields: tuple[str, ...]
    triggered_by: str
    allocation: Allocation | None = None
    needs_high_energy: bool = False

    @classmethod
    def from_data(cls, data: dict[str, Any]) -> Stream:
        """Build a stream from one entry of the field `streams` of a profile."""
        allocation = data.get("allocation")
        return cls(
            data["id"],
            data["description"],
            tuple(data["yields"]),
            data["triggered_by"],
            Allocation.from_data(allocation) if allocation else None,
            data.get("needs_high_energy", False),
        )


@dataclass(frozen=True)
class Stage:
    """A stage of a deliverable: the phase from which it exists as a milestone, and its defaults.

    The defaults `predictability` and `prior_margin` replace those of the type of the deliverable
    when they are stated.
    """

    id: str
    phase: str
    predictability: str | None = None
    prior_margin: float | None = None

    @classmethod
    def from_data(cls, data: dict[str, Any]) -> Stage:
        """Build a stage from one validated entry of a field `stages`."""
        return cls(data["id"], data["phase"], data.get("predictability"), data.get("prior_margin"))


def stages_from(data: list[dict[str, Any]]) -> tuple[Stage, ...]:
    """Return the stages of a validated field `stages`."""
    return tuple(Stage.from_data(stage) for stage in data)


@dataclass(frozen=True)
class DeliverableType:
    """A type of deliverable, with the defaults of each deliverable of the type."""

    id: str
    description: str
    predictability: str
    starting_phase: str
    prior_margin: float | None = None
    stages: tuple[Stage, ...] = ()

    @classmethod
    def from_data(cls, data: dict[str, Any]) -> DeliverableType:
        """Build a type from one entry of the field `deliverable_types` of a profile."""
        return cls(
            id=data["id"],
            description=data["description"],
            predictability=data["predictability"],
            starting_phase=data["starting_phase"],
            prior_margin=data.get("prior_margin"),
            stages=stages_from(data.get("stages", ())),
        )


@dataclass(frozen=True)
class Profile:
    """The configuration of the kernel for one domain."""

    name: str
    streams: dict[str, Stream]
    deliverable_types: dict[str, DeliverableType]
    enabled_mechanisms: dict[str, dict[str, Any]]
    worth_scale: str
    parameters: dict[str, Any]
    energy: dict[str, tuple[tuple[int, int], ...]] = field(default_factory=dict)
    recurrences: dict[str, str] = field(default_factory=dict)

    @classmethod
    def from_data(cls, data: dict[str, Any]) -> Profile:
        """Build a profile from a validated `settings/profile.yml`."""
        streams = [Stream.from_data(entry) for entry in data["streams"]]
        types = [DeliverableType.from_data(entry) for entry in data.get("deliverable_types", ())]
        overrides = {name: entry["value"] for name, entry in data.get("parameters", {}).items()}
        return cls(
            name=data["name"],
            streams={stream.id: stream for stream in streams},
            deliverable_types={kind.id: kind for kind in types},
            enabled_mechanisms=dict(data.get("enabled_mechanisms", {})),
            worth_scale=data["worth"]["scale"],
            parameters=overrides,
            energy=_energy(data.get("energy")),
            recurrences=dict(data.get("recurrences", {})),
        )

    @property
    def daily_marks(self) -> int:
        """Maximum number of tasks marked for one day."""
        return int(self.parameters.get("daily_marks", DEFAULT_DAILY_MARKS))

    @property
    def allocation_tolerance(self) -> float:
        """Admitted difference between the hours of a stream and its exact share, as a fraction."""
        return float(self.parameters.get("allocation_tolerance", DEFAULT_ALLOCATION_TOLERANCE))


# --- Hierarchy of work ----------------------------------------------------------------------------


@dataclass(frozen=True)
class Task:
    """A task, held in the file of its parent or in the holding file.

    The attribute `parent` is the identifier of the milestone or the question that holds the task,
    or None. A loose task has no parent and names its `stream`; a task of the holding file has
    neither. A loose task that recurs names its rule in `recurs`, holds in `completed` the date of
    its last completion, and reopens once its rule counts enough periods begun since then.
    """

    id: str
    title: str
    parent: str | None
    stream: str | None = None
    committed_week: date | None = None
    origin: str = "chosen"
    budget: timedelta | None = None
    marked_for: date | None = None
    main_objective: bool = False
    completed: date | None = None
    held_since: date | None = None
    depends_on: tuple[str, ...] = ()
    scheduled: date | None = None
    follow_up: date | None = None
    awaits: str | None = None
    hands_off: bool = False
    riskiest: bool = False
    importance: str | None = None
    steps: tuple[tuple[str, bool], ...] = ()
    request_kind: str | None = None
    prepares: str | None = None
    verifies: str | None = None
    non_negotiable: date | None = None
    recurs: str | None = None

    @classmethod
    def from_data(cls, data: dict[str, Any], parent: str | None) -> Task:
        """Build a task from one entry of a validated list of tasks."""
        return cls(
            id=data["id"],
            title=data["title"],
            parent=parent,
            stream=data.get("stream"),
            committed_week=_date_or_none(data.get("committed_week")),
            origin=data.get("origin", "chosen"),
            budget=_duration_or_none(data.get("budget")),
            marked_for=_date_or_none(data.get("marked_for")),
            main_objective=data.get("main_objective", False),
            completed=_date_or_none(data.get("completed")),
            held_since=_date_or_none(data.get("held_since")),
            depends_on=tuple(data.get("depends_on", ())),
            scheduled=_date_or_none(data.get("scheduled")),
            follow_up=_date_or_none(data.get("follow_up")),
            awaits=data.get("awaits"),
            hands_off=data.get("hands_off", False),
            riskiest=data.get("riskiest", False),
            importance=data.get("importance"),
            steps=tuple((step["title"], step.get("done", False)) for step in data.get("steps", ())),
            request_kind=data.get("request_kind"),
            prepares=data.get("prepares"),
            verifies=data.get("verifies"),
            non_negotiable=_date_or_none(data.get("non_negotiable")),
            recurs=data.get("recurs"),
        )

    @property
    def is_open(self) -> bool:
        """Whether the task is not completed for good; a recurring task never is."""
        return self.completed is None or self.recurs is not None

    @property
    def is_waiting(self) -> bool:
        """Whether the task waits for a party, by a follow-up date or by a wait."""
        return self.follow_up is not None or self.awaits is not None


@dataclass(frozen=True)
class Item:
    """A parent of level 3: a milestone or a question.

    The selection rule counts a question as a milestone, so one class holds the two kinds. A
    milestone without a deliverable serves its stream directly. A milestone that holds a stage of
    its deliverable names it in `stage`.
    """

    id: str
    kind: ItemKind
    title: str
    stream: str
    tasks: tuple[Task, ...] = ()
    deliverable: str | None = None
    stage: str | None = None
    status: str = "open"
    predictability: str | None = None
    budget: timedelta | None = None
    cycle: str | None = None
    rank: int | None = None
    origin: str = "chosen"
    non_negotiable: date | None = None
    depends_on: tuple[str, ...] = ()
    estimate: tuple[timedelta, timedelta, timedelta] | None = None
    deadline: Deadline | None = None

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
            stage=data.get("stage"),
            status=data.get("status", "open"),
            predictability=data.get("predictability"),
            budget=_duration_or_none(data.get("budget")),
            cycle=data.get("cycle"),
            rank=data.get("rank"),
            origin=data.get("origin", "chosen"),
            non_negotiable=_date_or_none(data.get("non_negotiable")),
            depends_on=tuple(data.get("depends_on", ())),
            estimate=_estimate(data.get("estimate")),
            deadline=Deadline.from_data(data.get("deadline")),
        )

    @property
    def planned_budget(self) -> timedelta | None:
        """Return the authored budget, or else the PERT value of the three durations, or None."""
        if self.budget is not None or self.estimate is None:
            return self.budget
        return pert(*self.estimate)

    @property
    def is_open(self) -> bool:
        """Whether the item is still open."""
        return self.status == "open"


@dataclass(frozen=True)
class Deadline:
    """A date that a party relies on, with its strictness and, optionally, the party."""

    date: date
    strictness: str
    party: PartyRef | None = None

    @classmethod
    def from_data(cls, data: dict[str, Any] | None) -> Deadline | None:
        """Build a deadline from a validated field `deadline`, or return None."""
        if data is None:
            return None
        return cls(
            parse_date(data["date"]), data["strictness"], PartyRef.from_data(data.get("party"))
        )


@dataclass(frozen=True)
class Party:
    """A party declared in the file of the parties, with its relations to the agent."""

    id: str
    name: str
    relations: tuple[str, ...] = ()
    class_of_service: dict[str, str] = field(default_factory=dict)

    @classmethod
    def from_data(cls, data: dict[str, Any]) -> Party:
        """Build a party from one validated entry of the file of the parties."""
        return cls(
            data["id"],
            data["name"],
            tuple(data.get("relations", ())),
            dict(data.get("class_of_service", {})),
        )


@dataclass(frozen=True)
class Purpose:
    """A purpose, spanning the strategic horizon."""

    id: str
    title: str
    description: str | None = None
    deadline: Deadline | None = None


@dataclass(frozen=True)
class Deliverable:
    """A result handed to the world or to a party, of one type declared by the profile.

    The attributes `phase` and `stages` hold what the file states; the type supplies them when the
    file states none, through `Plan.phase_of` and `Plan.stages_of`.
    """

    id: str
    title: str
    purpose: str
    type: str
    status: str
    phase: str | None = None
    stages: tuple[Stage, ...] | None = None
    accountable_to: PartyRef | None = None
    deadline: Deadline | None = None
    derived_from: str | None = None


# --- Calendar -------------------------------------------------------------------------------------


@dataclass(frozen=True)
class Block:
    """A block of one day: one stream for one contiguous span."""

    start: time
    length: timedelta
    stream: str

    @classmethod
    def from_data(cls, data: dict[str, Any]) -> Block:
        """Build a block from a validated entry of a day."""
        return cls(parse_time(data["start"]), parse_duration(data["length"]), data["stream"])


@dataclass(frozen=True)
class Appointment:
    """A block of one day fixed by a party: recurring in the typical week, or on one date.

    A recurring appointment is held on its weekday from its first date `first`, when stated, every
    `every_weeks` weeks counted from that date, or only at the `in_month` occurrences of its
    weekday in each month, 1 for the first and -1 for the last.
    """

    id: str
    start: time
    length: timedelta
    stream: str
    party: PartyRef
    title: str | None = None
    places: str | None = None
    first: date | None = None
    every_weeks: int = 1
    in_month: tuple[int, ...] = ()

    def occurs_on(self, day: date) -> bool:
        """Whether the recurring appointment is held on `day`, a date of its weekday."""
        if self.first is not None and day < self.first:
            return False
        if self.in_month:
            rank, last = occurrence_in_month(day)
            return rank in self.in_month or (last and -1 in self.in_month)
        if self.every_weeks > 1 and self.first is not None:
            weeks_elapsed = (day - self.first).days // 7
            return not weeks_elapsed % self.every_weeks
        return True

    @property
    def weekly_share(self) -> float:
        """The mean number of occurrences in a week."""
        if self.in_month:
            return len(self.in_month) * MONTHS_PER_WEEK
        return 1 / self.every_weeks

    @classmethod
    def from_data(cls, data: dict[str, Any]) -> Appointment:
        """Build an appointment from a validated entry of a day."""
        party = PartyRef.from_data(data["party"])
        assert party is not None
        return cls(
            id=data["id"],
            start=parse_time(data["start"]),
            length=parse_duration(data["length"]),
            stream=data["stream"],
            party=party,
            title=data.get("title"),
            places=data.get("places"),
            first=_date_or_none(data.get("from")),
            every_weeks=_weeks(data.get("every")) or 1,
            in_month=tuple(data.get("occurrences_in_month", ())),
        )


@dataclass(frozen=True)
class Unplaced:
    """An appointment without a fixed slot, which the calendar of dates places `times` per period.

    The period is `every_weeks` weeks, counted from `first` when it exceeds one week, or a calendar
    month when `every_weeks` is None. A period of one week is the current week.
    """

    id: str
    length: timedelta
    stream: str
    party: PartyRef
    title: str | None = None
    times: int = 1
    every_weeks: int | None = 1
    first: date | None = None

    def period_of(self, day: date) -> tuple[date, date] | None:
        """Return the first and the last date of the period that holds `day`, or None for a
        period of one week, which is the current week."""
        if self.every_weeks is None:
            start = day.replace(day=1)
            following = (start + timedelta(days=32)).replace(day=1)
            return start, following - timedelta(days=1)
        if self.every_weeks == 1 or self.first is None:
            return None
        length = 7 * self.every_weeks
        start = self.first + timedelta(days=(day - self.first).days // length * length)
        return start, start + timedelta(days=length - 1)

    @property
    def weekly_share(self) -> float:
        """The mean number of occurrences in a week."""
        if self.every_weeks is None:
            return self.times * MONTHS_PER_WEEK
        return self.times / self.every_weeks

    @classmethod
    def from_data(cls, data: dict[str, Any]) -> Unplaced:
        """Build an unplaced appointment from a validated entry of the typical week."""
        party = PartyRef.from_data(data["party"])
        assert party is not None
        return cls(
            id=data["id"],
            length=parse_duration(data["length"]),
            stream=data["stream"],
            party=party,
            title=data.get("title"),
            times=data.get("times", 1),
            every_weeks=_weeks(data.get("every")),
            first=_date_or_none(data.get("from")),
        )


@dataclass(frozen=True)
class TypicalDay:
    """One weekday of the typical week: its available spans, and what they hold."""

    spans: tuple[tuple[int, int], ...]
    appointed: tuple[Appointment, ...] = ()
    blocks: tuple[Block, ...] = ()

    @classmethod
    def from_data(cls, data: dict[str, Any]) -> TypicalDay:
        """Build a typical day from a validated entry of the field `days`."""
        return cls(
            spans=_spans(data["spans"]),
            appointed=tuple(Appointment.from_data(e) for e in data.get("appointed", ())),
            blocks=tuple(Block.from_data(e) for e in data.get("blocks", ())),
        )

    @property
    def available(self) -> timedelta:
        """The total length of the available spans of the day."""
        return timedelta(minutes=sum(end - start for start, end in self.spans))


@dataclass(frozen=True)
class TypicalWeek:
    """The time of the agent in a typical week, and its placement among the streams.

    The attribute `days` is empty when the agent states only the weekly hours.
    """

    predictable: bool
    poor_week: timedelta
    days: dict[str, TypicalDay] = field(default_factory=dict)
    weekly_hours: timedelta | None = None
    unplaced: tuple[Unplaced, ...] = ()

    @classmethod
    def from_data(cls, data: dict[str, Any]) -> TypicalWeek:
        """Build the typical week from a validated `settings/typical-week.yml`."""
        return cls(
            predictable=data["predictable"],
            poor_week=parse_duration(data["poor_week"]),
            days={day: TypicalDay.from_data(entry) for day, entry in data.get("days", {}).items()},
            weekly_hours=_duration_or_none(data.get("weekly_hours")),
            unplaced=tuple(Unplaced.from_data(e) for e in data.get("unplaced", ())),
        )

    @property
    def capacity(self) -> timedelta:
        """The working time of a typical week: the stated hours, or the sum of the spans."""
        if self.weekly_hours is not None:
            return self.weekly_hours
        return sum((day.available for day in self.days.values()), timedelta())

    @property
    def minimum_span(self) -> timedelta | None:
        """The shortest available span of the week, or None when no span is stated."""
        lengths = [end - start for day in self.days.values() for start, end in day.spans]
        return timedelta(minutes=min(lengths)) if lengths else None


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
class DayChange:
    """The departures of one date from the typical week.

    The blocks replace those of the typical day when they are stated; a value None keeps those of
    the typical day. The removed blocks, named by their start, and the
    added blocks then apply to the blocks of the date.
    """

    blocks: tuple[Block, ...] | None = None
    added_blocks: tuple[Block, ...] = ()
    removed_blocks: tuple[time, ...] = ()
    appointments: tuple[Appointment, ...] = ()
    cancelled: tuple[str, ...] = ()
    moved: dict[str, tuple[time, timedelta | None]] = field(default_factory=dict)

    @classmethod
    def from_data(cls, data: dict[str, Any]) -> DayChange:
        """Build the departures of one date from a validated entry of the field `days`."""
        blocks = data.get("blocks")
        return cls(
            blocks=tuple(Block.from_data(e) for e in blocks) if blocks is not None else None,
            added_blocks=tuple(Block.from_data(e) for e in data.get("added_blocks", ())),
            removed_blocks=tuple(parse_time(e) for e in data.get("removed_blocks", ())),
            appointments=tuple(Appointment.from_data(e) for e in data.get("appointments", ())),
            cancelled=tuple(data.get("cancelled", ())),
            moved={
                e["id"]: (parse_time(e["start"]), _duration_or_none(e.get("length")))
                for e in data.get("moved", ())
            },
        )


@dataclass(frozen=True)
class Absence:
    """A range of whole dates on which the agent is unavailable, with its reason."""

    start: date
    end: date
    reason: str | None = None

    @classmethod
    def from_data(cls, data: dict[str, Any]) -> Absence:
        """Build an absence from a validated entry of the field `unavailable`: `to` defaults to
        `from`, for an absence of one date."""
        start = parse_date(data["from"])
        return cls(start, parse_date(data["to"]) if "to" in data else start, data.get("reason"))

    def contains(self, day: date) -> bool:
        """Whether the absence covers `day`."""
        return self.start <= day <= self.end


# --- Logs -----------------------------------------------------------------------------------------


@dataclass(frozen=True)
class ClockEntry:
    """A mark of the start or the stop of work, written by the tool or recalled by the agent."""

    at: datetime
    event: Literal["start", "stop"]
    task: str | None = None
    recalled: bool = False

    @classmethod
    def from_data(cls, data: dict[str, Any]) -> ClockEntry:
        """Build a clock entry from a validated entry of a clock log."""
        return cls(
            parse_timestamp(data["at"]),
            data["event"],
            data.get("task"),
            data.get("recalled", False),
        )


@dataclass(frozen=True)
class DecisionEntry:
    """The decision taken at a checkpoint or at the completion of an item."""

    date: date
    milestone: str
    checkpoint_decision: str
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
    dates : dict[date, DayChange]
        The departures of single dates from the typical week.
    absences : tuple[Absence, ...]
        The ranges of dates on which the agent is unavailable.
    reviews : tuple[date, ...]
        The dates of the weekly reviews held, in order; each starts a week of commitment.
    sources : dict[str, str]
        For each identifier of a record or of a task, the path of its file, relative to the plan.
    excluded : set[str]
        Identifiers of the records whose file failed its validation. A computation that needs one
        of them is reported as undefined instead of being computed on a partial plan.
    """

    profile: Profile | None = None
    typical_week: TypicalWeek | None = None
    parties: dict[str, Party] = field(default_factory=dict)
    purposes: dict[str, Purpose] = field(default_factory=dict)
    deliverables: dict[str, Deliverable] = field(default_factory=dict)
    items: dict[str, Item] = field(default_factory=dict)
    loose: tuple[Task, ...] = ()
    holding: tuple[Task, ...] = ()
    archive: tuple[Task, ...] = ()
    inbox: tuple[str, ...] = ()
    ideas: tuple[str, ...] = ()
    cycles: dict[str, Cycle] = field(default_factory=dict)
    dates: dict[date, DayChange] = field(default_factory=dict)
    absences: tuple[Absence, ...] = ()
    reviews: tuple[date, ...] = ()
    clock: tuple[ClockEntry, ...] = ()
    decisions: tuple[DecisionEntry, ...] = ()
    deviations: tuple[DeviationEntry, ...] = ()
    sources: dict[str, str] = field(default_factory=dict)
    excluded: set[str] = field(default_factory=set)

    def tasks(self) -> list[tuple[Item | None, Task]]:
        """Return every task of a milestone or a question with its item, then every loose task."""
        held = [(item, task) for item in self.items.values() for task in item.tasks]
        return [*held, *((None, task) for task in self.loose)]

    def find_task(self, identifier: str) -> tuple[Item | None, Task] | None:
        """Return the task of this identifier with its item, None for a loose task, or None."""
        for item, task in self.tasks():
            if task.id == identifier:
                return item, task
        return None

    @staticmethod
    def stream_of(item: Item | None, task: Task) -> str | None:
        """Return the stream of a task: that of its item, or its own for a loose task."""
        return item.stream if item is not None else task.stream

    def _type_of(self, deliverable: Deliverable) -> DeliverableType | None:
        """Return the type of a deliverable declared by the profile, or None."""
        if self.profile is None:
            return None
        return self.profile.deliverable_types.get(deliverable.type)

    def phase_of(self, deliverable: Deliverable) -> str | None:
        """Return the phase of a deliverable: its own, or else the starting phase of its type."""
        if deliverable.phase is not None:
            return deliverable.phase
        kind = self._type_of(deliverable)
        return kind.starting_phase if kind else None

    def stages_of(self, deliverable: Deliverable) -> tuple[Stage, ...]:
        """Return the stages of a deliverable: its own, or else those of its type."""
        if deliverable.stages is not None:
            return deliverable.stages
        kind = self._type_of(deliverable)
        return kind.stages if kind else ()

    def stage_defaults(
        self, deliverable: Deliverable, stage: Stage
    ) -> tuple[str | None, float | None]:
        """Return the predictability and the prior margin of a stage: its own, else its type's."""
        kind = self._type_of(deliverable)
        return (
            stage.predictability or (kind.predictability if kind else None),
            stage.prior_margin or (kind.prior_margin if kind else None),
        )
