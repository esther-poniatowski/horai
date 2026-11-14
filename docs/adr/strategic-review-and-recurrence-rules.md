---
tags:
  - decision
status: accepted
created: 2026-11-14
index: "[Architecture decisions](docs/adr/_index.md)"
aliases:
  - Procedure of the strategic review
  - Recurrence rules
---
# Strategic review and recurrence rules

> [!QUESTION] Goal: how is the strategic review performed, and by which rules does a task recur beyond the default periods?

The kernel assigns the strategic review the admission of deliverables, their stop, the answers to the deviation entries and the reading of the ideas file, but no procedure stated its steps, and nothing fixed its cadence. The task that holds it could not recur, since `recurs` offered only a day, a week or a cycle.

## Decision

- **Procedure.** The [strategic review](../procedures/strategic-review.md) is held in a cool-down, before the cycle planning, in seven steps: purposes, close, policies, situation, ideas, admission, record.
- **Cadence.** The cadence of the review is the rule of recurrence of its task, `P2C` by default, about the 13 weeks that the estimate of the overhead assumes.
- **Rules of recurrence.** `recurs` takes a default rule, `daily`, `weekly` or `cycle`, a rule named in the field `recurrences` of the profile, or a period: `P<n>` followed by `D` (days), `W` (weeks of commitment), `M` (months) or `C` (cycles), the one designator that horai adds to ISO 8601. A named rule may not take the name of a default rule.
- **Reopening.** A recurring task is open again once its rule counts that many periods begun since its last completion. A period begins at each date, at each weekly review held, on the first of each month, or at the start of each cycle. With one period, the rule reproduces the default rules.

## Constraints that decide the rules

- **A cadence is stated once.** The recurrence of the task already states when the review comes back, so no parameter of the strategic horizon is added.
- **One notation of periods.** The appointments state their periods as ISO durations, so the tasks do as well.

## Options weighed

- **A fixed calendar counted from an anchor date.** Rejected: a recurring task is done when it is done, and its next opening follows its completion; the appointments keep the fixed calendar, since others fix their dates.
- **Rules written in words, such as `every 2 cycles`, for the tasks and the appointments.** Rejected by the author in favour of the ISO durations.
- **A mapping for cycles, or no unit of cycles beyond the default.** Rejected: the first gives one field two forms, and the second lets the review reopen in the middle of a cycle.
- **Inline rules only.** Rejected by the author in favour of named rules beside them, so that several tasks share one cadence.

## Consequences

- The task schema admits a period or a name in `recurs`, and the profile gains `recurrences`; the check reports a rule that resolves to no period.
- The plan of the author gives the task `strategic-review` the rule `P2C`.
