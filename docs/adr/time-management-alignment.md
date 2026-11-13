---
tags:
  - decision
status: accepted
created: 2026-11-13
index: "[Architecture decisions](docs/adr/_index.md)"
aliases:
  - Alignment with the time-management course
---
# Alignment with the time-management course

> [!QUESTION] Goal: which operational methods of the [time-management course](../references/time-management-course.md) does `horai` take up where its method lacked them, and how do its terms relate to theirs?

The course confirmed most mechanisms of the method, and exposed three gaps: estimates without any margin before calibration, no backward plan of a deadline, and an overhead budgeted but never measured.

## Decision

- **Prior margins.** Before a class of variance holds `calibration_min_samples` entries, its quantile ratio is the policy `prior_margin`: 2 for routine work and 3 for exploratory work, which the research profile raises to 4. Its median ratio is 1.
- **PERT.** A routine item may state three durations in place of its budget. Its budget is then their PERT value, and its share of the buffer of a deadline is its pessimistic duration less that value.
- **Retroplanning.** For each deadline, the roadmap shows by default the latest start of each milestone under it, and on demand the full [retroplanning](../kernel/objects/deadline.md#^retroplanning), down to the tasks that state a budget.
- **Overhead.** The planning acts are the tasks of one standing parent marked `overhead`, clocked like any work. Their time is the third core metric of the weekly review, against `overhead_budget`.
- **Terms.** A term of a reference method is adopted when the concept is the same and the term is free in `horai`; otherwise `horai` keeps its term and the reference note states the correspondence. Hence the *buffer* keeps its name for the course's margin of safety, the *appetite* is kept apart from the course's timeboxing, which places a task in the calendar, and the backward output is named *retroplanning*.

## Constraints that decide the choices

- **No inference at run time.** The prior margins are policies stated in the parameters, not estimates of the tool.
- **An appetite is a judgment of worth.** A margin corrects estimates and sizes buffers, and never changes an appetite.
- **The method is bounded by its own budget,** as the tenth commitment states, so its overhead must be measurable.

## Options weighed

- **Margins only, or PERT only.** Not adopted: the margins cover the cold start of every class, and PERT serves an item for which the agent can state its scenarios.
- **The latest starts of milestones only.** Not adopted: the author wants the full retroplanning available on demand.
- **A kind of clock entry for the rituals.** Rejected: one standing parent measures the overhead with the existing records.
- **Renaming every term after the reference methods.** Rejected: a term of a different concept would mislead.

## Consequences

- The 2-20-2-2 rule is a documented departure of the triage, for its first step only.
- The prior margins and the retroplanning act on the options of calibration and of imposed deadlines, and are implemented with them.
