import feedparser
import pandas as pd
import zipfile
import os
import ftplib


def upload_file(ftp, filename):
    with open(filename, 'rb') as f:
        ftp.storbinary('STOR ' + filename,f)

'''
url = "https://www.dailysecu.com/rss/clickTop.xml"

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

data = {'Title': titles, "Link": links, "Description": descriptions, "Author": authors, "pubDate":pubDates}

df= pd.DataFrame(data)
# 엑셀로 저장
df.to_excel("third.xlsx", index=False)
print("저장 완료: third.xlsx")
'''
RESULT_DIR = 'uploads'
zip_file = zipfile.ZipFile('quiz2.zip','w')

for root, dirs, files in os.walk(RESULT_DIR):
    for file in files:
        zip_file.write(os.path.join(root,file))
        
zip_file.close()

hostname = "192.168.241.128"
ftp = ftplib.FTP(hostname)
ftp.login('msfadmin','msfadmin')
upload_file(ftp, 'quiz2.zip')
ftp.quit()
