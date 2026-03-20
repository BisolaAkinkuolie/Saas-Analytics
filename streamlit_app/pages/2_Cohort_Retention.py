import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Cohort Retention", page_icon=" ", layout="wide")

st.title(" Cohort Retention Analysis")
st.markdown("Tracking month-over-month retention for every signup cohort over a 6 month window.")
st.divider()

# Load data
df = pd.read_csv("data/cohort_retention.csv")

# ── Key Metrics ───────────────────────────────────────────
col1, col2, col3 = st.columns(3)
col1.metric("Avg Month-0 Retention", "83.4%")
col2.metric("Avg Month-6 Retention", "84.9%")
col3.metric("Best Cohort at Month-6", "92.5%")
st.divider()

# ── Retention Heatmap ─────────────────────────────────────
st.subheader("Retention Heatmap by Cohort")
st.markdown("Each cell shows the % of users from that cohort still active N months after signup.")

heatmap_df = df.pivot_table(
    index="cohort_month",
    columns="months_since_signup",
    values="retention_rate"
).round(1)

heatmap_df.index = heatmap_df.index.astype(str).str[:7]
heatmap_df.columns = [f"Month {c}" for c in heatmap_df.columns]

fig_heatmap = px.imshow(
    heatmap_df,
    color_continuous_scale="Blues",
    text_auto=True,
    aspect="auto",
    labels=dict(x="Months Since Signup", y="Cohort Month", color="Retention %")
)
fig_heatmap.update_layout(
    height=500,
    margin=dict(l=20, r=20, t=20, b=20)
)
st.plotly_chart(fig_heatmap, use_container_width=True)

# ── Average Retention Line Chart ──────────────────────────
st.divider()
st.subheader("Average Retention Rate Across All Cohorts")
st.markdown("How retention evolves month by month when averaged across all cohorts.")

avg_retention = df.groupby("months_since_signup")["retention_rate"].agg(
    avg="mean",
    worst="min",
    best="max"
).round(1).reset_index()

fig_line = px.line(
    avg_retention,
    x="months_since_signup",
    y=["avg", "worst", "best"],
    markers=True,
    labels={
        "months_since_signup": "Months Since Signup",
        "value": "Retention Rate (%)",
        "variable": "Metric"
    },
    color_discrete_map={
        "avg": "#4C6EF5",
        "worst": "#FA5252",
        "best": "#40C057"
    }
)
fig_line.update_layout(
    height=400,
    margin=dict(l=20, r=20, t=20, b=20),
    yaxis=dict(ticksuffix="%")
)
st.plotly_chart(fig_line, use_container_width=True)

st.divider()
st.info("""
** Key Insight:** Retention slightly increases over time (83.4% → 84.9%), 
indicating natural selection , disengaged users churn early leaving a highly 
engaged sticky core. The spread between worst (70%) and best (92.5%) cohorts 
at month 6 warrants investigation into acquisition channel and plan tier mix.
""")