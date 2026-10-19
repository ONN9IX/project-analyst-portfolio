"""Strictly synthetic EVM learning workbook; not source-backed Smart Garden data."""
from pathlib import Path
import csv
from artifact_tool import Workbook,SpreadsheetFile
ROOT=Path(__file__).resolve().parents[1]
with (ROOT/'data/synthetic_evm_training.csv').open(encoding='utf-8') as f: rows=list(csv.reader(f))
wb=Workbook.create(); sh=wb.worksheets.add('EVM Training'); inf=wb.worksheets.add('Read me')
sh.merge_cells('A1:H2');sh.get_range('A1').values=[['EVM | УЧЕБНАЯ СИМУЛЯЦИЯ — НЕ РЕАЛЬНЫЙ ПРОЕКТ']]
sh.get_range('A1:H2').format={'fill':'#172A45','font':{'color':'#FFFFFF','bold':True,'size':15},'row_height':25,'vertical_alignment':'center'}
sh.get_range('A4:H4').values=[['Неделя','PV','EV','AC','SV = EV−PV','CV = EV−AC','SPI = EV/PV','CPI = EV/AC']]
sh.get_range('A4:H4').format={'fill':'#0B7285','font':{'color':'#FFFFFF','bold':True},'row_height':32}
for idx,r in enumerate(rows[1:],start=5):
    sh.get_range(f'A{idx}:D{idx}').values=[[int(x) for x in r]]
    sh.get_range(f'E{idx}:H{idx}').formulas=[[f'=C{idx}-B{idx}',f'=C{idx}-D{idx}',f'=IFERROR(C{idx}/B{idx},0)',f'=IFERROR(C{idx}/D{idx},0)']]
sh.get_range('B5:F10').set_number_format('#,##0')
sh.get_range('G5:H10').set_number_format('0.000')
sh.get_range('E5:F10').conditional_formats.add_cell_is({'operator':'lessThan','formula':0,'format':{'font':{'color':'#B91C1C'}}})
sh.get_range('A:A').format.column_width=12
sh.get_range('B:H').format.column_width=18
sh.get_range('A4:H10').format.row_height=29
sh.freeze_panes.freeze_rows(4)
sh.merge_cells('A13:H13');sh.get_range('A13').values=[['Все суммы придуманы для тренировки формул. Нельзя приписывать их Smart Garden или работодателю.']]
sh.get_range('A13:H13').format={'fill':'#EBF3F6','font':{'color':'#172A45'},'row_height':26}
inf.get_range('A1:B1').values=[['Термин','Значение']]
inf.get_range('A1:B1').format={'fill':'#172A45','font':{'color':'#FFFFFF','bold':True}}
records=[['PV','Плановая стоимость освоения'],['EV','Освоенный объём'],['AC','Фактические затраты'],['SV','EV минус PV'],['CV','EV минус AC'],['SPI','EV / PV'],['CPI','EV / AC'],['Статус','Synthetic training, not actual company records']]
inf.get_range('A2:B9').values=records
inf.get_range('A:A').format.column_width=18;inf.get_range('B:B').format.column_width=60
out=ROOT/'EVM Training.xlsx';SpreadsheetFile.export_xlsx(wb).save(str(out))
print('EVM created:',out)
try:print('EVM sample inspect',wb.inspect({'kind':'region','sheet_id':'EVM Training','range':'A9:H10'}).ndjson[:1800])
except Exception as e:print(type(e).__name__,str(e)[:160])
