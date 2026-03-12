USE saas_analytics;

WITH step1_signups AS (
    SELECT user_id, signup_date
    FROM users
),
step2_activated AS (
    SELECT DISTINCT user_id
    FROM events
),
step3_core_feature AS (
    SELECT DISTINCT e.user_id
    FROM events e
    JOIN features f ON e.feature_id = f.feature_id
    WHERE f.feature_name IN ('Dashboard','Analytics','User Management','Mobile App', 'Notifications','Dark Mode','Onboarding Wizard', 'Export to CSV', 'API Access')
),
step4_upgraded AS (
    SELECT DISTINCT user_id
    FROM users
    WHERE plan_tier IN ('starter', 'pro', 'enterprise')
),
funnel AS (
    SELECT
        COUNT(DISTINCT s1.user_id) AS step1_signups,
        COUNT(DISTINCT s2.user_id) AS step2_activated,
        COUNT(DISTINCT s3.user_id) AS step3_core_feature,
        COUNT(DISTINCT s4.user_id) AS step4_upgraded
    FROM step1_signups s1
    LEFT JOIN step2_activated s2 ON s1.user_id = s2.user_id
    LEFT JOIN step3_core_feature s3 ON s1.user_id = s3.user_id
    LEFT JOIN step4_upgraded s4 ON s1.user_id = s4.user_id
)
SELECT
    step1_signups,
    step2_activated,
    ROUND(step2_activated / step1_signups * 100, 1) AS pct_activated,
    step3_core_feature,
    ROUND(step3_core_feature / step2_activated * 100, 1) AS pct_used_core,
    step4_upgraded,
    ROUND(step4_upgraded / step1_signups * 100, 1) AS pct_upgraded
FROM funnel;

#--users who actually used core features but never upgraded
#--segmnented by usage intensity

WITH core_users AS (
	select distinct e.user_id
    from events e
    join features f on e.feature_id = e.feature_id
    where f.feature_name in ('Dashboard','Analytics','User Management','Mobile App', 'Notifications','Dark Mode','Onboarding Wizard', 'Export to CSV', 'API Access')
),
non_upgraders AS (
	select c.user_id 
    from core_users c
    join users u on c.user_id = u.user_id
    where u.Plan_tier = 'free'
),
usage_intensity AS (
	SELECT
		n.user_id,
		COUNT(DISTINCT s.session_id) AS total_sessions,
		COUNT(e.event_id) AS total_events,
		ROUND(COUNT(e.event_id) / COUNT(DISTINCT s.session_id), 1) AS events_per_session
	FROM non_upgraders n
	JOIN sessions s ON n.user_id = s.user_id
	JOIN events e ON n.user_id = e.user_id
	GROUP BY n.user_id
)
SELECT
    CASE
        WHEN total_sessions <= 5  THEN '1. Low (1-5 sessions)'
        WHEN total_sessions <= 15 THEN '2. Medium (6-15 sessions)'
        WHEN total_sessions <= 30 THEN '3. High (16-30 sessions)'
        ELSE '4. Power (30+ sessions)'
    END AS usage_segment,
    COUNT(*) AS user_count,
    ROUND(AVG(total_sessions), 1) AS avg_sessions,
    ROUND(AVG(total_events), 1) AS avg_events,
    ROUND(AVG(events_per_session), 1) AS avg_events_per_session
FROM usage_intensity
GROUP BY usage_segment
ORDER BY usage_segment;