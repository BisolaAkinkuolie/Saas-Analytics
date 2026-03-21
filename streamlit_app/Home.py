import streamlit as st


st.set_page_config(
    page_title="SaaS Product Analytics",
    page_icon="📊",
    layout="wide"
)

st.title(" SaaS Product Analytics Platform")
st.markdown("""
A end-to-end product analytics system simulating the analytics 
infrastructure a product data scientist would own at a B2B SaaS company.
""")

st.divider()

# Dataset Overview
st.subheader("Dataset Overview")
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Users", "1,000")
col2.metric("Subscriptions", "1,000")
col3.metric("Features", "20")
col4.metric("Sessions", "22,874")
col5.metric("Events", "206,721")

st.divider()

# Project Summary
st.subheader("What This Project Demonstrates")
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **Analysis Modules**
    -  Funnel & Conversion Analysis
    -  Cohort Retention Analysis
    -  Feature Adoption & Power User Scoring
    """)

with col2:
    st.markdown("""
    **SQL Skills Showcased**
    - Window functions & CTEs
    - Funnel & cohort analysis
    - Data modeling & schema design
    - Query performance optimization
    """)

st.divider()

# Key Findings
st.subheader("Key Findings")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Activation Rate", "85.3%", help="Users who took at least one action after signing up")
col2.metric("Month-6 Retention", "84.9%", help="Average retention across all cohorts at month 6")
col3.metric("Champion Users", "354", help="Users scoring in the top engagement tier")
col4.metric("Query Speedup", "7.4x", help="Performance gain after optimization")

st.divider()

st.markdown("""
    **Built with:** MySQL · Python · Faker · Streamlit · Plotly
    
    **Author:** Bisola Akinkuolie · [GitHub](https://github.com/BisolaAkinkuolie/Saas-Analytics)
""")