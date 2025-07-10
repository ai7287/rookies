from openpyxl import Workbook
wb = Workbook()

ws = wb.active
ws.title = "New Title"

for row in ws['A1:D4']:
    for cell in row:
        cell.value = "hello world"
wb.save("text.xlsx")
