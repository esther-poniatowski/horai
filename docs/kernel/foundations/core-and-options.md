---
tags:
  - theory
index: "[Foundations](docs/kernel/foundations/_index.md)"
aliases:
  - Core and options
  - Minimal core
  - Overhead of the method
---
# Core and options

> [!QUESTION] Goal: which part of the method is always installed, which parts are turned on by a profile, and what does each part cost in attention?

The method risks becoming the sink that it corrects: a planning system that absorbs the time owed to the work. It is therefore installed as a minimal core, and each further part is an option with a stated cost, as the tenth [commitment](commitments.md#^c-core) requires.

## Core

The core holds what is needed to answer the control questions of classification, allocation, placement, commitment, ordering and termination for an agent with no modulator. ^core

| Element | Objects and rules |
| --- | --- |
| Separation of inventory and commitment | the states `backlog`, `cycle` and `week`, with a hidden backlog |
| Allocation by stream | streams triggered by selection, by the calendar, by appointment and by accumulation, placed in blocks |
| Results | milestones with a definition of done, questions in exploration |
| Termination | appetites for exploratory items, estimates for routine ones, a checkpoint at any consumed budget, and the stop by default |
| Waits | a date of follow-up, `follow_up`, on each waiting task |
| Observation | the clock entries on tasks, from which the time spent is computed, the decision entries, and the deviation entries |
| Rituals | strategic review, cycle planning, weekly review, daily planning |

## Options

Each option adds objects, fields, a procedure and at most one metric. A profile turns it on when a [modulator](problem-class.md#^modulators) is present, or later, when a decision of the last cycle lacked the information that the option gives. ^options

| Option | Turned on when | Adds |
| --- | --- | --- |
| Tooling control | the agent builds its means | the trigger by demand, the tooling register, the [tooling request](../../procedures/tooling-request.md) |
| Milestone graph | dependencies between milestones matter | the graph, the unblocking key of the selection rule |
| Calibration | a reference class has enough entries | estimates of ratios, the predictability by threshold |
| Reactive work | requests arrive with an expected time of response | the reserve, request windows, the [triage](../../procedures/request-triage.md), the request log |
| External parties | the work waits on parties | party and wait records, latencies, the [external request](../../procedures/external-request.md) |
| Delegation | the agent hands its own work to others | the relation `delegates`, the logged verification |
| Imposed deadlines | dates are fixed from outside | the [feasibility test](../processes/imposed-deadlines.md), buffers |
| Quantified valuation | worths can be stated in a unit | values, costs of delay, the stop by value |
| Availability model | the time is fragmented or variable | the distribution of capacity, slots shorter than a block |
| Modules | the streams of one yield need a process of their own | the procedures of the module |

## Overhead

The core costs about $45 + 5 \times 5 + 60/6 + 120/13 + 5 \times 3 \approx 105$ minutes a week: the weekly review, five daily plannings, the cycle planning and the strategic review spread over their periods, and the close of each day. ^overhead

- **Options add their own time.** The feasibility test, the review of waits and the reading of buffers add about 10 to 20 minutes a week each when their option is on. A full configuration, such as the [consultant profile](../../profiles/consultant.md) as an example, reaches about 2.5 hours a week.
- **Work is not overhead.** The triage of a request is reactive work and is charged to the reserve. The checkpoint of an item is charged to the item.
- **Tooling removes the rest.** The computation of the views, the metrics, the percentiles, the timestamps of requests and the feasibility test is done by `horai`, and not by hand.
- **The overhead is measured.** The planning acts are loose tasks of a stream `planning`, triggered by the calendar, to which the typical week gives blocks. Their time is clocked like any work.
- **The overhead is bounded by a reserve.** The stream `planning` receives a reserve per week, at most `PT1H45M` by default, the cost of the core stated above. A profile that turns on options may raise it by the time that they add.
- **An overrun of the reserve is a deviation.** When the planning acts exceed the reserve of the stream `planning` over a cycle, an option is turned off or a ritual shortened.
