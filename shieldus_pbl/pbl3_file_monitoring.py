import os
import time
from datetime import datetime
import re

dir_path = "01/uploads"
pre_file = set(os.listdir(dir_path))

email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

while True:
    now = datetime.now()
    day = now.strftime("%Y-%m-%d")
    hour = now.strftime("%H:%M:%S")

    current_file = set(os.listdir(dir_path))
    result_diff = current_file - pre_file  # 새로 추가된 파일 목록

    for file_name in result_diff:
        file_path = os.path.join(dir_path, file_name)
        print(f"새로운 파일 탐지: {file_name}")

        with open(f"{day}월_탐지 보고서.txt", "a", encoding="utf-8") as file:
            file.write(f"작성자 : 김윤호\n")
            file.write(f"주요 내용: 신규 파일 탐지\n")
            file.write(f"시간 {hour}, 파일 이름: {file_name}\n")

            try:
                with open(file_path, "r", encoding="utf-8") as new_file:
                    for line_num, line in enumerate(new_file, start=1):
                        stripped = line.strip()
                        if stripped.startswith("#") or stripped.startswith("//"):
                            file.write(f"  [주석] {line_num}줄: {stripped}\n")
                            email_match = re.search(email_pattern, line)
                            if email_match:
                                file.write(f"→ 이메일 발견: {email_match.group()}\n")

            except Exception as e:
                file.write(f"  [오류] 파일을 열 수 없음: {e}\n")

            file.write("======================================\n")

    pre_file = current_file
    print("모니터링 중...")
    time.sleep(2)