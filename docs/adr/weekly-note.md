---
tags:
  - decision
status: superseded
created: 2026-11-11
index: "[Architecture decisions](docs/adr/_index.md)"
aliases:
  - Weekly note in place of a milestone invariant
---
# Weekly note in place of a milestone invariant

> [!QUESTION] Goal: how is the progress of a week attested, without a target that can be met by redefining the work?

> [!WARNING] Superseded
> The [ratified ontology](ratified-ontology.md) replaces the weekly note by a weekly report computed from the decision entries.

The first statement of the method required that each week close or measurably advance one milestone of a project.

## Decision

Each week ends with a [weekly note](../kernel/processes/feedback.md) that states what was learned or ruled out on each active project, and the supervisor reads it.

## Constraints that decide the form

- **A count of milestones can be gamed.** Slicing a milestone meets the invariant without any progress, and a budget ratio invites padded budgets.
- **Exploration closes no milestone.** A week that rules out an approach is productive, and the invariant would report it as empty.

## Options weighed

- **Milestone invariant.** Rejected for both constraints.
- **No weekly attestation.** Rejected: the drift toward tool work was invisible for want of one.

## Consequences

- The weekly review has a step of writing.
- The metrics number two, and neither is a target.
