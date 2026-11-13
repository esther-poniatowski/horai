---
tags:
  - theory
index: "[Foundations](docs/kernel/foundations/_index.md)"
aliases:
  - Dimensions
  - Dimensions of the problem
---
# Dimensions

> [!QUESTION] Goal: along which dimensions are the problem and its solution structured, and which values does each dimension admit?

Each dimension is represented by one object of the kernel. A [profile](../../profiles/_index.md) names or selects its values, and never adds a dimension. ^dimensions

## Dimensions of the work

| Dimension | What varies | Values in the kernel | Object | Related frameworks |
| --- | --- | --- | --- | --- |
| Role | the relation of the work to the value produced | production · tooling · survey · training · exchange · upkeep · duty | [stream](../objects/stream.md) | [strategic buckets](../../references/portfolio-and-phase-frameworks.md) |
| Regime | what triggers the work, and the form of its capacity | planned · pulled · floor · appointed · batched · reactive | [regime](../objects/regime.md) | [classes of service](../../references/queueing-and-reactive-work.md) |
| Level | the grain of a result | purpose · deliverable · milestone or question · task | [hierarchy of work](../objects/work-hierarchy.md) | work breakdown |
| Structural uncertainty | what is known of the ends and of the means | exploration · validation · delivery | [phase](../objects/phase.md) | [Cynefin, double diamond](../../references/portfolio-and-phase-frameworks.md) |
| Parametric uncertainty | the variance of a duration | routine · exploratory | [appetite](../objects/appetite.md) | [reference classes](../../references/duration-distributions.md) |
| Commensurability | whether worths can be compared in a unit | ordinal · quantified | [value](../objects/value.md) | [cost of delay](../../references/cost-of-delay.md) |

## Dimensions of the agent and of its relations

| Dimension | What varies | Values in the kernel | Object |
| --- | --- | --- | --- |
| Availability | the amount, the predictability and the contiguity of the time of the agent | a distribution of weekly capacity, a minimum block, an energy profile | [availability](../objects/availability.md) |
| Locus of action | who performs the next act | the agent · an external party | [external party](../objects/external-party.md) |
| Authority | what the agent can ask of others | none · delegates | the relation [`delegates`](../objects/external-party.md#^relations) |
| Principals | to whom the agent answers | none · one · several | [principal](../objects/external-party.md#^principal) |
| Origin of a commitment | who fixes a promise of result and its date | chosen · imposed · request | [commitment state](../objects/commitment-state.md), [deadline](../objects/deadline.md) |
| Origin of capacity | who fixes the use of a block of time | the agent · a party, which fixes, buys or rosters it | the regime [`appointed`](../objects/regime.md#^regimes) |
| Time scale | the span of a plan | strategic · cycle · week · day · block | [horizon](../objects/horizon.md) |

## Independence of the dimensions

- **Role and regime are independent.** A stream of the role production can be planned in one domain and reactive in another, as the [regimes](../objects/regime.md) state.
- **The two uncertainties are independent.** The phase is borne by a deliverable, and the class of variance by an item: a delivery phase contains exploratory items, and conversely.
- **Level and time scale are distinct.** The level is the grain of a result, and the time scale is the span of a plan. A milestone of one deliverable may span one week or three cycles.
- **The two origins are distinct.** An imposed commitment fixes a result and its date, and leaves the time of the work to the agent. An appointed block fixes the time, and may fix no result.

## Rules that are not dimensions

The dependence of a milestone on an artifact rather than on its generator is a rule, stated by the fourth [commitment](commitments.md#^c-pull) and by the note on [dependency](../objects/dependency.md#^artifact-dependency). It does not vary across instances, and is therefore not a dimension.
