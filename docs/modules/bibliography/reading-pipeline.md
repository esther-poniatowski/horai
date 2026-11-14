---
tags:
  - module
  - theory
index: "[Bibliography](docs/modules/bibliography/_index.md)"
aliases:
  - Reading pipeline
  - Positioning questions
---
# Reading pipeline

> [!QUESTION] Goal: how is reading selected and bounded, so that it positions each deliverable and starts from a definite point?

## Entry point

Each deliverable maintains a list of **positioning questions**, such as "which existing result is closest to this claim?" or "which method solves this subproblem?". Reading is selected against these questions, which gives the stream a starting point. ^positioning-questions

## Pipeline

A paper passes through four stages: inbox, triaged, read, synthesized. ^pipeline

- **Triage is delegated.** Automated agents perform the first pass on the inbox, and the reader decides to keep or to discard.
- **Work in progress is limited.** At most three papers are in the stage `read` at once, a default taken from [Kanban](../../references/kanban-and-lean-pull.md).
- **Depth is chosen.** A paper receives one of the three depths of [three-pass reading](../../references/three-pass-reading.md): a decision in ten minutes, a structured note in one hour, or a full reproduction, reserved for a paper whose method is reused.
- **A session ends with an artifact.** Each session yields a paragraph of related work or a note linked to the claims of a deliverable, as the [trigger by the calendar](../../kernel/objects/regime.md#^regimes) requires.

## Two modes

| Mode | Trigger | Budget |
| --- | --- | --- |
| Targeted | a positioning question or a milestone | the fixed sessions of the stream |
| Surveillance | alerts and new publications | one session a week |

The steps of a session are given in the [procedure for a reading session](reading-session.md).
