USE saas_analytics;

SELECT 'users' as table_name, count(*) as row_count from users
UNION ALL
SELECT 'subscriptions', count(*) from subscriptions
UNION ALL
SELECT 'features', count(*) from features
UNION ALL
SELECT 'sessions', count(*) from sessions
UNION ALL
SELECT 'events', count(*) from events;

Select *
from users;

select *
from subscriptions;

select *
from features;

select *
from sessions;

select *
from events;

select a.*,b.user_id,b.plan_tier
from users a
join subscriptions b on a.user_id = b.user_id;