# Healthcare KPI Analytics Dashboard

Python and SQL portfolio project for monitoring operational healthcare KPIs using synthetic data. The project demonstrates data generation, data cleansing, KPI calculation, SQL reporting, trend analysis, validation, and dashboard development.

This repository is intentionally built with synthetic data for public portfolio use. It does not contain employer data, protected health information, or proprietary claims extracts.

## Highlights

- Builds a synthetic healthcare operations dataset with encounters, departments, wait times, satisfaction scores, claim status, and readmission indicators.
- Calculates reporting KPIs including appointment volume, average wait time, readmission rate, claim denial rate, and patient satisfaction.
- Includes SQL queries for business reporting and operational analysis.
- Provides a Streamlit dashboard for interactive KPI monitoring and trend exploration.
- Includes tests for the metric-building logic.

## Tech Stack

Python, SQL, Pandas, Plotly, Streamlit, Pytest

## Project Structure

```text
data/
  healthcare_operations.csv
sql/
  kpi_queries.sql
src/
  build_metrics.py
  dashboard.py
  generate_data.py
tests/
  test_metrics.py
```

## Run Locally

Install dependencies:

```bash
pip install -r requirements.txt
```

Regenerate the sample dataset:

```bash
python src/generate_data.py
```

Run the dashboard:

```bash
streamlit run src/dashboard.py
```

Run tests:

```bash
pytest
```

## KPI Definitions

- **Appointment volume:** Count of encounters in the selected period.
- **Average wait time:** Mean wait time in minutes before appointment start.
- **Readmission rate:** Percent of encounters marked as readmitted within 30 days.
- **Claim denial rate:** Percent of encounters with denied claims.
- **Average satisfaction:** Mean patient satisfaction score on a 1-5 scale.

## Data Note

All data in this repository is synthetic and intended for portfolio and demonstration use only. The project is designed to show the structure of a healthcare analytics workflow without exposing confidential or regulated data.

