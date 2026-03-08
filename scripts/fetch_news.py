#!/usr/bin/env python3
"""
Fetch financial news from RSS feeds.
"""

import json
import feedparser
import datetime
from typing import List, Dict

# RSS feeds for financial news
FEEDS = {
    'Bloomberg': 'https://www.bloomberg.com/feed/podcast/etf-report.xml',
    'Reuters Business': 'https://www.reuters.com/business/rss',
    'Reuters Markets': 'https://www.reuters.com/news/rss/marketsNews',
    'Reuters Finance': 'https://www.reuters.com/finance/rss',
    'Financial Times': 'https://www.ft.com/?format=rss',
    'Wall Street Journal': 'https://feeds.a.dj.com/rss/RSSMarketsMain.xml',
    'CNBC': 'https://www.cnbc.com/id/100003114/device/rss/rss.html',
    'ASX News': 'https://www.asx.com.au/asx/rss/asxann.rss',
    'Yahoo Finance': 'https://finance.yahoo.com/news/rssindex',
}

def fetch_feed(url: str, max_items: int = 10) -> List[Dict]:
    """Fetch and parse an RSS feed."""
    try:
        feed = feedparser.parse(url)
        items = []
        for entry in feed.entries[:max_items]:
            items.append({
                'title': entry.get('title', 'No title'),
                'link': entry.get('link', ''),
                'published': entry.get('published', entry.get('updated', '')),
                'summary': entry.get('summary', entry.get('description', '')),
                'source': feed.feed.get('title', 'Unknown')
            })
        return items
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return []

def fetch_all_news(max_per_feed: int = 5) -> Dict:
    """Fetch news from all configured feeds."""
    all_articles = []
    sources_used = {}
    
    for source, url in FEEDS.items():
        articles = fetch_feed(url, max_items=max_per_feed)
        for article in articles:
            article['source_name'] = source
            all_articles.append(article)
        sources_used[source] = len(articles)
    
    # Sort by publication date (newest first)
    # Simple date parsing - assumes RFC 822 or ISO format
    def get_date(article):
        try:
            # Try parsing date string
            from email.utils import parsedate_to_datetime
            if article['published']:
                return parsedate_to_datetime(article['published'])
        except:
            pass
        return datetime.datetime.min
    
    all_articles.sort(key=get_date, reverse=True)
    
    return {
        'articles': all_articles,
        'sources': sources_used,
        'total': len(all_articles),
        'generated_at': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

if __name__ == "__main__":
    data = fetch_all_news()
    print(json.dumps(data, indent=2))
