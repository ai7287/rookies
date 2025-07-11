#스케줄링
import schedule
import time

def rss_url():
    print("Test입니다.")

schedule.every(3).seconds.do(rss_url) # 3초마다 job 실행

while True:
    schedule.run_pending()
    time.sleep(1)