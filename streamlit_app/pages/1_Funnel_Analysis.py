import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Funnel Analysis", page_icon="🔻", layout="wide")

st.title(" Funnel & Conversion Analysis")
st.markdown("Measuring user progression through the activation funnel and diagnosing conversion gaps.")
st.divider()

# Load data
funnel_df = pd.read_csv("data/funnel.csv")
intensity_df = pd.read_csv("data/usage_intensity.csv")

# ── Funnel Chart ──────────────────────────────────────────
st.subheader("Activation Funnel")

fig_funnel = go.Figure(go.Funnel(
    y=funnel_df["step"],
    x=funnel_df["users"],
    textinfo="value+percent initial",
    marker=dict(color=["#4C6EF5", "#5C8DEF", "#74AADE", "#91C4CC"]),
))
fig_funnel.update_layout(
    height=450,
    margin=dict(l=20, r=20, t=20, b=20)
)
st.plotly_chart(fig_funnel, use_container_width=True)

# ── Key Metrics ───────────────────────────────────────────
st.divider()
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Signups", "1,000")
col2.metric("Activation Rate", "85.3%", delta="-14.7% lost at signup")
col3.metric("Core Feature Usage", "100%", delta="of activated users")
col4.metric("Upgrade Rate", "49%", delta="490 paid users")

# ── Usage Intensity ───────────────────────────────────────
st.divider()
st.subheader("Non-Upgraders by Usage Intensity")
st.markdown("Users who used core features but never upgraded, segmented by engagement level.")

fig_intensity = px.bar(
    intensity_df,
    x="usage_segment",
    y="user_count",
    color="avg_sessions",
    text="user_count",
    color_continuous_scale="Blues",
    labels={
        "usage_segment": "Usage Segment",
        "user_count": "Number of Users",
        "avg_sessions": "Avg Sessions"
    }
)
fig_intensity.update_traces(textposition="outside")
fig_intensity.update_layout(
    height=400,
    margin=dict(l=20, r=20, t=20, b=20),
    coloraxis_showscale=False
)
st.plotly_chart(fig_intensity, use_container_width=True)

# ── Insight Box ───────────────────────────────────────────
st.divider()
st.info("""
** Key Insight:** 164 power users averaging 40 sessions and 15,370 events each remain 
on the free tier. These are the highest priority upgrade targets, deeply habituated users 
who need a nudge, not a pitch.
""")