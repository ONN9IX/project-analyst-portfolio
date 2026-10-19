from pathlib import Path
import csv
from datetime import date
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
ROOT=Path(__file__).resolve().parents[1]
with (ROOT/'data/github_issues_snapshot.csv').open(encoding='utf-8') as f:issues={int(r['issue_number']):r for r in csv.DictReader(f)}
ids=[1,27,32,52,86,94,98,102,117,124,131,152,158,177,201,221,226]
records=[]
for i in ids:
    row=issues[i]
    a=date.fromisoformat(row['created_date']);b=date.fromisoformat(row['closed_date'])
    records.append((i,a,b))
fig,ax=plt.subplots(figsize=(12,7.0))
for idx,(num,a,b) in enumerate(records):
    start=mdates.date2num(a)
    days=(b-a).days+1
    ax.barh(idx,days,left=start,height=.62)
ax.set_yticks(range(len(records)),labels=[f'Issue #{i}' for i,_,_ in records]);ax.invert_yaxis()
ax.xaxis.set_major_locator(mdates.DayLocator(interval=3))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m'))
ax.grid(axis='x',alpha=.25)
ax.set_title('Smart Garden: календарные периоды выбранных GitHub Issues',pad=16)
ax.set_xlabel('2026 год · от создания до закрытия Issue (не трудозатраты)')
ax.set_xlim(mdates.date2num(date(2026,9,22)),mdates.date2num(date(2026,10,15)))
fig.text(.06,.015,'Источник: публичные GitHub Issues, срез 13.10.2026. Минимум один день для событий, закрытых в дату создания.',fontsize=9)
fig.tight_layout(rect=[0,.04,1,1]);p=ROOT/'reports/ISSUE_TIMELINE.png';fig.savefig(p,dpi=170,bbox_inches='tight');print(p)
