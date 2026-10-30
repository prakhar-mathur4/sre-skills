"""Tests for scripts/sre_calc.py. Run from the repo root:

    python3 -m unittest discover -s tests

Expected values are worked out by hand (and match Site Reliability Workbook Ch 5, Table 5-8
for the burn rates).
"""
import pathlib
import subprocess
import sys
import unittest

CALC = pathlib.Path(__file__).resolve().parent.parent / "scripts" / "sre_calc.py"


def calc(*args):
    out = subprocess.run([sys.executable, str(CALC), *args], capture_output=True, text=True)
    if out.returncode != 0:
        raise AssertionError(f"sre_calc.py {' '.join(args)} failed:\n{out.stderr}")
    return out.stdout


class Downtime(unittest.TestCase):
    def test_three_nines(self):
        out = calc("downtime", "99.9")
        self.assertIn("error budget 0.1%", out)
        self.assertIn("43.2 min", out)  # 30 days * 1440 * 0.001
        self.assertIn("8.76 h", out)  # 365 days * 24 * 0.001


class Budget(unittest.TestCase):
    def test_time_based(self):
        out = calc("budget", "99.9", "--days", "28", "--bad-minutes", "25")
        self.assertIn("40.3 min", out)  # 28 * 1440 * 0.001 = 40.32
        self.assertIn("budget consumed  : 62.0%", out)  # 25 / 40.32

    def test_request_based(self):
        out = calc("requests", "99.9", "--total", "4.2e7", "--failed", "31000")
        self.assertIn("allowed failures : 42,000", out)
        self.assertIn("budget consumed  : 73.8%", out)


class BurnRate(unittest.TestCase):
    def test_30_day_window(self):
        out = calc("burn", "99.9", "--window-days", "30")
        self.assertIn("burn rate  14.4", out)
        self.assertIn("burn rate   6.0", out)
        self.assertIn("burn rate   1.0", out)

    def test_28_day_window(self):
        out = calc("burn", "99.9", "--window-days", "28")
        self.assertIn("burn rate  13.4", out)
        self.assertIn("burn rate   5.6", out)


class LowTraffic(unittest.TestCase):
    def test_low_traffic_flagged(self):
        out = calc("lowtraffic", "99.9", "--rps", "0.003")
        self.assertIn("allowed failures   : 7.3", out)
        self.assertIn("LOW TRAFFIC", out)

    def test_high_traffic_ok(self):
        out = calc("lowtraffic", "99.9", "--rps", "100")
        self.assertIn("Enough traffic", out)


class Compose(unittest.TestCase):
    def test_serial_and_parallel(self):
        out = calc("compose", "--serial", "99.95", "99.9", "--parallel", "99.5", "99.5")
        self.assertIn("serial chain [99.95, 99.9] -> 99.85005%", out)  # 0.9995 * 0.999
        self.assertIn("parallel replicas [99.5, 99.5] -> 99.99750%", out)  # 1 - 0.005^2
        self.assertIn("Combined availability: 99.84755%", out)


if __name__ == "__main__":
    unittest.main()
