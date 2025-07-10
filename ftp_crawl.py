#quiz 2 정답예시

import feedparser
from openpyxl import Workbook
import os
import zipfile
import ftplib

RESULT_DIR = "results"
if not os.path.exists(RESULT_DIR):
    os.makedirs(RESULT_DIR)

with open('list.txt', 'r', encoding='utf-8') as file:
    rss_urls=file.readlines()

    for index,url in enumerate(rss_urls):
        feed = feedparser.parse(url)

        titles = []
        links = []
        descriptions = []
        authors = []
        pubDates = []

        for entry in feed.entries:
            titles.append(entry.title)
            links.append(entry.link)
            descriptions.append(entry.description)
            authors.append(entry.author)
            pubDates.append(entry.published)

        wb = Workbook()
        ws = wb.active
        ws.title = f"{index+1}번째 Data"
        headers = ['Title', 'Link', 'Description', 'Author', 'pubDate']
        ws.append(headers)

        for i in range(len(titles)):
            ws.append([titles[i], links[i], descriptions[i], authors[i], pubDates[i]])

        file_path = os.path.join(RESULT_DIR, f"{index+1}_result.xlsx")
        wb.save(file_path)