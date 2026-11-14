---
tags:
  - definition
index: "[Objects](docs/kernel/objects/_index.md)"
aliases:
  - Trigger
  - Trigger of a stream
  - Regime
  - Scheduling regime
---
# Trigger

> [!QUESTION] Goal: what triggers the work of a stream, and which allocation does the stream usually receive?

The **trigger** of a [stream](stream.md) states what prompts its work and the event that closes a piece of work, and suggests the allocation that the stream usually receives. Six triggers are distinguished, each a value of the field `triggered_by`. ^regimes

| Triggered by | What prompts the work | Usual allocation | Closed by |
| --- | --- | --- | --- |
| `selection` | selection at a planning session | an exact share | the definition of done, or a [checkpoint](appetite.md#^checkpoint) |
| `demand` | the demand of a result that consumes its output | a share at most, or a charge to the consumer | the consumer unblocked |
| `calendar` | a recurring position in the calendar | a share at least, protected by its position; a reserve per week for the planning acts | the end of the session, with an artifact |
| `accumulation` | the accumulation of small items | none: positions of low energy, and the cool-down | the batch emptied |
| `arrival` | an arrival from an [external party](external-party.md) | a reserve per day or per week, under a level of service | the response |
| `appointment` | a block of time fixed by a party: an event at a fixed date, or time that the party has bought, rostered or is owed | none for the appointments, which are removed from the plannable capacity; a reserve per event, at most, for the preparation of each appointment that a task prepares | the end of the block |

The trigger suggests the allocation and does not fix it. A profile may state another allocation, and `check` rejects only an incoherent one, such as a share stated as a duration, or a reserve per event whose `events` name no appointment, as the [allocation of capacity](../processes/capacity-allocation.md#^forms) states.

## Usual pairings

The trigger is independent of what the stream yields, and a profile declares the pairing. The usual ones are: ^usual-pairings

| Yields | Usual trigger | Other triggers met |
| --- | --- | --- |
| `results` | `selection` | `arrival`, where results are delivered on request; `appointment`, where time is sold |
| `means` | `demand` | — |
| `knowledge` | `calendar` | — |
| `competence` | `calendar` | — |
| `network` | `accumulation` | `appointment`, for the events where people meet |
| `coordination` | `appointment` | `arrival`, for requests and correspondence |
| `organization` | `calendar` | — |
| `integrity` | `accumulation` | `arrival`, for incidents |
| `obligation` | `appointment` | `accumulation`, `arrival` |

## Opposed triggers

- **Calendar and arrival.** A minimum protects work that no event other than its position in the calendar triggers, and a reserve bounds work that every arrival triggers.
- **Selection and appointment.** A share is a part of the time that the agent allocates, and the block of an appointment is time that a party has fixed. The shares apply to the capacity that remains once the appointments and the reserves are removed, as the [allocation of capacity](../processes/capacity-allocation.md) states.
