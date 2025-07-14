import feedparser
from newspaper import Article
from summa.summarizer import summarize

# The Hacker News RSS URL
rss_url = "https://feeds.bbci.co.uk/news/world/rss.xml"
rss_feed = feedparser.parse(rss_url)

print(f"총 {len(rss_feed.entries)}개의 기사 발견\n")

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'

for p in rss_feed.entries:
    url = p.link

    try:
        article = Article(url, language='en', browser_user_agent=USER_AGENT)
        article.download()
        article.parse()

        NewsFeed = article.text
        NewsSum = summarize(NewsFeed)

        print(f"제목: {article.title}\n")
        print(f"원문:\n{NewsFeed[:1000]}...\n")  # 원문 일부만 출력
        print(f"요약:\n{NewsSum}\n")
        print("=" * 100 + "\n")

    except Exception as e:
        print(f"기사 처리 실패: {url}")
        print(f"에러: {e}\n")
