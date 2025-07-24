from flask import Flask, request, render_template
from datetime import datetime
import os

from modules.zip import zip_directory
from modules.upload import connect_ftp, upload_to_ftp

app = Flask(__name__)

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    host = request.form.get('host', '').strip()
    user = request.form.get('username', '').strip()
    pw = request.form.get('password', '').strip()

    if not host or not user or not pw:
        return "모든 입력값을 입력해주세요."

    try:
        ftp = connect_ftp(host, user, pw)
        files = []
        ftp.retrlines('LIST', lambda line: files.append(line))
        ftp.quit()
        return render_template('index.html', files=files, host=host, username=user, password=pw)
    except Exception as e:
        return f"로그인 실패: {str(e)}"

@app.route('/upload_zip', methods=['POST'])
def upload_zip():
    host = request.form.get('host')
    user = request.form.get('username')
    pw = request.form.get('password')

    backup_dir = os.path.join('static', 'backup')
    now = datetime.now().strftime('%Y-%m-%d')
    zip_filename = f"backup_{now}.zip"
    zip_path = os.path.join('static', zip_filename)

    # zip 파일 저장할 폴더가 없으면 생성
    zip_folder = os.path.dirname(zip_path)
    if not os.path.exists(zip_folder):
        os.makedirs(zip_folder)

    try:
        from modules.zip import zip_directory
        from modules.upload import connect_ftp, upload_to_ftp

        zip_directory(backup_dir, zip_path)

        ftp = connect_ftp(host, user, pw)
        upload_to_ftp(ftp, zip_path, zip_filename)
        ftp.quit()

        return f"압축 및 FTP 업로드 완료: {zip_filename}"
    except Exception as e:
        return f"오류 발생: {e}"

if __name__ == '__main__':
    app.run(debug=True)
