"""Validate the strictly synthetic DataBridge project-operations scenario.

No external services, libraries or real company data are used.
Run from project repo root: python cases/databridge/verify.py
"""
from pathlib import Path
import csv

FILE = Path(__file__).resolve().parent / "data" / "monthly_delivery_simulated.csv"
EXPECTED_MONTHS = [f"2026-{m:02d}" for m in range(2, 10)]
EXPECTED_SOURCE = "synthetic_scenario"
FIELDS = (
    "planned_deliverables",
    "accepted_deliverables",
    "deferred_deliverables",
    "planned_hours",
    "actual_hours",
)

with FILE.open(encoding="utf-8-sig", newline="") as f:
    rows = list(csv.DictReader(f))

assert len(rows) == 8, f"Expected 8 months, got {len(rows)}"
assert [row["month"] for row in rows] == EXPECTED_MONTHS, "Invalid month sequence"

for row in rows:
    assert row["source_type"] == EXPECTED_SOURCE, "Source must be labeled synthetic"
    for field in FIELDS:
        row[field] = int(row[field])
        assert row[field] >= 0, f"Negative {field} for {row['month']}"
    assert row["planned_deliverables"] > 0
    assert row["accepted_deliverables"] + row["deferred_deliverables"] == row["planned_deliverables"], (
        f"Inconsistent monthly delivery balance in {row['month']}"
    )

totals = {field: sum(row[field] for row in rows) for field in FIELDS}
expected = {
    "planned_deliverables": 65,
    "accepted_deliverables": 59,
    "deferred_deliverables": 6,
    "planned_hours": 696,
    "actual_hours": 722,
}
assert totals == expected, f"Totals differ: {totals}"

acceptance_pct = 100 * totals["accepted_deliverables"] / totals["planned_deliverables"]
hours_variance = totals["actual_hours"] - totals["planned_hours"]
hours_variance_pct = 100 * hours_variance / totals["planned_hours"]

assert round(acceptance_pct, 1) == 90.8
assert hours_variance == 26
assert round(hours_variance_pct, 1) == 3.7

print("DataBridge synthetic scenario: PASS")
print(f"Months: {len(rows)}")
print(f"Delivered: {totals['accepted_deliverables']}/{totals['planned_deliverables']} ({acceptance_pct:.1f}%)")
print(f"Hours: {totals['actual_hours']}/{totals['planned_hours']} (+{hours_variance}, +{hours_variance_pct:.1f}%)")
print("All figures are simulated, not real employment or company performance.")
