from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Slack API 토큰과 메시지를 보낼 채널 설정
SLACK_API_TOKEN = "xoxb-9161188941607-9161236765159-C522gerTUS1YAdv22N6Za3Se"
SLACK_CHANNEL = "C0955R06Z36"

def send_message(channel, text):
    # WebClient 인스턴스 생성
    client = WebClient(token=SLACK_API_TOKEN)
    
    try:
        # 채널에 메시지 전송
        response = client.chat_postMessage(
            channel=channel,
            text=text
        )
        # 응답 출력
        print("Message sent successfully:", response["message"]["text"])
    except SlackApiError as e:
        # 에러 처리
        print("Error sending message:", e.response["error"])

# 메시지 전송 함수 호출
send_message(SLACK_CHANNEL, "Hello, this is a test message from Slack API!")