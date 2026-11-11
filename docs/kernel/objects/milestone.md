---
tags:
  - definition
index: "[Objects](docs/kernel/objects/_index.md)"
aliases:
  - Milestone
  - Definition of done
---
# Milestone

> [!QUESTION] Goal: which object carries the budget and the dependencies of a piece of work, at a grain where a roadmap is legible?

A **milestone** is a verifiable result, stated with the test by which its completion is judged. ^milestone

- **Definition of done.** The test is written before the work starts, and names an observable state. When the result is handed to an [external party](external-party.md), the test is the acceptance by that party. ^definition-of-done
- **Grain.** A deliverable in a structured [phase](phase.md) holds `milestones_open` open milestones, so that the [graph](dependency.md#^milestone-graph) of all active deliverables stays within a few tens of nodes.
- **Unit of worth.** A milestone is the smallest item whose completion stops a cost of delay or delivers a value. The worth of a result is therefore stated, and compared, at the milestone and not at the task, as the [selection rule](../processes/task-selection.md#^valuation-key) states.
- **Carried attributes.** A milestone carries its stream, its budget, its class of variance, the time consumed, its dependencies, its consumers, and where they apply its [deadline](deadline.md), its rank or its [value](value.md), as the [milestone record](../../specification/milestone-record.md) documents.

> [!WARNING] Milestones in exploration
> A milestone presupposes that the result can be named in advance. During exploration this presupposition fails, and the unit of planning is a time-boxed question, as the [phases](phase.md) state.
