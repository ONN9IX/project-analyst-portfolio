-- DataBridge Solutions: strictly SYNTHETIC 8-month project-operations scenario.
-- These values are not employees' real working hours or a company's actual results.
-- Run from the ROOT of project-analyst-portfolio:
-- psql -d your_database -f cases/databridge/sql/project_monitoring.sql

DROP TABLE IF EXISTS databridge_delivery_simulated;

CREATE TABLE databridge_delivery_simulated (
    month TEXT PRIMARY KEY CHECK (month ~ '^2026-(0[2-9])$'),
    planned_deliverables INTEGER NOT NULL CHECK (planned_deliverables > 0),
    accepted_deliverables INTEGER NOT NULL CHECK (accepted_deliverables >= 0),
    deferred_deliverables INTEGER NOT NULL CHECK (deferred_deliverables >= 0),
    planned_hours INTEGER NOT NULL CHECK (planned_hours >= 0),
    actual_hours INTEGER NOT NULL CHECK (actual_hours >= 0),
    source_type TEXT NOT NULL CHECK (source_type = 'synthetic_scenario'),
    CHECK (accepted_deliverables + deferred_deliverables = planned_deliverables)
);

-- psql meta-command, file path relative to the command working directory:
\copy databridge_delivery_simulated FROM 'cases/databridge/data/monthly_delivery_simulated.csv' WITH (FORMAT csv, HEADER true)

-- 1. Overall simulated status.
SELECT
    SUM(planned_deliverables) AS planned,
    SUM(accepted_deliverables) AS accepted,
    SUM(deferred_deliverables) AS deferred,
    ROUND(100.0 * SUM(accepted_deliverables) / NULLIF(SUM(planned_deliverables),0),1) AS acceptance_share_pct,
    SUM(planned_hours) AS planned_hours,
    SUM(actual_hours) AS actual_hours,
    SUM(actual_hours) - SUM(planned_hours) AS variance_hours
FROM databridge_delivery_simulated;

-- 2. Month-by-month status.
SELECT
    month,
    planned_deliverables,
    accepted_deliverables,
    deferred_deliverables,
    ROUND(100.0 * accepted_deliverables / NULLIF(planned_deliverables,0),1) AS acceptance_pct,
    actual_hours - planned_hours AS variance_hours,
    ROUND(100.0 * (actual_hours - planned_hours) / NULLIF(planned_hours,0),1) AS variance_pct
FROM databridge_delivery_simulated
ORDER BY month;

-- 3. Simulated trailing 3-month sum of accepted deliveries.
-- Rows, rather than calendar days: there is exactly one row per month.
SELECT
    month,
    accepted_deliverables,
    SUM(accepted_deliverables) OVER (
        ORDER BY month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ) AS accepted_last_three_months
FROM databridge_delivery_simulated
ORDER BY month;

-- 4. Highlight months with lower acceptance or unusually high hours.
SELECT month, planned_deliverables, accepted_deliverables, planned_hours, actual_hours
FROM databridge_delivery_simulated
WHERE accepted_deliverables::NUMERIC / planned_deliverables < 0.80
   OR actual_hours::NUMERIC / NULLIF(planned_hours,0) > 1.10
ORDER BY month;
