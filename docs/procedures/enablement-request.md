---
tags:
  - procedure
index: "[Procedures](docs/procedures/_index.md)"
aliases:
  - Enablement request
---
# Enablement request

> [!QUESTION] Goal: when the work appears blocked by a missing means, what is built, how far, and under which budget?

The request applies the rules of [enablement](../kernel/processes/enablement.md).

1. **Artifact.** Name the artifact that the consumer needs, and the consumer itself: a milestone, or a kind of request that recurs.
2. **Result test.** If the means is itself delivered and valued, treat it as a milestone of production and leave this procedure.
3. **Manual route.** Produce the artifact by hand, by a means made for the occasion, or obtain it from outside, and count the occurrence.
4. **Recurrence test.** If the count has reached `recurrence_threshold`, and the cost of verifying and maintaining a durable means is below the cost of the manual route, continue. Otherwise stop here.
5. **Make or obtain.** Where the valuation is quantified, compare the cost of building with the cost of obtaining the means from outside.
6. **Slice.** State the smallest end-to-end path that produces the artifact for this consumer.
7. **Budget.** If the consumer is a milestone of the cycle, charge an appetite to it and drive the slice without interruption. Otherwise schedule the slice within the ceiling of the stream.
8. **Close.** Close the request when the consumer is unblocked. Record each generalization left aside under the standing parent of debt.
