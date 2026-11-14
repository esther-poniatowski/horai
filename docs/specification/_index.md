---
tags:
  - index
index: "[horai documentation](docs/_index.md)"
aliases:
  - Specification
---
# Specification

Documents the fields of each record of a plan and the views computed from them.

> [!WARNING] Status
> The records below state what the method requires of any implementation. The files that hold them, and the conventions of every file, are stated in the [file layout](file-layout.md). A field marked with an option is required only when the profile turns that option on.

> [!IMPORTANT] Authored and computed fields
> Each field is either **authored**, a judgment or a fact that the agent records, or **computed**, a value that the tool derives from authored fields by a rule stated in the kernel. A computed field is never edited by hand. A tool never sets an authored field by a rule. A tool writes an authored field only to transcribe a value that the agent states, to record an observed fact such as a timestamp, or to assign a new identifier. The column *Kind* of each table states which. ^authored-computed

## Files

- [File layout](file-layout.md): locates the file of each record, and states the conventions of every file

## Configuration

- [Profile record](profile-record.md): documents the fields by which a profile configures the kernel
- [Typical week record](typical-week-record.md): documents the time of the agent in a typical week and its placement among the streams

## Plan

- [Level records](milestone-record.md): documents the fields of a purpose, a deliverable, a milestone and a question
- [Task record](task-record.md): documents the fields that a task adds to its identifier and its dependencies
- [Party record](party-record.md): documents the fields of an external party and of a wait
- [Calendar record](calendar-record.md): documents the cycles, and the departures of each week from the typical week
- [Capture record](capture-record.md): documents the files that keep captured work outside the commitments

## Observation

- [Log record](log-record.md): documents the entries from which the estimates and the metrics are computed
- [Views](views.md): documents the views of a plan and the question that each answers
