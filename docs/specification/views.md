---
tags:
  - specification
  - wip
index: "[Specification](docs/specification/_index.md)"
aliases:
  - Views
  - Views of a plan
---
# Views

> [!QUESTION] Goal: which views of a plan are generated, and which question does each answer?

Each view is computed from the records and is never authored. No view displays the backlog. The parts marked with an option appear only when the profile turns it on.

| View | Question answered | Records read | Content |
| --- | --- | --- | --- |
| Roadmap | where does each deliverable stand, and what comes next? | purposes, deliverables, milestones, waits, deadlines | per deliverable, its phase and status; the [milestone graph](../kernel/objects/dependency.md#^milestone-graph) with the successor work and the external dependencies; per milestone of the cycle, the time consumed against the budget; per deadline, its slack, and the buffer consumed against the work done |
| Week | what is committed now, and what is awaited? | tasks in the state `week`, calendar, waits, requests | the tasks grouped by stream, in the order of the [selection rule](../kernel/processes/task-selection.md#^selection-rule), with the marks of the day; the blocks, the windows and the appointed blocks; the follow-ups due; the requests open, by class of service |
| Tooling register | which work on means is pulled, and by what? | milestones of the role tooling, the standing parents of debt | each item with its consumers, and the register of debt |
| Weekly report | what was decided and completed over the week? | decision entries, completed tasks | per deliverable, the decisions of the week with their rationales, and the tasks completed, as the [feedback process](../kernel/processes/feedback.md#^weekly-report) states |

> [!NOTE]
> A view of the backlog is opened only during a planning session. The waits, the requests and the deviations are parts of the week view and not views of their own, so that the number of views stays at four. A further view is added only under the condition that the [feedback process](../kernel/processes/feedback.md) states.
