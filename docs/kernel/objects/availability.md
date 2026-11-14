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

> [!QUESTION] Goal: how much time does the agent have, how predictably, and in which spans, so that capacity is not assumed constant and contiguous?

The **availability** of the agent describes its working time by four features. The [profile record](../../specification/profile-record.md) states the energy hours, which follow the agent; the [typical week record](../../specification/typical-week-record.md) states the other features, which follow its situation; and the logs estimate the amount. ^availability

| Feature | Statement | Effect |
| --- | --- | --- |
| Amount | the weekly capacity, as a distribution: its median and a low quantile | the feasibility test uses the low quantile |
| Predictability | whether the time of next week is known at the weekly review | an unpredictable week is planned on its low quantile |
| Minimum block | the shortest contiguous span of time that the agent can usually count on | bounds the length of a [block](horizon.md#^block) |
| Energy hours | the hours of high energy, at which demanding work succeeds, for every day or per weekday | places the blocks of the streams that need it |

## Plannable capacity

The **plannable capacity** of a week is the available time less the appointments and less the reserves. The appointments are the times that others fix, in any stream: the recurring ones, the ones without a fixed slot, which the typical week lists as unplaced, and the ones of one date. The reserves are the durations that the allocations of the streams state. A reserve per event counts as the budget of each task that prepares an appointment of the week. The shares of the [allocation of capacity](../processes/capacity-allocation.md) divide the plannable capacity, and not the whole time. The plannable capacity of a cycle is that of its weeks, less the reserves per cycle. ^plannable-capacity

## Fragmented time

When the minimum block is shorter than `block_length`, blocks are replaced by **slots**: spans of the available length, each assigned to one stream. The rule of no change of stream within a slot holds, and work that needs a long span, such as a proof or a draft, is scheduled in the rare long spans first. ^slots

> [!NOTE]
> Fragmented availability raises the cost of each switch. The method does not remove that cost: it states it, so that the allocation is set on the time that is usable and not on the nominal time.
