---
tags:
  - decision
status: accepted
created: 2026-11-12
index: "[Architecture decisions](docs/adr/_index.md)"
aliases:
  - Kernel with research first
  - Scope of the software
---
# Kernel with research first

> [!QUESTION] Goal: for which agents is `horai` built first, given that the method is stated as a general kernel configured by domain profiles?

The documentation states a kernel for any agent who allocates its own time across several kinds of work and several horizons, and five profiles that configure it.

## Decision

The software implements the kernel and its mechanism of profiles, and builds and tests only the [research profile](../profiles/research.md) at first. The other profiles keep the status of proposals until a user of their domain exists.

## Constraints that decide the scope

- **A researcher must use the tool soon.** Testing five profiles delays the first delivery.
- **The three layers are already separated.** Hard-coding the research domain would discard the [three-layer architecture](three-layer-architecture.md), which costs little to keep.

## Options weighed

- **Research only, hard-coded.** Rejected: it abandons the separation of the kernel from the values of a domain.
- **All five profiles from the start.** Rejected for the first constraint.

## Consequences

- The code reads the research profile as one profile among possible others, and names no research term in the kernel.
- The tests of the other profiles are deferred, and no claim about those domains is made from use.
