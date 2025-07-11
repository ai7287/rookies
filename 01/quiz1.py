#  인프라 활용을 위한 파이썬 / 웹스크레핑 -request 라이브의 퀴즈

import requests
from bs4 import BeautifulSoup

url = "https://www.malware-traffic-analysis.net/2023/index.html"

header_info = {'user-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'}
r = requests.get(url, headers=header_info,verify=False)
soup = BeautifulSoup(r.text, 'html.parser')

results = []

tags = soup.select("#main_content > div.content > ul > li> a.main_menu")
# ul 점모양

results= []
for tag in tags:
    link_text = tag.text
    link_href = f"'https://www.malware-traffic-analysis.net/2023/{tag.get('href')}'"
    results.append(f"{link_text}\n: {link_href}\n")
    print(link_text)
    print(link_href)

with open("malware.xlsx", "w", encoding="utf-8") as file:
    for result in results:
        file.write(result)