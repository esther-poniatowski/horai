---
tags:
  - procedure
index: "[Procedures](docs/procedures/_index.md)"
aliases:
  - Strategic review
---
# Strategic review

> [!QUESTION] Goal: which deliverables are active, and which policies hold, for the coming cycles, within `ritual_durations.strategic_review`?

The review is held in a cool-down, before the [cycle planning](cycle-planning.md), when the task `strategic-review` of the stream of planning reopens. Its rule of recurrence fixes the cadence, `P2C` by default: every two cycles.

1. **Purposes.** Confirm each purpose and its deadline. Retire a purpose that no longer guides the work.
2. **Close.** Mark as done each deliverable that was delivered. Stop each deliverable whose phase has not advanced over `stall_cycles` cycles without a recorded reason, or whose deadlines no [adjustment](../kernel/objects/deadline.md#^adjustment-order) can meet.
3. **Policies.** Read the deviation entries logged since the last review. For each, either protect the policy, or change it in the profile with its reason. A policy is never changed to match the logs, as the [two kinds of revision](../kernel/processes/feedback.md#^two-revisions) state.
4. **Situation.** When the situation of the agent has changed, such as a teaching semester or a new recurring appointment, rewrite the typical week and the allocations together, and run `horai check`.
5. **Ideas.** Read the [ideas file](../kernel/objects/work-hierarchy.md#^ideas-file), and mark the ideas ready to become deliverables. No idea is archived.
6. **Admission.** Admit deliverables, from those awaiting admission and the ready ideas, while a place is free under `active_deliverables_max` and the [deadline feasibility](deadline-feasibility.md) passes with every deadline, as the rule of [admission](../kernel/processes/planning-horizons.md#^admission) states. A deliverable derived from another shares the place of its source. Give each admitted deliverable its phase and its deadlines.
7. **Record.** Complete the task `strategic-review`, which reopens when its rule of recurrence counts enough cycles.

> [!NOTE]
> Without the option of imposed deadlines, step 6 tests no deadline, and step 2 stops a deliverable on its phase alone.
