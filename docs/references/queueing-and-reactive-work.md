---
tags:
  - reference
index: "[References](docs/references/_index.md)"
aliases:
  - Queueing and reactive work
  - Classes of service
  - Maker's schedule
---
# Queueing and reactive work

## Results of queueing theory

For a single server with arrivals at random at rate $\lambda$ and exponential service at rate $\mu$, the utilization is $\rho = \lambda/\mu$, and the mean wait before service is

$$W_q = \frac{\rho}{\mu\,(1 - \rho)}.$$

The wait is unbounded as $\rho \to 1$. Kingman's approximation extends the result to general distributions: the wait keeps the factor $\rho/(1-\rho)$, multiplied by a term that grows with the variability of the arrivals and of the service [kingman1961].

## Service in windows

A server that attends a queue only at set times is a *polling* or *vacation* system. Its waiting time is dominated by the interval between two visits, and the load accumulated over an interval must be cleared in one visit. The relevant quantity is then the distribution of the load per visit, not the utilization alone [takagi1986].

## Practices

- **Classes of service.** Kanban distinguishes classes of items by the profile of their cost of delay, such as expedite, fixed date, standard and intangible, and serves each under its own policy [anderson2010].
- **Maker's schedule.** Graham opposes the schedule of a manager, cut in hours, to that of a maker, who needs half-days without interruption, and observes that one meeting can destroy a half-day of the second kind [graham2009].

## Bearing on `horai`

- A person who serves requests in windows is a polling system. The [reserve](../kernel/processes/reactive-work.md#^reserve) is therefore sized on a quantile of the load per window, and the condition $\rho < 1$ is kept only as the condition of stability.
- The three [classes of service](../kernel/processes/reactive-work.md#^classes-of-service) of the kernel reduce the classes of Kanban to what one agent needs.
- The [windows](../kernel/objects/horizon.md#^window) between blocks apply the maker's schedule to requests: arrivals are batched so that a block is not cut.
- The assumptions of the model are rough for one person: the service is not exponential, and the arrivals are not independent. The result is used for its direction, not for its values.

## Sources

- [kingman1961] ○ Kingman, "The single server queue in heavy traffic", *Mathematical Proceedings of the Cambridge Philosophical Society*, 57(4), 1961, pp. 902–904
- [anderson2010] ○ Anderson, *Kanban: Successful Evolutionary Change for Your Technology Business*, Blue Hole Press, 2010
- [graham2009] ○ Graham, "Maker's Schedule, Manager's Schedule", 2009
- [takagi1986] ○ Takagi, *Analysis of Polling Systems*, MIT Press, 1986
