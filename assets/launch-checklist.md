# Launch / Production Readiness Checklist: <Service or feature>

Adapted from SRE book Ch 27 (Launch Coordination Checklist), Appendix E, Ch 32 (PRR), and Site Reliability Workbook Ch 14, 16, 18. Mark each item ✅ / ⚠️ / ❌ / N/A with a note.

## Architecture & dependencies
- [ ] Architecture diagram; request flow from user to backends documented
- [ ] All dependencies listed, with their SLOs and owners; behavior when each is down defined
- [ ] No single points of failure; redundancy across zones/regions as needed
- [ ] Non-critical dependencies fail open / degrade gracefully

## Capacity
- [ ] Expected load estimated (launch spike vs. steady state), including retries (`capacity-estimate-worksheet.md`)
- [ ] Load tested to and beyond expected peak; known breaking point
- [ ] N+2 provisioning (survive planned + unplanned outage)
- [ ] Autoscaling limits and quotas checked

## Reliability & overload
- [ ] SLIs/SLOs defined (`slo-document-template.md`) and error budget policy approved by product, dev and SRE (`error-budget-policy-template.md`)
- [ ] Deadlines/timeouts on all RPCs; propagated downstream
- [ ] Retries bounded, with exponential backoff + jitter, at one layer only
- [ ] Load shedding / rate limiting; graceful degradation plan
- [ ] Health checks don't cause cascading removal under load
- [ ] Caches: behavior on cold cache / cache failure understood

## Monitoring & alerting
- [ ] Four golden signals dashboarded (latency, traffic, errors, saturation)
- [ ] Pages are symptom-based, SLO-driven (multiwindow burn rate), actionable; others route to tickets
- [ ] Alert rules unit-tested (e.g., `promtool test rules`); low-traffic paths checked (`sre_calc.py lowtraffic`)
- [ ] Every page has a runbook/playbook entry
- [ ] Black-box probing of user-facing endpoints

## Release & rollback
- [ ] Reproducible, hermetic builds; config under version control and reviewed
- [ ] Canary / gradual rollout plan with automated health gating, concurrent control group, and defined abort criteria (`canary-plan-template.md`)
- [ ] Config changes go through the same gradual, reversible rollout as binaries; config is hermetic and reviewed
- [ ] Feature flags for risky behavior; tested kill switch
- [ ] Rollback tested and fast; data/schema migrations reversible or staged

## Data
- [ ] Backups configured AND a restore has been tested end-to-end
- [ ] Soft delete / retention for user data; integrity validation
- [ ] Privacy/security review complete

## Operations
- [ ] On-call rotation staffed and trained (drills / wheel of misfortune run); escalation paths defined
- [ ] Incident process known (roles, comms channel, status page)
- [ ] Launch-day plan: timing, who's watching, go/no-go criteria, rollback trigger
- [ ] Toil estimated; manual operations automated or scheduled for automation

## External
- [ ] Customer communication / support briefed
- [ ] Legal, compliance, abuse/anti-DoS considerations
