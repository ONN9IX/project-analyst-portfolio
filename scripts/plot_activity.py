from pathlib import Path
import csv
from datetime import datetime
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
with (ROOT/'reports/daily_activity.csv').open(encoding='utf-8',newline='') as f:rows=list(csv.DictReader(f))
dates=[datetime.strptime(x['date'],'%Y-%m-%d') for x in rows]
created=[int(x['issues_created']) for x in rows]
closed=[int(x['issues_closed']) for x in rows]
merged=[int(x['prs_merged']) for x in rows]
fig,ax=plt.subplots(figsize=(11,4.8))
ax.plot(dates,created,marker='o',linewidth=1.8,label='Создано Issues')
ax.plot(dates,closed,marker='o',linewidth=1.8,label='Закрыто Issues')
ax.plot(dates,merged,marker='o',linewidth=1.8,label='Merged PR')
ax.set_title('GitHub: ежедневная активность · 23.09–13.10.2026')
ax.set_ylabel('Количество событий за день')
ax.legend()
ax.grid(alpha=.2)
fig.autofmt_xdate();fig.tight_layout()
fig.savefig(ROOT/'reports/ACTIVITY_TREND.png',dpi=165)
print('Activity chart saved')
