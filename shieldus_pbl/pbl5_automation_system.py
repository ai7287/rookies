import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook
from email.message import EmailMessage
import smtplib
from datetime import datetime
import os
from dotenv import load_dotenv

def mail_sender():
    load_dotenv()

    # 1. 날짜 정보
    today_str = datetime.now().strftime('%Y-%m-%d')
    
    # 2. 발신자 정보 (환경 변수에서 불러옴)
    SENDER_EMAIL = os.getenv("SECRET_ID")
    SENDER_PASSWORD = os.getenv("SECRET_PASS")

    # 3. 스크래핑
    url = "https://www.malware-traffic-analysis.net/2024/index.html"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    tags = soup.select("#main_content ul li a")

    # 4. 엑셀 저장
    filename = f"malware_{today_str}.xlsx"
    wb = Workbook()
    ws = wb.active
    ws.title = "Malware URL"
    ws.append(["제목", "링크"])

    for tag in tags:
        title = tag.text.strip()
        href = tag.get("href")
        link = url + href if not href.startswith("http") else href
        ws.append([title, link])

    wb.save(filename)
    print(f"[+] 엑셀 저장 완료: {filename}")

    # 5. 수신자 입력
    recv_email = input("수신자 이메일 주소: ")

    # 6. 이메일 작성
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

    # 7. SMTP 전송
    with smtplib.SMTP_SSL("smtp.naver.com", 465) as smtp:
        smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
        smtp.send_message(msg)
        print("[+] 이메일 전송 완료!")

if __name__ == "__main__":
    mail_sender()

hmm