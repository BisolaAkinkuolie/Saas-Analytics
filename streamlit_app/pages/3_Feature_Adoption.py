import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Feature Adoption", page_icon="", layout="wide")

st.title(" Feature Adoption Analysis")
st.markdown("Measuring feature adoption rates across the product catalog.")
st.divider()

# Load data
df = pd.read_csv("data/feature_adoption.csv")

# ── Key Metrics ───────────────────────────────────────────
col1, col2, col3 = st.columns(3)
col1.metric("Avg Core Feature Adoption", "85%")
col2.metric("Avg Premium Feature Adoption", "42%")
col3.metric("Total Features", "20")
st.divider()

# ── Filter ────────────────────────────────────────────────
feature_type = st.radio(
    "Filter by feature type:",
    options=["All", "Free", "Premium"],
    horizontal=True
)

if feature_type != "All":
    filtered_df = df[df["feature_type"] == feature_type]
else:
    filtered_df = df

# ── Adoption Rate Bar Chart ───────────────────────────────
st.subheader("Feature Adoption Rate")
st.markdown("Percentage of total users who have used each feature at least once.")

fig_adoption = px.bar(
    filtered_df.sort_values("adoption_rate", ascending=True),
    x="adoption_rate",
    y="feature_name",
    color="feature_type",
    orientation="h",
    text="adoption_rate",
    color_discrete_map={
        "Free": "#4C6EF5",
        "Premium": "#F59F00"
    },
    labels={
        "adoption_rate": "Adoption Rate (%)",
        "feature_name": "Feature",
        "feature_type": "Feature Type"
    }
)
fig_adoption.update_traces(texttemplate="%{text}%", textposition="outside")
fig_adoption.update_layout(
    height=550,
    margin=dict(l=20, r=20, t=20, b=20),
    xaxis=dict(ticksuffix="%")
)
st.plotly_chart(fig_adoption, use_container_width=True)

# ── Events Per User Chart ─────────────────────────────────
st.divider()
st.subheader("Engagement Intensity by Feature")
st.markdown("Average number of events per user for each feature — measures stickiness, not just reach.")

fig_intensity = px.bar(
    filtered_df.sort_values("events_per_user", ascending=True),
    x="events_per_user",
    y="feature_name",
    color="feature_type",
    orientation="h",
    text="events_per_user",
    color_discrete_map={
        "Free": "#4C6EF5",
        "Premium": "#F59F00"
    },
    labels={
        "events_per_user": "Avg Events Per User",
        "feature_name": "Feature",
        "feature_type": "Feature Type"
    }
)
fig_intensity.update_traces(textposition="outside")
fig_intensity.update_layout(
    height=550,
    margin=dict(l=20, r=20, t=20, b=20)
)
st.plotly_chart(fig_intensity, use_container_width=True)

st.divider()
st.info("""
** Key Insight:** Premium features average 12-13 events per user vs core 
features at 19-20 , suggesting premium features lack stickiness relative 
to their price point. A product team would investigate whether users fully 
understand the value of what they're paying for.
""")