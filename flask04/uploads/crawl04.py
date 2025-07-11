import requests
from bs4 import BeautifulSoup

keyword = input("키워드 입력: ")
url = f"https://kin.naver.com/search/list.naver?query={keyword}"
# https://kin.naver.com/search/list.naver?query=%ED%8C%8C%EC%9D%B4%EC%8D%AC

header_info = {
    "user-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
}
r = requests.get(url, headers=header_info, verify=False)
soup = BeautifulSoup(r.text, "html.parser")

titles = soup.select("#s_content > div.section > ul > li > dl > dt > a")
dates = soup.select("#s_content > div.section > ul > li> dl > dd.txt_inline")

# titles,dates 개수가 일치해야함
for title, data in zip(titles, dates):
    print(f"질문 : {title.text}")
    print(f"날짜 : {data.text}")

# 네이버 지식인 결과값 가져오기 (input값이 검색값 ex - 파이썬)
