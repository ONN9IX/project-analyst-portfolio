"""Build reproducible descriptive project reporting from GitHub CSV snapshots.

No invented budgets, sprints, due dates, hour-based lead times, or story points.
"""
from pathlib import Path
from collections import Counter
from datetime import date,timedelta
import csv, json

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'; REPORTS=ROOT/'reports'

def read_csv(name):
    with (DATA/name).open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f))

def write_csv(name,headers,records):
    with (REPORTS/name).open('w',encoding='utf-8',newline='') as f:
        w=csv.writer(f);w.writerow(headers);w.writerows(records)

def summarize(issues,prs):
    return {
        'snapshot_date': (json.loads((DATA/'refresh_info.json').read_text(encoding='utf-8'))['refreshed_at_utc'][:10] if (DATA/'refresh_info.json').exists() else '2026-10-13'),
        'issues_total':len(issues),
        'issues_open':sum(x['state']=='open' for x in issues),
        'issues_closed':sum(x['state']=='closed' for x in issues),
        'issues_closed_share':round(sum(x['state']=='closed' for x in issues)/len(issues),4),
        'prs_total':len(prs),
        'prs_merged':sum(x['outcome']=='merged' for x in prs),
        'prs_open':sum(x['outcome']=='open' for x in prs),
        'prs_closed_without_merge':sum(x['outcome']=='closed_not_merged' for x in prs),
        'prs_merged_share':round(sum(x['outcome']=='merged' for x in prs)/len(prs),4),
        'issues_assignee_blank':sum(not x['assignee'] for x in issues),
        'first_issue_created':min(x['created_date'] for x in issues),
        'last_issue_created':max(x['created_date'] for x in issues)
    }

def main():
    issues=read_csv('github_issues_snapshot.csv'); prs=read_csv('github_prs_snapshot.csv')
    assert len({x['issue_number'] for x in issues})==len(issues),'Issue duplicate IDs'
    assert len({x['pr_number'] for x in prs})==len(prs),'PR duplicate IDs'
    for row in issues:
        assert (row['state']=='closed')==bool(row['closed_date']),f'Invalid closure field {row}'
        assert not row['closed_date'] or row['closed_date']>=row['created_date']
    for row in prs:
        assert (row['outcome']=='merged')==bool(row['merged_date']),f'Invalid merge field {row}'
        assert not row['merged_date'] or row['merged_date']>=row['created_date']
    REPORTS.mkdir(exist_ok=True)
    summary=summarize(issues,prs)
    (REPORTS/'snapshot_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    dates=sorted(set(x['created_date'] for x in issues)|set(x['created_date'] for x in prs)|set(x['closed_date'] for x in issues if x['closed_date'])|set(x['merged_date'] for x in prs if x['merged_date']))
    first=date.fromisoformat(min(dates));last=date.fromisoformat(max(dates));days=(last-first).days+1
    c1=Counter(x['created_date'] for x in issues);c2=Counter(x['closed_date'] for x in issues if x['closed_date']);c3=Counter(x['created_date'] for x in prs);c4=Counter(x['merged_date'] for x in prs if x['merged_date'])
    trend=[]
    for n in range(days):
        day=(first+timedelta(days=n)).isoformat()
        trend.append([day,c1[day],c2[day],c3[day],c4[day]])
    write_csv('daily_activity.csv',['date','issues_created','issues_closed','prs_created','prs_merged'],trend)
    assignees=Counter(x['assignee'] or '(не назначен)' for x in issues)
    write_csv('assignee_distribution.csv',['assignee','issues_in_snapshot'],sorted(assignees.items(),key=lambda x:(-x[1],x[0])))
    status=f'''# Project status report — {summary['snapshot_date']}\n\n**Источник:** публичные GitHub Issues / Pull Requests [Smart Garden](https://github.com/ONN9IX/smart-garden). Срез зафиксирован {summary['snapshot_date']}; это исторические данные, а не непрерывный мониторинг.\n\n## Сводка\n\n| Метрика | Значение | Как рассчитано |\n|---|---:|---|\n| Issues в срезе | {summary['issues_total']} | все обычные Issues, без PR |\n| Закрытые Issues | {summary['issues_closed']} | `state = closed` |\n| Открытые Issues | {summary['issues_open']} | `state = open` |\n| Доля закрытых Issues | {summary['issues_closed_share']*100:.1f}% | закрытые / все Issues |\n| PR всего | {summary['prs_total']} | все Pull Requests |\n| Объединённые PR | {summary['prs_merged']} | `merged_at` заполнен |\n| Открытые PR | {summary['prs_open']} | `state = open` |\n| Закрытые без merge PR | {summary['prs_closed_without_merge']} | `state = closed`, `merged_at = null` |\n\n## Интерпретация\n\nВысокая доля закрытых Issues отражает **статус GitHub-реестра**, а не процент готовности продукта. Одна Issue может быть маленькой технической задачей, а другая — отдельным крупным этапом. Назначения (`assignee`) также не равны фактически затраченным часам.\n\nВ README исходного проекта технический MVP описан как сформированный; стадии 1–6 технически приняты. При этом проект **не заявлен как production-ready для реальных персональных данных**.\n\n## Открытые зоны внимания — подтверждённые примеры\n\n- [#223 — персональные данные / 152-ФЗ](https://github.com/ONN9IX/smart-garden/issues/223): нельзя считать юридическую готовность завершённой.\n- [#187 — подготовка пилота](https://github.com/ONN9IX/smart-garden/issues/187): пилот зависит от проверки сценариев и правовой готовности.\n- [#162 — универсальные профили](https://github.com/ONN9IX/smart-garden/issues/162): расширение доменной модели, риски усложнения scope.\n- [#189 — PWA](https://github.com/ONN9IX/smart-garden/issues/189): требуется отдельная проверка мобильных пользовательских сценариев.\n\n## Следующий управленческий шаг (рекомендация аналитика, не официальное решение команды)\n\n1. Перед пилотом отдельно утвердить **go/no-go** по безопасности и персональным данным.\n2. Открытые направления разбить на небольшие проверяемые поставки; зафиксировать владельца и критерии готовности.\n3. Начать собирать реальные плановые даты, фактические трудозатраты, оценки сложности и причины блокировок: сейчас их недостаточно для честного EVM, SPI/CPI и оценки исполнения сроков.\n\n## Ограничения\n\n- API-срез на дату 13.10.2026; изменения позже не отражены.\n- В данных нет согласованного baseline по срокам, бюджету и ресурсам, поэтому **не рассчитаны** план-факт бюджета, стоимость, velocity и производительность отдельных людей.\n- Поле даты фиксирует календарный день, поэтому разницу между открытием и закрытием Issue нельзя считать реальной трудоёмкостью.\n- Названия добавлены только для избранных Issues; для остальных первоисточник открывается по `source_url`.\n'''
    (REPORTS/'PROJECT_STATUS_REPORT.md').write_text(status,encoding='utf-8')
    print(json.dumps(summary,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
