---
tags:
  - procedure
index: "[Procedures](docs/procedures/_index.md)"
aliases:
  - Cycle planning
---
# Cycle planning

> [!QUESTION] Goal: how are the milestones and the questions of a cycle selected, and how are their budgets assigned?

The session lasts `ritual_durations.cycle_planning` and takes place in the cool-down.

1. **Close.** For each item of the ending cycle, record its decision entry if none is recorded yet: `done` for a completed item, and a [checkpoint decision](checkpoint-decision.md) for an item whose budget was consumed or that remains unfinished. An item carried into the next cycle needs a decision `renew` or `reduce`; without it, its budget keeps counting the time spent in the ending cycle. Let the tool recompute the [estimates](../kernel/foundations/parameters.md#^parameter-kinds).
2. **Phases.** Confirm or change the [phase](../kernel/objects/phase.md) of each active deliverable, and record each transition with its reason. Run `horai stages` to create the milestones of the stages that the deliverables have reached, and state the `done_when` of each.
3. **Select.** List the open items, milestones and questions, with or without a deliverable, whose dependencies are done or will be within the cycle. The phase of each deliverable decides which of its items exist.
4. **Classify.** Assign each selected item its [predictability](../kernel/objects/appetite.md#^variance-classes), by threshold where the calibration is on.
5. **Budget.** Give an estimate to each `routine` item, corrected by the median ratio of the `routine` items of its [class of calibration](../kernel/processes/uncertainty-control.md#^calibration), or three durations whose PERT value is its estimate, and an appetite to each `exploratory` item. Under a cardinal worth, state the value and the cost of delay of each milestone; under an ordinal worth, rank the items of each stream.
6. **Feasibility.** Run the [deadline feasibility](deadline-feasibility.md) on all deadlines of the plan, with the budgets of step 5 included, and apply its adjustments.
7. **Fit.** Sum the budgets by stream and compare them with the capacity of the cycle in the [calendar record](../specification/calendar-record.md). In each stream, remove the lowest-ranked items until the sum fits, never a [non-negotiable](../kernel/foundations/commitments.md#^c-non-negotiable) item. A stream that holds a selected item states an allocation, which `check` verifies.
8. **Pull.** For each selected milestone, list the artifacts that it needs. Open a [tooling request](tooling-request.md) for each artifact that no existing means produces, and an [external request](external-request.md) for each artifact that a party supplies.
9. **Reserve.** Where reactive work is on, read the computed length of the request windows, and place them as blocks of the stream triggered by arrival.
10. **Commit.** Record the cycle on each selected item, so that its tasks enter the [state](../kernel/objects/commitment-state.md#^state-rule) `cycle`. Archive the tasks of the holding file that the [orphan rule](../kernel/objects/work-hierarchy.md#^orphan-rule) designates.
