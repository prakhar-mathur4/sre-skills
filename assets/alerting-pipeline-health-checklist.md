# Alerting Pipeline Health Checklist: <System / team>

Use this to prove that an alert would actually reach a human, and to catch things that fail silently, like an expired certificate. It works on its own, and it backs the alerting section of `reliability-gap-assessment.md`. Based on SRE book Ch 6 and 10; Workbook Ch 4, 5. Examples use Prometheus, Alertmanager and a PagerDuty-style pager; translate to your tools.

**Checked by:** <name>  **Date:** <YYYY-MM-DD>  **Scope:** <services, environments, alert routes>

Mark each item ✅ / ⚠️ / ❌ / ❓. Only mark ✅ for something you saw work (a test result, a config, an acknowledgement), not something you were told.

## 1. Silence is not health
An empty alert list proves nothing until you know the signal could have fired. A query that returns no series is not the same as zero errors: if the exporter, scrape job or log pipeline died, the data is absent and a rule like `errors > 0` stays quiet forever.

- [ ] For each paging alert, you can name how you know its input data is still arriving (for example `absent()`, `up == 0`, or a freshness check).
- [ ] Rules on ratios and counters handle missing data on purpose (alert on absence, or document why not).
- [ ] You have seen each paging alert fire at least once, in production or in a test.

## 2. Heartbeat (dead man's switch)
An alert that always fires, sent to an **external** receiver that pages you when the heartbeats stop arriving. It covers the whole chain at once: rule evaluation, the alert manager, the network path and the integration.

- [ ] A heartbeat rule exists and is always firing (sample below).
- [ ] The receiver lives **outside** the monitoring stack and outside the production failure domain (a hosted heartbeat or cron-monitor service, or a separate account/region). Something that depends on the thing being watched can't tell you it died.
- [ ] The receiver pages a human when the heartbeat is missing for N minutes (pick N from your repeat interval, usually 2-3x).
- [ ] The heartbeat has a named owner, and that owner is not "the monitoring stack".

## 3. End-to-end synthetic test alert
A heartbeat shows messages are flowing. A scheduled test shows a person gets them.

- [ ] A synthetic alert runs on a schedule (for example weekly, and after any routing or integration change).
- [ ] It travels the real path: source -> rule -> route -> receiver -> **a human acknowledges it**. A delivered notification nobody acknowledged isn't a pass.
- [ ] The test alert is labelled so it is obviously a test and doesn't create a real incident.
- [ ] Failed tests create a ticket with an owner.

## 4. Owners and escalation
- [ ] Every alert route has a named owner (a team or rotation, not a person who may leave).
- [ ] Every route that pages has an escalation: secondary, then manager or incident commander.
- [ ] Every warning or ticket channel has a named owner who reads it on a schedule. A warning channel nobody owns doesn't count as coverage.
- [ ] There is a catch-all route, so an alert with an unexpected label set doesn't vanish. The catch-all has an owner too.
- [ ] Contact details and on-call schedules are current (checked this quarter).

## 5. Integration and configuration health
- [ ] Pager/chat integration credentials: expiry dates are known, and rotation doesn't silently break delivery (check keys, tokens, webhook URLs).
- [ ] Pager services and integrations are enabled, not disabled or in a "paused" state.
- [ ] No maintenance window left on past its end date, and no stale silences. List them regularly (read-only commands below).
- [ ] Silences have an owner, a reason and an expiry. Never silence an alert to "fix" a noisy one; fix or remove the rule (SRE book Ch 6, Workbook Ch 5).

## 6. Alert on the alerting system itself
- [ ] Notification failures are alerted on (for Alertmanager: `alertmanager_notifications_failed_total` rising per integration).
- [ ] Rule evaluation failures and slow evaluations are alerted on (for Prometheus: `prometheus_rule_evaluation_failures_total`, missed iterations).
- [ ] Scrape/ingest health, config reload failures and storage or queue saturation are alerted on.
- [ ] These meta-alerts route through a path that doesn't depend on the component that is failing (see section 7).

## 7. Separate failure domains
If the thing that broke production also breaks your ability to see or fix it, you are blind at the worst moment (SRE book Ch 6, Ch 14).

- [ ] Monitoring and alerting don't share the production failure domain (cluster, region, account, network, DNS).
- [ ] An external black-box probe from outside your network checks the critical user journeys.
- [ ] The status page is hosted outside production.
- [ ] Runbooks and incident docs are readable when production (and its SSO) is down; a printed or offline copy exists for the top few.
- [ ] Out-of-band communication exists (a chat or phone bridge that doesn't depend on your own infrastructure or SSO).
- [ ] Break-glass access works without the identity provider being up, is audited, and has been tested.

## 8. Rolling out these checks safely
- [ ] New heartbeat and watchdog alerts go to a **non-paging** channel first. A flaky watchdog that pages will create a paging storm and teach people to ignore it. Promote to paging after about a week without false alarms.
- [ ] Change routing in one place at a time, and run the test alert (section 3) after each change.
- [ ] Keep the old route until the new one has passed an end-to-end test.

## How to test it

Start with read-only checks. These only read state and don't notify anyone. Flags vary a little by version; adjust `--alertmanager.url` to your setup.

```bash
# What is firing right now? (read-only)
amtool alert query --alertmanager.url=http://localhost:9093

# Which silences exist, and when do they expire? (read-only)
amtool silence query --alertmanager.url=http://localhost:9093

# Validate the config file parses (read-only)
amtool check-config alertmanager.yml

# Which receiver would this label set go to? (read-only, offline)
amtool config routes test --config.file=alertmanager.yml \
  severity=page service=checkout

# Show the whole routing tree (read-only)
amtool config routes show --config.file=alertmanager.yml
```

Check that every paging label set you care about routes to a receiver with an owner, and that something unexpected lands in the catch-all rather than nowhere.

### Sample heartbeat rule (Prometheus)
```yaml
groups:
  - name: pipeline-health
    rules:
      - alert: Heartbeat
        expr: vector(1)        # always true, so it always fires
        labels:
          severity: heartbeat  # route on this label, see below
        annotations:
          summary: "Always-firing heartbeat; absence means the alert pipeline is broken."
```

Routing note: send `severity="heartbeat"` to a dedicated receiver that forwards to the **external** heartbeat service, with a short `repeat_interval` (for example 1 minute) so the receiver notices quickly when messages stop. Don't send it to your normal paging or chat receivers. The page comes from the external service when heartbeats stop, not from the heartbeat alert itself.

### Send a test alert (⚠️ notifies real people)
- **Affects:** whoever is on the receiving route, and anything that auto-creates incidents from it.
- **Reversible?** The notification can't be unsent. The alert resolves on its own after its end time.
- **Before:** label it clearly as a test, tell the on-call, and use the least-noisy route that still exercises the full path. Start with a non-paging channel.
- **Undo:** resolve or expire the test alert, and close any incident or ticket it opened.

```bash
amtool alert add SyntheticPipelineTest severity=test service=pipeline-check \
  --annotation=summary="Scheduled pipeline test, please acknowledge" \
  --alertmanager.url=http://localhost:9093
```

## Time bombs: things that expire
Certificates, credentials, API keys, domain registrations, quotas and licences all fail on a date or a threshold, usually with no traffic-based signal beforehand. They break everything at once.

- [ ] An inventory exists listing each item, what it protects, its expiry or limit, and a named **owner**. Build it from discovery (scan endpoints, secret stores, registrar, cloud quota pages), not memory.
- [ ] Tiered alerts reach a pager **before the point of no return**. A common shape: ticket at about 30 days, business-hours page at about 14, page at about 7. Scale these to how long a renewal really takes (a domain transfer or a vendor-signed certificate can take weeks; an automated ACME renewal takes minutes).
- [ ] Rule of thumb: page when the remaining time is shorter than the time needed to renew, plus margin.
- [ ] Renewal is automated where possible, **and** a renewal-failure alert exists, so a silently broken renewer is noticed long before expiry.
- [ ] Quotas and licences alert on both usage trend and distance to the limit.
- [ ] Expiry checks are done from outside, on what clients actually see (not only on the file on disk).

Example expiry alerts (Prometheus with a blackbox exporter; adjust metric names):
```yaml
- alert: CertExpiryTicket
  expr: (probe_ssl_earliest_cert_expiry - time()) < 30 * 86400
  labels: {severity: ticket}
- alert: CertExpiryPage
  expr: (probe_ssl_earliest_cert_expiry - time()) < 7 * 86400
  labels: {severity: page}
```

### ⚠️ EMERGENCY REISSUE: read before replacing a certificate in a hurry
Reissuing under pressure causes second outages.

- **Affects:** every client of the endpoint. Clients that pin the old certificate or key, and mTLS peers that trust a specific issuer or fingerprint, can start failing the moment you swap.
- **Reversible?** Only if you kept the old files and the old certificate hasn't expired. A revoked or expired certificate can't be restored.
- **Rate limits:** repeated failed ACME orders can hit the CA's rate limits and lock you out of issuing for days. Don't retry in a loop.

Do this in order:
1. **Read-only first.** Check the CAA records (`dig CAA example.com`) so the CA you plan to use is allowed. List who pins the certificate or key (mobile apps, partners, mTLS peers, config in other repos).
2. Keep the old certificate, key and chain, backed up and labelled.
3. Issue the new certificate and **validate it on one endpoint or one load balancer** first (use a staging or test name if the CA offers one).
4. Swap **one load balancer at a time**, checking error rates between each.
5. Verify from outside: the full chain (`openssl s_client -connect host:443 -servername host -showcerts`) and the SAN list covers every hostname served.
6. Have a rollback ready: how to put the old certificate back, and who does it.
7. Afterwards, fix the cause (broken renewer, no owner, no alert) and add it to the inventory.
