USE saas_analytics;

# Cohort Retention Analysis

WITH cohort_base AS (
	SELECT
		user_id,
        Date_format(signup_date, '%Y-%m-01') as Cohort_month # Assign each user to their sign up month cohort
	from users
	),
user_activity AS (
	Select distinct
		user_id,
        date_format(event_timestamp, '%Y-%m-01') AS activity_month  ### get each users active months from events
	from events
	),
cohort_activity AS (
	select 
		c.user_id,
        c.cohort_month,
        a.activity_month,
        timestampdiff(Month,c.cohort_month,a.activity_month) AS months_since_signup
	from cohort_base c
	join user_activity a on c.user_id = a.user_id
	),
cohort_sizes AS (
	select 
		cohort_month,
        count(distinct user_id) as cohort_size
	from cohort_base c
	group by cohort_month
	),
retention_counts AS (
	select 
		cohort_month,
        months_since_signup,
        count(distinct user_id) as retained_users   ### Count of retained users per month
	from cohort_activity
	where months_since_signup between 0 and 6
    group by cohort_month, months_since_signup
)
Select 
	r.cohort_month,
    cs.cohort_size,
    r.months_since_signup,
    r.retained_users,
    ROUND(r.retained_users / cs.cohort_size * 100,1) AS retention_rate   ## Final Retention 
from retention_counts r
join cohort_sizes cs on r.cohort_month = cs.cohort_month
order by r.cohort_month,r.months_since_signup

        




