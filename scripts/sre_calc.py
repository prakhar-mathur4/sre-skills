#!/usr/bin/env python3
"""SRE availability / error-budget calculator.

Subcommands:
  downtime <slo%>                         allowed downtime per hour/day/week/month/quarter/year
  budget <slo%> --days D --bad-minutes M  time-based error budget consumed and remaining
  requests <slo%> --total N --failed F    request-based availability and budget
  burn <slo%> --window-days D             burn rates and page/ticket thresholds
  lowtraffic <slo%> --rps R               how many failures the budget allows; is paging viable?
  compose --serial A B ... --parallel C D  availability of serial deps and redundant replicas
"""
import argparse

PERIODS = [("hour", 1 / 24), ("day", 1), ("week", 7), ("30-day month", 30), ("quarter", 91.25), ("year", 365)]


def fmt_minutes(m: float) -> str:
    if m < 1:
        return f"{m * 60:.1f} s"
    if m < 120:
        return f"{m:.1f} min"
    if m < 48 * 60:
        return f"{m / 60:.2f} h"
    return f"{m / 1440:.2f} days"


def downtime(a):
    budget = 1 - a.slo / 100
    print(f"SLO {a.slo}% -> error budget {budget * 100:.4g}%")
    for name, days in PERIODS:
        print(f"  per {name:13s} {fmt_minutes(days * 1440 * budget)}")


def budget(a):
    allowed = a.days * 1440 * (1 - a.slo / 100)
    used = a.bad_minutes / allowed * 100 if allowed else float("inf")
    achieved = 100 * (1 - a.bad_minutes / (a.days * 1440))
    print(f"Window {a.days} days, SLO {a.slo}%")
    print(f"  allowed downtime : {fmt_minutes(allowed)}")
    print(f"  bad minutes      : {fmt_minutes(a.bad_minutes)}")
    print(f"  achieved         : {achieved:.4f}%")
    print(f"  budget consumed  : {used:.1f}%  (remaining {fmt_minutes(max(allowed - a.bad_minutes, 0))})")


def requests(a):
    allowed = a.total * (1 - a.slo / 100)
    achieved = 100 * (1 - a.failed / a.total)
    print(f"SLO {a.slo}% over {a.total:,.0f} requests")
    print(f"  allowed failures : {allowed:,.0f}")
    print(f"  failed           : {a.failed:,.0f}")
    print(f"  achieved         : {achieved:.4f}%")
    print(f"  budget consumed  : {a.failed / allowed * 100:.1f}%")


def burn(a):
    # Multiwindow, multi-burn-rate thresholds (Site Reliability Workbook Ch 5, Table 5-8).
    budget = 1 - a.slo / 100
    print(f"SLO {a.slo}%, {a.window_days}-day window, budget {budget * 100:.4g}%")
    print("  burn rate 1 = budget lasts exactly the window")
    for pct, hours, kind in [(2, 1, "page (long 1h, short 5m)"), (5, 6, "page (long 6h, short 30m)"), (10, 72, "ticket (long 3d, short 6h)")]:
        rate = (pct / 100) * a.window_days * 24 / hours
        print(f"  {pct:>2}% budget in {hours:>2}h -> burn rate {rate:5.1f}, error ratio > {rate * budget * 100:.4g}%  [{kind}]")


def lowtraffic(a):
    # Site Reliability Workbook Ch 5, "Low-Traffic Services and Error Budget Alerting".
    budget = 1 - a.slo / 100
    total = a.rps * a.window_days * 86400
    allowed = total * budget
    per_hour = a.rps * 3600
    print(f"SLO {a.slo}%, {a.rps:g} req/s ({per_hour:,.1f} req/h), {a.window_days:g}-day window")
    print(f"  requests in window : {total:,.0f}")
    print(f"  allowed failures   : {allowed:,.1f}")
    if per_hour > 0:
        one_fail_rate = 1 / per_hour
        print(f"  one failure in 1h  : {one_fail_rate * 100:.3g}% error rate = burn rate {one_fail_rate / budget:,.3g}x,"
              f" {100 / allowed:.1f}% of the window's budget")
    if allowed < 100:
        print("  -> LOW TRAFFIC: single failures dominate. Consider (Workbook Ch 5): synthetic traffic,"
              " grouping related services, client retries with backoff, or a lower SLO / longer window.")
    else:
        print("  -> Enough traffic for standard multiwindow burn-rate alerting.")


def compose(a):
    serial = 1.0
    for x in a.serial or []:
        serial *= x / 100
    parallel = None
    if a.parallel:
        miss = 1.0
        for x in a.parallel:
            miss *= 1 - x / 100
        parallel = 1 - miss
        print(f"  parallel replicas {a.parallel} -> {parallel * 100:.5f}% (assumes independent failures)")
    if a.serial:
        print(f"  serial chain {a.serial} -> {serial * 100:.5f}%")
    total = serial * (parallel if parallel is not None else 1)
    print(f"Combined availability: {total * 100:.5f}%  (budget {(1 - total) * 100:.4g}%)")


p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
sub = p.add_subparsers(dest="cmd", required=True)
s = sub.add_parser("downtime"); s.add_argument("slo", type=float); s.set_defaults(f=downtime)
s = sub.add_parser("budget"); s.add_argument("slo", type=float); s.add_argument("--days", type=float, default=30); s.add_argument("--bad-minutes", type=float, required=True); s.set_defaults(f=budget)
s = sub.add_parser("requests"); s.add_argument("slo", type=float); s.add_argument("--total", type=float, required=True); s.add_argument("--failed", type=float, required=True); s.set_defaults(f=requests)
s = sub.add_parser("burn"); s.add_argument("slo", type=float); s.add_argument("--window-days", type=float, default=30); s.set_defaults(f=burn)
s = sub.add_parser("lowtraffic"); s.add_argument("slo", type=float); s.add_argument("--rps", type=float, required=True); s.add_argument("--window-days", type=float, default=28); s.set_defaults(f=lowtraffic)
s = sub.add_parser("compose"); s.add_argument("--serial", type=float, nargs="+"); s.add_argument("--parallel", type=float, nargs="+"); s.set_defaults(f=compose)
args = p.parse_args()
args.f(args)
