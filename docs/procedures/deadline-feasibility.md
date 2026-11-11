---
tags:
  - procedure
index: "[Procedures](docs/procedures/_index.md)"
aliases:
  - Deadline feasibility
---
# Deadline feasibility

> [!QUESTION] Goal: how are the dates that the agent cannot move tested together, before a new one is accepted or proposed, and at each cycle?

The procedure applies the [test of imposed deadlines](../kernel/processes/imposed-deadlines.md). The computations of steps 3 to 5 are done by the tool.

1. **Record.** Record the new deadline on the level that it concerns, with its kind and the party that relies on it. For a deadline of the kind `resource`, record the quantity left and its rate of consumption.
2. **Work.** Check that every item under each deadline has a budget. For a deliverable in exploration, state the date at which it must leave that phase, and count its appetite as its demand.
3. **Demand.** For each deadline, compute the demand and the buffer from the budgets and the estimates of the ratios.
4. **Slack.** Sort the deadlines by date, and compute the cumulative slack per stream, then over the plan.
5. **Requests.** Compute the latest date of each external request under a deadline.
6. **Adjust.** If the demand exceeds the capacity at some date, apply the adjustments in their [order](../kernel/objects/deadline.md#^adjustment-order): scope, capacity of the other `planned` and `pulled` streams, date or resource, and the floors last. Record each in an adjustment entry, with what it displaces.
7. **Answer.** Accept the date, accept it with the adjustments, propose another date, or decline. An imposed date that cannot be declined is recorded with its adjustments in the same way.
