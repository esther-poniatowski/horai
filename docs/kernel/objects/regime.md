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

The **regime** of a [stream](stream.md) states the trigger of its work, the form of its capacity, and the event that closes a piece of work. Six regimes are distinguished. ^regimes

| Regime | Trigger | Form of capacity | Closed by |
| --- | --- | --- | --- |
| `planned` | selection at a planning session | a share | the definition of done, or a [checkpoint](appetite.md#^checkpoint) |
| `pulled` | the demand of a result that consumes its output | a ceiling, or a charge to the consumer | the consumer unblocked |
| `floor` | a recurring position in the calendar | a protected minimum | the end of the session, with an artifact |
| `batched` | the accumulation of small items | slots of low energy, and the cool-down | the batch emptied |
| `reactive` | an arrival from an [external party](external-party.md) | a reserve, under a level of service | the response |
| `appointed` | a block of time fixed by a party: an event at a fixed date, or time that the party has bought, rostered or is owed | the blocks, removed from the plannable capacity; a share for their preparation, and optionally a cap per appointment, which the profile states for the stream and an appointment may override | the end of the block |

## Usual pairings

The regime is independent of the role, and a profile declares the pairing. The usual ones are: ^usual-pairings

| Role | Usual regime | Other regimes met |
| --- | --- | --- |
| Production | `planned` | `reactive`, where results are delivered on demand; `appointed`, where time is sold |
| Tooling | `pulled` | — |
| Survey | `floor` | — |
| Training | `floor` | — |
| Exchange | `appointed` | `reactive`, for requests and correspondence |
| Upkeep | `batched` | `reactive`, for incidents |
| Duty | `appointed` | `batched`, `reactive` |

## Opposed regimes

- **Floor and reactive.** A floor protects work that nothing triggers, and a reserve bounds work that everything triggers.
- **Planned and appointed.** A share is a part of the time that the agent allocates, and an appointed block is time that a party has fixed. The shares apply to the capacity that remains once the appointed blocks are removed, as the [allocation of capacity](../processes/capacity-allocation.md) states.
