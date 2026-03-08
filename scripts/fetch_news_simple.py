#!/usr/bin/env python3
"""
Fetch financial news from RSS feeds - no external dependencies.
"""

import json
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
import datetime
from typing import List, Dict

# RSS feeds for financial news
FEEDS = {
    'Reuters Markets': 'https://www.reuters.com/news/rss/marketsNews',
    'Yahoo Finance': 'https://finance.yahoo.com/news/rssindex',
    'CNBC': 'https://www.cnbc.com/id/100003114/device/rss/rss.html',
}

def fetch_feed(url: str, max_items: int = 5) -> List[Dict]:
    """Fetch and parse an RSS feed using standard library."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            data = response.read().decode('utf-8', errors='ignore')
        
        # Parse XML
        root = ET.fromstring(data)
        
        # Find items (RSS 2.0 format)
        items = []
        # RSS items are typically <channel><item>...</item></channel>
        channel = root.find('channel')
        if channel is not None:
            elements = channel.findall('item')
        else:
            # Atom feed?
            elements = root.findall('{http://www.w3.org/2005/Atom}entry')
        
        for elem in elements[:max_items]:
            def get_text(tag):
                el = elem.find(tag)
                return el.text if el is not None else ''
            
            title = get_text('title') or ''
            link = get_text('link') or ''
            desc = get_text('description') or get_text('summary') or ''
            pub_date = get_text('pubDate') or get_text('updated') or ''
            
            if title and link:
                items.append({
                    'title': title.strip(),
                    'link': link.strip(),
                    'published': pub_date.strip(),
                    'summary': desc.strip()[:200] + ('...' if len(desc) > 200 else ''),
                })
        return items
    except Exception as e:
        import sys
        print(f"Error fetching {url}: {e}", file=sys.stderr)
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
    
    # Simple sort: try to put newer first, but don't fail on bad dates
    # We'll keep insertion order (sources are in order of preference)
    # Or we can reverse so newest sources' items appear first
    all_articles.reverse()
    
    return {
        'articles': all_articles,
        'sources': sources_used,
        'total': len(all_articles),
        'generated_at': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

if __name__ == "__main__":
    data = fetch_all_news()
    print(json.dumps(data, indent=2))
