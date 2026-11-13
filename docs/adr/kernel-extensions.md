---
tags:
  - decision
status: proposed
created: 2026-11-11
index: "[Architecture decisions](docs/adr/_index.md)"
aliases:
  - Extensions of the kernel
  - Single agent with external parties
---
# Extensions of the kernel

> [!QUESTION] Goal: how do reactive work, external collaborators, imposed deadlines and quantified cost enter a method that schedules one agent?

The research instance had little of each, and the first statement of the method ignored them. Other domains are dominated by one or several, as the [comparison of instances](../profiles/comparison.md) shows.

## Decision

The four features are [modulators](../kernel/foundations/problem-class.md#^modulators) of the class of problems. Each is an extension that the kernel defines and that a profile turns on.

| Extension | Principle adopted |
| --- | --- |
| Reactive work | a [reserve](../kernel/processes/reactive-work.md#^reserve) sized above the load, classes of service, and windows between the blocks |
| External parties | a party is [never scheduled](../kernel/foundations/commitments.md#^c-own-acts): each relation is reduced to acts of the agent, and a wait is an explicit condition |
| Imposed deadlines | a deadline is the imposed counterpart of an appetite, with a [feasibility test](../kernel/processes/imposed-deadlines.md#^feasibility-test), one buffer and a fixed order of adjustments |
| Quantified cost | a cost of delay [orders within a stream](../kernel/foundations/commitments.md#^c-valuation), bounds an appetite, and never moves capacity between streams |

## Constraints that decide the principles

- **One agent.** The method allocates one attention. The assignment of work among several persons is a different problem, with its own literature, and stays outside.
- **Arrivals must not be ranked against plans,** or the last arrival wins, as the [diagnosis](../kernel/foundations/diagnosis.md) states.
- **A latency is not work.** The time of a party runs in parallel with the work of the agent, so it is an edge of the graph and not an item of the plan.
- **Deferred payoff has no observable price.** A comparison in a unit starves the roles sensing and capability, which is the failure that the method corrects.

## Options weighed

- **Collaborators as further agents with their own plans.** Rejected for the first constraint.
- **Requests entered in the common backlog with a priority.** Rejected for the second.
- **A global order by cost of delay.** Rejected for the fourth: the ordering result holds for the items of one queue, and the streams are not one queue.
- **Self-imposed deadlines as commitment devices.** Rejected: they reproduce the inflation of dates, and the appetite already fixes time from inside.

## Consequences

- The commitments numbered nine, and the control questions seven, with [coordination](../kernel/foundations/control-questions.md). The second review raised them to ten and nine, as the decisions on the [minimal core](minimal-core.md) and on the [additional dimensions](additional-dimensions.md) record.
- Each extension adds fields to the records, one metric and one procedure, all inactive when the extension is off.
- The second review amended three of the four principles: the deadline test became [cumulative](cumulative-feasibility.md), the cost of delay is applied [at the milestone](milestone-level-valuation.md), and the reserve is sized on a quantile of the load per window, as the note on [reactive work](../kernel/processes/reactive-work.md#^reserve) states. The ban on valuation across streams was narrowed to the floors and the reserve.
