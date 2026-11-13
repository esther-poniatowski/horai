---
tags:
  - specification
  - wip
index: "[Specification](docs/specification/_index.md)"
aliases:
  - Availability record
---
# Availability record

> [!QUESTION] Goal: which fields state the working time of the agent, so that capacity is planned on the time that is usable?

The availability is recorded apart from the profile, since it changes with the situation of the agent and not with its domain.

| Field | When it is required | Kind | Values | Source |
| --- | --- | --- | --- | --- |
| `capacity` | always | authored | the weekly capacity in hours, as a median and a low quantile | [availability](../kernel/objects/availability.md#^availability) |
| `predictable` | always | authored | whether the time of the next week is known at the weekly review | [availability](../kernel/objects/availability.md#^availability) |
| `minimum_block` | always | authored | a duration: the shortest contiguous span of time that the agent can usually count on | [slots](../kernel/objects/availability.md#^slots) |
| `energy` | always | authored | the hours at which demanding work succeeds | [availability](../kernel/objects/availability.md#^availability) |
| `capacity_estimate` | option availability model | computed | the distribution of the weekly capacity, from the clock entries | [estimates](../kernel/foundations/parameters.md#^parameter-kinds) |
