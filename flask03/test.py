#pip install python-docx
#pip install docx2pdf

from docx import Document
from docx2pdf import convert

name = input("이름을 입력하세요:")
course = input("과정명을 입력하세요:")
date = input("날짜를 입력하세요:")

doc = Document('template.docx')

for paragraph in doc.paragraphs:
    if 'NAME' in paragraph.text:
        paragraph.text = paragraph.text.replace('NAME', name)
    elif 'COURSE' in paragraph.text:
        paragraph.text = paragraph.text.replace('COURSE', course)
    elif 'DATE' in paragraph.text:
        paragraph.text = paragraph.text.replace('DATE', date)

doc.save('result.docx')
convert('result.docx', 'result.pdf')