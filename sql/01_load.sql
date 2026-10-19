-- Run from the repository root: psql -d project_analyst -f sql/00_schema.sql
-- Then: psql -d project_analyst -f sql/01_load.sql
\copy project_issues (issue_number,created_date,closed_date,state,assignee,title_if_recorded,source_url) FROM 'data/github_issues_snapshot.csv' WITH (FORMAT csv, HEADER true, NULL '');
\copy project_pull_requests (pr_number,created_date,merged_date,outcome,source_url) FROM 'data/github_prs_snapshot.csv' WITH (FORMAT csv, HEADER true, NULL '');
