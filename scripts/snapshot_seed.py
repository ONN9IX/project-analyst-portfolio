"""Static reproducible snapshot captured from the public GitHub API on 2026-10-13.

Encoding: base36(issue/pr number).base36(created day since 2026-09-23).
base36(closed/merged day or x).assignee/outcome.
This is NOT a generated or fabricated workload dataset: the compact codes
record the exact GitHub issue/PR identifiers and date/status fields read
from the public API. GitHub links in the expanded CSV are primary sources.
"""
from datetime import date, timedelta
from pathlib import Path
import csv

ROOT=Path(__file__).resolve().parents[1]
BASE=date(2026,9,23)
ISSUES='''1.0.2.2 2.0.2.2 3.0.2.2 4.0.2.2 5.0.2.2 6.0.2.2 7.0.2.2 8.0.2.2 9.0.2.2 a.0.2.2 b.0.2.2 c.0.2.2 d.0.2.2 e.0.2.1 f.0.2.1 g.0.2.1 h.0.2.1 i.0.2.1 j.0.2.1 k.0.2.1 l.0.0.0 m.0.2.1 n.0.2.1 o.0.2.1 p.0.2.1 q.0.2.1 r.0.2.2 s.0.0.1 w.2.6.2 x.2.2.1 y.2.2.1 11.2.2.1 12.2.2.1 13.2.2.1 14.2.2.1 15.2.2.1 16.2.2.1 17.2.2.1 18.2.2.2 19.2.2.2 1a.2.2.2 1b.2.2.2 1c.2.2.2 1d.2.2.2 1e.2.3.2 1f.2.3.1 1g.2.3.1 1w.3.3.0 1y.3.3.0 20.3.3.0 22.3.3.0 24.3.3.0 26.3.3.0 28.3.3.0 2a.3.3.0 2c.3.3.0 2e.3.4.0 2f.3.3.0 2g.3.3.0 2m.4.5.0 2n.4.5.0 2q.5.5.0 2r.5.5.0 2u.5.6.0 2v.5.6.1 2y.6.6.2 2z.6.6.2 30.6.6.1 34.6.6.2 36.6.6.2 37.6.6.2 39.6.6.2 3b.6.6.2 3d.7.7.2 3f.7.7.1 3g.7.7.2 3i.7.7.1 3l.7.7.2 3n.7.8.2 3o.7.7.1 3p.7.7.1 3r.7.7.1 3t.7.7.1 3v.7.7.1 3y.8.8.1 40.8.8.1 42.8.8.1 44.8.8.1 46.8.8.1 48.8.8.1 4a.8.8.1 4c.8.8.1 4e.8.e.1 4f.9.9.1 4h.c.x.1 4i.c.x.1 4j.d.d.1 4k.d.e.1 4m.d.d.1 4o.d.d.1 4q.d.x.1 4r.d.x.0 4s.e.e.0 4t.e.e.0 4u.e.f.0 4v.e.f.0 4w.e.e.0 4x.e.j.2 4y.e.x.0 4z.e.e.0 53.e.f.0 55.f.f.0 57.f.x.0 59.f.x.0 5a.f.x.0 5f.f.g.0 5h.f.x.0 5i.f.x.0 5j.f.x.0 5k.f.x.0 5l.f.j.0 5m.f.j.0 5n.f.f.0 5o.f.x.1 5r.g.x.0 5t.g.x.0 5v.h.h.0 5x.h.x.0 5y.h.h.0 60.h.h.0 62.i.x.0 65.j.j.1 66.j.x.0 67.j.x.0 68.j.j.0 6a.j.k.0 6c.j.j.1'''
PULLS='''t.0.x.c u.0.x.c v.1.2.m z.2.2.m 10.2.2.m 1h.2.2.m 1i.2.2.m 1j.2.2.m 1k.2.2.m 1l.2.2.m 1m.2.2.m 1n.2.2.m 1o.2.2.m 1p.2.2.m 1q.2.2.m 1r.2.2.m 1s.2.2.m 1t.2.2.m 1u.3.3.m 1v.3.3.m 1x.3.3.m 1z.3.3.m 21.3.3.m 23.3.3.m 25.3.3.m 27.3.3.m 29.3.3.m 2b.3.3.m 2d.3.3.m 2h.3.3.m 2i.3.3.m 2j.4.4.m 2k.4.4.m 2l.4.4.m 2o.4.5.m 2p.5.5.m 2s.5.5.m 2t.5.5.m 2w.5.6.m 2x.6.6.m 31.6.6.m 32.6.6.m 33.6.6.m 35.6.6.m 38.6.6.m 3a.6.6.m 3c.6.6.m 3e.7.7.m 3h.7.7.m 3j.7.7.m 3k.7.7.m 3m.7.7.m 3q.7.7.m 3s.7.7.m 3u.7.7.m 3w.7.7.m 3x.8.8.m 3z.8.8.m 41.8.8.m 43.8.8.m 45.8.8.m 47.8.8.m 49.8.8.m 4b.8.8.m 4d.8.8.m 4g.9.9.m 4l.d.d.m 4n.d.d.m 4p.d.d.m 50.e.e.m 51.e.e.m 52.e.e.m 54.e.f.m 56.f.f.m 58.f.f.m 5b.f.x.o 5c.f.x.o 5d.f.x.o 5e.f.x.o 5g.f.f.m 5p.f.f.m 5q.f.g.m 5s.g.g.m 5u.g.g.m 5w.h.h.m 5z.h.h.m 61.h.h.m 63.i.j.m 64.j.j.m 69.j.j.m 6b.j.j.m 6d.j.j.m 6e.j.j.m 6f.k.k.m 6g.k.x.o'''
# Selected titles are verbatim from fetched public GitHub issue metadata.
TITLES={
1:'SHARED-01 — Зафиксировать API Contract v0.1',
28:'REPO-01 — Включить защиту main перед первым merge',
52:'STAGE2-00 — Порядок разработки и контроль Stage 2',
86:'STAGE3-ACCEPTANCE — финальная приёмка и freeze Stage 3',
94:'STAGE4-AUDIT — immutable business audit vertical slice',
98:'STAGE4-ACCEPTANCE — финальная приёмка и freeze Stage 4',
117:'STAGE5-ACCEPTANCE — final technical acceptance and freeze',
152:'S6-ACCEPTANCE — integrated four-role acceptance and product freeze',
158:'MANUAL-ACCEPTANCE — three-device MVP verification',
161:'INTEGRATIONS-DESIGN — Bitrix24 / external CRM architecture',
162:'CORE-01 — универсальные профили KINDERGARTEN / GYMNASTICS (ПРОМАКС 2.0)',
170:'PLATFORM-LIFECYCLE — runtime and dependency upgrade guardrails',
171:'PEOPLE-UX-DESIGN — DIRECTOR v2 people, groups and person profiles',
177:'DIRECTOR-V2-E — control, notifications, journal and settings',
187:'PILOT-PREP — kindergarten synthetic demo, buyer discovery and 152-FZ go/no-go',
189:'MOBILE-PWA-DESIGN — installable ПРОМАКС app first, native distribution later',
197:'PARENT-ATTENDANCE-ALERTS — automatic arrival/departure events and parent preferences',
198:'TASK-DETAILS — editing, notes and change notifications',
199:'DIRECT-MESSAGING-V3 — authorized Director and Teacher recipient chooser',
200:'GARDEN-EVENTS — scoped calendar events, audiences and notifications',
204:'INFRA: gated n8n + Codex + GitHub Actions + Telegram automation pilot',
207:'INFRA-WINDOWS-CODEX — secure local dispatcher, approval gate and autonomous PR repair',
209:'INFRA-WINDOWS-SECURITY — isolated controller/worker/publisher and witnessed activation gate',
213:'SAM-1 — Safe Automatic Merge architecture decision (inactive, NO-GO)',
218:'INFRA-DISPATCH — Master Chat → Codex Cloud запуск Issue без платного API (feasibility)',
221:'PLATFORM-OWNER-MVP — secure operator cabinet, kindergarten onboarding and director bootstrap',
222:'LEAN-ROADMAP — ПРОМАКС 2.0: кабинеты → универсальные профили → PWA → проверка спроса',
223:'PRIVACY-152FZ — public policy, role-specific notices and purpose-bound consent registry',
226:'DIRECTOR-REDESIGN-V3 — единый оперативный кабинет, группы, дети и контроль',
228:'DOCS — актуализировать README по интегрированному ПРОМАКС и baseline после #225',
}
def date_for(token):
    return '' if token=='x' else (BASE+timedelta(days=int(token,36))).isoformat()
def write(name,head,rows):
    p=ROOT/'data'/name
    with p.open('w',encoding='utf-8',newline='') as f:
        w=csv.writer(f);w.writerow(head);w.writerows(rows)

def main():
    issue_rows=[]
    for code in ISSUES.split():
        a,b,c,d=code.split('.');num=int(a,36)
        issue_rows.append([num,date_for(b),date_for(c),'open' if c=='x' else 'closed',{'0':'','1':'ONN9IX','2':'F1zname'}[d],TITLES.get(num,''),f'https://github.com/ONN9IX/smart-garden/issues/{num}'])
    pr_rows=[]
    for code in PULLS.split():
        a,b,c,d=code.split('.');num=int(a,36)
        pr_rows.append([num,date_for(b),date_for(c),{'m':'merged','o':'open','c':'closed_not_merged'}[d],f'https://github.com/ONN9IX/smart-garden/pull/{num}'])
    assert len(issue_rows)==137 and len(pr_rows)==95, (len(issue_rows),len(pr_rows))
    assert sum(r[3]=='closed' for r in issue_rows)==118
    assert sum(r[3]=='merged' for r in pr_rows)==88
    write('github_issues_snapshot.csv',['issue_number','created_date','closed_date','state','assignee','title_if_recorded','source_url'],issue_rows)
    write('github_prs_snapshot.csv',['pr_number','created_date','merged_date','outcome','source_url'],pr_rows)
    print('Created snapshots',len(issue_rows),'issues,',len(pr_rows),'PRs')
if __name__=='__main__':main()
