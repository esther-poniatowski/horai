---
tags:
  - index
index: "[Kernel](docs/kernel/_index.md)"
aliases:
  - Objects of a plan
---
# Objects

Defines the objects that a plan states. Each later note uses the notes listed before it.

## Kinds of work and the time of the agent

- [Stream and yield](stream.md): types each piece of work by what it yields, so that time is allocated before tasks are compared
- [Trigger](regime.md): types each stream by what triggers its work and by the allocation that it usually receives
- [Availability](availability.md): states how much time the agent has, how predictably, and in which spans

## Results and their structure

- [Hierarchy of work](work-hierarchy.md): places each task under the result or the stream that it serves, from the purpose to the task
- [Milestone](milestone.md): defines the verifiable result that carries the budgets and the dependencies
- [Phase](phase.md): tells exploration from validation and from delivery, since each is planned differently
- [Dependency](dependency.md): states on what a milestone depends, and why that is an artifact and not its generator
- [External party](external-party.md): defines the persons outside the agent on whom the work waits, who wait on it, or to whom the agent delegates

## Promises, time and value

- [Commitment state](commitment-state.md): separates a recorded task from a task committed for a horizon
- [Deadline](deadline.md): defines a date that the agent cannot move alone, and the margin that protects it
- [Appetite](appetite.md): fixes the time that a piece of work is worth, according to its predictability
- [Value](value.md): states on which scale the worth of a result is stated, and what a cost of delay measures
- [Horizon](horizon.md): defines the nested time scales at which plans are stated
