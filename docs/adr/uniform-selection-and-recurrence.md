---
tags:
  - decision
status: accepted
created: 2026-11-14
index: "[Architecture decisions](docs/adr/_index.md)"
aliases:
  - Uniform selection of a cycle
  - Recurrence of appointments
---
# Uniform selection and recurrence of appointments

> [!QUESTION] Goal: by which single rule does a cycle select its items, how does every stream that holds committed work receive time, and how often can an appointment recur?

A review of the framework found that a milestone without a deliverable, such as the follow-up of a conference, fits no step of the cycle planning. The planning selected up to `milestones_per_cycle` milestones per deliverable in a structured phase, and the questions of each deliverable in exploration, so three cases were distinguished and the third had no rule. The stream of such a milestone had no allocation, so its capacity in a cycle was zero and the fit removed the milestone. The same review found that a recurring appointment could only repeat every week, so a supervision every two weeks or a monthly meeting misstated the plannable time.

## Decision

- **One rule of selection.** The cycle planning lists the open items, milestones and questions, with or without a deliverable, whose dependencies are done or will be within the cycle. It budgets each item, ranks the items of each stream, and removes the lowest-ranked items of a stream until the budgets fit its capacity. The phase of a deliverable decides only which items exist. The parameter `milestones_per_cycle` is retired.
- **Class of calibration.** The class of an item is its stream, the type of its deliverable, and its predictability. An item without a deliverable has no type, and shares its class with the items of its stream that have none.
- **Time of a stream.** A stream that holds committed work, an item selected for the current cycle or a task committed for the week, states an allocation. The check reports one that does not. Episodic work, such as the follow-up of conferences, takes a reserve per cycle, placed by blocks in the calendar of dates.
- **Recurrence of appointments.** A recurring appointment may state `from`, the date of its first occurrence, and either `every`, a number of weeks counted from `from`, or `occurrences_in_month`, the occurrences of its weekday in each month, `1` for the first and `-1` for the last. An appointment without a slot states `times` per period; its period, `every`, is a number of weeks counted from `from`, or a calendar month, `P1M`. The field `per_week` is retired. The typical week counts each appointment at its mean time per week.

## Constraints that decide the rules

- **One rule, no case.** The items of a cycle share a stream, a budget and a rank, so a rule that holds for one holds for all.
- **The capacity bounds the cycle.** The fit to the capacity of each stream bounds the selected work; the cap on active deliverables bounds the parallel results at the strategic horizon, and the dependencies order the milestones of one deliverable.
- **No work without time.** A stream without an allocation receives no block, so its committed work could never be selected for a block.

## Options weighed

- **A limit per deliverable, or else per stream.** Rejected: it keeps a case for the items without a deliverable.
- **A limit of items per stream.** Rejected: the fit to capacity already bounds a stream, and the parameter would add a second bound of the same quantity.
- **The time of the cool-down, or time borrowed from another stream.** Rejected: the first delays every follow-up to the end of the cycle, and the second spends the time of one stream on the work of another.
- **Periods in weeks only.** Rejected by the author in favour of exact monthly rules, at the cost of a second form of recurrence.

## Consequences

- The cycle planning, the horizons, the parameters and the calibration state the single rule.
- The schemas of the typical week and of the dates change in place; a dated appointment admits no recurrence.
- The calendar of a date, the plannable time and the check of the unplaced appointments read the recurrence.
