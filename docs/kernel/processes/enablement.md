---
tags:
  - theory
index: "[Processes](docs/kernel/processes/_index.md)"
aliases:
  - Enablement
  - Pull rule
  - Constraint logic
---
# Enablement

> [!QUESTION] Goal: how is the work on means bounded, so that it serves the results without absorbing them?

A milestone depends on an [artifact, not on its generator](../objects/dependency.md#^artifact-dependency). Five rules follow for the streams of the role enablement.

1. **Pull rule.** No task of enablement exists without a named milestone that consumes its output. The task is done when that milestone is unblocked, not when the means is complete. ^pull-rule
2. **Manual first.** The artifact is first produced by hand, by a means made for the occasion, or obtained from outside. A durable means is justified at the recurrence `recurrence_threshold`. ^manual-first
3. **Thin slice.** The work implements the smallest end-to-end path that serves the consumer. Generalizations go to the register of debt, a [standing parent](../objects/work-hierarchy.md#^standing-parent) processed in the cool-down.
4. **Constraint rule.** A means that blocks a milestone of the cycle is the constraint of the system: it is driven without interruption to a thin slice, under a fixed [appetite](../objects/appetite.md) charged to the consuming milestone. The ceiling of the stream applies only to the work that blocks nothing. ^constraint-rule
5. **No overrun outward.** An enablement theme never extends into the theme of another stream, as the [rule of overrun](capacity-allocation.md#^overrun) states. This closes the route by which work on means absorbed whole days.

## Limits of the rules

- **Means that are results.** The rules do not apply to a means that is delivered and valued for itself, which [belongs to production](../objects/stream.md#^means-as-result).
- **Delegation changes the costs.** When the building of a means is delegated, to an automated agent or to an [external party](../objects/external-party.md), building is cheap and the scarce resources are verification and maintenance. The recurrence test therefore weighs the cost of maintaining the means, and the time of verification is [logged](feedback.md#^verification-time).
- **Make or obtain.** Where the [value](../objects/value.md) is quantified, the cost of building is compared with the cost of obtaining the means from outside.
- **Recurrent requests pull enablement.** A reactive request that recurs is a consumer in the sense of the pull rule, as the process of [reactive work](reactive-work.md) states.

The rules derive from [Lean pull](../../references/kanban-and-lean-pull.md) and from the [theory of constraints](../../references/critical-path-and-constraints.md). The decision on [constraint logic](../../adr/enablement-constraint-logic.md) records why a flat ceiling was rejected. The steps are given in the [procedure for an enablement request](../../procedures/enablement-request.md).
