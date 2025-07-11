from flask import Flask, render_template, request, send_file
import os
from datetime import datetime
import zipfile

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def list():
     UPLOAD_PATH = "uploads"
     files = []
     for file in os.listdir(UPLOAD_PATH):
          
          file_path = os.path.join(UPLOAD_PATH, file)
          file_size = os.path.getsize(file_path)
          file_ctime = datetime.fromtimestamp(os.path.getctime(file_path)).strftime('%Y-%m-%d %H:%M:%S')
          print(f"경로: {file_path}, 크기: {file_size}, ctime: {file_ctime}")
          files.append((file, file_size, file_ctime, file_path))
     return render_template('list.html', files=files)

@app.route('/compress', methods=['GET', 'POST'])
def compress():
    UPLOAD_PATH = "uploads"
    files = request.form.getlist('files')
    zip_path = os.path.join(UPLOAD_PATH, "compress.zip")
    
    with zipfile.ZipFile(zip_path, 'w') as zip_file:
         for file in files:
            file_path = os.path.join(UPLOAD_PATH, file)
            zip_file.write(file_path, file)

    return send_file(zip_path, as_attachment=True)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
        UPLOAD_PATH = "uploads"
        file = request.files['file']
        file_path = os.path.join(UPLOAD_PATH, file.filename)
        file.save(file_path)
        return "업로드 완료"

if __name__ == "__main__":
    app.run(debug=True)