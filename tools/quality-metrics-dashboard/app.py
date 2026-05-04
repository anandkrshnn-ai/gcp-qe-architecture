import streamlit as st
import pandas as pd
import numpy as np

# Mocking GCP Cloud Monitoring Data Extraction for demonstration
def fetch_dora_metrics():
    # In a real tool, this would query BigQuery or Cloud Monitoring
    return {
        "deployment_frequency": "Daily",
        "lead_time": "4 hours",
        "change_failure_rate": "2.5%",
        "mttr": "45 mins"
    }

def fetch_defect_escape_rate():
    # Mock data showing trend
    dates = pd.date_range(start="2026-01-01", periods=5, freq='M')
    rates = [40, 25, 15, 8, 3] # Drastic reduction over time
    return pd.DataFrame({"Date": dates, "Defect Escape Rate (%)": rates})

st.set_page_config(page_title="QE Architecture Dashboard", layout="wide")

st.title("🚀 GCP Quality Engineering Metrics Dashboard")
st.markdown("Real-time visibility into DORA metrics, SLO burn rates, and Defect Escape trends.")

st.divider()

# DORA Metrics Section
st.header("1. DORA Metrics (Elite Performer Tracking)")
col1, col2, col3, col4 = st.columns(4)
metrics = fetch_dora_metrics()

col1.metric("Deployment Frequency", metrics["deployment_frequency"], "Improved")
col2.metric("Lead Time for Changes", metrics["lead_time"], "-2 hours")
col3.metric("Change Failure Rate", metrics["change_failure_rate"], "-1.5%")
col4.metric("Time to Restore Service", metrics["mttr"], "-15 mins")

st.divider()

# Defect Escape Section
st.header("2. Defect Escape Analysis")
st.markdown("Percentage of bugs found in production vs. pre-production.")
df_defects = fetch_defect_escape_rate()
st.line_chart(df_defects.set_index("Date"))

st.divider()

# SLO Burn Rate Section
st.header("3. Active SLO Burn Rates")
st.markdown("If Error Budget > 100%, deployments are automatically gated.")

slo_data = pd.DataFrame({
    "Service": ["Payment API", "Catalog Service", "Inventory Sync"],
    "Tier": ["Tier 1", "Tier 2", "Tier 3"],
    "Target SLO": ["99.99%", "99.9%", "99.0%"],
    "Current SLI": ["99.995%", "99.92%", "98.5%"],
    "Error Budget Consumed": [50, 80, 150], # 150 means violation
})

def color_budget(val):
    color = 'red' if val > 100 else 'green' if val < 80 else 'orange'
    return f'color: {color}'

st.dataframe(slo_data.style.map(color_budget, subset=['Error Budget Consumed']))

st.sidebar.title("Configuration")
st.sidebar.text_input("GCP Project ID", value="my-production-project")
st.sidebar.button("Refresh Data")
