import os
import time
from datetime import datetime

dir_path = "uploads"
pre_file = set(os.listdir(dir_path))

while True:
    #날짜 표시
    now = datetime.now()
    day = now.strftime("%Y-%m-%d")
    hour = now.strftime("%H:%M:%S")
    
    current_file = set(os.listdir(dir_path))
    result_diff = current_file - pre_file

    for file_name in result_diff:
        print(f"새로운 파일 탐지: {file_name}")
        with open(f"{day}월_탐지 보고서.txt", "a", encoding="utf-8") as file:
            file.write(f"작성자 : 김윤호")
            file.write(f"주요 내용: 신규 파일 탐지\n")
            file.write(f"시간 {hour}, 파일 이름: {file_name}\n")
            file.write(f"======================================\n")

    pre_file = current_file
    print("모니터링 중")
    time.sleep(1)