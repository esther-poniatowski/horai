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
| `availability` | always | the weekly capacity as a median and a low quantile, its predictability, the minimum block, the energy profile | [availability](../kernel/objects/availability.md#^availability) |
| `streams` | always | one entry per stream | [stream](../kernel/objects/stream.md#^streams) |
| `streams: role` | per stream | `production` · `enablement` · `sensing` · `capability` · `interface` · `upkeep` · `duty` | [roles](../kernel/objects/stream.md#^roles) |
| `streams: regime` | per stream | `planned` · `pulled` · `floor` · `calendar` · `batched` · `reactive` · `committed` | [regimes](../kernel/objects/regime.md#^regimes) |
| `streams: capacity` | per stream | a value in the form that the regime fixes | [forms of capacity](../kernel/processes/capacity-allocation.md#^forms) |
| `levels` | always | the names of the purpose and of the deliverable | [levels](../kernel/objects/work-hierarchy.md#^levels) |
| `phases` | always | the names of the three phases | [phases](../kernel/objects/phase.md#^phases) |
| `evidence_note` | always | its name, and its readers | [evidence note](../kernel/processes/feedback.md#^evidence-note) |
| `options` | always | the [options](../kernel/foundations/core-and-options.md#^options) turned on | [core and options](../kernel/foundations/core-and-options.md) |
| `reactive` | option reactive work | the kinds of request, each with its class of service, optionally per party, and the stream to which a conversion goes; the time of response of each class | [reactive work](../kernel/processes/reactive-work.md) |
| `parties` | option external parties | the kinds of party with their relations, and the principals | [relations](../kernel/objects/external-party.md#^relations) |
| `deadlines` | option imposed deadlines | the kinds of deadline met in the domain | [deadline](../kernel/objects/deadline.md) |
| `valuation` | always | `ordinal`, or the unit and the initial cost of capacity | [value](../kernel/objects/value.md#^scales) |
| `modules` | when a module is used | the modules, each with the stream that it serves | [modules](../modules/_index.md) |
| `parameters` | optional | overrides of the [policies](../kernel/foundations/parameters.md#^parameter-table), each with its reason | [parameters](../kernel/foundations/parameters.md) |

## Checks

A profile is checked against four constraints:

1. every stream has one role and one regime;
2. the floors, the reserve and the shares fit in the [plannable capacity](../kernel/objects/availability.md#^plannable-capacity) at the low quantile of the availability;
3. at least one stream of each of the roles sensing and capability holds a floor, or the profile states why its domain lacks one;
4. the reserve and the committed blocks leave at least `discretion_min` of the capacity, or the profile states that it runs in the [degraded mode](../kernel/foundations/problem-class.md).
