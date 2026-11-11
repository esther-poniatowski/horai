---
tags:
  - procedure
index: "[Procedures](docs/procedures/_index.md)"
aliases:
  - Cycle planning
---
# Cycle planning

> [!QUESTION] Goal: how are the milestones and the questions of a cycle selected, and how are their budgets assigned?

The session lasts 60 minutes by default and takes place in the cool-down.

1. **Close.** For each milestone of the ending cycle, record its outcome entry. Let the tool recompute the [estimates](../kernel/foundations/parameters.md#^parameter-kinds).
2. **Phases.** Confirm or change the [phase](../kernel/objects/phase.md) of each active deliverable, and record each transition with its reason.
3. **Select.** Choose up to `milestones_per_cycle` milestones per deliverable in a structured phase, whose dependencies are done or will be within the cycle. Choose the questions of each deliverable in exploration.
4. **Classify.** Assign each selected item its [class of variance](../kernel/objects/appetite.md#^variance-classes), by threshold where the calibration is on.
5. **Budget.** Give an estimate to each `routine` item, corrected by the median ratio of its class, and an appetite to each `exploratory` item. Where the valuation is quantified, state the value and the cost of delay of each milestone; otherwise rank the milestones of each stream.
6. **Feasibility.** Run the [deadline feasibility](deadline-feasibility.md) on all deadlines of the plan, with the budgets of step 5 included, and apply its adjustments.
7. **Fit.** Sum the budgets by stream and compare them with the capacity of the cycle in the [calendar record](../specification/calendar-record.md). Remove items until the sum fits.
8. **Pull.** For each selected milestone, list the artifacts that it needs. Open an [enablement request](enablement-request.md) for each artifact that no existing means produces, and an [external request](external-request.md) for each artifact that a party supplies.
9. **Reserve.** Where reactive work is on, read the computed length of the windows, and place them.
10. **Commit.** Set the selected items to the state `cycle`, and prune the holding file of the tasks that `orphan_cycles` cycles have left unselected.
