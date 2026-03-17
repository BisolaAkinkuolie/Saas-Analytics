# SaaS Product Analytics Engine

An end-to-end product analytics system built with MySQL and Python, simulating the analytics infrastructure I would  own at a B2B SaaS , Iaas, Paas company.

Built to demonstrate advanced SQL skills including window functions, CTEs, funnel analysis, cohort retention, feature adoption scoring, and query performance optimization.

---

## Project Structure
```
saas-analytics/
├── analysis/
│   ├── funnel_analysis.sql
│   ├── cohort_retention.sql
    |__ Funnel_Analysis_without_comments.sql
│   ├── feature_adoption_power_users.sql
│   └── performance_optimization.sql
├── config.example.py
├── db_connection.py
├── generate_data.py
└── README.md
```

---

## Dataset

Synthetic data generated with Python's Faker library, simulating 2 years of activity on a B2B SaaS platform.

| Table | Rows | Description |
|---|---|---|
| users | 1,000 | Signups across 5 regions and 4 plan tiers |
| subscriptions | 1,000 | MRR, plan changes and churn dates |
| features | 20 | Product catalog across Core, Advanced and Enterprise tiers |
| sessions | 22,874 | User sessions with device type and duration |
| events | 206,721 | Granular user actions across all features |

---

## Setup

### Prerequisites
- MySQL 8.0+
- Python 3.10+

### Installation

1. Clone the repo:
```bash
git clone https://github.com/BisolaAkinkuolie/Saas-Analytics.git
cd Saas-Analytics
```

2. Install dependencies:
```bash
pip install faker pymysql pandas
```

3. Configure credentials:
```bash
cp config.example.py config.py
# Edit config.py with your MySQL credentials
```

4. Create the database and schema in MySQL Workbench:
```sql
CREATE DATABASE IF NOT EXISTS saas_analytics;
```
Then run the schema creation script from the project root.

5. Generate synthetic data:
```bash
python generate_data.py
```

---

## Analysis Modules

### Module 1: Funnel & Conversion Analysis
`analysis/funnel_analysis.sql`

Measures user progression through a 4-step activation funnel and diagnoses conversion gaps.

**Key Findings:**
- 85.3% activation rate — 147 users signed up but never took a single action, flagging an onboarding gap
- 100% of activated users engaged with core features
- 363 engaged users never upgraded despite heavy product usage
- 164 power users averaging 40 sessions and 15,370 events each remain on the free tier — the highest priority upgrade targets for any growth campaign

**SQL concepts:** CTEs, LEFT JOINs, conditional aggregation, drop-off rate calculations

---

### Module 2: Cohort Retention Analysis
`analysis/cohort_retention.sql`

Tracks month-over-month retention for every signup cohort over a 6 month window.

**Key Findings:**
- Month-6 average retention of 84.9% with a remarkably flat churn curve, suggesting strong product stickiness after initial activation
- Retention slightly increases over time (83.4% → 84.9%), indicating natural selection — disengaged users churn early leaving a highly engaged core
- Significant spread between worst (70%) and best (92.5%) cohorts at month 6 — warrants investigation into what differentiates high vs low retention cohorts by acquisition channel or plan tier mix

| Month | Avg Retention | Worst Cohort | Best Cohort |
|---|---|---|---|
| 0 | 83.4% | 61.9% | 92.5% |
| 3 | 84.2% | 70.0% | 90.6% |
| 6 | 84.9% | 71.4% | 92.5% |

**SQL concepts:** CTEs, TIMESTAMPDIFF, DATE_FORMAT, cohort joining, window aggregation

---

### Module 3: Feature Adoption & Power User Scoring
`analysis/feature_adoption_power_users.sql`

Measures feature adoption rates across the product catalog and builds a composite power user scoring model using window functions.

**Key Findings:**
- Core features show 85% adoption across all users
- Premium feature adoption plateaus at ~42%, perfectly mirroring the paid user base — suggesting premium features are not yet pulling free users toward upgrading
- Premium features average 12-13 events per user vs core features at 19-20 — suggesting premium features lack stickiness relative to their price
- 35% of users qualify as Champions, averaging 38 sessions and 17 unique features used
- Sharp engagement cliff between Regular (14 avg sessions) and Casual (2.9 avg sessions) segments — prime re-engagement opportunity
- Champions on starter plans identified as highest-value upsell targets

| Segment | Users | Avg Sessions | Avg Events | Avg Features Used |
|---|---|---|---|---|
| Champion | 354 | 38.3 | 350 | 16.9 |
| Power User | 289 | 23.2 | 210 | 13.7 |
| Regular | 138 | 14.2 | 123 | 12.1 |
| Casual | 219 | 2.9 | 23.6 | 2.9 |

**SQL concepts:** CTEs, NTILE window function, RANK, weighted scoring model, feature joins

---

### Module 4: Performance Optimization
`analysis/performance_optimization.sql`

Demonstrates the full optimization cycle — baseline measurement, EXPLAIN analysis, indexing strategy, and query rewriting.

**Results:**

| | Slow Query | Optimized Query |
| Execution time | 0.922 sec | 0.125 sec |
| Improvement | | **7.4x faster** |

**What caused the slowdown:**
- Full table scan (`type = ALL`) on the features table
- `Using temporary` — MySQL created an in-memory temp table for GROUP BY
- `Using filesort` — MySQL sorted results manually with no index support

**How it was fixed:**
- Added 5 targeted indexes on high-frequency filter and join columns
- Rewrote query using CTEs to pre-filter events before joining, reducing the join surface from 206k rows to only the relevant subset
- Key lesson: query structure matters as much as indexes — filtering early beats indexing everything

**SQL concepts:** EXPLAIN, index strategy, CTE-based query rewriting, performance benchmarking

---

## Skills Demonstrated

- Advanced MySQL — window functions, CTEs, complex joins, subqueries
- Product analytics — funnel analysis, cohort retention, feature adoption, user segmentation
- Data modeling — normalized schema design with foreign key relationships
- Performance optimization — EXPLAIN analysis, indexing strategy, query rewriting
- Python — synthetic data generation with Faker, pymysql, batch inserts
- Software practices — git version control, credential management, modular project structure

---

## Author

Bisola Akinkuolie
[GitHub](https://github.com/BisolaAkinkuolie)