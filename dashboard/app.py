import streamlit as st
import requests
from google.cloud import bigquery
from streamlit_autorefresh import st_autorefresh
from streamlit_echarts import st_echarts

st.set_page_config(page_title="Cybersecurity Platform", layout="wide")

st.title("🔐 Cybersecurity Anomaly Detection Platform")

tab1, tab2 = st.tabs(["🧠 Manual Prediction", "📡 Live Streaming Monitor"])

# ============================================
# 🧠 TAB 1 — MANUAL PREDICTION
# ============================================

with tab1:

    st.header("Manual Anomaly Check")

    transactions = st.slider("Transactions in last 5 min", 0, 500, 10)
    avg_amount = st.number_input("Average Amount", value=200.0)
    high_risk_flag = st.selectbox("High Risk Flag", [0, 1])

    if st.button("Analyze"):

        try:
            response = requests.post(
                "https://cyber-api-866483429072.us-central1.run.app/predict",
                json={
                    "transactions_last_5min": transactions,
                    "avg_amount": avg_amount,
                    "high_risk_flag": high_risk_flag,
                },
            )

            result = response.json()

            if result["prediction"] == "ANOMALY":
                st.error("🚨 Suspicious Activity Detected!")
            else:
                st.success("✅ Normal Behavior")

            anomaly_score = result["anomaly_score"]

            st.subheader("Anomaly Score")

            option = {
                "series": [
                    {
                        "type": "gauge",
                        "progress": {"show": True},
                        "detail": {"formatter": "{value}%"},
                        "data": [{"value": anomaly_score * 100}],
                    }
                ]
            }

            st_echarts(option, height="300px")

            st.write("Full Response:", result)

        except:
            st.warning("⚠ FastAPI is not running on port 8000.")

# ============================================
# 📡 TAB 2 — LIVE STREAMING
# ============================================

with tab2:

    st.header("Live Streaming Events (From BigQuery)")

    # Auto refresh every 5 seconds
    st_autorefresh(interval=5000, key="refresh")

    client = bigquery.Client()

    query = """
    SELECT
        user_id,
        COUNT(*) as total_events,
        SUM(CASE WHEN event_type='login_fail' THEN 1 ELSE 0 END) as failed_logins,
        SAFE_DIVIDE(
            SUM(CASE WHEN event_type='login_fail' THEN 1 ELSE 0 END),
            COUNT(*)
        ) as failure_rate
    FROM `cyber-security-de2-487020.cyber_dataset.raw_logs`
    GROUP BY user_id
    ORDER BY failure_rate DESC
    LIMIT 50
    """

    df = client.query(query).to_dataframe()

    def highlight(row):
        if row["failure_rate"] > 0.7:
            return ["background-color: red"] * len(row)
        return [""] * len(row)

    styled_df = df.style.apply(highlight, axis=1)

    st.dataframe(styled_df, width="stretch")
