---
tags:
  - decision
status: accepted
created: 2026-11-14
index: "[Architecture decisions](docs/adr/_index.md)"
aliases:
  - Energy of a stream
  - Overrun by bounds
  - Appointments in any stream
---
# Properties apart from the trigger

> [!QUESTION] Goal: which properties decide the check of energy, the protection from overrun and the streams of the appointments, so that each rule follows the work that it governs?

The decision on [streams, allocation and loose tasks](streams-allocation-and-loose-tasks.md) removed the control of the trigger over the allocation. A review of the framework then found three other rules that still read the trigger. Only the blocks of streams triggered by selection were checked against the hours of high energy, so a demanding stream triggered by the calendar, such as the derivation of mathematics, was never checked. The overrun rule protected the streams triggered by the calendar, whereas a minimum is what needs protection. An appointment could name only a stream triggered by appointment, so the days of a conference could not sit in the stream of the conferences.

## Decision

- **Energy.** A stream may state `needs_high_energy: true`. The check reports each block of such a stream that lies outside the hours of high energy of the profile, whatever triggers the stream.
- **Overrun.** A block may extend into the next block only when the next block belongs to the same stream, or to a stream without a minimum while the extending stream has one. No block extends into the block of a stream with a minimum, bounded `at_least` or `exact`.
- **Appointments.** An appointment names any stream of the profile, and a task of any stream may prepare it. A reserve per event may belong to any stream, and the appointments named in its `events` must exist.
- **Trigger.** The trigger states what prompts the work, and suggests an allocation. It still decides that the request windows hold the reserve of a stream triggered by arrival, a rule that a later decision on the request windows may revise.

## Constraints that decide the rules

- **A property belongs to the object whose variation it follows.** The need for energy varies with the work of a stream, and the protection of a block with the minimum of its stream. Neither varies with what prompts the work.
- **A stream is a domain of work.** Each time that a party fixes belongs to the stream of its domain, so a restriction of appointments to one trigger would require a duplicate stream for each domain.

## Options weighed

- **The need for energy per task.** Rejected: each demanding task must then be marked, and the selection gains a key, while one stream rarely mixes demanding and light work in proportions that the blocks cannot follow.
- **No energy check.** Rejected: the hours of high energy would then constrain nothing.

## Consequences

- The profile schema gains the field `needs_high_energy`, and its description of the trigger no longer claims to fix the allocation.
- The check of energy reads the new field; the checks of appointments, of preparations and of reserves per event no longer read the trigger.
- The kernel notes on the [allocation of capacity](../kernel/processes/capacity-allocation.md) state the overrun rule by bounds.
