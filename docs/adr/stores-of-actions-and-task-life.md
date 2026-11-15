---
tags:
  - decision
status: accepted
created: 2026-11-15
index: "[Architecture decisions](docs/adr/_index.md)"
aliases:
  - Stores of actions
  - Life of a task
  - Complexity of a task
---
# Stores of actions and life of a task

> [!QUESTION] Goal: in which file does a folder keep its actions, and which fields state the wording, the life, the demand and the boundaries of a task, so that the records read as forms and as condensed views?

The first records of the author, read as forms, exposed seven defects. Each milestone was a file named by its identifier, so the actions of a folder had no uniform name. The test `done_when` of a group of follow-up actions restated its tasks. A task recorded only its completion, so a dropped task could not be recorded. A task bore a `title` that held paragraphs, links and remarks. Tasks of one stream differ in their demand on the agent, which the stream alone stated. The labels of a former system of tasks overlapped the streams and the items. Steps had no stated boundary with tasks, and the levels of work had no operational criterion.

## Decision

- **One store per folder.** A folder keeps its milestones, its questions and its loose tasks in one store of actions, `horai:actions@1`, under the file name that the configuration key `actions_file` sets, `TODO.yml` by default, the same in every folder. The central folder keeps its own store in `plan/`. Each item and each task states its identifier in its field `id`. An invalid entry of a store is excluded alone. The types `horai:milestone@1`, `horai:question@1` and `horai:task-list@1` are retired; a purpose, a deliverable and a cycle keep one file each, named by their identifier.
- **Success criteria.** The field `done_when` is replaced by an optional list `success_criteria`, each criterion an observable state that can be checked. An item without the list is done once its tasks are closed.
- **Life of a task.** A task owns the dates of its life: `created`, `started`, `completed`, and `cancelled` with its date and its reason. Its status, open, completed or cancelled, is computed. A cancelled task is closed for good, and releases the tasks that depend on it. The sessions of work stay in the clock log; `check` reports a `started` later than the first session on the task.
- **Wording.** A task and a step state an `action`, one brief imperative sentence of at most 90 characters, and their `details` in Markdown.
- **Complexity.** A task may state its `complexity`, `low`, `medium` or `high`, which defaults to the `complexity` of its stream. The field `complexity` of a stream replaces `needs_high_energy`: the blocks of a stream of high complexity belong at the hours of high energy. Outside those hours, the selection offers the tasks of high complexity after all the others.
- **Served streams.** A task takes the time of one stream. A loose task may also state `consumed_by`, the milestones, questions or streams that its result serves.
- **Boundaries.** A milestone is a result with a test of done, budgeted and finished within one cycle. A task is one action committed for a week, startable without further planning, and done in one block or a few. A step is a check inside one task, one level deep; a step that needs its own date, dependency or selection becomes a task.
- **Forms.** Every field of a schema bears a label and an instruction, and the status of an item is `open` by default, so that Ekphrasis presents each record as a form.

## Constraints that decide the formats

- **One store of actions per folder,** as the rules of the vault of the author require, under one name that any folder repeats.
- **Events where they happen.** A life event of a task happens once and belongs to the task; a session of work happens many times a day, and each start ends the session running on any task, so the sessions stay in one ordered log.
- **A field is read by a rule.** The complexity is read by the check of the blocks and by the selection.

## Options weighed

- **A free file name per item, or identity by the file name.** Rejected: the first leaves a folder with several files, and the second forbids a uniform name.
- **A required test of done, with guidance.** Rejected: a group of follow-up actions would restate its tasks.
- **A pause, or an explicit status.** Rejected: a wait and the backlog cover the pause, and a written status could contradict the dates.
- **The sessions on the task.** Rejected: `start` and `stop` would rewrite the files of the projects many times a day.
- **`title` with `description`, or `task` with `details`.** Rejected: a title names a heading, and the key `task` repeats the name of the record.
- **A field of complexity beside `needs_high_energy`.** Rejected: two properties would state one demand on the agent.
- **Labels of the kind of change.** Rejected: the question, the duplicate, the help and the documentation are covered by the question item, the cancellation, the wait and the deliverable types, and no rule reads the others.
- **A time split across streams.** Rejected: a task would be offered in several kinds of block, and its time counted in fractions.
- **Nested steps.** Rejected: they would rebuild a hierarchy of tasks that escapes the selection and the budgets.

## Consequences

- The loader reads the stores of actions, centrally and under the roots, with the name of the configuration, and the command `stages` appends the milestones of the stages to the store of the folder of their deliverable.
- The fixture plan, and the plan of the author in Geonexus, move their milestones and their task lists into stores.
- This decision replaces the field `done_when`, and the field `needs_high_energy` of the decision on [properties apart from the trigger](properties-apart-from-the-trigger.md).
