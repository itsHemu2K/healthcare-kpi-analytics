from __future__ import annotations

import csv
import random
from datetime import date, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "healthcare_operations.csv"


DEPARTMENTS = ["Primary Care", "Cardiology", "Orthopedics", "Pediatrics", "Neurology"]
REGIONS = ["North", "South", "East", "West"]
PAYERS = ["Commercial", "Medicare", "Medicaid", "Self Pay"]
CLAIM_STATUSES = ["Approved", "Approved", "Approved", "Pending", "Denied"]


def build_rows(row_count: int = 750, seed: int = 42) -> list[dict[str, object]]:
    random.seed(seed)
    start = date(2025, 1, 1)
    rows: list[dict[str, object]] = []

    for encounter_id in range(1, row_count + 1):
        encounter_date = start + timedelta(days=random.randint(0, 179))
        department = random.choice(DEPARTMENTS)
        region = random.choice(REGIONS)
        payer = random.choice(PAYERS)

        wait_base = {
            "Primary Care": 18,
            "Cardiology": 28,
            "Orthopedics": 24,
            "Pediatrics": 15,
            "Neurology": 32,
        }[department]
        wait_time = max(3, int(random.gauss(wait_base, 8)))

        satisfaction = max(1.0, min(5.0, round(5.1 - (wait_time / 25) + random.uniform(-0.35, 0.35), 1)))
        readmitted = random.random() < {
            "Primary Care": 0.05,
            "Cardiology": 0.12,
            "Orthopedics": 0.07,
            "Pediatrics": 0.04,
            "Neurology": 0.1,
        }[department]
        claim_status = random.choice(CLAIM_STATUSES)
        claim_amount = round(random.uniform(120, 2200), 2)

        rows.append(
            {
                "encounter_id": encounter_id,
                "encounter_date": encounter_date.isoformat(),
                "department": department,
                "region": region,
                "payer": payer,
                "wait_time_minutes": wait_time,
                "satisfaction_score": satisfaction,
                "readmitted_30_days": int(readmitted),
                "claim_status": claim_status,
                "claim_amount": claim_amount,
            }
        )

    return rows


def write_csv(rows: list[dict[str, object]], output: Path = OUTPUT) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    write_csv(build_rows())
    print(f"Wrote {OUTPUT}")

