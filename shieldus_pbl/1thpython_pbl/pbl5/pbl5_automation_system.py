import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook
from email.message import EmailMessage
import smtplib
from datetime import datetime
import os
import re
import time
from dotenv import load_dotenv

def mail_sender():
    load_dotenv()

    # 날짜
    today_str = datetime.now().strftime('%Y-%m-%d')

    # 환경 변수에서 Gmail 로그인 정보와 수신자 이메일 로드
    SENDER_EMAIL = os.getenv("SECRET_ID")
    SENDER_PASSWORD = os.getenv("SECRET_PASS")
    recv_email = os.getenv("RECEIVER_EMAIL")

    # 스크래핑
    url = "https://www.malware-traffic-analysis.net/2024/index.html"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    tags = soup.select("#main_content ul li a")

    # 엑셀 저장
    filename = f"malware_{today_str}.xlsx"
    wb = Workbook()
    ws = wb.active
    ws.title = "Malware URL"
    ws.append(["제목", "링크"])

    for tag in tags:
        title = tag.text.strip()
        if re.fullmatch(r'\d{4}-\d{2}-\d{2}', title):
            continue  # 날짜만 있는 제목은 제외

        href = tag.get("href")
        link = url + href if not href.startswith("http") else href
        ws.append([title, link])

    wb.save(filename)
    print(f"[+] 엑셀 저장 완료: {filename}")

    # 이메일 작성
    msg = EmailMessage()
    msg['Subject'] = f"[스크래핑 결과] Malware Traffic Report - {today_str}"
    msg['From'] = SENDER_EMAIL
    msg['To'] = recv_email
    msg.set_content("스크래핑한 결과를 첨부합니다.")

    with open(filename, 'rb') as f:
        msg.add_attachment(
            f.read(),
            maintype='application',
            subtype='octet-stream',
            filename=os.path.basename(filename)
        )

    # 이메일 전송
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
        smtp.send_message(msg)
        print(f"[{datetime.now()}] 이메일 전송 완료!")

def run_daily(target_hour=21, target_minute=5):
    print(f"[+] 매일 {target_hour:02d}:{target_minute:02d}에 자동 실행 대기 중...")

    while True:
        now = datetime.now()
        if now.hour == target_hour and now.minute == target_minute:
            mail_sender()
            time.sleep(60)  # 1분 대기 (중복 실행 방지)

        time.sleep(10)  # 10초 간격으로 시간 체크

if __name__ == "__main__":
    run_daily(target_hour=21, target_minute=5)  # 오후 9시
