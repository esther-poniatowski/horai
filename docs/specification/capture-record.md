---
tags:
  - specification
  - wip
index: "[Specification](docs/specification/_index.md)"
aliases:
  - Capture record
  - Inbox
  - Holding file
  - Ideas file
---
# Capture record

> [!QUESTION] Goal: which records keep captured work outside the commitments, so that it waits for a planning session without competing for attention, and leaves the plan when no session selects it?

## Inbox

The inbox receives the work that arises during a block, and is emptied at each [weekly review](../procedures/weekly-review.md). Each entry is one line of authored text: an interruption, a task, an idea, a defect, or a request of the class `scheduled`. An entry bears no other field.

## Holding file

The holding file keeps the tasks that serve no milestone and name no stream. Each entry is a [task record](task-record.md) without a `parent` and without a `stream`. Its field `held_since` states the date at which it entered the file.

## Ideas file

The [ideas file](../kernel/objects/work-hierarchy.md#^ideas-file) keeps the ideas of possible deliverables, for the strategic review. Each entry is one line of authored text, and is never archived.

## Archive

The archive keeps, unchanged, the task records removed from the holding file by the [orphan rule](../kernel/objects/work-hierarchy.md#^orphan-rule).
