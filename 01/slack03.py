from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Slack API 토큰과 메시지를 보낼 채널 설정
SLACK_API_TOKEN = "xoxb-9161188941607-9161236765159-C522gerTUS1YAdv22N6Za3Se"
SLACK_CHANNEL = "C0955R06Z36"
# 채널 접근 후 URL 뒤에서 확인 가능

def upload_file(channel, file_path, message):
    # WebClient 인스턴스 생성
    client = WebClient(token=SLACK_API_TOKEN)
    
    try:
        # 파일을 Slack 채널에 업로드하고, 해당 파일에 메시지를 추가합니다.
        response = client.files_upload_v2(
            channel=channel, 
            file=file_path,
            initial_comment=message
        )
        # 업로드 성공 메시지 출력
        print("File uploaded successfully:", response["file"]["name"])
    except SlackApiError as e:
        # 에러 처리
        print("Error uploading file:", e.response["error"])

# 파일 업로드 및 메시지 전송 함수 호출
upload_file(SLACK_CHANNEL, "malware.xlsx", "보안뉴스 수집 완료")