---
tags:
  - decision
status: accepted
created: 2026-11-13
index: "[Architecture decisions](docs/adr/_index.md)"
aliases:
  - Typical week
  - Types of deliverable
---
# Typical week and types of deliverable

> [!QUESTION] Goal: which records state the time of the agent and the kinds of its results, so that an author fills them from the way the week is actually reasoned?

The first plan of the author, drafted for the pilot in Geonexus, exposed four defects of the formats. The availability stated weekly hours, whereas the author reasons in the spans available on each day, which vary across days and are constrained by meetings fixed by others. The field `energy` was free text, which no rule reads. The profile named one kind of deliverable, whereas a researcher delivers papers, posters, talks, chapters and software. The labels of the streams, of the levels and of the phases restated names without operational effect.

> [!WARNING] Partly replaced
> The decision on [streams, allocation and loose tasks](streams-allocation-and-loose-tasks.md) replaces the place of the energy hours in the typical week. The decision on [properties apart from the trigger](properties-apart-from-the-trigger.md) replaces the check of energy by regime. The decision on [dates, reviews and recurring tasks](dates-reviews-and-recurring-tasks.md) replaces the exceptions held by the record of a week, and the records of future weeks. The decision on [parties, derived deliverables and the lifetimes of the profile](parties-and-derived-deliverables.md) retires the latency of the reviewing party on a type.

## Decision

- **Streams.** The identifier of a stream is its name, a slug read in every record. Its `description` opens on the verb that states what the stream does, such as "advances", "derives" or "solves". The field `name` is retired.
- **Typical week.** One record of the typical week replaces the availability record and the week template. For each weekday, it states the available spans, the recurring meetings fixed by others, each with an identifier, and the blocks and windows of the streams, which must lie in the free spans. It states the hours of high energy, for all days or per day. The weekly capacity and the minimum block are computed from the spans. Only the predictability and the capacity of a poor week remain authored. A form in weekly hours remains for an agent without fixed spans.
- **Energy.** The check reports a block of a stream of the regime `planned` placed outside the hours of high energy.
- **Exceptions.** The record of a week holds every departure from the typical week: a one-off appointment, a recurring meeting cancelled or moved on one date by its identifier, a block of its own changed, and a day or a range of days unavailable. The record of a future week may be written as soon as a change is known, named by the planned date of its review, and the review completes it. The record type of the dated appointment is retired.
- **Types of deliverable.** The profile declares the types of deliverable, each with an identifier and a description, and four defaults for each deliverable of the type:
  - the class of variance of its work, and its prior margin before calibration; the ratios of time are logged and calibrated per type;
  - its starting phase;
  - the latency of the party that reviews it, from which the retroplanning dates the submission;
  - its template of stages, the milestones with which a new deliverable of the type starts.

  A deliverable names its type, and may override its starting phase and its template of stages.
- **Labels.** The profile fields `levels` and `phases` are retired, and the method uses its own terms. A purpose may hold a `description` that no rule reads. Its deadline stays operational.

## Constraints that decide the formats

- **A field is authored only when a rule reads it, or when the author needs it to read the record.** A label that renames a term of the method fails both conditions.
- **The typical week has one source.** Spans, meetings and blocks are read together, and the check of a block against the free spans stays within one file. What is given to the agent and what the agent chooses are distinguished by the kind of entry, not by the file.
- **The feasibility test needs the future meetings and absences,** so a change known in advance must be recordable before its week opens.

## Options weighed

- **An abbreviated identifier beside a full name.** Rejected: an abbreviation must be decoded in every record, as the single letters were.
- **The availability and the week template as two files.** Rejected for the constraint of one source.
- **Dated change records apart from the weeks.** Rejected by the author in favour of one record per week, made possible by the records of future weeks.
- **The phases of Nanda as labels of the research profile.** Rejected: the mapping gives one object two names. The [phases of research](../references/research-phases.md) remain the source of the phases of the method.

## Consequences

- The schemas of the profile, the week and the deliverable change in place, keeping the version 1, since no format of horai has been published. The schema of the typical week replaces two schemas, and the schema of the appointment is retired.
- The loader, the checks, the week view and the fixture plan follow the new formats.
- The plan of the author in Geonexus is migrated to the new formats before its first week of use.
