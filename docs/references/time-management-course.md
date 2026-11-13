---
tags:
  - reference
index: "[References](docs/references/_index.md)"
aliases:
  - Time-management course
  - SMART objectives
  - Eisenhower matrix
  - Retroplanning
  - PERT estimate
  - 2-20-2-2 rule
---
# Time-management course

A doctoral course on time management and priorities, given in two parts [neuroptima] [baelde], gathers the common operational methods of personal organization. This note states the methods with a defined procedure, rule or threshold, and leaves out the advice on health, psychology and communication habits.

## Methods

- **SMART and SMARTER objectives.** An objective is Specific, Measurable, Assignable (or Ambitious and Accepted), Realistic and Temporal, with a deadline. SMARTER adds Ethics or Assessed, and Reflected or Reviewed [baelde, p. 9–14].
- **Eisenhower matrix.** Each action is placed on two axes. Importance concerns the consequences of not doing it; urgency concerns time, when the time needed to finish approaches the time left before the term. Important and urgent actions are done; important ones are planned; urgent ones are delegated or transferred; the others are eliminated, or kept in an idea box [neuroptima, p. 2] [baelde, p. 17–20].
- **Margins of estimation.** An estimate is multiplied by 2 for a known task, by 3 or 4 for an unknown one, and by 4 to 10 for research. The three-point estimate of PERT computes $(T_{opt} + 4\,T_{prob} + T_{pess})/6$, and a project is estimated by the sum of its decomposed tasks [baelde, p. 21–22].
- **Retroplanning.** The tasks are listed, estimated and ordered; the delivery date is fixed, and the tasks are placed backward from the last one, with a margin of safety before delivery [baelde, p. 87–91].
- **Productivity laws.** Each law comes with a rule [neuroptima, p. 5] [baelde, p. 28–29]:
  - Parkinson: work fills the time allotted, so deadlines are set close;
  - Carlson: a task done at once takes less time than one done in pieces, so interruptions are avoided and similar tasks grouped;
  - Murphy: everything takes longer than planned, so time is kept free for the unexpected;
  - the law of emergencies: when emergencies take half of a day, priorities and efficiency are lost;
  - Illich: past a threshold of hours, efficiency decreases, so breaks are taken;
  - Laborit: the easy task is preferred, so the hard one is done first.
- **The 2-20-2-2 rule.** An unexpected request that takes 2 minutes is done at once; 20 minutes, after the current task; 2 hours, its deadline is negotiated; 2 days, a change of priority is asked [baelde, p. 25].
- **Focus.** Concentration builds over about 20 minutes and declines after about 2 hours, and an interruption restarts its build-up. Sessions of 1 h 30 separated by breaks, the Pomodoro of 20 to 25 minutes, and email answered 2 or 3 times a day follow from it [neuroptima, p. 3–5] [baelde, p. 45–49, 78].
- **Audit of time.** The activities that consume time are listed, divided into those that originate with the agent and those imposed from outside, and classed as to stop, to reduce or impossible to change [neuroptima, p. 2–3].

## Bearing on `horai`

The methods enter `horai` in three ways: as a mechanism of the method, as a mechanism that differs by design, or not at all. Each term of the method that differs from the course is kept under the rule of terms that the [documentation conventions](../_index.md) state.

| Method | Mechanism of `horai` | Relation |
| --- | --- | --- |
| Eisenhower: urgency | the [deadline key](../kernel/processes/task-selection.md#^selection-rule), raised when the [buffer runs ahead](../kernel/objects/deadline.md#^buffer-consumption): the time left against the time needed | implemented, against an outside term |
| Eisenhower: importance | the rank, or the cost of delay, of a milestone; within one parent, the importance of a task | implemented |
| Eisenhower: do, plan, delegate, eliminate | the selection of the next task; the commitment of the cycle and of the week; [delegation](../kernel/objects/external-party.md#^relations) and the redirection of a request; the [ideas file](../kernel/objects/work-hierarchy.md#^ideas-file) and the stop at a checkpoint | implemented |
| Margins of estimation | the [prior margins](../kernel/processes/uncertainty-control.md#^calibration) before calibration, then the ratios logged per class of variance | implemented |
| PERT | the three durations of a routine item, whose PERT value is its budget | implemented |
| Retroplanning | the [retroplanning](../kernel/objects/deadline.md#^retroplanning) of a deadline: the latest start of each milestone, and on demand of each task | implemented |
| Parkinson | the [appetite](../kernel/objects/appetite.md#^appetite): the time of chosen work is fixed in advance, and a date set by the agent is not a deadline | implemented differently |
| Carlson | blocks of one stream, the regime `batched`, and interruptions limited to the class `immediate` | implemented |
| Murphy | the reserve, the planning on the low quantile of the capacity, and the buffers | implemented |
| Law of emergencies | the [reserve](../kernel/processes/reactive-work.md#^reserve) bounds the reactive load, and its excess is a deviation | implemented |
| Laborit | the riskiest task first within its milestone, and the planned stream placed at the hours of highest energy | implemented |
| 2-20-2-2 | the triage: a request served in a window, or converted, with its feasibility tested | departs on the first step, as the note on [reactive work](../kernel/processes/reactive-work.md#^triage) states |
| Audit of time | the clock entries, the hours per stream against the allocation, and the [overhead](../kernel/foundations/core-and-options.md#^overhead) of the method | implemented |
| Focus and breaks | blocks of `block_length`, in place of short sessions; breaks are not planned | partly |

The letters of SMARTER are carried by several records:

| Letter | Mechanism of `horai` |
| --- | --- |
| Specific | the title and the scope of a milestone, and the open question of an exploration |
| Measurable | the definition of done of a milestone: a test of completion, or the acceptance by a party |
| Assignable, Accepted | the agent by default; a party under the relation `delegates`; the acceptance by a principal |
| Realistic | the fit of the budgets of a cycle to its capacity, and the feasibility test of deadlines |
| Temporal | the appetite or the budget of chosen work, and the deadline of imposed work |
| Assessed | the decision entry at each checkpoint and at each completion |
| Reviewed | the weekly review, the cycle planning and the strategic review |

Two letters are carried partly. A question of an exploration has no test of completion, since it is judged by the information gained. No record carries Ethics.

## Sources

- [neuroptima] ✓ Neuroptima, *Training: Time Management, Priorities and Personal Organization*, course handout for doctoral students, 16 pages.
- [baelde] ✓ Aurélien Baelde, *Time Management, Priorities and Personal Organization*, course slides, 100 pages.
