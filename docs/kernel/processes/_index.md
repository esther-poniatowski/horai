---
tags:
  - index
index: "[Kernel](docs/kernel/_index.md)"
aliases:
  - Processes of the kernel
---
# Processes

Defines the rules that govern the objects of a plan. Each process answers one or several [control questions](../foundations/control-questions.md).

## Allocation, commitment and ordering

- [Allocation of capacity](capacity-allocation.md): divides the week among the streams before any task is selected, in the form that each regime requires
- [Planning across horizons](planning-horizons.md): links the plans of the strategic horizon, the cycle, the week and the day
- [Selection of the next task](task-selection.md): fixes the rule by which the next task follows from the plan

## Termination and adaptation

- [Control of uncertainty](uncertainty-control.md): justifies budgets and checkpoints from the distribution of durations
- [Feedback](feedback.md): tunes the parameters of the method from a small set of metrics and a periodic note

## Means and ends

- [Enablement](enablement.md): bounds the work on means by the results that consume them

## Coordination

- [Reactive work](reactive-work.md): bounds the unplanned requests by a reserve, classes of service and windows
- [External coordination](external-coordination.md): makes the waits on external parties explicit, and orders the acts that start them
- [Protection of imposed deadlines](imposed-deadlines.md): tests the feasibility of a date fixed from outside, and orders the adjustments when it fails
