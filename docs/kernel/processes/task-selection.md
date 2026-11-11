---
tags:
  - theory
index: "[Processes](docs/kernel/processes/_index.md)"
aliases:
  - Selection of the next task
  - Selection rule
---
# Selection of the next task

> [!QUESTION] Goal: given the plan of the week, by which rule does the next task follow?

The selection never compares tasks of different streams, since the current [theme](../objects/horizon.md#^theme) fixes the stream. The one exception is the [window](../objects/horizon.md#^window), in which requests and tasks that release a wait are served whatever their stream.

**Selection rule.** The candidates are the tasks in the state `week`, of the stream of the current theme, whose milestone has no open dependency and which are not [waiting](../objects/external-party.md#^waiting). The rule first chooses a milestone, then a task within it, by four keys applied in order. A key that the profile does not supply is skipped. ^selection-rule

1. **Deadline.** A milestone under a deadline whose [buffer is running ahead](../objects/deadline.md#^buffer-consumption) comes first.
2. **Release of a wait.** A task that starts the latency of an [external party](../objects/external-party.md), such as a request, a brief or a handoff for review, comes next, since that latency runs in parallel with the work of the agent. Such a task may be done in the next window, without waiting for the theme of its stream. ^release-key
3. **Unblocking.** Where a [milestone graph](../objects/dependency.md#^graph-uses) exists, the milestone with the largest successor work comes next.
4. **Worth.** Among the remaining milestones, the order is by decreasing $\gamma / w$, the cost of delay over the remaining work, where the [value](../objects/value.md) is quantified, and by the rank set at the cycle planning otherwise. ^valuation-key

Within the chosen milestone, tasks are taken in their local order, and among unordered tasks the one marked as the riskiest comes first. The choices that these keys do not settle are left to the agent, who weighs the energy available and the momentum of the work.

## Grounds of the keys

- **Worth at the milestone.** Completing one task of a milestone stops no cost of delay, so the ratio is applied to milestones, with their remaining work as the duration. Applied to tasks, it would interleave the tasks of several milestones and delay the completion of each.
- **The ratio is a heuristic here.** For one agent, items of known durations, linear costs of delay and no precedence, the order of decreasing $\gamma_j / d_j$ minimizes the total cost of delay, as the note on the [cost of delay](../../references/cost-of-delay.md) states. With precedence the problem is hard, and with estimated durations the guarantee is lost. The composition of the keys is therefore a stated heuristic, not an optimum.
- **Risk first within a milestone.** The riskiest task is done first, so that a failure occurs while most of the budget remains.
- **In exploration, the keys keep their order.** A question under a deadline or awaiting a party is handled by the first two keys. The last key uses the rank, which the agent sets by the information that each question is expected to yield.
- **Priority is an output.** The rule replaces the priority assigned by hand, as the [commitment states](../objects/commitment-state.md) state.
