---
tags:
  - definition
index: "[Objects](docs/kernel/objects/_index.md)"
aliases:
  - Regime
  - Scheduling regime
---
# Regime

> [!QUESTION] Goal: what triggers the work of a stream, and in which form does the stream receive its capacity?

The **regime** of a [stream](stream.md) states the trigger of its work, the form of its capacity, and the event that closes a piece of work. Seven regimes are distinguished. ^regimes

| Regime | Trigger | Form of capacity | Closed by |
| --- | --- | --- | --- |
| `planned` | selection at a planning session | a share | the definition of done, or a [checkpoint](appetite.md#^checkpoint) |
| `pulled` | the demand of a result that consumes its output | a ceiling, or a charge to the consumer | the consumer unblocked |
| `floor` | a recurring position in the calendar | a protected minimum | the end of the session, with an artifact |
| `calendar` | an external event at a fixed date | a cap on the preparation | the event |
| `batched` | the accumulation of small items | slots of low energy, and the cool-down | the batch emptied |
| `reactive` | an arrival from an [external party](external-party.md) | a reserve, under a level of service | the response |
| `committed` | a block of time that a party has bought, rostered or is owed | blocks fixed in the calendar, removed from the plannable capacity | the end of the block |

## Usual pairings

The regime is independent of the role, and a profile declares the pairing. The usual ones are: ^usual-pairings

| Role | Usual regime | Other regimes met |
| --- | --- | --- |
| Production | `planned` | `reactive`, where results are delivered on demand; `committed`, where time is sold |
| Enablement | `pulled` | — |
| Sensing | `floor` | — |
| Capability | `floor` | — |
| Interface | `calendar` | `reactive`, for requests and correspondence |
| Upkeep | `batched` | `reactive`, for incidents |
| Duty | `committed` | `calendar`, `batched`, `reactive` |

## Opposed regimes

- **Floor and reactive.** A floor protects work that nothing triggers, and a reserve bounds work that everything triggers.
- **Planned and committed.** A share is a part of the time that the agent allocates, and a committed block is time that the agent has already given away. The shares apply to the capacity that remains once the committed blocks are removed, as the [allocation of capacity](../processes/capacity-allocation.md) states.
