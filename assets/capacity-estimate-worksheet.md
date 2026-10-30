# Capacity Estimate Worksheet (NALSD)

Non-abstract large system design: work through the design rounds with real numbers (Site Reliability Workbook Ch 12). Show every assumption, so others can check it.

## 0. Requirements
- What the system does, and its SLOs (latency, availability, freshness, durability):
- Load: peak QPS, average QPS, peak/average ratio, growth over 12–24 months:
- Data: item size, items per day, retention, read/write ratio:
- Constraints: budget, regions, compliance, dependencies:

## 1. Is it possible? (one machine, ignore scale)
Simplest design that meets the functional requirements. List the components and how data flows.

## 2. Can we do better?
Look for simplifications, cheaper algorithms, caching, batching, or precomputation.

## 3. Is it feasible? (scale with numbers)
| Resource | Per-request / per-item cost | × load | Total | Per-machine capacity | Machines needed |
|---|---|---|---|---|---|
| CPU | | | | | |
| RAM | | | | | |
| Disk (capacity) | | | | | |
| Disk (IOPS / throughput) | | | | | |
| Network (egress / ingress) | | | | | |

Reference numbers to sanity-check against (orders of magnitude; adjust for your hardware):
- Memory read: ~100 ns. SSD random read: ~100 µs. HDD seek: ~10 ms.
- Same-datacenter round trip: ~0.5 ms. Cross-continent round trip: ~70–150 ms.
- 1 Gbps NIC: ~125 MB/s. 10 Gbps: ~1.25 GB/s.
- Example from School of SRE: a feed page of 5 × 300 KB images on a 1 Gbps NIC supports only ~83 concurrent page loads per second per host.

## 4. Is it resilient?
- Failure domains: machine → rack/ToR → zone → region. What happens if each is lost?
- **N+2**: capacity still meets peak with one planned and one unplanned loss.
- Dependencies: what happens when each is slow or down? Timeouts, retries (budgeted), fallbacks.
- Overload behaviour: load shedding, criticality, graceful degradation.
- Data: replication, backups, restore time.

## 5. Can we do better?
Cost reductions, simplifications, and removing single points of failure.

## Bill of materials
| Component | Count per region | Regions | Total | Notes |
|---|---|---|---|---|

## Open questions and assumptions to verify
-
