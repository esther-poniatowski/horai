---
tags:
  - index
index: "[horai documentation](docs/_index.md)"
aliases:
  - Architecture decisions
---
# Architecture decisions

Records the choices of method that later work on `horai` must respect, so that a reader can judge whether a changed constraint reopens one of them.

> [!IMPORTANT] Form of a decision record
> Each record states the decision, the constraints that forced it, the options weighed and its consequences. Its frontmatter states its status and its dates. A decision on the software itself may instead follow the [long template](adr-template.md).

## Ratified foundation

> [!IMPORTANT] Status of the records
> A record of status `accepted` was ratified by the author, and a record of status `superseded` was replaced by a ratified one. Every other record is a proposal.

- [Kernel with research first](kernel-with-research-first.md): decides for which agents the software is built first
- [Constraints of the software](software-constraints.md): decides the constraints that every part of the software respects
- [Python core and Obsidian plugin](python-core-and-plugin.md): decides where a plan lives and where its rules are computed
- [Ratified commitments](ratified-commitments.md): records which commitments of the method the author ratified, and the non-negotiable mark
- [Ratified ontology](ratified-ontology.md): records the objects that the software manipulates
- [Record formats](record-formats.md): decides in which files and notations the records of a plan are stored
- [Distributed records](distributed-records.md): decides how the records of a plan sit beside the projects and folders that they concern
- [Alignment with the time-management course](time-management-alignment.md): decides which methods of the course the method takes up, and how its terms relate to theirs
- [Typical week and types of deliverable](typical-week-and-deliverable-types.md): decides how the time of the agent and the kinds of its results are recorded
- [Explicit names](explicit-names.md): decides the names of the fields of the records and of their values
- [Appointments and stages](appointments-and-stages.md): decides how preparation, appointments without a slot, changes of one block and the stages of a deliverable are recorded
- [Streams, allocation and loose tasks](streams-allocation-and-loose-tasks.md): decides how a stream receives its time, which records hold the tasks outside deliverables, and where parties and energy sit
- [Properties apart from the trigger](properties-apart-from-the-trigger.md): decides which properties of a stream govern the checks of energy, the overrun and the appointments
- [Dates, reviews and recurring tasks](dates-reviews-and-recurring-tasks.md): decides which records hold the departures of dates, the start of each week of commitment, and recurring work
- [Request windows and stages](request-windows-and-stages.md): decides how request windows are placed, and how a stage of a deliverable becomes a milestone
- [Strategic review and recurrence rules](strategic-review-and-recurrence-rules.md): decides the procedure of the strategic review, and the rules by which a task recurs
- [Settings and yields](settings-and-yields.md): decides where the settings of a plan sit, and which outcomes a stream yields
- [Parties, derived deliverables and the lifetimes of the profile](parties-and-derived-deliverables.md): decides where a party is described, how a derived deliverable counts under the cap, and whether the situation carries a date
- [Uniform selection and recurrence](uniform-selection-and-recurrence.md): decides the single rule by which a cycle selects its items, the time of every stream with committed work, and the periods of appointments
- [Ratified core rules](ratified-core-rules.md): fixes the rules of the core before the first increment, and ratifies the amendments of its documentation gate

## Architecture of the method

- [Three-layer architecture](three-layer-architecture.md): decides how the general method is separated from the values and the processes of a domain
- [Role and regime as independent dimensions](role-and-regime.md): decides how a kind of work is typed, once work arrives on demand
- [Extensions of the kernel](kernel-extensions.md): decides how reactive work, external parties, imposed deadlines and quantified cost enter a method for one agent

## Decisions of the first review

> [!NOTE] Vocabulary of these records
> The five decisions below were taken on the research instance, before the generalization, and keep its vocabulary: the streams P, T, B and L are those of the [research profile](../profiles/research.md), now identified as `inquiry`, `tools`, `bibliography` and `training`, of the roles production, tooling, survey and training. Each decision holds for the kernel.

- [Variance classes in place of a Pareto law](variance-classes.md): decides on which work an appetite replaces an estimate
- [Phase-dependent planning](phase-dependent-planning.md): decides where a plan states milestones and their graph
- [Constraint logic for enablement](enablement-constraint-logic.md): decides how the time given to means is bounded
- [Weekly note in place of a milestone invariant](weekly-note.md): decides how the progress of a week is attested
- [Day theming](day-theming.md): decides the unit of time to which a stream is assigned

## Decisions of the second review

- [Cumulative feasibility of deadlines](cumulative-feasibility.md): decides how several deadlines are tested against one capacity
- [Valuation at the milestone](milestone-level-valuation.md): decides at which level worth is compared, and how a renewal is judged on worth
- [Policies and estimates](policies-and-estimates.md): decides which parameters the logs may revise
- [Minimal core](minimal-core.md): decides how the overhead of the method is bounded
- [Additional dimensions](additional-dimensions.md): decides which features of the agent and of its relations the kernel represents
