---
tags:
  - theory
index: "[Foundations](docs/kernel/foundations/_index.md)"
aliases:
  - Commitments of the method
---
# Commitments of the method

> [!QUESTION] Goal: from which commitments do the rules of the method follow?

1. **Commitment is separate from inventory.** A task is recorded without any promise, and enters a plan only by an act of planning at a stated horizon. ^c-inventory
2. **Capacity precedes tasks.** Capacity is divided among streams before any task is selected, so that the share of a stream never depends on the urgency of its tasks. The one exception is the recorded adjustment that an imposed deadline requires, in its [fixed order](../objects/deadline.md#^adjustment-order). ^c-capacity
3. **Time is fixed and scope varies, where variance is high or the date is imposed.** Exploratory work receives a budget fixed in advance, and work under an imposed deadline receives its date from outside. In both cases the scope adjusts. Routine work is estimated. ^c-fixed-time
4. **Enablement is pulled.** A means is built because a named result consumes its output, and to the extent that this result requires. ^c-pull
5. **Planning depends on the phase.** A plan states milestones and their graph only where the structure of the work is known. Exploration is planned by questions and judged by the information gained. ^c-phase
6. **Logs revise estimates, and decisions revise policies.** Every number is a [parameter](parameters.md). An estimate is revised from the records of the agent, and a policy only by a recorded decision. ^c-logs
7. **Arrivals are bounded by a reserve.** Unplanned requests are served from a capacity reserved for them, in windows of their own, and do not displace the planned work at the moment of their arrival, except for the class `immediate`, whose interruptions are logged and counted in the load. ^c-reserve
8. **Only the acts of the agent are scheduled.** An external party is never scheduled, including a party to which the agent delegates. A plan states the request, the follow-up, the review and the fallback, which are acts of the agent. ^c-own-acts
9. **Valuation never reduces a floor or the reserve.** A quantified worth orders milestones within a stream, and may inform a recorded trade-off between streams of the regimes `planned` and `pulled` at the strategic review. It never reduces the capacity of a floor or of the reserve, since the payoff of the work that they protect is real and has no observable price. ^c-valuation
10. **The method is bounded by its own budget.** The method is installed as its [minimal core](core-and-options.md#^core), and an option is turned on only when its modulator is present or a decision lacked it. ^c-core

> [!NOTE]
> Commitments 3 and 5 were revised after the first review, as the decisions on [variance classes](../../adr/variance-classes.md) and on [phase-dependent planning](../../adr/phase-dependent-planning.md) record. Commitments 7 to 9 were added with the [extensions of the kernel](../../adr/kernel-extensions.md). Commitments 2, 6 and 9 were narrowed, and commitment 10 added, after the second review, as the decisions on [policies and estimates](../../adr/policies-and-estimates.md) and on the [minimal core](../../adr/minimal-core.md) record.
