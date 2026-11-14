---
tags:
  - decision
status: accepted
created: 2026-11-14
index: "[Architecture decisions](docs/adr/_index.md)"
aliases:
  - One parties file
  - Derived deliverables
  - Lifetimes of the profile
---
# Parties, derived deliverables and the lifetimes of the profile

> [!QUESTION] Goal: where is a party described, which field states the delay of a reviewer, how does a deliverable derived from another count under the cap, and does the situation of the agent carry a date of validity?

A review of the framework found four last defects. A party was described in three places: the file of the parties, a file per party specified without a schema, and a field of the profile that the profile schema rejected. The field `review_latency` of a type of deliverable was read by no rule. The cap on active deliverables counted an article, its abstract and its talk as three results. The profile held properties of three lifetimes, and neither the profile nor the typical week carried a date of validity.

## Decision

- **One parties file.** `parties.yml` is the single record of a party: its `id`, its `name`, and optionally its `relations` and its `class_of_service` per kind of request. The file per party and the field `parties` of the profile are retired. The principal of a deliverable is the party that its field `accountable_to` names. A wait keeps its own record. The `party` of a deadline names a declared party, or an occasional one, and is checked like the others.
- **No latency on a type.** The field `review_latency` is retired. The latency of a party is logged per party, and below `latency_min_samples` the wait states its expected date.
- **Derived deliverables.** A deliverable may state `derived_from`, the deliverable that it presents, such as the article of a talk. It shares the place of its source under `active_deliverables_max`. Its source is derived from no other deliverable.
- **No date of validity.** The profile and the typical week describe the current situation, without a date. A change of situation rewrites them, and the checks of past dates read the new values.

## Constraints that decide the formats

- **One place per object.** A party is one object, so one record holds every authored field of it.
- **A field is authored only when a rule reads it.** No rule reads a latency per type, and the wait already holds the cold start of a latency.
- **The cap counts lines of work.** A talk that presents an article continues the work of the article, whereas an independent talk is a line of its own, so the relation is stated per deliverable.

## Options weighed

- **A file per party, or two linked records.** Rejected: the first multiplies small files, and the second keeps two places for one party.
- **A flag on the type of a derived deliverable.** Rejected: an independent talk would escape the cap.
- **Dated situation records, holding the typical week and the allocation amounts.** Rejected by the author, who keeps the allocations in the profile and accepts that the past is judged against the current values.
- **A dated profile and a dated typical week.** Rejected by the author: each change of situation would copy the whole profile.

## Consequences

- The schema of the parties gains the relations and the classes of service; the deadline names a party; the deliverable gains `derived_from`; the profile loses `review_latency`.
- The specification of the party record describes the entries of `parties.yml` and the wait.
- A change of situation that must not rewrite the judgement of past weeks would reopen this decision.
