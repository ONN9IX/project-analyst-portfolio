"""Refresh source CSV snapshots from GitHub REST API. Requires internet; read-only.

Usage: python scripts/refresh_from_github.py
Then: python scripts/build_reports.py
Dashboard.xlsx is a dated delivered artifact and is NOT silently updated by this script.
"""
from pathlib import Path
from datetime import datetime,timezone
from urllib.request import Request,urlopen
from urllib.parse import urlencode
from urllib.error import HTTPError
import json, csv, time

ROOT=Path(__file__).resolve().parents[1]
BASE='https://api.github.com/repos/ONN9IX/smart-garden'

def paginated(kind):
    rows=[]
    for page in range(1,21):
        params=urlencode({'state':'all','per_page':100,'page':page,'sort':'created','direction':'asc'})
        req=Request(f'{BASE}/{kind}?{params}',headers={'Accept':'application/vnd.github+json','User-Agent':'project-analyst-portfolio'})
        with urlopen(req,timeout=30) as resp:batch=json.load(resp)
        if not isinstance(batch,list):raise ValueError('Unexpected GitHub response')
        rows.extend(batch)
        if len(batch)<100:break
        time.sleep(.1)
    return rows

def day(s):return s[:10] if s else ''
def write(name,headers,records):
    with (ROOT/'data'/name).open('w',encoding='utf-8',newline='') as f:
        w=csv.writer(f);w.writerow(headers);w.writerows(records)

def main():
    issues=[i for i in paginated('issues') if 'pull_request' not in i]
    prs=paginated('pulls')
    write('github_issues_snapshot.csv',['issue_number','created_date','closed_date','state','assignee','title_if_recorded','source_url'],[
        [i['number'],day(i['created_at']),day(i['closed_at']),i['state'],i['assignee']['login'] if i['assignee'] else '',i['title'],i['html_url']] for i in issues])
    write('github_prs_snapshot.csv',['pr_number','created_date','merged_date','outcome','source_url'],[
        [p['number'],day(p['created_at']),day(p['merged_at']),'merged' if p['merged_at'] else ('open' if p['state']=='open' else 'closed_not_merged'),p['html_url']] for p in prs])
    stamp=datetime.now(timezone.utc).isoformat(timespec='seconds')
    (ROOT/'data'/'refresh_info.json').write_text(json.dumps({'refreshed_at_utc':stamp,'source_repository':'ONN9IX/smart-garden','issues':len(issues),'prs':len(prs)},indent=2)+'\n')
    print(f'Refreshed {len(issues)} Issues and {len(prs)} PRs at {stamp}')
if __name__=='__main__':main()
