# Roadmap

The roadmap of horai lists the steps of each increment, with the state of each step. An increment opens with the decisions that it needs, each ratified by the author and recorded in the [accepted decision records](docs/adr/_index.md). It closes on an exit criterion measured in use. Each completed step carries the date of its check, and the [handoff](docs/handoff.md) carries the state between sessions.

## Increment 1: read side and clock

- [x] **Gate**: ratify the scope, the constraints, the architecture, the commitments, the ontology, the record formats and the core rules. (2026-11-13)
- [x] **Environment**: create the environment `horai`, with PyYAML, jsonschema and its type stubs. (2026-11-13)
- [x] **Schemas**: write the JSON Schemas of the 19 record types, with the shared definitions in one file. (2026-11-13)
- [x] **Loading**: read YAML with the core types, validate each file, isolate the invalid ones, and resolve the configuration at a configurable path. (2026-11-13)
- [x] **Rules**: compute the commitment state, the time spent, the remaining work and the selection in tiers, and check the references across records. (2026-11-13)
- [x] **Commands**: `check`, `next`, `view week`, `start` and `stop`. (2026-11-13)
- [x] **Tests**: a fixture plan of the research profile, and tests of each rule with planted failures. (2026-11-13)
- [x] **Streams**: identify the streams of the research profile by slugs. (2026-11-13)
- [ ] **Exit criterion**: the plan of the author passes `check`, and `next`, `view week`, `start` and `stop` serve one week of daily planning.

## Integration with Geonexus

- [x] **Assessment**: measure the task lists of Geonexus against the records of horai. (2026-11-13)
- [x] **Gate**: decide the placement of distributed records, the standing parent of each folder, steps, dependencies across parents, the quadrant of importance and urgency within a parent, and due dates as deadlines of the parent. (2026-11-13)
- [x] **Loading**: declare the roots in the configuration, and discover the records of the hierarchy by their key `_schema` under them. (2026-11-13)
- [x] **Records**: add the fields `importance` and `steps` to the task, and admit dependencies across parents in the schema, the checks and the selection. (2026-11-13)
- [x] **Selection**: order the tasks of one parent by quadrant, then by importance, then by the riskiest mark. (2026-11-13)
- [ ] **Geonexus rule**: amend the rule on task tracking of Geonexus for the areas that horai covers, under its instructions for agents and its commit gate.
- [x] **Pilot**: draft the central folder `planning/` of Geonexus, and migrate the task list of the CCS 2026 satellite into a standing parent beside it; the original list stays until the author has compared the two. (2026-11-13)
- [x] **Gate**: decide the labels of the streams, the typical week, the exceptions held by the week, the energy hours and the types of deliverable, after the review of the drafted plan. (2026-11-13)
- [x] **Names**: ratify the naming criterion and the renames of the [explicit names](docs/adr/explicit-names.md). (2026-11-13)
- [x] **Formats**: implement the [typical week and the types of deliverable](docs/adr/typical-week-and-deliverable-types.md) and the [explicit names](docs/adr/explicit-names.md) in the schemas, the loader, the checks, the week view, the fixture plan and the specification. (2026-11-13)
- [x] **Terms of the method**: carry the explicit names into the kernel notes, the procedures, the profiles, the modules and the references. (2026-11-13)
- [ ] **Names of files and anchors**: rename the notes `regime.md` and `stream.md`, and the anchors that keep the former terms (`^regimes`, `^roles`, `^floors`, `^standing-parent`, `^variance-classes`, `^release-key`, `^principal`), with every link to them.
- [x] **Gate**: decide the preparation per appointment, the unplaced appointments, the added and removed blocks, the phase of each stage and the argument plan. (2026-11-13)
- [x] **Gate**: decide the allocation by mode, bound and anchor, the scale of the worth, the declared parties, the retirement of the permanent areas, the milestones without a deliverable, the order of loose tasks, the stream of planning and the energy in the profile. (2026-11-14)
- [x] **Streams, appointments and stages**: implement the [streams, allocation and loose tasks](docs/adr/streams-allocation-and-loose-tasks.md) and the [appointments and stages](docs/adr/appointments-and-stages.md) in the schemas, the selection, the calendar, the checks, the fixture plan, the specification, the method notes, and the plan of the author in Geonexus. (2026-11-14)
- [x] **Review fixes**: keep the budget of a carried milestone, check the blocks of the preparations, ignore a mark on a closed record, and correct four minor defects found by the adversarial review. (2026-11-14)
- [x] **Gate**: decide the calendar of dates and the review log, the energy of a stream, the overrun by bounds, the appointments in any stream, the recurring tasks and the backlog of loose tasks. (2026-11-14)
- [x] **Dates, reviews and recurrence**: implement the decisions on [properties apart from the trigger](docs/adr/properties-apart-from-the-trigger.md) and on [dates, reviews and recurring tasks](docs/adr/dates-reviews-and-recurring-tasks.md) in the schemas, the loader, the rules, the week view, the fixture plan, the notes, and the plan of the author in Geonexus. (2026-11-14)
- [x] **Request windows and stages**: implement the decision on [request windows and stages](docs/adr/request-windows-and-stages.md), with the command `stages`. (2026-11-14)
- [x] **Uniform selection and recurrence**: implement the decision on [uniform selection and recurrence](docs/adr/uniform-selection-and-recurrence.md). (2026-11-14)
- [x] **Parties and derived deliverables**: implement the decision on [parties, derived deliverables and the lifetimes of the profile](docs/adr/parties-and-derived-deliverables.md), which closes the findings of the adversarial review. (2026-11-14)
- [x] **Settings and yields**: implement the decision on [settings and yields](docs/adr/settings-and-yields.md): the folder `settings/`, and `yields` as a list of nine values. (2026-11-14)
- [ ] **Suggested blocks**: compute the blocks of a typical week from the allocation of the streams, the spans, the appointments and the energy hours, as a proposal that the author edits.
- [ ] **Forms**: publish the schemas of horai as a registry of Kleisis, and pin horai in the schema resources of Geonexus, so that Ekphrasis renders the records.
- [ ] **Migration**: carry the plan of the author in Geonexus to the new formats, and settle the placeholders with the author.

## Alignment with the time-management course

- [x] **Assessment**: compare the operational methods of the course with the mechanisms of horai, in a reference note with the correspondence of each method. (2026-11-13)
- [x] **Gate**: decide the prior margins, the PERT estimate, the retroplanning, the measured overhead and the rule of terms. (2026-11-13)
- [x] **PERT**: three durations of a routine item, whose PERT value is its budget, with their checks. (2026-11-13)
- [x] **Overhead**: the standing parent marked `overhead`, whose time the week view compares with `overhead_budget`. (2026-11-13)

## Increment 2: write side

- [ ] **Commands**: capture into the inbox, mark the day, complete a task, commit the week, and record a decision entry.
- [ ] **Writer**: a round-trip YAML writer that changes only the edited value of a file.
- [ ] **Protocol**: `horai serve --stdio`, the versioned protocol between the core and the plugin.

## Increment 3: forms and plugin

- [ ] **Forms**: bind the schemas of horai to Ekphrasis, so that each record is filled through a form.
- [ ] **Plugin**: the live views of the week and of the roadmap, over the protocol.

## Increment 4: cycle loop

- [ ] **Procedures**: cycle planning, checkpoint decisions, admission and stall, deviation entries.
- [ ] **Views**: the weekly report and the roadmap.

## Later increments

- [ ] **Imposed deadlines and calibration**: the deadline key, the feasibility test and the buffers, with the share of a PERT item; the retroplanning, latest starts by default and the full retroplanning on demand; the estimates of the ratios, with the prior margins before calibration.
- [ ] **External parties and delegation**: party and wait records, latencies, the release key.
- [ ] **Tooling control and milestone graph**: the tooling register, the unblocking key.
- [ ] **Reactive work**: requests, triage and windows.
- [ ] **Quantified valuation and availability model**.
- [ ] **Modules**: bibliography and mathematical mastery, then writing, delegation, meeting preparation, and experiments and simulations.
- [ ] **Package documentation**: build the guide and the API with Sphinx.
