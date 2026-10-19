-- 1. Snapshot totals by issue state (not project readiness).
SELECT state, COUNT(*) AS issue_count,
       ROUND(100.0*COUNT(*)/SUM(COUNT(*)) OVER(),1) AS share_pct
FROM project_issues GROUP BY state ORDER BY issue_count DESC;

-- 2. PR lifecycle: merged and closed_without_merge are different outcomes.
SELECT outcome, COUNT(*) AS prs,
       ROUND(100.0*COUNT(*)/SUM(COUNT(*)) OVER(),1) AS share_pct
FROM project_pull_requests GROUP BY outcome ORDER BY prs DESC;

-- 3. Daily fact table. Independent event streams, not a JOIN on date that
-- multiplies rows and inflates metrics.
WITH issue_created AS (
    SELECT created_date AS day, COUNT(*) AS created_count FROM project_issues GROUP BY 1
), issue_closed AS (
    SELECT closed_date AS day, COUNT(*) AS closed_count FROM project_issues
    WHERE closed_date IS NOT NULL GROUP BY 1
), pr_merged AS (
    SELECT merged_date AS day, COUNT(*) AS merged_count FROM project_pull_requests
    WHERE merged_date IS NOT NULL GROUP BY 1
), all_dates AS (
    SELECT day FROM issue_created UNION SELECT day FROM issue_closed UNION SELECT day FROM pr_merged
)
SELECT d.day, COALESCE(ic.created_count,0) AS issue_created,
       COALESCE(i2.closed_count,0) AS issue_closed,
       COALESCE(p.merged_count,0) AS pr_merged
FROM all_dates d
LEFT JOIN issue_created ic ON ic.day=d.day
LEFT JOIN issue_closed i2 ON i2.day=d.day
LEFT JOIN pr_merged p ON p.day=d.day
ORDER BY d.day;

-- 4. Issues per GitHub assignee. Empty != no performer.
SELECT COALESCE(NULLIF(assignee,''),'(не назначен)') AS assignee,
       COUNT(*) AS total,
       COUNT(*) FILTER (WHERE state='open') AS open_issues
FROM project_issues GROUP BY 1 ORDER BY total DESC;

-- 5. Closure patterns in whole CALENDAR days (NOT logged hours).
SELECT issue_number,created_date,closed_date,
       (closed_date-created_date) AS elapsed_calendar_days,source_url
FROM project_issues WHERE state='closed'
ORDER BY elapsed_calendar_days DESC,issue_number LIMIT 20;

-- 6. Rolling 7-day PR merge volume on calendar-day series.
WITH all_days AS (
    SELECT generate_series(MIN(created_date),MAX(created_date),INTERVAL '1 day')::date AS day
    FROM project_pull_requests
), per_day AS (
    SELECT d.day, COUNT(p.pr_number) AS merged_today
    FROM all_days d LEFT JOIN project_pull_requests p ON p.merged_date=d.day
    GROUP BY d.day
)
SELECT day,merged_today,
       SUM(merged_today) OVER (ORDER BY day ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS merged_last_7_days
FROM per_day ORDER BY day;

-- 7. Evidence of Stage gates. Their closed_date is NOT the stage start/end duration.
SELECT issue_number,state,created_date,closed_date,source_url
FROM project_issues WHERE issue_number IN (33,52,86,98,117,152)
ORDER BY issue_number;
