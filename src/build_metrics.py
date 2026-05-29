from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "healthcare_operations.csv"


def load_data(path: Path = DATA_PATH) -> pd.DataFrame:
    data = pd.read_csv(path, parse_dates=["encounter_date"])
    required = {
        "encounter_id",
        "encounter_date",
        "department",
        "region",
        "payer",
        "wait_time_minutes",
        "satisfaction_score",
        "readmitted_30_days",
        "claim_status",
        "claim_amount",
    }
    missing = required - set(data.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    return data


def calculate_kpis(data: pd.DataFrame) -> dict[str, float]:
    total = len(data)
    if total == 0:
        return {
            "appointment_volume": 0,
            "average_wait_time": 0.0,
            "readmission_rate": 0.0,
            "claim_denial_rate": 0.0,
            "average_satisfaction": 0.0,
        }

    denied_claims = data["claim_status"].eq("Denied").sum()
    return {
        "appointment_volume": int(total),
        "average_wait_time": round(float(data["wait_time_minutes"].mean()), 1),
        "readmission_rate": round(float(data["readmitted_30_days"].mean() * 100), 1),
        "claim_denial_rate": round(float(denied_claims / total * 100), 1),
        "average_satisfaction": round(float(data["satisfaction_score"].mean()), 2),
    }


def monthly_trends(data: pd.DataFrame) -> pd.DataFrame:
    monthly = data.copy()
    monthly["month"] = monthly["encounter_date"].dt.to_period("M").dt.to_timestamp()
    return (
        monthly.groupby("month", as_index=False)
        .agg(
            appointment_volume=("encounter_id", "count"),
            average_wait_time=("wait_time_minutes", "mean"),
            readmission_rate=("readmitted_30_days", "mean"),
            claim_denial_rate=("claim_status", lambda s: s.eq("Denied").mean()),
            average_satisfaction=("satisfaction_score", "mean"),
        )
        .round(
            {
                "average_wait_time": 1,
                "readmission_rate": 3,
                "claim_denial_rate": 3,
                "average_satisfaction": 2,
            }
        )
    )


def department_summary(data: pd.DataFrame) -> pd.DataFrame:
    return (
        data.groupby("department", as_index=False)
        .agg(
            appointment_volume=("encounter_id", "count"),
            average_wait_time=("wait_time_minutes", "mean"),
            readmission_rate=("readmitted_30_days", "mean"),
            claim_denial_rate=("claim_status", lambda s: s.eq("Denied").mean()),
            average_satisfaction=("satisfaction_score", "mean"),
            total_claim_amount=("claim_amount", "sum"),
        )
        .sort_values("appointment_volume", ascending=False)
        .round(
            {
                "average_wait_time": 1,
                "readmission_rate": 3,
                "claim_denial_rate": 3,
                "average_satisfaction": 2,
                "total_claim_amount": 2,
            }
        )
    )

