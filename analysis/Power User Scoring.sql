## Power user scoring

USE saas_analytics;


-- PART 2: POWER USER SCORING


WITH user_stats AS (
    SELECT
        u.user_id,
        u.full_name,
        u.plan_tier,
        u.region,
        COUNT(DISTINCT s.session_id)                    AS total_sessions,
        COUNT(DISTINCT e.event_id)                      AS total_events,
        COUNT(DISTINCT e.feature_id)                    AS unique_features_used,
        COUNT(DISTINCT DATE_FORMAT(
            e.event_timestamp, '%Y-%m-01'))             AS active_months,
        ROUND(COUNT(DISTINCT e.event_id) /
            NULLIF(COUNT(DISTINCT s.session_id), 0), 1) AS events_per_session,
        DATEDIFF(MAX(e.event_timestamp),
            MIN(e.event_timestamp))                     AS days_active_span
    FROM users u
    LEFT JOIN sessions s ON u.user_id = s.user_id
    LEFT JOIN events e ON u.user_id = e.user_id
    GROUP BY u.user_id, u.full_name, u.plan_tier, u.region
),
scored_users AS (
    SELECT
        user_id,
        full_name,
        plan_tier,
        region,
        total_sessions,
        total_events,
        unique_features_used,
        active_months,
        events_per_session,
        days_active_span,
        -- Score each dimension using NTILE into quartiles
        NTILE(4) OVER (ORDER BY total_sessions)         AS sessions_quartile,
        NTILE(4) OVER (ORDER BY total_events)           AS events_quartile,
        NTILE(4) OVER (ORDER BY unique_features_used)   AS features_quartile,
        NTILE(4) OVER (ORDER BY active_months)          AS months_quartile,
        NTILE(4) OVER (ORDER BY events_per_session)     AS intensity_quartile
    FROM user_stats
),
power_scores AS (
    SELECT
        user_id,
        full_name,
        plan_tier,
        region,
        total_sessions,
        total_events,
        unique_features_used,
        active_months,
        events_per_session,
        -- Weighted power score out of 20
        (sessions_quartile * 1) +
        (events_quartile * 1) +
        (features_quartile * 2) +
        (months_quartile * 1) +
        (intensity_quartile * 1) AS power_score
    FROM scored_users
)
SELECT
    user_id,
    full_name,
    plan_tier,
    region,
    total_sessions,
    total_events,
    unique_features_used,
    active_months,
    events_per_session,
    power_score,
    CASE
        WHEN power_score >= 18 THEN 'Champion'
        WHEN power_score >= 14 THEN 'Power User'
        WHEN power_score >= 10 THEN 'Regular'
        WHEN power_score >= 6  THEN 'Casual'
        ELSE 'At Risk'
    END AS user_segment
FROM power_scores
ORDER BY power_score DESC;