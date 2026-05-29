from __future__ import annotations

import plotly.express as px
import streamlit as st

from build_metrics import calculate_kpis, department_summary, load_data, monthly_trends


st.set_page_config(page_title="Healthcare KPI Analytics", layout="wide")

st.title("Healthcare KPI Analytics")
st.caption("Synthetic operational dataset for KPI reporting and dashboard development.")

data = load_data()

departments = sorted(data["department"].unique())
regions = sorted(data["region"].unique())

with st.sidebar:
    selected_departments = st.multiselect("Department", departments, default=departments)
    selected_regions = st.multiselect("Region", regions, default=regions)

filtered = data[
    data["department"].isin(selected_departments)
    & data["region"].isin(selected_regions)
]

kpis = calculate_kpis(filtered)
cols = st.columns(5)
cols[0].metric("Appointments", f"{kpis['appointment_volume']:,}")
cols[1].metric("Avg Wait", f"{kpis['average_wait_time']} min")
cols[2].metric("Readmission", f"{kpis['readmission_rate']}%")
cols[3].metric("Claim Denial", f"{kpis['claim_denial_rate']}%")
cols[4].metric("Avg Satisfaction", f"{kpis['average_satisfaction']}/5")

trend_data = monthly_trends(filtered)
dept_data = department_summary(filtered)

left, right = st.columns(2)

with left:
    st.subheader("Monthly Appointment Volume")
    st.plotly_chart(
        px.line(trend_data, x="month", y="appointment_volume", markers=True),
        use_container_width=True,
    )

with right:
    st.subheader("Average Wait Time by Department")
    st.plotly_chart(
        px.bar(dept_data, x="department", y="average_wait_time", color="department"),
        use_container_width=True,
    )

st.subheader("Department KPI Summary")
st.dataframe(dept_data, use_container_width=True)

