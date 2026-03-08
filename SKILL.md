---
name: financial-news
description: "Fetch and visualize financial news from RSS feeds (Bloomberg, Reuters, WSJ, CNBC, ASX, etc.). Generates interactive dashboard with charts and clickable headlines. Supports filtering by source."
metadata:
  {
    "openclaw": {
      "emoji": "📰",
      "requires": { "bins": ["python3"] },
      "install": [
        {
          "id": "pip",
          "kind": "pip",
          "packages": ["feedparser"],
          "label": "Install feedparser library for RSS feeds"
        }
      ]
    }
  }
---

# Financial News Skill

Retrieve the latest financial market news from major global sources and display in an interactive dashboard with charts and filtering.

## Overview

This skill fetches articles from RSS feeds of leading financial news outlets and generates a beautiful, dark-themed dashboard with:
- Real-time chart of article distribution by source
- Clickable news cards with summaries and timestamps
- Filter buttons to focus on specific sources
- Responsive design for desktop and mobile

## Sources

- **Bloomberg** - Global financial news
- **Reuters Business/Markets/Finance** - Wire news
- **Financial Times** - Business & finance
- **Wall Street Journal** - US markets
- **CNBC** - Real-time market coverage
- **ASX News** - Australian market updates
- **Yahoo Finance** - Market headlines

## Usage

### Basic
```bash
python3 ~/.openclaw/workspace/skills/financial-news/scripts/run.py
```

Or simply:
```bash
cd ~/.openclaw/workspace/skills/financial-news/scripts && ./run.py
```

### From OpenClaw (once registered)
```
Show me financial news
Get latest market news with charts
Display financial news dashboard
```

## Output

- Fetches up to 5 latest articles per source
- Saves raw JSON to `output/news.json`
- Generates interactive HTML dashboard at `output/dashboard.html`
- Displays stats: total articles, number of sources

## Dashboard Features

- **Top bar**: Title and generation timestamp
- **Stats cards**: Total articles, sources count
- **Charts**: Bar chart + doughnut chart showing source distribution
- **Filter buttons**: Click to show only articles from a specific source
- **News grid**: Cards with title (linked), summary, source badge, timestamp
- **Dark theme**: Easy on the eyes

## Customization

Edit `scripts/fetch_news.py` to:
- Add/remove RSS feeds
- Change `max_items` per feed
- Modify date parsing

Edit `scripts/generate_dashboard.js` (actually it's embedded in `generate_dashboard.py`) to tweak colors, layout, or chart types.

## Dependencies

```bash
pip install feedparser
```

Or if you don't have pip, the skill will attempt to use system Python packages.

## Limitations

- RSS feed availability depends on publishers (some may require authentication or have paywalls)
- Parsing quality varies by feed format
- No AI summarization (just raw summaries from feeds)
- No portfolio-specific news (yet)

## Future Ideas

- Add more feeds (Seeking Alpha, FinViz, MarketWatch)
- Add stock ticker filtering
- Generate morning/evening cron summaries
- Integrate with WhatsApp/Telegram delivery
- Cache previous runs to avoid duplicates

---

**Note:** This is a custom skill built for OpenClaw. For enterprise-grade news with AI summaries, consider installing `finance-news` from Clawhub (requires additional API setup).
