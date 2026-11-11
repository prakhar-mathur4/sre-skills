---
tags: [skill-creator]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

hey, this is our infra repo (terraform, k8s manifests and our prometheus alerts are in this folder). we want to make the platform more reliable. what SLOs and alerts should we have?

Input files: terraform/main.tf, k8s/storefront-api.yaml, k8s/order-worker.yaml, monitoring/alerts.yaml
