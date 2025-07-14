import requests
from bs4 import BeautifulSoup

keyword = input("키워드 입력: ")
url = f"https://thehackernews.com/search?by-date=true&q={keyword}"
#https://kin.naver.com/search/list.naver?query=%ED%8C%8C%EC%9D%B4%EC%8D%AC

header_info = {'user-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'}
r = requests.get(url, headers=header_info,verify=False)
soup = BeautifulSoup(r.text, 'html.parser')

titles = soup.select("#___gcse_0 > div > div > div > div.gsc-wrapper > div.gsc-resultsbox-visible > div.gsc-resultsRoot.gsc-tabData.gsc-tabdActive > div > div.gsc-expansionArea > div > div > div.gsc-thumbnail-inside > div > a")

print(titles)