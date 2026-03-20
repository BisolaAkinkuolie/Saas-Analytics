import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Power Users", page_icon="🏆", layout="wide")

st.title(" Power User Scoring")
st.markdown("Composite engagement scoring model identifying user segments by product behaviour.")
st.divider()

# Load data
df = pd.read_csv("data/power_user_segments.csv")

# ── Key Metrics ───────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
col1.metric("Champion Users", "354", help="Power score ≥ 18")
col2.metric("Power Users", "289", help="Power score 14-17")
col3.metric("Regular Users", "138", help="Power score 10-13")
col4.metric("Casual Users", "219", help="Power score 6-9")
st.divider()

# ── Segment Distribution ──────────────────────────────────
st.subheader("User Segment Distribution")

col1, col2 = st.columns(2)

with col1:
    fig_pie = px.pie(
        df,
        names="user_segment",
        values="user_count",
        color="user_segment",
        color_discrete_map={
            "Champion": "#4C6EF5",
            "Power User": "#40C057",
            "Regular": "#F59F00",
            "Casual": "#FA5252",
            "At Risk": "#868E96"
        },
        hole=0.4
    )
    fig_pie.update_layout(
        height=380,
        margin=dict(l=20, r=20, t=20, b=20)
    )
    st.plotly_chart(fig_pie, use_container_width=True)

with col2:
    fig_bar = px.bar(
        df,
        x="user_segment",
        y="user_count",
        color="user_segment",
        text="user_count",
        color_discrete_map={
            "Champion": "#4C6EF5",
            "Power User": "#40C057",
            "Regular": "#F59F00",
            "Casual": "#FA5252",
            "At Risk": "#868E96"
        },
        labels={
            "user_segment": "Segment",
            "user_count": "Number of Users"
        }
    )
    fig_bar.update_traces(textposition="outside", showlegend=False)
    fig_bar.update_layout(
        height=380,
        margin=dict(l=20, r=20, t=20, b=20)
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# ── Engagement Comparison ─────────────────────────────────
st.divider()
st.subheader("Engagement Metrics by Segment")
st.markdown("How each segment compares across key behavioural dimensions.")

metric = st.selectbox(
    "Select metric to compare:",
    options=["avg_sessions", "avg_events", "avg_features_used", "avg_active_months", "avg_events_per_session"],
    format_func=lambda x: x.replace("avg_", "Avg ").replace("_", " ").title()
)

fig_compare = px.bar(
    df,
    x="user_segment",
    y=metric,
    color="user_segment",
    text=metric,
    color_discrete_map={
        "Champion": "#4C6EF5",
        "Power User": "#40C057",
        "Regular": "#F59F00",
        "Casual": "#FA5252",
        "At Risk": "#868E96"
    },
    labels={
        "user_segment": "Segment",
        metric: metric.replace("avg_", "Avg ").replace("_", " ").title()
    }
)
fig_compare.update_traces(textposition="outside", showlegend=False)
fig_compare.update_layout(
    height=400,
    margin=dict(l=20, r=20, t=20, b=20)
)
st.plotly_chart(fig_compare, use_container_width=True)

# ── Segment Breakdown Table ───────────────────────────────
st.divider()
st.subheader("Full Segment Breakdown")
st.dataframe(
    df.rename(columns={
        "user_segment": "Segment",
        "user_count": "Users",
        "avg_sessions": "Avg Sessions",
        "avg_events": "Avg Events",
        "avg_features_used": "Avg Features Used",
        "avg_active_months": "Avg Active Months",
        "avg_events_per_session": "Avg Events/Session"
    }),
    use_container_width=True,
    hide_index=True
)

st.divider()
st.info("""
** Key Insight:** 35% of users qualify as Champions averaging 38 sessions 
and 17 unique features used. Champions on starter plans are the highest-value 
upsell targets, deeply engaged users paying entry-level prices. The Casual 
segment (219 users, 2.9 avg sessions) represents the prime re-engagement opportunity.
""")