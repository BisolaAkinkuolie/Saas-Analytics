USE saas_analytics;

#--Business Question : Find all power users (i.e 30+ sessions)
#--who used premium features in the last 6 months
#--ranked by total events

SELECT 
	u.user_id,
    u.full_name,
    u.plan_tier,
    u.region,
    count(distinct s.session_id) as total_sessions,
    count(Distinct e.event_id) as total_events,
    count(Distinct f.feature_id) as unique_features
from users u
join sessions s on u.user_id = s.user_id
join events e on u.user_id = e.user_id
join features f on e.feature_id = f.feature_id
where f.is_premium = 1
and e.event_timestamp >= date_sub(Now(), interval 6 month) 
and u.is_active = 1
group by u.user_id, u.full_name, u.plan_tier,u.region
having total_sessions >= 30
order by total_events desc;


## Understanding the execution process and time
EXPLAIN
SELECT 
	u.user_id,
    u.full_name,
    u.plan_tier,
    u.region,
    count(distinct s.session_id) as total_sessions,
    count(Distinct e.event_id) as total_events,
    count(Distinct f.feature_id) as unique_features
from users u
join sessions s on u.user_id = s.user_id
join events e on u.user_id = e.user_id
join features f on e.feature_id = f.feature_id
where f.is_premium = 1
and e.event_timestamp >= date_sub(Now(), interval 6 month) 
and u.is_active = 1
group by u.user_id, u.full_name, u.plan_tier,u.region
having total_sessions >= 30
order by total_events desc;

## The Fix--Optimizing the query
CREATE INDEX idx_events_timestamp
	on events(event_timestamp);

CREATE INDEX idx_events_user_feature
	ON events(user_id, feature_id);

CREATE INDEX idx_features_premium
	on features(is_premium);

CREATE INDEX idx_users_active
	on users(is_active);
    
CREATE INDEX idx_sessions_user
	on sessions(user_id);
    
## STEP 2: re-writtem optimized query
## --Pre-filter events first in a CTE before joining
## to reduce the number of rows mysql has to process

With filtered_events as (
	select
		e.user_id,
        e.event_id,
        e.feature_id,
        e.session_id
	from events e
    join features f on e.feature_id = f.feature_id
    where f.is_premium = 1
    and e.event_timestamp >= date_sub(now(), interval 6 month)
),
user_session_counts as (
	select
		user_id,
        count(distinct session_id) as total_sessions
	from sessions
    group by user_id
),
aggregated as (
	select
		fe.user_id,
        count(distinct fe.event_id) as total_events,
        count(distinct fe.feature_id) as unique_features
	from filtered_events fe
    group by fe.user_id
)
select 
	u.user_id,
    u.full_name,
    u.plan_tier,
    u.region,
    usc.total_sessions,
    a.total_events,
    a.unique_features
from aggregated a 
join users u on a.user_id = u.user_id
join user_session_counts usc on a.user_id = usc.user_id
where u.is_active = 1
and usc.total_sessions >= 30
order by a.total_events desc;

EXPLAIN
With filtered_events as (
	select
		e.user_id,
        e.event_id,
        e.feature_id,
        e.session_id
	from events e
    join features f on e.feature_id = f.feature_id
    where f.is_premium = 1
    and e.event_timestamp >= date_sub(now(), interval 6 month)
),
user_session_counts as (
	select
		user_id,
        count(distinct session_id) as total_sessions
	from sessions
    group by user_id
),
aggregated as (
	select
		fe.user_id,
        count(distinct fe.event_id) as total_events,
        count(distinct fe.feature_id) as unique_features
	from filtered_events fe
    group by fe.user_id
)
select 
	u.user_id,
    u.full_name,
    u.plan_tier,
    u.region,
    usc.total_sessions,
    a.total_events,
    a.unique_features
from aggregated a 
join users u on a.user_id = u.user_id
join user_session_counts usc on a.user_id = usc.user_id
where u.is_active = 1
and usc.total_sessions >= 30
order by a.total_events desc;
