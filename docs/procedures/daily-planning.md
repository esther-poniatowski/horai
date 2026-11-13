---
tags:
  - procedure
index: "[Procedures](docs/procedures/_index.md)"
aliases:
  - Daily planning
---
# Daily planning

> [!QUESTION] Goal: how are the objectives of a day fixed from the committed week, within `ritual_durations.daily_planning`?

1. **Calendar.** Read the blocks, the windows and the appointed blocks of the day.
2. **Main objective.** For the longest block, apply the [selection rule](../kernel/processes/task-selection.md#^selection-rule) and mark the first task as the main objective.
3. **Other marks.** Mark further tasks, one per remaining block, up to `daily_marks`.
4. **During a block.** Mark the start of each task worked, and its stop. Record each interruption, idea or defect in the inbox, and return to the task. Serve only a request of the class `immediate`, and log the interruption.
5. **During a window.** Run the [request triage](request-triage.md) on the requests received, and do the tasks that release a wait. Return the unused part of the window to the next block.
6. **Close.** Assign each span of a planned block that no clock entry covers, and each task still running, to a task, or leave it untracked. The [time spent](../specification/log-record.md) is computed from the clock entries.
