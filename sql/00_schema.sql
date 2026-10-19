-- PostgreSQL 14+; snapshots from the public ONN9IX/smart-garden repository.
-- Issue != Pull Request. Tables intentionally kept separate.
DROP TABLE IF EXISTS project_pull_requests;
DROP TABLE IF EXISTS project_issues;
CREATE TABLE project_issues (
    issue_number INTEGER PRIMARY KEY,
    created_date DATE NOT NULL,
    closed_date DATE,
    state TEXT NOT NULL CHECK (state IN ('open','closed')),
    assignee TEXT,
    title_if_recorded TEXT,
    source_url TEXT NOT NULL,
    CONSTRAINT consistent_issue_state CHECK (
        (state='closed' AND closed_date IS NOT NULL) OR
        (state='open' AND closed_date IS NULL)
    ),
    CONSTRAINT issue_dates CHECK (closed_date IS NULL OR closed_date >= created_date)
);
CREATE TABLE project_pull_requests (
    pr_number INTEGER PRIMARY KEY,
    created_date DATE NOT NULL,
    merged_date DATE,
    outcome TEXT NOT NULL CHECK (outcome IN ('open','merged','closed_not_merged')),
    source_url TEXT NOT NULL,
    CONSTRAINT consistent_pr_state CHECK (
        (outcome='merged' AND merged_date IS NOT NULL) OR
        (outcome <> 'merged' AND merged_date IS NULL)
    ),
    CONSTRAINT pr_dates CHECK (merged_date IS NULL OR merged_date >= created_date)
);
