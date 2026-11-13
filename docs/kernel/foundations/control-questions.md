---
tags:
  - theory
index: "[Foundations](docs/kernel/foundations/_index.md)"
aliases:
  - Control questions
  - Control functions
---
# Control questions

> [!QUESTION] Goal: which questions must any solution of the problem answer, and which mechanism of the kernel answers each?

The [root question](overview.md#^root-question) divides into nine control questions. A system that leaves one of them without a stated rule answers it by default, usually by the order of arrival. ^nine-questions

| Function | Question | Mechanism of the kernel |
| --- | --- | --- |
| Classification | of which kind is this work? | [role, stream](../objects/stream.md) and [regime](../objects/regime.md); [phase](../objects/phase.md); [class of variance](../objects/appetite.md#^variance-classes) |
| Admission | which deliverables are active, which start, and which are stopped? | the strategic review of the [planning process](../processes/planning-horizons.md#^admission), under the limit `active_deliverables_max` |
| Allocation | how much capacity does each kind receive? | [allocation of capacity](../processes/capacity-allocation.md) |
| Placement | when, within the week, does each kind receive its capacity? | [blocks and windows](../objects/horizon.md#^block), under the [availability](../objects/availability.md) of the agent |
| Commitment | which subset is promised, for which horizon, and to whom? | [commitment states](../objects/commitment-state.md), [planning across horizons](../processes/planning-horizons.md), [deadlines](../objects/deadline.md) |
| Ordering | which item comes next? | [selection rule](../processes/task-selection.md) |
| Termination | when does a piece of work stop? | [appetite and checkpoint](../objects/appetite.md), [control of uncertainty](../processes/uncertainty-control.md) |
| Coordination | on whom does the work wait, and who waits on it? | [external parties](../objects/external-party.md), [coordination](../processes/external-coordination.md), [reactive work](../processes/reactive-work.md) |
| Adaptation | how are the estimates and the policies revised? | [feedback](../processes/feedback.md) |

The task inventory of the [diagnosis](diagnosis.md) answers the first question in part, by tags, and none of the others.

## Order of the answers

The questions are answered in the order of the table, and each answer bounds the next:

- admission precedes allocation, so that capacity is divided among few deliverables;
- allocation and placement precede ordering, so that tasks are compared only within one stream and one block;
- commitment precedes ordering, so that the candidates of a selection are few;
- termination is fixed before the work starts, so that it does not depend on the state of mind of the agent at the moment of the overrun.
