---
tags:
  - index
aliases:
  - horai documentation
---
# horai documentation

Directs a reader of `horai` to the folder that serves one task: understanding the general method, configuring it for a domain, applying it, deciding a design question, or consulting the external literature.

> [!IMPORTANT] Three layers
> The method is stated in three layers, which the note on the [layers](kernel/foundations/layers.md) separates by a test:
> - the **kernel** holds the concepts and the rules that no domain vocabulary enters;
> - a **profile** declares the values that configure the kernel for one domain;
> - a **module** holds a process that exists only for one role of work in some domains.

> [!IMPORTANT] Note conventions
> - **Frontmatter.** Each note states its `tags`, the `index` note that lists it, and its `aliases`. A decision also states its `status` and its dates.
> - **Tags.** `index` · `theory` · `definition` · `procedure` · `specification` · `profile` · `module` · `decision` · `reference` · `wip`.
> - **Goal.** Each note other than an index or a reference opens with the question that it answers.
> - **Anchors.** A defining sentence ends with a block anchor (`^name`), by which other notes cite it.
> - **One home per fact.** A concept is stated in the kernel, its values in a profile, its steps in a procedure, its fields in the specification, and its external grounds in a reference. Other notes link to that home and do not restate it.
> - **Reading marks.** In a list of sources, ✓ marks a source consulted during the [review of 2026-11-11](kernel/foundations/evidence-status.md), and ○ marks a source cited without being consulted.

## Understand the method

- [Kernel](kernel/_index.md): states the general theory of the allocation of attention, with the grounds and the strength of support of each choice

## Configure the method for a domain

- [Profiles](profiles/_index.md): declares the configuration of the kernel for each domain, and compares the instances
- [Modules](modules/_index.md): states the processes that serve one role of work in particular domains

## Apply the method

- [Procedures](procedures/_index.md): guides the performance of each recurring act of planning, review and decision
- [Specification](specification/_index.md): documents the fields of each record and the views computed from them
- [User guide](guide/installation.md): guides the installation and the use of the package

## Decide a design question

- [Architecture decisions](adr/_index.md): records the choices of method that later work must respect

## Consult the external literature

- [References](references/_index.md): states on their own terms the methodologies and the findings on which the method draws
