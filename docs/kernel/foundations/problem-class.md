---
tags:
  - theory
index: "[Foundations](docs/kernel/foundations/_index.md)"
aliases:
  - Class of problems
  - Conditions of membership
  - Modulators
---
# Class of problems

> [!QUESTION] Goal: under which conditions is a situation an instance of the problem that the method solves, and along which features do the instances differ?

## The problem

The method addresses the self-directed allocation of one scarce resource, the attention of one **agent**, which cannot be parallelized. ^problem

## Conditions of membership

A situation belongs to the class when four conditions hold. ^conditions

1. **Heterogeneous delay of payoff.** Some work pays off soon and visibly, other work later and indirectly, so no single scale of priority ranks both.
2. **Unbounded inflow of options.** The work that could be done always exceeds the capacity.
3. **Discretion.** The agent decides the allocation of at least a stated fraction of its capacity, the parameter `discretion_min` of the [parameters](parameters.md#^parameter-table). Below it, commitment and stopping are imposed from outside, and the method has little to decide. ^discretion
4. **Separated time scales.** The purposes span months or years, and the execution spans hours.

## Modulators

The other features vary across the instances. Each activates an object or an option of the kernel, which a [profile](../../profiles/_index.md) turns on. ^modulators

| Modulator | Question that it raises | Object or option |
| --- | --- | --- |
| Endogenous means | does the agent build part of the means on which its results depend? | [enablement](../processes/enablement.md) |
| Structural uncertainty | are some results unknown until explored? | [phase](../objects/phase.md) |
| Reactive load | how much work arrives unplanned, with an expected time of response? | [reactive work](../processes/reactive-work.md) |
| External dependence | on whom does the work wait, and who waits on it? | [external parties](../objects/external-party.md), [coordination](../processes/external-coordination.md) |
| Delegation | does the agent hand part of its own work to others? | the relation [`delegates`](../objects/external-party.md#^relations) |
| Several principals | does the agent answer to more than one party? | the [principal](../objects/external-party.md#^principal) per deliverable |
| Imposed deadlines | which dates are fixed from outside? | [deadlines](../objects/deadline.md), [their test](../processes/imposed-deadlines.md) |
| Committed capacity | is part of the time sold, rostered or owed in advance? | the regime [`committed`](../objects/regime.md#^regimes) |
| Fragmented availability | is the time available in short, unpredictable pieces? | [availability](../objects/availability.md) |
| Quantifiable cost | can the value of a result, or the cost of its delay, be stated in a unit? | [value](../objects/value.md) |

The [comparison of instances](../../profiles/comparison.md) places each profile on the conditions and on the modulators.

## Boundaries of the class

- **Homogeneous queue.** Work of one kind that arrives as a stream of similar items fails condition 1, and needs only the control of a flow.
- **Fully structured project.** A project whose network of activities is known, and whose means are given, needs only the scheduling of its activities.
- **Insufficient discretion.** When the reactive load and the committed capacity leave less than `discretion_min`, the method degrades to its [minimal core](core-and-options.md): the floors and the reserve are kept, the remainder is served as it arrives, and the excess is a finding for the [admission of deliverables](control-questions.md#^nine-questions).
- **Direction of others.** The agent may delegate work and await its output. The allocation of the work of a team, and the balance of its loads, are outside the kernel: other persons enter a plan as [external parties](../objects/external-party.md), which the agent does not schedule.
