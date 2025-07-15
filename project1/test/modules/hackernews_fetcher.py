# modules/hackernews_fetcher.py

import feedparser
from summa.summarizer import summarize
from datetime import datetime
import re
import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
from .translator import translate_text_to_korean

load_dotenv()
SCRAPER_API_KEY = os.getenv("SCRAPER_API_KEY")

def fetch_summary_with_scraperapi(article_url):
    try:
        proxy_url = f"http://api.scraperapi.com/?api_key={SCRAPER_API_KEY}&url={article_url}"
        response = requests.get(proxy_url, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        paragraphs = soup.find_all("p")
        content = "\n".join(p.get_text(strip=True) for p in paragraphs)

        if content.strip():
            summary = summarize(content, words=100)
            return summary.strip() if summary else "요약 내용 없음"
        else:
            return "본문 없음"
    except Exception as e:
        print(f"요약 실패 ({article_url}): {e}")
        return "요약 실패"

def fetch_hacker_news(keyword):
    url = "https://thehackernews.com/feeds/posts/default"
    feed = feedparser.parse(url)
    results = []

    for entry in feed.entries:
        title = entry.title
        link = entry.link
        
        if keyword and keyword.lower() not in title.lower():
            continue
        
        published_dt = datetime.strptime(entry.published, "%a, %d %b %Y %H:%M:%S %z")
        published = published_dt.strftime("%Y-%m-%d")
        
        cve_match = re.search(r"CVE-\d{4}-\d{4,7}", title, re.IGNORECASE)
        cve_id = cve_match.group() if cve_match else ""

        summary = fetch_summary_with_scraperapi(link)
        description_ko = translate_text_to_korean(summary)
        
        
        results.append({
            "source": "HackerNews",
            "id": title,
            "description_en": "", # 원본 설명 필드
            "description_ko": description_ko,
            "score": None,
            "link": link,
            "published_date": published,
            "cve_id_in_title": cve_id,
        })
    return results