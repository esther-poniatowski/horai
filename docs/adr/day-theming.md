---
tags:
  - decision
status: proposed
created: 2026-11-11
index: "[Architecture decisions](docs/adr/_index.md)"
aliases:
  - Day theming
---
# Day theming

> [!QUESTION] Goal: to which unit of time is a stream assigned?

The first statement of the method assigned a stream to each span of 90 minutes, with a change of task allowed only at the end of a span.

## Decision

A stream is assigned to a [block](../kernel/objects/horizon.md#^block) of a half-day or a day. Only the slots of the streams L and B are fixed by the clock. A block may overrun when the work is in flow.

## Constraints that decide the unit

- **The length of 90 minutes has no support.** The review found no good evidence for it, as the note on [attention and switching](../references/attention-and-switching.md) states.
- **A switch has a cost, and a proof attempt holds a state that is expensive to rebuild.** The findings on attention argue for fewer switches, not for scheduled ones.
- **Floors need a fixed position.** Without a fixed slot, the streams L and B lose to the others, which is the failure that the method corrects.

## Options weighed

- **Spans of 90 minutes.** Rejected for the first two constraints.
- **One project per week.** Not adopted: it minimizes switches, and leaves the floors and the meetings without a place.

## Consequences

- The calendar of a week holds blocks, and the daily slot of the stream L.
- The share of a stream is counted in blocks, and checked against the logged hours.
