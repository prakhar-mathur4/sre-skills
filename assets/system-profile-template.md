# System Profile: <System / product>

Save this as `sre-context.md` in the repo root (or wherever your team keeps ops docs). The agent reads it at the start of every reliability task, so reviews, SLOs and incident help start from your real system instead of assumptions. Based on what a production readiness review needs to know (SRE book Ch 27, 32; Workbook Ch 18).

**Last updated:** <YYYY-MM-DD>  **Updated by:** <name or "agent, confirmed by name">
**Sources read:** <repos and paths read: Terraform, Helm/K8s manifests, code, alert rules, dashboards>
**Not read / no access:** <anything the profile can't speak for>

Mark anything not confirmed by a file or by the owning team as ❓. Never put secrets, tokens, internal hostnames you can't share, or customer data in this file.

## 1. Product and users
- What the product does, in one or two sentences:
- Who uses it (consumers, businesses, internal teams) and when (time zones, peak hours, seasonal peaks):
- The 2–3 user flows that matter most (e.g., login, checkout, search), and what "broken" means for each:
- Commitments: SLAs, contracts, regulatory requirements:

## 2. Where it runs
- Platform: <VMs / Kubernetes / Docker / serverless / managed services>
- Cloud and regions: <provider, regions, zones; single- or multi-region>
- Infrastructure as code: <Terraform / Pulumi / CloudFormation / none; repo path>
- Deploys: <how code and config reach production; canary or all at once; who can push>

## 3. Components and dependencies

| Component | What it does | Runs on | Talks to | Stateful? | Owner |
|---|---|---|---|---|---|
| | | | | | |

Critical path for each important flow (e.g., `web → api-gateway → payments-api → ledger-service → Postgres`):
-

External dependencies (payment provider, DNS, CDN, auth, email):
-

## 4. Traffic and scale
- Requests per second, peak and average, for each important flow:
- Data size and growth:
- Low-traffic paths (too quiet for burn-rate paging; check with `sre_calc.py lowtraffic`):

## 5. Observability today
- Metrics: <Prometheus / Datadog / New Relic / CloudWatch …>
- Logs and traces: <tool, retention>
- Dashboards that on-call actually uses:
- Alerting: <where rules live, how many pages a week, where they route>
- SLOs today: <none / list with targets and windows>

## 6. Team and on-call
- Team size and time zones:
- On-call rotation and escalation:
- Runbooks: <where, how current>

## 7. Known risks and history
- Recent incidents and their triggers (last 6–12 months):
- Known fragile parts, single points of failure, manual steps:

## 8. Open questions
Things the agent couldn't verify and needs answered:
-
