---
tags:
  - decision
status: accepted
created: 2026-11-14
index: "[Architecture decisions](docs/adr/_index.md)"
aliases:
  - Streams, allocation and loose tasks
  - Allocation of a stream
---
# Streams, allocation and loose tasks

> [!QUESTION] Goal: how does a stream receive its time, which records hold the tasks that serve no deliverable, and where do the parties and the energy of the agent sit?

The review of the first plan of the author exposed five defects. A share of the plannable week cannot state time whose amount others set, such as requests and the preparation of meetings. The worth of milestones was named by the field that carries it under one scale. Parties were free names, so a typo created a party. The permanent areas duplicated the streams, and a finite group of loose tasks, such as the follow-up of a conference, had no parent. The energy hours, a stable property of the agent, sat in the typical week, which changes with the situation.

> [!WARNING] Partly replaced
> The decision on [dates, reviews and recurring tasks](dates-reviews-and-recurring-tasks.md) replaces the state `cycle` of a loose task, and the decision on [properties apart from the trigger](properties-apart-from-the-trigger.md) replaces the restriction of a reserve per event to a stream triggered by appointment.

## Decision

- **Allocation.** The allocation of a stream states four independent properties:
  - `mode`: `share`, a fraction of the plannable time, or `reserve`, a duration;
  - `bound`: `at_least`, `at_most` or `exact`;
  - `amount`: a fraction for a share, a duration for a reserve;
  - `per`: `day`, `week`, `cycle` or `event`, `week` when absent; with `per: event`, the optional list `events` narrows the events to some appointments.

  The plannable time of a week is the available time, less the appointments, less the reserves. The shares divide that remainder. A reserve per event counts only for an appointment that a task prepares, and a preparation task that states no budget takes the amount. The reserve of a stream triggered by arrival is a prior, which the logged load replaces. The trigger of a stream no longer fixes the form of its allocation, and the check rejects only an incoherent combination, such as a share stated as a duration.
- **Worth.** The profile states `worth: {scale}`, where `scale` is `ordinal` or `cardinal`. A cardinal worth also states its `unit` and its `worth_per_hour`. Under an ordinal worth, the field `rank` of an item carries the order.
- **Parties.** A file `parties.yml` declares each party with an identifier and a name. A field `party` or `accountable_to` names a declared party by its identifier, or an occasional party by a mapping `{name: ...}`. An undeclared identifier is an error.
- **Loose tasks.** The permanent areas are retired. A task serves a milestone or a question, from which it takes its stream, or names its stream directly. A folder ships its loose tasks in a task list, `horai:task-list@1`, beside the files that they touch. The holding file keeps only the tasks that name neither a milestone nor a stream.
- **Finite work outside a deliverable.** A milestone may omit its deliverable. It then serves its stream directly, and closes by its `done_when`, as the follow-up of a conference does.
- **Order of loose tasks.** Within the block of a stream, a loose task that is important and urgent precedes the milestones of the stream. The other loose tasks follow the ranked milestones, in the order of their quadrant and of their importance.
- **Planning.** The planning acts are loose tasks of a stream `planning`, triggered by the calendar, whose reserve per week, at most `PT1H45M` by default, replaces the parameter `overhead_budget`. The typical week gives that stream its blocks.
- **Energy.** The profile states the hours of high energy, `energy: {high}`, for every day or per weekday. The check reads them against the blocks of the typical week.

## Constraints that decide the formats

- **A share fits only time that the agent divides.** Time whose amount a party sets, or that one event calls for, is a duration.
- **A stream is a domain of activity that persists across time.** A group of tasks around one event closes, so it is a milestone, not a stream.
- **A task needs a stream, not a permanent parent.** The permanent parent existed only to give a stream to loose work, which a field of the task gives directly.
- **The profile describes the agent, and the typical week its situation.** The energy hours follow the agent.

## Options weighed

- **A share or a duration for each bound.** Rejected: a share then has no defined base once hours are reserved; the order of computation fixes it.
- **`ordering` as the name of the worth.** Rejected: under the cardinal scale, the amounts also decide the checkpoints, which the name hides.
- **Streams and areas merged, each area a stream.** Rejected: every group of tasks would need its own allocation and blocks.
- **Areas kept beside the streams.** Rejected by the author: the stream already gives a loose task what the area gave.
- **A new kind of record for finite loose work.** Rejected: a milestone without a deliverable holds it with no new kind.
- **Loose tasks always after the milestones.** Rejected: an urgent and important loose task would need the non-negotiable mark to pass.

## Consequences

- This decision replaces:
  - the weekly share of preparation and the field `default_budget` of the decision on [appointments and stages](appointments-and-stages.md);
  - the energy in the typical week of the decision on the [typical week and the types of deliverable](typical-week-and-deliverable-types.md);
  - the names `worth: {by}`, `permanent-area` and the forms of allocation of the decision on [explicit names](explicit-names.md);
  - the standing parent of a folder of the decision on [distributed records](distributed-records.md).
- The schemas of the profile, the milestone, the typical week and the holding file change in place. The schemas of the task list and of the parties are added, and the schema of the permanent area is removed.
- The selection gains the order of loose tasks. The week view compares the time of the stream `planning` with its reserve.
- A command that computes the blocks of a typical week from the allocation, the spans, the appointments and the energy hours is added to the roadmap.
