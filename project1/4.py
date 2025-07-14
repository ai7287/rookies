import feedparser
from newspaper import Article
from summa.summarizer import summarize
import pandas as pd
from datetime import datetime
import re


def get_all_articles():
    url = "https://thehackernews.com/feeds/posts/default"
    feed = feedparser.parse(url)

    results = []
    for entry in feed.entries:
        title = entry.title
        link = entry.link
        published_first = entry.published
        
        published = datetime.strptime(published_first, "%a, %d %b %Y %H:%M:%S %z").strftime("%Y-%m-%d")

        if keyword and keyword.lower() not in title.lower():
            continue
        
        cve_match = re.search(r"CVE-\d{4}-\d{4,5}", title)
        cve_id = cve_match.group() if cve_match else ""

        results.append({
            "title": title,
            "link": link,
            "date": published,
            "CVE ID": cve_id
        })

    return results

def save_to_excel(articles):
    df = pd.DataFrame(articles)
    filename = f"thehackernews_{datetime.now().strftime('%Y-%m-%d')}.xlsx"
    
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='hackersnew')

    print(f"엑셀 저장 완료: {filename}")

if __name__ == "__main__":
    keyword = input("키워드 입력: ").strip()
    articles = get_all_articles()
    if articles:
        save_to_excel(articles)
    else:
        print("검색 결과가 없습니다.")