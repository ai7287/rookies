from flask import Flask, request, render_template
from ftplib import FTP

app = Flask(__name__)

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    # 사용자가 입력한 값에서 공백 제거
    host = request.form.get('host', '').strip()
    user = request.form.get('username', '').strip()
    pw = request.form.get('password', '').strip()

    if not host or not user or not pw:
        return "❗ 모든 입력값을 입력해주세요."

    try:
        # FTP 접속 시도
        ftp = FTP(host)
        ftp.login(user=user, passwd=pw)

        # 현재 경로 및 파일 목록 출력
        print("📁 현재 경로:", ftp.pwd())
        print("📄 파일 목록:")
        files = []
        ftp.retrlines('LIST', lambda line: files.append(line))
        for f in files:
            print(f)

        ftp.quit()

        return render_template('index.html', files=files, host=host)
    except Exception as e:
        print("🚨 에러 발생:", e)
        return f"로그인 실패: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
