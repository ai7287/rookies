from flask import Flask, render_template, request, send_file
from docx import Document
from docx2pdf import convert

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def certificate():
    if request.method == 'POST':
        name = request.form.get('name')
        course = request.form.get('course')
        date = request.form.get('date')

        doc = Document("template.docx")  # replace with your template file
        for paragraph in doc.paragraphs:
            if 'NAME' in paragraph.text:
                paragraph.text = paragraph.text.replace('NAME', name)
            elif 'COURSE' in paragraph.text:
                paragraph.text = paragraph.text.replace('COURSE', course)
            elif 'DATE' in paragraph.text:
                paragraph.text = paragraph.text.replace('DATE', date)

        doc_filename = f"{name}_{course}_certificate.docx"
        pdf_filename = f"{name}_{course}_certificate.pdf"
        doc.save(doc_filename)

        convert(doc_filename, pdf_filename)

        return send_file(pdf_filename, as_attachment=True)
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)