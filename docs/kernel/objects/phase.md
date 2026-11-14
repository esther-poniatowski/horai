---
tags:
  - definition
index: "[Objects](docs/kernel/objects/_index.md)"
aliases:
  - Phase
  - Structural uncertainty
  - Exploration, validation, delivery
---
# Phase

> [!QUESTION] Goal: in which phases of a deliverable can results be named in advance, and how is the work planned in the others?

The **phase** of a deliverable states what is known of its ends and of its means. Three phases are distinguished, and every profile uses their names. ^phases

| Phase | State of knowledge | Aim | Unit of planning | Judged by |
| --- | --- | --- | --- | --- |
| Exploration | the result worth producing is not yet stated | gain information about what is true, wanted or feasible | a question under a time box | the information gained |
| Validation | the result is stated, and whether it holds or can be made is unverified | confirm or reject the stated result | a [milestone](milestone.md) | its definition of done |
| Delivery | the result is established, and the means are known | produce and hand over | a milestone | its definition of done |

- **No graph in exploration.** The absence of a clear next step is normal in exploration. A graph of milestones drawn in that phase would be fictitious, and its precedences would give false precision.
- **A transition is a decision.** A deliverable passes to validation when a result worth producing is stated, and returns to exploration when it fails. The transition is recorded at a [cycle planning](../../procedures/cycle-planning.md).
- **The phase is borne by the deliverable, not by the task.** Tasks inherit it through their parent.
- **A stage waits for its phase.** A type of deliverable may list stages, each with the phase from which it exists. A stage becomes a milestone when its deliverable enters that phase, so that no milestone is created during exploration. The milestone is named after the deliverable and the stage, and takes the predictability of the stage, or else that of the type.
- **A deadline can force a phase.** An [imposed deadline](deadline.md) on a deliverable still in exploration is a risk that the [feasibility test](../processes/imposed-deadlines.md) reports, since no estimate of the remaining work exists.

The phases derive from accounts of [research practice](../../references/research-phases.md) and agree with the [frameworks of structural uncertainty](../../references/portfolio-and-phase-frameworks.md) of other domains.
