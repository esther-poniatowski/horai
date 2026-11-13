---
tags:
  - decision
status: proposed
created: 2026-11-11
index: "[Architecture decisions](docs/adr/_index.md)"
aliases:
  - Three-layer architecture
---
# Three-layer architecture

> [!QUESTION] Goal: how is the general method separated from what belongs to one domain, so that `horai` is reusable beyond research?

The method was first stated for doctoral research. Its rules depend on the structure of a [class of problems](../kernel/foundations/problem-class.md), and research entered only through a vocabulary, default values and two processes.

## Decision

The method is stated in three [layers](../kernel/foundations/layers.md#^layers): a kernel without the vocabulary of a domain, a profile that declares the values of one domain, and modules that hold the processes of one role in some domains.

## Constraints that decide the layers

- **Reuse.** `horai` is an open resource, and a method stated in the terms of research cannot be adopted elsewhere without being rewritten.
- **The six roles recur.** The [comparison of instances](../profiles/comparison.md) finds the same roles of work in five domains, with different regimes, capacities and modulators.
- **Values and rules differ in their grounds.** A rule follows from a commitment, and a value is a default that the logs revise. Mixing them hides which statements are open to tuning.

## Options weighed

- **One method per domain.** Rejected: the rules would be duplicated and would drift apart.
- **Kernel and profile only.** Rejected: a process such as the reading of a literature is neither a general rule nor a value.
- **A kernel with user-defined rules.** Rejected: a profile that adds rules can contradict a commitment, so a profile only selects values and turns extensions on.

## Consequences

- No note of the kernel uses a term of a domain, except in an example marked as such.
- A [profile record](../specification/profile-record.md) is the only place where a domain is configured.
- Only the research profile is tested. The other profiles are sketches, and the generality of the kernel is conceptual until one of them is used.
