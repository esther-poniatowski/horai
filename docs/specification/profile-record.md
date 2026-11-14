---
tags:
  - specification
  - wip
index: "[Specification](docs/specification/_index.md)"
aliases:
  - Profile record
---
# Profile record

> [!QUESTION] Goal: which fields does a profile state, so that the kernel is configured for a domain without any change of its rules?

All fields are authored.

| Field | When it is required | Values | Source |
| --- | --- | --- | --- |
| `name` | always | the name of the domain | [layers](../kernel/foundations/layers.md) |
| `streams` | always | one entry per stream | [stream](../kernel/objects/stream.md#^streams) |
| `streams: description` | per stream | what the stream does, opening on its most specific verb, such as "advances" or "derives" | [stream](../kernel/objects/stream.md#^streams) |
| `streams: yields` | per stream | a list of one or several of `results` · `means` · `knowledge` · `competence` · `network` · `coordination` · `organization` · `integrity` · `obligation`: what the work gives the agent | [yields](../kernel/objects/stream.md#^roles) |
| `streams: triggered_by` | per stream | `selection` · `demand` · `calendar` · `accumulation` · `arrival` · `appointment`: what prompts the work | [triggers](../kernel/objects/regime.md#^regimes) |
| `streams: needs_high_energy` | optional | `true` when the blocks of the stream belong at the hours of high energy; `false` when absent | [energy](../adr/properties-apart-from-the-trigger.md) |
| `streams: allocation` | optional | the time that the stream receives: `mode` (`share`, a fraction of the plannable time, or `reserve`, a duration), `bound` (`at_least`, `at_most` or `exact`), `amount`, and `per` (`day`, `week`, `cycle` or `event`, `week` when absent), with `events` to narrow a reserve per event to some appointments | [allocation](../adr/streams-allocation-and-loose-tasks.md) |
| `recurrences` | optional | the named rules of recurrence that tasks cite in `recurs`, each a period such as `P3M` or `P2C`; a name may not be a default rule, `daily`, `weekly` or `cycle` | [recurrence rules](../adr/strategic-review-and-recurrence-rules.md) |
| `deliverable_types` | always | one entry per type of deliverable: an identifier, a description, the `predictability` of its work, its `starting_phase`, and optionally its `prior_margin`, and its `stages`, each with an `id`, the phase from which it exists as a milestone, `validation` or `delivery`, and optionally a `predictability` and a `prior_margin` that replace those of the type | [typical week and types of deliverable](../adr/typical-week-and-deliverable-types.md) |
| `enabled_mechanisms` | always | the [optional mechanisms](../kernel/foundations/core-and-options.md#^options) that run beside the core, each with its settings | [core and options](../kernel/foundations/core-and-options.md) |
| `reactive` | option reactive work | the kinds of request, each with its class of service, optionally per party, and the stream to which a conversion goes; the time of response of each class | [reactive work](../kernel/processes/reactive-work.md) |
| `deadlines` | option imposed deadlines | the kinds of deadline met in the domain | [deadline](../kernel/objects/deadline.md) |
| `worth` | always | `scale: ordinal`, under which the items of a stream are ordered by their rank, or `scale: cardinal`, with the `unit` and the `worth_per_hour`, the worth of one hour of the agent in that unit | [allocation and worth](../adr/streams-allocation-and-loose-tasks.md) |
| `energy.high` | optional | the spans of high energy, as a list for every day or as a list per weekday | [availability](../kernel/objects/availability.md#^availability) |
| `modules` | when a module is used | the modules, each with the stream that it serves | [modules](../modules/_index.md) |
| `parameters` | optional | overrides of the [policies](../kernel/foundations/parameters.md#^parameter-table), each with its reason | [parameters](../kernel/foundations/parameters.md) |

## Checks

A profile is checked against four constraints:

1. every stream states what it yields and what triggers it; the `events` of a reserve per event name appointments of the calendar, and the exact and minimum shares sum to at most the plannable time, which `check` reports otherwise;
2. the minimums, the reserve and the shares fit in the [plannable capacity](../kernel/objects/availability.md#^plannable-capacity) of a poor week;
3. at least one stream that yields knowledge and one that yields competence state a minimum, bounded `at_least` or `exact`, or the profile states why its domain lacks one;
4. the reserve and the appointments leave at least `discretion_min` of the capacity, or the profile states that it runs in the [degraded mode](../kernel/foundations/problem-class.md).
