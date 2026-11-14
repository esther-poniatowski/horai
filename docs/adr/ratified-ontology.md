---
tags:
  - decision
status: accepted
created: 2026-11-13
index: "[Architecture decisions](docs/adr/_index.md)"
aliases:
  - Ratified ontology
  - Objects of horai
---
# Ratified ontology

> [!QUESTION] Goal: which objects does `horai` manipulate, so that the record formats and the code are built on a set that the author has ratified?

## Decision

The author ratifies the objects below, with the changes stated for each.

- **Streams.** A stream bears a role and a regime, both from closed lists. Four roles are renamed so that each names its work: *tooling* (formerly enablement), *survey* (formerly sensing), *exchange* (formerly interface) and *training* (formerly capability). The *cycle* keeps its name. The regimes `calendar` and `committed` merge into one regime, [`appointed`](../kernel/objects/regime.md#^regimes): a block of time fixed by a party, removed from the plannable capacity, with an optional cap on its preparation. Six regimes remain.
- **Levels of work.** A purpose, a deliverable, a milestone or a question, and a task. An *item* is a milestone or a question. A task serves one milestone, one question or one [standing parent](../kernel/objects/work-hierarchy.md#^standing-parent), and waits in the holding file while it has none.
- **Time.** The cycle, the week, the block, the window and the marks of the day. The *block*, formerly the theme, assigns one stream to a contiguous span of a day, and `theme_length` becomes `block_length`.
- **Capture.** The inbox, the holding file, the ideas file and the archive, as the [capture record](../specification/capture-record.md) states.
- **Observation.** Three entries of the [log record](../specification/log-record.md):
  - the *clock entry*, which replaces the time entry: the tool writes one when the agent marks the start or the stop of a task. The *time spent* per task and per day is computed from the clock entries and stored nowhere, and the close of the day prompts for the spans left unmarked;
  - the *decision entry*, formerly the outcome entry, whose rationale is required except for `done`;
  - the *deviation entry*, formerly the finding entry.

  The evidence note is removed, as redundant with the decision entries. A [weekly report](../kernel/processes/feedback.md#^weekly-report), computed from the decisions and the completed tasks, replaces it for any reader.
- **Appointments.** A dated appointed block is an *appointment*, recorded as soon as it is known. Its preparation is a task linked to it, drawn from a share of the appointed stream, and compared with an optional cap per appointment.
- **Configuration.** The profile, and an [availability record](../specification/typical-week-record.md) kept apart from it.
- **Identifiers.** The identifier of a task is the slug of its title, fixed at creation.
- **Options.**
  - **Imposed deadlines:** the kinds `hard` and `soft` only. The exhaustion of a resource is a `hard` deadline whose date the agent revises.
  - **External parties and waits, delegation, reactive work:** ratified as stated.
  - **Tooling control:** ratified without the rule *manual first*, so a means may be built at its first need.
  - **Milestone graph, calibration, quantified valuation and the availability model:** ratified as stated.
- **Modules.** The mechanism, and the modules [bibliography](../modules/bibliography/_index.md) and [mathematical mastery](../modules/mathematical-mastery/_index.md). Four modules are proposed for the research profile: writing, delegation, meeting preparation, and experiments and simulations. The module on delegation covers the preparation of a brief as well as the review of its output.

## Constraints that decide the changes

- **A distinction must change a computation or a behavior.** The regimes `calendar` and `committed` both describe a block fixed by a party with its preparation, and the notes left the duration of a meeting unassigned.
- **A term must name its object.** A theme names a practice, not a span of time. A finding names the result of a check as well as a deviation from a policy. Enablement, sensing, interface and capability name an effect, a metaphor or an attribute, and not the work of their role.
- **A record must not restate another.** A written evidence note restates the rationales of the decisions of its week.

## Options weighed

- **The kind `resource`, with a date computed from a rate of consumption.** Rejected: a date revised by hand serves the same use, with one kind fewer.
- **The rule *manual first*.** Rejected: the count of manual repetitions delays a means that the agent already judges worth building.
- **Evidence note kept as an option.** Rejected for the third constraint.

## Consequences

- This record supersedes the decision on the [weekly note](weekly-note.md), and the parts of the decisions on [additional dimensions](additional-dimensions.md) and on [cumulative feasibility](cumulative-feasibility.md) that introduced the regime `committed` and the kind `resource`.
- The option *committed capacity* is removed: appointed blocks belong to the core.
- The record formats are decided next, on this set of objects.
