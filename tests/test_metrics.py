import pandas as pd

from src.build_metrics import calculate_kpis, department_summary, monthly_trends


def sample_data():
    return pd.DataFrame(
        {
            "encounter_id": [1, 2, 3, 4],
            "encounter_date": pd.to_datetime(["2025-01-01", "2025-01-15", "2025-02-01", "2025-02-10"]),
            "department": ["Primary Care", "Primary Care", "Cardiology", "Cardiology"],
            "region": ["North", "South", "North", "South"],
            "payer": ["Commercial", "Medicare", "Commercial", "Medicaid"],
            "wait_time_minutes": [10, 20, 30, 40],
            "satisfaction_score": [5.0, 4.0, 3.0, 2.0],
            "readmitted_30_days": [0, 0, 1, 1],
            "claim_status": ["Approved", "Denied", "Approved", "Denied"],
            "claim_amount": [100.0, 200.0, 300.0, 400.0],
        }
    )


def test_calculate_kpis():
    kpis = calculate_kpis(sample_data())

    assert kpis["appointment_volume"] == 4
    assert kpis["average_wait_time"] == 25.0
    assert kpis["readmission_rate"] == 50.0
    assert kpis["claim_denial_rate"] == 50.0
    assert kpis["average_satisfaction"] == 3.5


def test_monthly_trends():
    trends = monthly_trends(sample_data())

    assert len(trends) == 2
    assert list(trends["appointment_volume"]) == [2, 2]


def test_department_summary():
    summary = department_summary(sample_data())

    assert set(summary["department"]) == {"Primary Care", "Cardiology"}
    assert summary["total_claim_amount"].sum() == 1000.0

