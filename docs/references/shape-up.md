---
tags:
  - reference
index: "[References](docs/references/_index.md)"
aliases:
  - Shape Up
---
# Shape Up

Shape Up is the product-development method of Basecamp, described by Singer [singer2019]. It replaces the estimate of a piece of work by an **appetite**: the time that the result is worth, fixed in advance, with a scope shaped to fit it.

## Method

- **Appetite.** The question "how long will this take?" is replaced by "how much time is this worth?". Time is fixed and scope varies [singer2019].
- **Cycle and cool-down.** Work proceeds in cycles of six weeks, each followed by a cool-down of two weeks without scheduled work.
- **Circuit breaker.** A project that is not finished at the end of its cycle is cancelled by default, and not extended.
- **Betting.** The work of a cycle is chosen at a meeting before it, and no backlog is maintained.

## Bearing on `horai`

- The [appetite](../kernel/objects/appetite.md#^appetite), the [cool-down](../kernel/objects/horizon.md#^cycle) and the [stop by default](../kernel/processes/uncertainty-control.md#^stop-default) come from this method.
- The method addresses product teams. The review of 2026-11-11 found that its chapter on appetite cites anecdotes and no data, and found no controlled evidence for fixed time and variable scope in research.
- `horai` departs from it on two points: the length of a cycle follows the dates of the party to whom the agent is accountable, and appetites apply to [exploratory work only](../adr/variance-classes.md).

## Sources

- [singer2019] ✓ (chapter 3) [Singer, *Shape Up: Stop Running in Circles and Ship Work that Matters*, Basecamp, 2019](https://basecamp.com/shapeup/1.2-chapter-03)
