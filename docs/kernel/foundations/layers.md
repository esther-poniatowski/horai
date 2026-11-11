---
tags:
  - theory
index: "[Foundations](docs/kernel/foundations/_index.md)"
aliases:
  - Layers
  - Kernel, profile and module
---
# Layers

> [!QUESTION] Goal: by which test is a statement of the method assigned to the kernel, to a profile or to a module?

The method is stated in three layers, as the decision on the [three-layer architecture](../../adr/three-layer-architecture.md) records. ^layers

| Layer | Content | Test of membership |
| --- | --- | --- |
| Kernel | objects, rules, and the forms of the parameters | the statement stays true when each term of a domain is replaced by the role that it plays, and it contains no number |
| Profile | values of the parameters for one domain | the statement is a value of a parameter that the kernel declares |
| Module | a process attached to one role | the process exists only for that role, and only in some domains |

*Example*: "work on means is pulled by a result that consumes its output" is a statement of the kernel. "The stream of tools receives a ceiling of 15%" is a value of a profile. "A text is read at one of three depths" belongs to a module of the role sensing.

## Numbers in the kernel

A number stated in a note of the kernel is the default of a [parameter](parameters.md#^parameter-table), named there, and overridable by a profile. A number that appears in the kernel without being listed among the parameters is a defect. ^no-hidden-number

The test of the first row therefore has two parts: no vocabulary of a domain, and no number other than a named default. Neither part establishes generality, which only the use of profiles in several domains can show.

## Rules of dependence

- **A profile depends on the kernel, and never the converse.** No note of the kernel links to a profile except as an example, marked as such.
- **A module depends on the kernel and names its role.** A profile lists the modules that it uses.
- **A profile turns options on, and adds no rule.** The [options](core-and-options.md#^options) are defined in the kernel, and a profile declares which apply.
- **Policies and estimates are revised differently.** A policy changes only by a decision at the strategic review, and an estimate is revised from the logs, as the [parameters](parameters.md#^parameter-kinds) state.

The fields of a profile are documented in the [profile record](../../specification/profile-record.md).
