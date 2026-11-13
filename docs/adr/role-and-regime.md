---
tags:
  - decision
status: proposed
created: 2026-11-11
index: "[Architecture decisions](docs/adr/_index.md)"
aliases:
  - Role and regime as independent dimensions
---
# Role and regime as independent dimensions

> [!QUESTION] Goal: how is a kind of work typed, once the same kind can be planned in one domain and arrive on demand in another?

In the research instance, each stream had one fixed regime, so the stream alone typed the work. The addition of reactive work raised the question of whether it is a seventh kind of work.

## Decision

A stream is typed on two independent dimensions: its [role](../kernel/objects/stream.md#^roles), which states its relation to value, and its [regime](../kernel/objects/regime.md#^regimes), which states its trigger and the form of its capacity. Reactive work is a regime and not a role.

## Constraints that decide the typing

- **Requests have no single relation to value.** The support of a customer is an interface, an incident is upkeep, and a client request under contract is production. Their common feature is the arrival, which is a matter of regime.
- **The form of capacity follows the trigger.** A share, a floor and a reserve are different objects, and each belongs to one regime whatever the role.

## Options weighed

- **A seventh role of response.** Rejected for the first constraint.
- **Regime fixed by role.** Rejected: it holds in research and fails in the profiles where production is delivered on demand.

## Consequences

- A profile declares the pairing of each stream, and the kernel states the [usual pairings](../kernel/objects/regime.md#^usual-pairings).
- The rules of allocation are stated per regime, and the rules of worth per role.
- The second review added the role duty and the regime `committed`, as the decision on the [additional dimensions](additional-dimensions.md) records. Neither changes the independence of the two dimensions.
