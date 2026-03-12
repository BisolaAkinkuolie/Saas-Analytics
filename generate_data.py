import pymysql
import random
from faker import Faker
from datetime import timedelta
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

fake = Faker()
connection = pymysql.connect(
    host= DB_HOST,
    user= DB_USER,
    password= DB_PASSWORD,
    database= DB_NAME
)
cursor = connection.cursor()

#---Generate (users)
print("Generating Users...")
plan_tiers = ['free','starter','pro','enterprise']
plan_weights = [0.5,0.25,0.15,0.10]
regions = ['North America', 'Europe', 'Asia Pacific', 'Latin America', 'Africa']

users = []
for _ in range(1000):
    users.append((
        fake.unique.email(),
        fake.name(),
        fake.company(),
        random.choice(regions),
        random.choices(plan_tiers, weights=plan_weights)[0],
        fake.date_between(start_date='-2y', end_date='today'),
        random.choices([True, False], weights=[0.85, 0.15])[0]
    ))

cursor.executemany("""
    INSERT INTO users (email, full_name, company, region, plan_tier, signup_date, is_active)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
""", users)
connection.commit()
print(f"✓ {len(users)} users inserted")

# --- 2. SUBSCRIPTIONS (1 per user) ---
print("Generating subscriptions...")
plan_mrr = {'free': 0, 'starter': 49, 'pro': 149, 'enterprise': 499}

cursor.execute("SELECT user_id, plan_tier, signup_date FROM users")
all_users = cursor.fetchall()

subscriptions = []
for user_id, plan_tier, signup_date in all_users:
    start_date = signup_date
    churn_date = None
    end_date = None
    if random.random() < 0.2:
        churn_date = fake.date_between(start_date=start_date, end_date='today')
        end_date = churn_date
    subscriptions.append((
        user_id, plan_tier,
        plan_mrr[plan_tier],
        start_date, end_date, churn_date
    ))

cursor.executemany("""
    INSERT INTO subscriptions (user_id, plan_tier, mrr, start_date, end_date, churn_date)
    VALUES (%s, %s, %s, %s, %s, %s)
""", subscriptions)
connection.commit()
print(f"✓ {len(subscriptions)} subscriptions inserted")

# --- 3. FEATURES (20 features) ---
print("Generating features...")
features = [
    ('Dashboard', 'Core', False), ('User Management', 'Core', False),
    ('API Access', 'Core', False), ('Analytics', 'Core', False),
    ('Export to CSV', 'Core', False), ('Custom Reports', 'Advanced', True),
    ('Team Collaboration', 'Advanced', True), ('Integrations', 'Advanced', True),
    ('Webhooks', 'Advanced', True), ('SSO Login', 'Advanced', True),
    ('Audit Logs', 'Enterprise', True), ('Priority Support', 'Enterprise', True),
    ('Custom SLA', 'Enterprise', True), ('Dedicated Manager', 'Enterprise', True),
    ('White Labeling', 'Enterprise', True), ('Data Warehouse Sync', 'Enterprise', True),
    ('Mobile App', 'Core', False), ('Notifications', 'Core', False),
    ('Dark Mode', 'Core', False), ('Onboarding Wizard', 'Core', False)
]

cursor.executemany("""
    INSERT INTO features (feature_name, feature_category, is_premium)
    VALUES (%s, %s, %s)
""", features)
connection.commit()
print(f"✓ {len(features)} features inserted")

# --- 4. SESSIONS + EVENTS (~100k events) ---
print("Generating sessions and events (this may take a moment)...")

cursor.execute("SELECT user_id, signup_date, plan_tier FROM users WHERE is_active = 1")
active_users = cursor.fetchall()

cursor.execute("SELECT feature_id, is_premium FROM features")
all_features = cursor.fetchall()
free_features = [f[0] for f in all_features if not f[1]]
premium_features = [f[0] for f in all_features if f[1]]

event_types = ['click', 'view', 'create', 'edit', 'delete', 'export', 'share']
device_types = ['desktop', 'mobile', 'tablet']
device_weights = [0.65, 0.25, 0.10]

total_events = 0
batch_sessions = []
batch_events = []

for user_id, signup_date, plan_tier in active_users:
    num_sessions = random.randint(5, 50)
    for _ in range(num_sessions):
        session_start = fake.date_time_between(
            start_date=signup_date, end_date='now'
        )
        session_end = session_start + timedelta(minutes=random.randint(2, 120))
        device = random.choices(device_types, weights=device_weights)[0]
        batch_sessions.append((user_id, session_start, session_end, device))

cursor.executemany("""
    INSERT INTO sessions (user_id, session_start, session_end, device_type)
    VALUES (%s, %s, %s, %s)
""", batch_sessions)
connection.commit()

# Fetch inserted session IDs
cursor.execute("SELECT session_id, user_id FROM sessions")
session_rows = cursor.fetchall()

# Map user_id -> list of session_ids
from collections import defaultdict
user_sessions = defaultdict(list)
for session_id, user_id in session_rows:
    user_sessions[user_id].append(session_id)

# Build a plan lookup
cursor.execute("SELECT user_id, plan_tier FROM users")
user_plan = {row[0]: row[1] for row in cursor.fetchall()}

for user_id, sessions in user_sessions.items():
    plan = user_plan[user_id]
    available_features = free_features.copy()
    if plan in ('pro', 'enterprise', 'starter'):
        available_features += premium_features

    for session_id in sessions:
        num_events = random.randint(3, 15)
        for _ in range(num_events):
            batch_events.append((
                user_id,
                session_id,
                random.choice(available_features),
                random.choice(event_types),
                fake.date_time_between(start_date='-2y', end_date='now')
            ))

# Insert events in batches of 10,000
print("Inserting events in batches...")
batch_size = 10000
for i in range(0, len(batch_events), batch_size):
    cursor.executemany("""
        INSERT INTO events (user_id, session_id, feature_id, event_type, event_timestamp)
        VALUES (%s, %s, %s, %s, %s)
    """, batch_events[i:i+batch_size])
    connection.commit()
    print(f"   Inserted {min(i+batch_size, len(batch_events))} / {len(batch_events)} events")

total_events = len(batch_events)

print(f" {len(batch_sessions)} sessions inserted")
print(f" {total_events} events inserted")
print("\n Data generation complete!")
cursor.close()
connection.close()