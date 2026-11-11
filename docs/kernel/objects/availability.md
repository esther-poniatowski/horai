---
tags:
  - definition
index: "[Objects](docs/kernel/objects/_index.md)"
aliases:
  - Availability
  - Capacity of the agent
  - Plannable capacity
---
# Availability

> [!QUESTION] Goal: how much time does the agent have, how predictably, and in which blocks, so that capacity is not assumed constant and contiguous?

The **availability** of the agent describes its working time by four features, which a profile states and the logs estimate. ^availability

| Feature | Statement | Effect |
| --- | --- | --- |
| Amount | the weekly capacity, as a distribution: its median and a low quantile | the feasibility test uses the low quantile |
| Predictability | whether the time of next week is known at the weekly review | an unpredictable week is planned on its low quantile |
| Minimum block | the shortest contiguous block that the agent can usually count on | bounds the length of a [theme](horizon.md#^theme) |
| Energy profile | the hours at which demanding work succeeds | places the themes of the streams that need it |

## Plannable capacity

The **plannable capacity** of a week is the available time minus the blocks of the regime [`committed`](regime.md#^regimes). The [allocation of capacity](../processes/capacity-allocation.md) divides the plannable capacity, and not the whole time. ^plannable-capacity

## Fragmented time

When the minimum block is shorter than a half-day, themes are replaced by **slots**: blocks of the available length, each assigned to one stream. The rule of no change of stream within a slot holds, and the work of a theme that needs a long block, such as a proof or a draft, is scheduled in the rare long blocks first. ^slots

> [!NOTE]
> Fragmented availability raises the cost of each switch. The method does not remove that cost: it states it, so that the allocation is set on the time that is usable and not on the nominal time.
