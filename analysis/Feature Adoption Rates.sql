USE saas_analytics;

# -- Feature Adoption Rates 
With total_users AS (
	Select COUNT(Distinct user_id) AS total
    from users
),
feature_usage AS (
	Select
    f.feature_name,
    f.feature_category,
    f.is_premium,
    COUNT(distinct e.user_id) AS unique_users,
    COUNT(e.event_id) AS total_events,
    ROUND(COUNT(e.event_id) / COUNT(Distinct e.user_id),1) AS events_per_user
from events e
join features f on e.feature_id = f.feature_id
group by f.feature_id, f.feature_name, f.feature_category,f.is_premium
)
select
	fu.feature_name,
    fu.feature_category,
    fu.is_premium,
    fu.unique_users,
    ROUND(fu.unique_users / t.total * 100, 1) AS adoption_rate,
    fu.total_events,
    fu.events_per_user
from feature_usage fu
cross join total_users t
order by adoption_rate desc;

