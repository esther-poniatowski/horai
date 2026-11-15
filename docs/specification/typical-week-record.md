---
tags:
  - specification
  - wip
index: "[Specification](docs/specification/_index.md)"
aliases:
  - Typical week record
  - Availability record
---
# Typical week record

> [!QUESTION] Goal: which fields state the time of the agent in a typical week and its placement among the streams, so that capacity is planned on the time that is usable?

The typical week states the [availability](../kernel/objects/availability.md#^availability) of the agent as the agent reasons about it: the spans available on each weekday, the appointments fixed by others within them, and the blocks of the streams. A date departs from it in the calendar of dates, as the [calendar record](calendar-record.md) states.

## Week

| Field | When it is required | Kind | Values | Source |
| --- | --- | --- | --- | --- |
| `predictable` | always | authored | whether the free time of the coming week is known at the weekly review | [availability](../kernel/objects/availability.md#^availability) |
| `poor_week` | always | authored | a duration: the working time of a poor week, on which an unpredictable week is planned | [availability](../kernel/objects/availability.md#^availability) |
| `days` | unless `weekly_hours` is stated | authored | for each weekday, the fields of the next table | [block](../kernel/objects/horizon.md#^block) |
| `weekly_hours` | unless `days` is stated | authored | a duration: the working time of a typical week, for an agent without fixed spans | [availability](../kernel/objects/availability.md#^availability) |
| `unplaced` | optional | authored | the appointments held without a fixed slot, each with an identifier, a length, the stream, the party, optionally a title, a number `times` per period (1 when absent), and a period `every`: a number of weeks such as `P2W`, counted from the date `from`, or a calendar month, `P1M`, one week when absent; the calendar of dates places them | [recurrence](../adr/uniform-selection-and-recurrence.md) |
| `capacity` | always | computed | the working time of a typical week: `weekly_hours`, or else the sum of the spans | [plannable capacity](../kernel/objects/availability.md#^plannable-capacity) |
| `minimum_span` | with `days` | computed | the shortest available span of the week | [slots](../kernel/objects/availability.md#^slots) |
| `capacity_estimate` | option availability model | computed | the distribution of the weekly capacity, from the clock entries | [estimates](../kernel/foundations/parameters.md#^parameter-kinds) |

## Day

A span is written as its start and its end, such as `08:30-12:30`, and the end may be `24:00`. A block and an appointment are written as a start and a length. A request window is a block of a stream triggered by arrival.

| Field | When it is required | Kind | Values | Source |
| --- | --- | --- | --- | --- |
| `spans` | always | authored | the spans available on the weekday, disjoint | [availability](../kernel/objects/availability.md#^availability) |
| `appointed` | optional | authored | the recurring appointments of the weekday, each with an identifier, a start, a length, the stream, the party, optionally a title, optionally `from`, the date of its first occurrence, and either `every`, a number of weeks such as `P2W` counted from `from`, or `occurrences_in_month`, such as `[1, -1]` for the first and the last of the month; every week when neither is stated | [recurrence](../adr/uniform-selection-and-recurrence.md) |
| `blocks` | optional | authored | per block, a start, a length and one stream | [block](../kernel/objects/horizon.md#^block) |

The identifier of a recurring appointment is unique in the plan, and an appointment held on several weekdays keeps one identifier on all of them. A week cancels or moves one occurrence of it by that identifier.

## Checks

- **Spans.** The spans of a weekday end after they start, and do not overlap.
- **Placement.** Each block and appointment lies within a span, and no two of them overlap.
- **Streams.** A block and an appointment name a stream of the profile.
- **Recurrence.** The date `from` of a recurring appointment falls on its weekday.
- **Energy.** A block of a stream of high `complexity` lies within the spans of high energy that the [profile](profile-record.md) states for its weekday. A block outside them is reported as a warning.
- **Allocation.** The plannable time of the typical week is its spans, less the mean weekly time of the recurring and the unplaced appointments, less the reserves per week and per day. The blocks of each stream give it the share of that time, or the reserve, that its allocation states; the blocks of a stream triggered by arrival, its request windows, hold its reserve. An exact amount is met within `allocation_tolerance`, and a deviation is reported as a warning. A reserve per event is checked on the week of its appointments, as the [calendar record](calendar-record.md) states.
