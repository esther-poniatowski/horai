---
tags:
  - specification
  - wip
index: "[Specification](docs/specification/_index.md)"
aliases:
  - Calendar record
  - Cycle record
  - Calendar of dates
---
# Calendar record

> [!QUESTION] Goal: which fields state the cycles, and the departures of single dates from the typical week, so that the allocation can be checked and the views computed?

## Cycle

| Field | When it is required | Kind | Values | Source |
| --- | --- | --- | --- | --- |
| `id` | always | authored | an identifier, which names the file of the cycle | [file layout](file-layout.md) |
| `start`, `end` | always | authored | dates | [cycle](../kernel/objects/horizon.md#^cycle) |
| `cool_down` | always | authored | the dates of the cool-down | [cycle](../kernel/objects/horizon.md#^cycle) |
| `capacity` | always | computed | the plannable capacity of the cycle: that of its weeks, less the reserves per cycle, per stream, at the low quantile of the availability | [plannable capacity](../kernel/objects/availability.md#^plannable-capacity) |

## Dates of a month

The departures of single dates from the [typical week](typical-week-record.md) are recorded in the file of their month, as soon as they are known, whatever the date of the next weekly review. The week of commitment does not depend on these files: it starts at a review held, as the [review log](log-record.md) records it.

| Field | When it is required | Kind | Values | Source |
| --- | --- | --- | --- | --- |
| `month` | always | authored | the month of the file, which names it | [file layout](file-layout.md) |
| `unavailable` | when an absence starts in the month | authored | per absence, `from`, its first date, optionally `to`, its last date, `from` when absent, and optionally a `reason`, shown in the week view | [availability](../kernel/objects/availability.md#^availability) |
| `days` | when a date of the month departs from the typical week | authored | for each such date, the fields of the next table | [weekly review](../procedures/weekly-review.md) |

## Departures of a date

A date takes only the fields of its departures. The calendar of the date is the typical day of its weekday, changed by these fields. A date covered by an absence holds no entry.

| Field | Values | Effect |
| --- | --- | --- |
| `blocks` | per block, a start, a length and one stream | the blocks of the date, in place of those of the typical day |
| `removed_blocks` | the starts of typical blocks | those blocks are removed on this date |
| `added_blocks` | per block, a start, a length and one stream | blocks added on this date |
| `appointments` | per appointment, an identifier, a start, a length, the stream, the party, and optionally a title, and `places`, the identifier of the unplaced appointment that it places | appointments of this date only, added to the recurring ones |
| `cancelled` | identifiers of recurring appointments | the occurrences of this date are cancelled |
| `moved` | per recurring appointment, its identifier, a new start, and optionally a new length | the occurrence of this date is held at another hour |

The preparation of an appointment, when it calls for one, is a task that names it in `prepares`, with a budget, and an added block of its stream holds that budget.

## Checks

- **Month of the file.** Each date of `days`, and the first date of each absence, falls within the month of the file.
- **Absences.** An absence ends on or after its first date.
- **Recurring appointments.** A cancelled or moved identifier names a recurring appointment of the weekday of the date.
- **Blocks.** A removed start names a block of the date.
- **Unplaced appointments.** Each unplaced appointment of the typical week is placed `times` in each of its periods. A period of one week is the seven dates that start at the last review held; a longer period is checked in the week in which it ends. A week whose dates are all unavailable is not checked, nor is an ended week; a shortfall is reported as a warning.
- **Preparations.** Over the same dates, the blocks of a stream hold at least the budgets of the preparation tasks committed at that review, and each budget lies within the bound of the reserve per event of its stream; a deviation is reported as a warning.
- **Streams.** A block and an appointment name a stream of the profile.
