---
tags:
  - decision
status: accepted
created: 2026-11-11
index: "[Architecture decisions](docs/adr/_index.md)"
aliases:
  - Additional dimensions
  - Availability, delegation, principals and duty
---
# Additional dimensions

> [!QUESTION] Goal: which features of the agent and of its relations must the kernel represent, beyond those of its work, to cover the domains that the second review tested?

The second review found that the kernel assumed a constant and contiguous capacity, one principal, an agent who delegates nothing, time wholly at the disposal of the agent, and no obligation outside its purposes. A clinician on a rota, a researcher who teaches, a carer with fragmented time, a consultant who sells days and a researcher who hands work to automated agents each broke one assumption.

## Decision

The kernel adds:

- the object [availability](../kernel/objects/availability.md), with the amount, the predictability, the minimum block and the energy profile of the time of the agent;
- the regime [`committed`](../kernel/objects/regime.md#^regimes), for time sold, rostered or owed, removed from the plannable capacity;
- the role [duty](../kernel/objects/stream.md#^roles), for obligations owed to an affiliation, with a rule of exclusivity between roles;
- the relation [`delegates`](../kernel/objects/external-party.md#^relations), with a brief and a review, and a [principal per deliverable](../kernel/objects/external-party.md#^principal);
- two [control questions](../kernel/foundations/control-questions.md): admission and placement;
- two conditions of membership turned into modulators: endogenous means and structural uncertainty.

## Constraints that decide the additions

- **Each addition was required by a tested domain,** as the [comparison of instances](../profiles/comparison.md) records.
- **One agent remains the subject.** The direction of a team stays outside: delegation is handled as an external dependency that the agent verifies, and the allocation of the work of others is not planned.

## Options weighed

- **Duty as a kind of interface.** Rejected: interface work serves the purposes of the agent, and duty does not, so a single stream would misreport the allocation.
- **Committed time as a calendar regime.** Rejected: a calendar regime caps preparation for an event, whereas committed time is a block given away, which must be removed before the shares are applied.

## Consequences

- The profile record states the availability, the options and the overrides of the policies.
- The dimension "means and ends" is removed from the table of dimensions, since it is a rule and not a varying feature.
