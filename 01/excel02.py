from openpyxl import Workbook
wb = Workbook()

ws = wb.active
ws.title = "New Title"

for i in range(10):
    row_cell = ws.cell(row=(i+1), column=1)
    row_cell.value = str(i+1) + "번째 데이터 저장"
wb.save("excel_data2.xlsx")
