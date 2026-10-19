"""One-off static Excel portfolio artifact, assembled with artifact_tool.

Requires artifact_tool in the Python environment; if unavailable, follow
../docs/EXCEL_RECREATE.md to refresh the exported snapshot in Excel.
"""
from pathlib import Path
import csv
import base64
from artifact_tool import Workbook,SpreadsheetFile

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'Project Dashboard.xlsx'

def csv_rows(path):
    with path.open(encoding='utf-8',newline='') as f:return list(csv.reader(f))

navy='#172A45'; teal='#0B7285'; white='#FFFFFF'; pale='#EBF3F6'; grey='#5B6471'
header={'fill':navy,'font':{'bold':True,'color':white},'row_height':28,'vertical_alignment':'center'}
subheader={'fill':pale,'font':{'bold':True,'color':navy},'row_height':27}
wb=Workbook.create()
dashboard=wb.worksheets.add('Dashboard')
issues=wb.worksheets.add('Issues')
prs=wb.worksheets.add('PRs')
trend=wb.worksheets.add('Daily Activity')
risks=wb.worksheets.add('Risks')
method=wb.worksheets.add('Methodology')

# Raw snapshots. Avoid truncation of numeric identifiers, retain source URLs.
irows=csv_rows(ROOT/'data/github_issues_snapshot.csv')
prows=csv_rows(ROOT/'data/github_prs_snapshot.csv')
trows=csv_rows(ROOT/'reports/daily_activity.csv')
rrows=csv_rows(ROOT/'data/risk_register_training.csv')

for sheet,rows,columns in [(issues,irows,7),(prs,prows,5),(trend,trows,5),(risks,rrows,8)]:
    # Risk data has 8 input columns, ninth column is a formula.
    matrix=[]
    for idx,row in enumerate(rows):
        if sheet==issues and idx:
            row=[int(row[0]),*row[1:]]
        if sheet==prs and idx:
            row=[int(row[0]),*row[1:]]
        if sheet==trend and idx:
            row=[row[0],*map(int,row[1:])]
        if sheet==risks and idx:
            row=[row[0],row[1],int(row[2]),int(row[3]),*row[4:]]
        matrix.append(row)
    if sheet==risks:
        matrix[0].append('risk_score')
        for row in matrix[1:]:row.append(None)
    sheet.get_range_by_indexes(0,0,len(matrix),len(matrix[0])).values=matrix
    sheet.get_range_by_indexes(0,0,1,len(matrix[0])).format=header
    sheet.freeze_panes.freeze_rows(1)
    sheet.get_range_by_indexes(0,0,len(matrix),len(matrix[0])).format.row_height=21
    sheet.get_range_by_indexes(0,0,1,len(matrix[0])).format.row_height=34
    sheet.get_range_by_indexes(0,0,len(matrix),len(matrix[0])).format.vertical_alignment='center'

issues.get_range('A:A').format.column_width=10
issues.get_range('B:C').format.column_width=14
issues.get_range('D:E').format.column_width=16
issues.get_range('F:F').format.column_width=47
issues.get_range('G:G').format.column_width=60
prs.get_range('A:A').format.column_width=12
prs.get_range('B:C').format.column_width=15
prs.get_range('D:D').format.column_width=23
prs.get_range('E:E').format.column_width=58
trend.get_range('A:A').format.column_width=17
trend.get_range('B:E').format.column_width=19
risks.get_range('A:A').format.column_width=11
risks.get_range('B:B').format.column_width=47
risks.get_range('C:D').format.column_width=17
risks.get_range('E:E').format.column_width=29
risks.get_range('F:F').format.column_width=17
risks.get_range('G:G').format.column_width=53
risks.get_range('H:H').format.column_width=54
risks.get_range('I:I').format.column_width=15
risks.get_range('I2').formulas=[['=C2*D2']]
risks.get_range(f'I2:I{len(rrows)}').fill_down()
risks.get_range(f'I2:I{len(rrows)}').conditional_formats.add_color_scale({'minColor':'#E8F4EB','midColor':'#FFF1C6','maxColor':'#FCE4E4'})

# Dashboard with spreadsheet-native formulas; no hardcoded KPI counts.
dashboard.merge_cells('A1:L2')
dashboard.get_range('A1').values=[['PROJECT OPERATIONS | GITHUB SNAPSHOT']]
dashboard.get_range('A1:L2').format={'fill':navy,'font':{'bold':True,'color':white,'size':17},'row_height':27,'vertical_alignment':'center'}
dashboard.merge_cells('A3:L3')
dashboard.get_range('A3').values=[['13.10.2026 · Smart Garden, данные только для чтения · не финансовая отчётность']]
dashboard.get_range('A3:L3').format={'fill':pale,'font':{'color':navy,'size':11},'row_height':26}
dashboard.get_range('A5:B5').values=[['ISSUES','Количество']]
dashboard.get_range('E5:F5').values=[['PULL REQUESTS','Количество']]
dashboard.get_range('A5:B5').format=header
dashboard.get_range('E5:F5').format=header
for row,label in [(6,'Всего Issues'),(7,'Закрыто'),(8,'Открыто'),(9,'Доля закрытых')]:
    dashboard.get_range(f'A{row}').values=[[label]]
for row,label in [(6,'Всего PR'),(7,'Merged'),(8,'Open'),(9,'Closed (no merge)')]:
    dashboard.get_range(f'E{row}').values=[[label]]
iend=len(irows); pend=len(prows)
for cell,form in {
    'B6':f'=COUNTA(Issues!A2:A{iend})',
    'B7':f'=COUNTIF(Issues!D2:D{iend},"closed")',
    'B8':f'=COUNTIF(Issues!D2:D{iend},"open")',
    'B9':'=IFERROR(B7/B6,0)',
    'F6':f'=COUNTA(PRs!A2:A{pend})',
    'F7':f'=COUNTIF(PRs!D2:D{pend},"merged")',
    'F8':f'=COUNTIF(PRs!D2:D{pend},"open")',
    'F9':f'=COUNTIF(PRs!D2:D{pend},"closed_not_merged")',
}.items():dashboard.get_range(cell).formulas=[[form]]
dashboard.get_range('B9').set_number_format('0.0%')
dashboard.get_range('A6:B9').format.row_height=29
dashboard.get_range('E6:F9').format.row_height=29
dashboard.get_range('B6:B9').format={'font':{'bold':True,'color':teal,'size':13},'horizontal_alignment':'right'}
dashboard.get_range('F6:F9').format={'font':{'bold':True,'color':teal,'size':13},'horizontal_alignment':'right'}
dashboard.get_range('B9').set_number_format('0.0%')
dashboard.merge_cells('A12:L12')
dashboard.get_range('A12').values=[['ЧТО НЕЛЬЗЯ ЗАКЛЮЧИТЬ ИЗ ЭТИХ ДАННЫХ']]
dashboard.get_range('A12:L12').format=header
dashboard.merge_cells('A13:L14')
dashboard.get_range('A13').values=[['Доля закрытых Issues НЕ равна готовности проекта. Нет плана сроков, бюджета, часов, story points и подтверждённых затрат: SPI/CPI, velocity и выполнение плана здесь не рассчитываются.']]
dashboard.get_range('A13:L14').format={'fill':pale,'font':{'color':navy},'wrap_text':True,'row_height':27,'vertical_alignment':'center'}
dashboard.merge_cells('A17:F17')
dashboard.get_range('A17').values=[['Источники и воспроизводимость']]
dashboard.get_range('A17:F17').format=subheader
dashboard.merge_cells('A18:L18');dashboard.get_range('A18').values=[['Issues и PRs · публичный REST API GitHub · дата среза 13.10.2026']]
dashboard.merge_cells('A19:L19');dashboard.get_range('A19').values=[['Все объекты имеют source_url. Pull Requests исключены из Issues.']]
dashboard.merge_cells('A20:L20');dashboard.get_range('A20').values=[['Методика — docs/ANALYSIS_METHOD.md; тесты — python -m unittest discover -s tests -v']]
dashboard.merge_cells('A22:L22');dashboard.get_range('A22').values=[['Управленческие вопросы: персональные данные (#223), пилот (#187), универсальные профили (#162), PWA (#189).']]
dashboard.get_range('A18:L22').format.row_height=27
for col in ['A','E']:
    dashboard.get_range(f'{col}:{col}').format.column_width=27
for col in ['B','F']:
    dashboard.get_range(f'{col}:{col}').format.column_width=16
for col in ['C','D','G','H','I','J','K','L']:
    dashboard.get_range(f'{col}:{col}').format.column_width=10

# Add a trend visualization to the separate dedicated worksheet.
try:
    c=trend.charts.add('line',trend.get_range(f'A1:C{len(trows)}'))
    c.title_text='Динамика регистрации и закрытия Issues'
    c.set_position('G2','Q18')
except Exception as ex:
    print('Chart warning:',type(ex).__name__,str(ex)[:160])

# Embed a chart preview inside the dashboard, below the KPI panel.
try:
    dashboard.merge_cells('A25:L25')
    dashboard.get_range('A25').values=[['ЕЖЕДНЕВНАЯ АКТИВНОСТЬ · исторический снимок GitHub API']]
    dashboard.get_range('A25:L25').format=header
    chart_png=(ROOT/'reports/ACTIVITY_TREND.png').read_bytes()
    dashboard.images.add({'dataUrl':'data:image/png;base64,'+base64.b64encode(chart_png).decode(),
        'anchor':{'from':{'row':26,'col':0},'extent':{'widthPx':1130,'heightPx':440}}})
except Exception as ex:
    print('Embedded chart warning:',type(ex).__name__,str(ex)[:150])

# Methods panel: explicit distinctions between observed fields and analyst assumptions.
method.get_range('A1:B1').values=[['Показатель / правило','Пояснение']]
method.get_range('A1:B1').format=header
methods=[
 ('Дата среза','13 октября 2026; это не live-отчёт'),
 ('Источник','Публичные GitHub Issues и Pull Requests репозитория ONN9IX/smart-garden'),
 ('Issues','Из общего endpoint /issues исключены записи с объектом pull_request'),
 ('Закрытые Issues','state=closed, закрытие не означает готовность всего продукта'),
 ('PR merged','merged_at != null, не путать с просто closed'),
 ('Сроки','Календарные даты GitHub не равны человеко-часам'),
 ('Бюджет / EVM','Не рассчитаны: нет PV, EV, AC и baseline'),
 ('Риски','Вероятность/влияние — экспертные учебные оценки, не факты исходного проекта'),
 ('ПДн','Технический MVP не равен production-ready для обработки реальных ПДн'),
 ('Обновление','python scripts/refresh_from_github.py и затем build_reports.py; XLSX вручную обновить'),
]
method.get_range_by_indexes(1,0,len(methods),2).values=[list(x) for x in methods]
method.get_range('A:A').format.column_width=28
method.get_range('B:B').format.column_width=95
method.get_range(f'A2:B{len(methods)+1}').format.row_height=30
method.get_range(f'B2:B{len(methods)+1}').format.wrap_text=True
method.freeze_panes.freeze_rows(1)

SpreadsheetFile.export_xlsx(wb).save(str(OUT))
try:
    print('Dashboard KPI inspect:', wb.inspect({'kind':'region','sheet_id':'Dashboard','range':'A5:F9'}).ndjson[:1500])
except Exception as e:
    print('Inspect warning',type(e).__name__,str(e)[:250])
print('Excel saved:',OUT,OUT.stat().st_size)
