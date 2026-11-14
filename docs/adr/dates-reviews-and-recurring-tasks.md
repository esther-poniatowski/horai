---
tags:
  - decision
status: accepted
created: 2026-11-14
index: "[Architecture decisions](docs/adr/_index.md)"
aliases:
  - Calendar of dates
  - Review log
  - Recurring tasks
---
# Dates, reviews and recurring tasks

> [!QUESTION] Goal: which records hold the departures of single dates, the start of each week of commitment, and the work that recurs, so that each follows its own calendar?

The record of a week held two objects with different calendars. It bounded the commitments, which run from one weekly review to the next, and it held the departures of dates from the typical week. Its file was named by the planned date of its review, so a record written ahead became the current week on that date, even when the review was postponed, and the tasks of the week then left the selection. An absence of three weeks took one entry per date, spread over the files of reviews that would not be held. Two records overlapped when a review moved, and a departure recorded in the second record for a shared date was ignored.

The loose tasks showed two further defects. A recurring act, such as the weekly review, and a one-off task shared one form, whose single date of completion closed the recurring act for good. A loose task was in the state `cycle` as soon as it named its stream, so it could not wait in the backlog.

> [!WARNING] Partly replaced
> The decision on [the strategic review and the recurrence rules](strategic-review-and-recurrence-rules.md) extends `recurs` with periods, named rules and a count since the last completion.

## Decision

- **Calendar of dates.** The departures of single dates are recorded in a calendar of dates, one file per month, `calendar/dates/<month>.yml`, of type `horai:dates@1`. A range of whole dates on which the agent is unavailable is stated once, under `unavailable`, by its first date, its last date and its reason, in the file of the month of its first date.
- **Review log.** A weekly review held is an event, recorded in a review log, `log/reviews/<month>.yml`, of type `horai:review-log@1`. A week of commitment runs from a review held to the next one held. The field `committed_week` of a task names the date of the review that committed it. The check reports a last review older than seven days. The record of a week is retired.
- **Recurring tasks.** A loose task may state `recurs`: `daily`, `weekly` or `cycle`. A recurring task is always in the state `week`. Its field `completed` holds the date of its last completion, and the task is open again from the start of its next period.
- **State of a loose task.** A loose task stays in the backlog until a weekly review commits it to its week. It has no state `cycle`.

## Constraints that decide the formats

- **A record follows one calendar.** A departure belongs to its date, whenever the review is held; a commitment belongs to the review that made it.
- **An event is logged when it happens.** A review planned is not a review held, so only the log can start a week.
- **A record states no promise that nobody made.** A loose task is promised only by a weekly review.

## Options weighed

- **A file per review held, apart from the dates.** Rejected: the file would hold one field for an event that the log already records.
- **The record of a week, repaired.** A week would become current once its review is marked as held, and absences would take ranges. Rejected: an absence would still span several files, and overlapping weeks would still need a rule.
- **Recurring work recorded on its stream, without a task.** The clock would name the stream. Rejected by the author in favour of an explicit recurrence, at the cost of a mechanism of completion per period.
- **A field `cycle` on a loose task, like a milestone.** Rejected: each cycle planning would select and budget small tasks.

## Consequences

- The schema of the week is replaced by the schema of the dates, and a schema of the review log is added. The task schema gains `recurs`, admitted only on a loose task, and exclusive of `committed_week`.
- The state rule, the calendar of a date, the checks of the current week and the week view read the review log and the calendar of dates.
- This decision replaces the records of future weeks and the exceptions held by the record of a week, as decided on the [typical week and the types of deliverable](typical-week-and-deliverable-types.md), and the state `cycle` of loose tasks, as decided on [streams, allocation and loose tasks](streams-allocation-and-loose-tasks.md).
