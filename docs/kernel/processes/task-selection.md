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

The selection never compares tasks of different streams, since the current [block](../objects/horizon.md#^block) fixes the stream. Two exceptions are admitted. In a [request window](../objects/horizon.md#^window), the tasks of its stream are served, then the tasks of any stream that hand off to a party. While an item is marked non-negotiable, every block and request window serves it, except the blocks of the appointments.

**Selection rule.** The candidates are the open tasks in the state `week`, of the stream of the current block, which are not [waiting](../objects/external-party.md#^waiting). The milestone of a candidate, when it has one, must have no open dependency and no consumed budget, since continuation without a [checkpoint](../objects/appetite.md#^checkpoint) decision is excluded. While an open item is marked [non-negotiable](../foundations/commitments.md#^c-non-negotiable), the candidates are the open tasks of that item, whatever the stream of the current block, or the marked task alone. A mark left on a closed item or a completed task is ignored, and `check` reports it. They enter the week as a [lateral entry](planning-horizons.md#^lateral-entries). The waiting tasks, and the tasks of a milestone whose budget is consumed, stay excluded. ^non-negotiable-key

The rule first chooses a milestone, then a task within it, by four keys. In this rule, a question counts as a milestone. The loose tasks of the stream are placed before or after the milestones, as the order of loose tasks below states. Each key orders only the milestones left tied by the keys before it. A key that the profile does not supply is skipped. ^selection-rule

1. **Deadline.** A milestone under a deadline whose [buffer is running ahead](../objects/deadline.md#^buffer-consumption) comes first.
2. **Hand-off to a party.** A milestone comes next when it holds a candidate task that starts the latency of an [external party](../objects/external-party.md), such as a request, a brief or a handoff for review. Within its milestone, that task leads among the tasks whose predecessors in the local order are done, since the latency runs in parallel with the work of the agent. Such a task, marked `hands_off`, may be done in the next request window, without waiting for the block of its stream. ^release-key
3. **Unblocking.** Where a [milestone graph](../objects/dependency.md#^graph-uses) exists, the milestone with the largest successor work comes next. A milestone outside the graph has a successor work of zero.
4. **Worth.** Among the remaining milestones, the order is by decreasing $\gamma / w$, the cost of delay over the remaining work, under a cardinal [worth](../objects/value.md), and by the rank set at the cycle planning under an ordinal worth. ^valuation-key

Within the chosen milestone, a task is taken only once its predecessors are done, wherever they sit. Among the tasks that this order leaves free, the quadrant of importance and urgency decides: important and urgent first, then important, then urgent, then the others. A task is important at the levels `highest` and `high`, and urgent once its scheduled date is reached. Within one quadrant, the higher importance comes first, then the task marked as the riskiest. The choices that these keys do not settle are left to the agent, who weighs the energy available and the momentum of the work.

**Order of loose tasks.** Within the block of a stream, a [loose task](../objects/work-hierarchy.md#^standing-parent) that is important and urgent precedes the milestones of the stream. The other loose tasks follow the ranked milestones, in the order of their quadrant, then of their importance.

## Grounds of the keys

- **Worth at the milestone.** Completing one task of a milestone stops no cost of delay, so the ratio is applied to milestones, with their remaining work as the duration. Applied to tasks, it would interleave the tasks of several milestones and delay the completion of each.
- **The ratio is a heuristic here.** For one agent, items of known durations, linear costs of delay and no precedence, the order of decreasing $\gamma_j / d_j$ minimizes the total cost of delay, as the note on the [cost of delay](../../references/cost-of-delay.md) states. With precedence the problem is hard, and with estimated durations the guarantee is lost. The composition of the keys is therefore a stated heuristic, not an optimum.
- **An important and urgent loose task comes first.** Placed after the milestones, it would need the non-negotiable mark to pass before them.
- **Risk first within a quadrant.** Among comparable tasks, the riskiest is done first, so that a failure occurs while most of the budget remains.
- **Importance by hand within a parent only.** The quadrant orders the tasks of one parent, after the matrix of Eisenhower, as the decision on [distributed records](../../adr/distributed-records.md) records. It also orders the loose tasks of one stream, which have no parent. Across parents, the keys above compose urgency and importance.
- **In exploration, the keys keep their order.** A question under a deadline or awaiting a party is handled by the keys of the deadline and of the hand-off to a party. The last key uses the rank, which the agent sets by the information that each question is expected to yield.
- **Priority is an output.** The rule replaces the priority assigned by hand, as the [commitment states](../objects/commitment-state.md) state.
