# modules/notification.py

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

load_dotenv()

def send_slack_file(channel, file_path, message):
    slack_token = os.getenv("SLACK_API_TOKEN")
    if not slack_token:
        print("슬랙 API 토큰이 설정되지 않았습니다.")
        return
        
    client = WebClient(token=slack_token)
    try:
        response = client.files_upload_v2(
            channel=channel,
            file=file_path,
            initial_comment=message
        )
        print("Slack 파일 전송 완료:", response["file"]["name"])
    except SlackApiError as e:
        print(f"Slack 파일 전송 오류: {e.response['error']}")

def send_email_with_attachment(file_path, to_email):
    send_email = os.getenv("SECRET_ID")
    send_pwd = os.getenv("SECRET_PASS")
    
    if not all([send_email, send_pwd]):
        print("이메일 ID 또는 PW가 설정되지 않았습니다.")
        return

    smtp_name = "smtp.naver.com"
    smtp_port = 587

    msg = MIMEMultipart()
    msg['Subject'] = "보안 정보 통합 검색 결과 보고서"
    msg['From'] = send_email
    msg['To'] = to_email

    body = "요청하신 검색 결과 보고서를 첨부파일로 전달드립니다."
    msg.attach(MIMEText(body, 'plain', 'utf-8'))

    try:
        with open(file_path, 'rb') as f:
            mime = MIMEBase('application', 'vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            mime.set_payload(f.read())
            encoders.encode_base64(mime)
            mime.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(file_path)}"')
            msg.attach(mime)

        s = smtplib.SMTP(smtp_name, smtp_port)
        s.starttls()
        s.login(send_email, send_pwd)
        s.sendmail(send_email, to_email, msg.as_string())
        s.quit()
        print(f"이메일 전송 완료: {to_email}")
    except Exception as e:
        print(f"이메일 전송 중 오류 발생: {e}")