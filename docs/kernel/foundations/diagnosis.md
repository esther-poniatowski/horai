---
tags:
  - theory
index: "[Foundations](docs/kernel/foundations/_index.md)"
aliases:
  - Diagnosis of a task inventory
  - Storage layer and control system
---
# Diagnosis of a task inventory

> [!QUESTION] Goal: why does a centralized list of tasks, with identifiers, priorities, dates and dependencies, neither select the next task nor allocate attention?

A task inventory is a storage layer and not a control system: it records what could be done, and states no rule that decides what is done now, for how long, and when to stop. ^storage-not-control

Five structural defects follow. ^defects

| Defect | Mechanism | Symptom |
| --- | --- | --- |
| Inventory and commitment are conflated | every recorded task competes permanently for attention | priorities and due dates inflate until many tasks are urgent and high |
| Dependencies sit at the grain of the task | the graph has hundreds of nodes, spread over local items | the structure of the work stays implicit, and no roadmap can be read |
| Heterogeneous work is ranked on one scale | work whose payoff is deferred loses every comparison | the training and the knowledge of the environment decay |
| Arrivals and plans share one list | each request competes with the planned work at the moment it arrives | the plan is displaced by whatever arrived last |
| Waits are invisible | an item that awaits another party looks like an item that awaits the agent | the item is forgotten, or occupies attention to no effect |

Each defect is corrected by one part of the kernel:

- the [commitment states](../objects/commitment-state.md) separate what is recorded from what is committed for a horizon;
- the [milestone](../objects/milestone.md) carries the dependencies, at a grain where a graph is legible;
- the [streams](../objects/stream.md) receive their time by [allocation](../processes/capacity-allocation.md), so that no task of one stream is compared with a task of another;
- the process of [reactive work](../processes/reactive-work.md) gives arrivals a reserve and request windows of their own;
- the [waiting condition](../objects/external-party.md#^waiting) removes an item from the candidates and replaces it by a dated follow-up.
