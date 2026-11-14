---
tags:
  - handoff
index: "[horai documentation](docs/_index.md)"
aliases:
  - Handoff
---
# Handoff

The handoff carries the state of the development of horai from one agent session to the next. Each session reads it first, works on the open step of the [roadmap](../TODO.md), checks the steps that it completes there, and updates this note before ending.

## Task state

- **Increment 1.** The commands `check`, `next`, `view week`, `start` and `stop` run on a plan in the [file layout](specification/file-layout.md), as the [CLI reference](guide/cli-reference.md) states. The exit criterion, one week of use on the plan of the author, is open.
- **Formats.** The [typical week and the types of deliverable](adr/typical-week-and-deliverable-types.md) and the [explicit names](adr/explicit-names.md) are implemented in the schemas, the loader, the checks, the week view, the fixture plan and the specification notes. The calendar of a date is computed in `src/horai/rules/calendar.py`, and its checks in `src/horai/rules/calendar_checks.py`.
- **Terms of the method.** The kernel notes, the procedures, the profiles, the modules and the references are carried to the explicit names; the decision records keep the terms of their time. The names of two notes and of seven anchors still carry the former terms, as the roadmap lists.
- **Pilot in Geonexus.** The configuration `config/tools/horai.yml`, the central folder `planning/` and the record `conferences/2026-08_ccs/ccs-2026-follow-up.yml` pass `horai check`. The author is reviewing their values, which are marked as placeholders. The original task list `conferences/2026-08_ccs/TODO.md` stays beside the record until the author has compared the two. The rules of Geonexus on task tracking, work state, organization and the toolchain are amended to admit records of horai, with an exception for that comparison.
- **Streams, appointments and stages.** The decisions on [appointments and stages](adr/appointments-and-stages.md) and on [streams, allocation and loose tasks](adr/streams-allocation-and-loose-tasks.md) are implemented. The plan of the author in Geonexus follows them and passes `horai check`, except for warnings on values that the author settles: the energy hours, and the placement of the supervision in the week.
- **Review of the framework.** An adversarial review found fifteen defects, all now settled. Findings 1, 3, 12 and 15 are fixed; findings 2, 4 to 11, 13 and 14 are decided by the decisions on [parties, derived deliverables and the lifetimes of the profile](adr/parties-and-derived-deliverables.md), [properties apart from the trigger](adr/properties-apart-from-the-trigger.md), on [dates, reviews and recurring tasks](adr/dates-reviews-and-recurring-tasks.md), on [request windows and stages](adr/request-windows-and-stages.md) and on [uniform selection and recurrence](adr/uniform-selection-and-recurrence.md).
- **Version control.** Nothing of the formats, the pilot or the rule amendments is committed, in horai or in Geonexus.

## Active constraints

- **Accepted decisions.** The records of status `accepted` in the [decision index](adr/_index.md) bind every change. A choice that departs from one of them is put to the author before it is applied.
- **Ratification first.** Each decision is asked to the author through questions that state the alternatives, and is recorded before code is written.
- **Explicit names.** A field name, read with its value in a record, states what the value means without the glossary, as the decision on [explicit names](adr/explicit-names.md) fixes.
- **No consumer yet.** No format of horai is published, so every format keeps the version 1, and no code serves the migration of former formats.
- **Sources of a migration.** A list migrated into records of horai is deleted only on the request of the author.
- **Environment.** Python tools run through `conda run -n horai python -m …`; the bare command `pytest` resolves outside the environment.
- **Geonexus.** A change in Geonexus follows its own [instructions for agents](../../../research/geonexus/AGENTS.md), its rule on task tracking, and its commit gate `elenchos check`. The checked-out tree of Geonexus holds unrelated changes of the author, and another agent session may commit there concurrently.

## Open questions

- **Placeholders of the author.** The stream `conferences` with its reserve per cycle of `PT6H`, and the `done_when` of the CCS follow-up, are drafted values marked in their files.
- **Energy warnings.** The author keeps the energy hours `09:00-13:00`; the six warnings of `calendar/energy` on the blocks of `training` and `inquiry` outside them are known and accepted.
- **Stage defaults in Geonexus.** The stage `submission` of the type `article` states `predictability: routine`; the other stages take the predictability of their type, pending the review of the author.
- **Overrun rule.** The rule of overrun by bounds is stated in the kernel; no code applies it, since no command extends a block.
- **Gate of Geonexus.** The gate fails on the uncommitted migration to logical targets of another session (the configuration of Anagraphe, the environment, the schema resources), not on the files of horai; a commit in Geonexus waits for that migration.
- **Index of `planning/`.** The amended rule on organization exempts `planning/` from an `_index.md`. The exemption was drafted by an agent and awaits the author.
- **Forms in Ekphrasis.** The schemas of horai reach Ekphrasis once horai publishes a registry of Kleisis and Geonexus pins a commit of horai, which requires a push to GitHub approved by the author.
- **Dependencies across stores.** A task of horai cannot depend on a line of a task list, nor the reverse; the rule of Geonexus requires moving an action into one store first. A wider integration is deferred.
- **Rule of the minimums.** The profile check of a minimum for the streams that yield knowledge and competence names two values of `yields`, whereas the property it protects is work of deferred payoff that nothing triggers. The author has not decided whether to restate it.
- **Types of deliverable of the profiles.** The types and their defaults in the notes of the profiles, beyond the paper and the poster of the research profile, were proposed by an agent and await the review of the author.
- **Class of calibration.** The decision on the types of deliverable calibrates the ratios per type. The kernel note on the control of uncertainty reads it as per type of deliverable and class of predictability, so that routine and exploratory work of one type are not pooled; the author has not confirmed that reading.
- **Lint baseline of the tests.** The tests hold 85 findings of pylint, 78 of them missing docstrings, all in code that predates the format change.

## Provenance

- The method: the notes of [docs/](_index.md), and the accepted decision records.
- The task lists of Geonexus, measured by a script of the ignored workspace `.agent-tmp/`, which also holds the proposals and the review sheet that preceded the first ratification.
- The [time-management course](references/time-management-course.md), and the account of the [phases of research](references/research-phases.md).
- The siblings consulted: Ekphrasis for forms built from schemas, Anagraphe for logical targets and generated indexes, Kleisis for the schema registry, Elenchos for the commit gate of Geonexus.

## Decision log

The decisions of the author are recorded in the accepted records of the [decision index](adr/_index.md). The latest are the decisions on [properties apart from the trigger](adr/properties-apart-from-the-trigger.md), on [dates, reviews and recurring tasks](adr/dates-reviews-and-recurring-tasks.md) on [request windows and stages](adr/request-windows-and-stages.md), on [uniform selection and recurrence](adr/uniform-selection-and-recurrence.md), on [parties, derived deliverables and the lifetimes of the profile](adr/parties-and-derived-deliverables.md) on [settings and yields](adr/settings-and-yields.md) and on [the strategic review and the recurrence rules](adr/strategic-review-and-recurrence-rules.md); each earlier record whose points they replace names them in a callout. For recurring work, the author chose a field `recurs` over clock entries that name a stream; the value `cycle` was added beside `daily` and `weekly` for the cycle planning. Two choices of the same session are recorded where they apply: every format keeps the version 1 until a first publication, and the loader reports a record of an unknown type instead of skipping it, but serves no migration of former formats.
