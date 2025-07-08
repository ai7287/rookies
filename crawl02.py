import requests
from bs4 import BeautifulSoup

url = "https://www.dailysecu.com/"

header_info = {'user-Agent': 'MMozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'}
r = requests.get(url, headers=header_info,verify=False)
soup = BeautifulSoup(r.text, 'html.parser')

links = soup.find_all('a')

for link in links:
    print(f"{link.string}: {link.get('href')}")