#!/usr/bin/env python3
"""
Generate financial news dashboard from fetch_news.py output.
"""

import json
import os
import datetime
from pathlib import Path

def load_news_data(json_path: str) -> dict:
    with open(json_path, 'r') as f:
        return json.load(f)

def categorize_articles(articles: list) -> dict:
    """Categorize articles into the four required categories."""
    categories = {
        "🌍 Geopolitical & Market Impact": [],
        "📈 Stock Picks & Analyst Recommendations": [],
        "💰 Wealth Management Insights": [],
        "🏭 Defense & Tech": []
    }
    
    # Keywords for categorization
    geo_keywords = ['war', 'iran', 'trump', 'fed', 'central bank', 'g7', 'china', 'india', 'relince', 'admini', 'policy', 'tariff', 'trade', 'diplomacy', 'oil', 'energy', 'refiner', 'strait', 'hormuz', 'military', 'navy', 'minelayer', 'blockade', 'nomination', 'powell', 'warsh', 'tillis']
    stock_keywords = ['stock', 'buy', 'sell', 'analyst', 'upgrade', 'downgrade', 'target', 'earnings', 'revenue', 'profit', 'dividend', 'portfolio', 'investment', 'bullish', 'bearish', 'rating', 'top picks', 'wall street']
    wealth_keywords = ['wealth', 'retirement', 'saving', 'credit card', 'perks', 'benefits', 'personal finance', 'budget', 'tax', 'estate', 'insurance', 'inheritance', 'women', 'family', 'education', 'home', 'mortgage']
    defense_tech_keywords = ['defense', 'military', 'weapon', 'drone', 'missile', 'lockheed', 'anduril', 'raytheon', 'boeing', 'defense tech', 'command and control', 'army', 'navy', 'air force', 'space', 'satellite', 'cyber', 'ai', 'artificial intelligence', 'nvidia', 'amd', 'chip', 'semiconductor', 'oracle', 'cloud', 'data center', 'layoffs']
    
    for article in articles:
        title = article['title'].lower()
        summary = article.get('summary', '').lower()
        text = title + ' ' + summary
        
        # Check in priority order: Geo > Stock > Wealth > Defense
        if any(kw in text for kw in geo_keywords):
            categories["🌍 Geopolitical & Market Impact"].append(article)
        elif any(kw in text for kw in stock_keywords):
            categories["📈 Stock Picks & Analyst Recommendations"].append(article)
        elif any(kw in text for kw in wealth_keywords):
            categories["💰 Wealth Management Insights"].append(article)
        elif any(kw in text for kw in defense_tech_keywords):
            categories["🏭 Defense & Tech"].append(article)
        else:
            # Default to Geopolitical if no match
            categories["🌍 Geopolitical & Market Impact"].append(article)
    
    return categories

def generate_text_summary(data: dict, output_path: str):
    """Generate formatted text summary."""
    articles = data['articles']
    total = data['total']
    generated = data['generated_at']
    
    # Categorize
    categories = categorize_articles(articles)
    
    # Source info with URLs
    source_info = {
        "CNBC": "https://www.cnbc.com",
        "Yahoo Finance": "https://finance.yahoo.com",
        "Reuters Markets": "https://www.reuters.com/markets",
        "Reuters": "https://www.reuters.com",
        "Bloomberg": "https://www.bloomberg.com",
        "WSJ": "https://www.wsj.com",
        "Financial Times": "https://www.ft.com"
    }
    
    # Count sources
    source_counts = {}
    for article in articles:
        src = article['source_name']
        source_counts[src] = source_counts.get(src, 0) + 1
    
    # Build header
    date_str = generated.split()[0] if ' ' in generated else generated
    lines = [f"Top Financial News — {date_str}", "", "📰 Latest Headlines", ""]
    
    # Build categorized sections in required order
    category_order = [
        "🌍 Geopolitical & Market Impact",
        "📈 Stock Picks & Analyst Recommendations",
        "💰 Wealth Management Insights",
        "🏭 Defense & Tech"
    ]
    for emoji_category in category_order:
        cat_articles = categories.get(emoji_category, [])
        if cat_articles:
            lines.append(f"{emoji_category}")
            lines.append("")
            for article in cat_articles:
                title = article['title']
                link = article.get('link', '#')
                source = article['source_name']
                lines.append(f"• {title} — {link} ({source})")
            lines.append("")
    
    # Build footer
    lines.append("Sources: " + ", ".join([f"{src} ({source_info.get(src, 'https://example.com')}) ({count})" for src, count in sorted(source_counts.items())]))
    lines.append(f"Total: {total}")
    lines.append(f"Generated: {generated}")
    
    # Get HTML dashboard path
    html_file = output_path.parent / 'dashboard.html'
    workspace_root = Path('/home/dongcc/.openclaw/workspace')
    try:
        rel_path = html_file.relative_to(workspace_root)
        http_url = f"http://192.168.3.78:8002/{rel_path}"
        file_url = f"file://{html_file.resolve()}"
    except:
        http_url = "http://localhost:8002/skills/financial-news/scripts/output/dashboard.html"
        file_url = f"file://{html_file}"
    
    lines.append(f"Dashboard (HTTP): {http_url}")
    lines.append(f"Dashboard (file): {file_url}")
    
    # Write file
    txt_file = output_path.parent / 'summary.txt'
    with open(txt_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    print(f"✅ Text summary generated: {txt_file}")

def generate_html(data: dict, output_path: str):
    """Generate dashboard HTML with Chart.js and news cards."""
    
    articles = data['articles']
    total = data['total']
    generated = data['generated_at']
    
    # Group by source for chart
    source_counts = {}
    for article in articles:
        src = article['source_name']
        source_counts[src] = source_counts.get(src, 0) + 1
    
    # Build HTML
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Financial News Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * {{ margin:0; padding:0; box-sizing:border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif; background: #0a0a0a; color: #e0e0e0; padding: 20px; }}
        .header {{ display:flex; justify-content:space-between; align-items:center; margin-bottom: 20px; padding-bottom: 15px; border-bottom: 1px solid #333; }}
        .header h1 {{ font-size: 1.8rem; color: #00d4ff; }}
        .meta {{ font-size: 0.9rem; color: #888; }}
        .stats {{ display: flex; gap: 15px; margin-bottom: 20px; }}
        .stat-card {{ background: #1a1a1a; border: 1px solid #333; border-radius: 8px; padding: 15px 20px; text-align: center; flex: 1; }}
        .stat-value {{ font-size: 1.5rem; font-weight: bold; color: #00d4ff; }}
        .stat-label {{ font-size: 0.85rem; color: #888; margin-top: 5px; }}
        .chart-row {{ display: flex; gap: 20px; margin-bottom: 20px; }}
        .chart-col {{ flex: 1; background: #1a1a1a; border: 1px solid #333; border-radius: 8px; padding: 15px; }}
        .chart-col h3 {{ font-size: 1rem; margin-bottom: 10px; color: #aaa; }}
        .chart-container {{ position: relative; height: 250px; }}
        .news-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 15px; margin-top: 20px; }}
        .news-card {{ background: #1a1a1a; border: 1px solid #333; border-radius: 8px; padding: 15px; transition: transform 0.2s, box-shadow 0.2s; }}
        .news-card:hover {{ transform: translateY(-3px); box-shadow: 0 4px 12px rgba(0,212,255,0.15); border-color: #00d4ff; }}
        .news-title {{ font-size: 1rem; font-weight: 600; margin-bottom: 8px; line-height: 1.4; }}
        .news-title a {{ color: #e0e0e0; text-decoration: none; }}
        .news-title a:hover {{ color: #00d4ff; }}
        .news-summary {{ font-size: 0.85rem; color: #aaa; margin-bottom: 10px; line-height: 1.5; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; }}
        .news-meta {{ display: flex; justify-content: space-between; font-size: 0.75rem; color: #666; }}
        .news-source {{ color: #00d4ff; }}
        .filters {{ display: flex; gap: 10px; margin-bottom: 15px; flex-wrap: wrap; }}
        .filter-btn {{ padding: 6px 14px; background: #222; border: 1px solid #444; color: #ccc; border-radius: 20px; cursor: pointer; font-size: 0.8rem; transition: all 0.2s; }}
        .filter-btn.active, .filter-btn:hover {{ background: #00d4ff; border-color: #00d4ff; color: #000; }}
        @media (max-width: 768px) {{
            .chart-row {{ flex-direction: column; }}
            .header h1 {{ font-size: 1.4rem; }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>💰 Financial News Dashboard</h1>
        <div class="meta">Generated: {generated}</div>
    </div>

    <div class="stats">
        <div class="stat-card">
            <div class="stat-value">{total}</div>
            <div class="stat-label">Total Articles</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{len(source_counts)}</div>
            <div class="stat-label">News Sources</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{max(source_counts.values()) if source_counts else 0}</div>
            <div class="stat-label">Top Source Count</div>
        </div>
    </div>

    <div class="chart-row">
        <div class="chart-col">
            <h3>Articles by Source</h3>
            <div class="chart-container">
                <canvas id="sourceChart"></canvas>
            </div>
        </div>
        <div class="chart-col">
            <h3>Source Distribution</h3>
            <div class="chart-container">
                <canvas id="pieChart"></canvas>
            </div>
        </div>
    </div>

    <div class="filters">
        <button class="filter-btn active" data-filter="all">All Sources</button>
'''

    # Add filter buttons for each source
    for source in sorted(source_counts.keys()):
        html += f'        <button class="filter-btn" data-filter="{source}">{source}</button>\n'

    html += '''    </div>

    <div class="news-grid" id="newsGrid">
'''

    # Add news cards
    for article in articles:
        title = article['title'].replace('"', '&quot;')
        link = article.get('link', '#')
        summary = article.get('summary', '').replace('"', '&quot;')
        source = article['source_name']
        published = article.get('published', '')[:16] if article.get('published') else ''
        
        html += f'''        <div class="news-card" data-source="{source}">
            <div class="news-title"><a href="{link}" target="_blank">{title}</a></div>
            <div class="news-summary">{summary}</div>
            <div class="news-meta">
                <span class="news-source">{source}</span>
                <span>{published}</span>
            </div>
        </div>
'''

    html += '''    </div>

    <script>
        // Chart.js configuration
        const sourceData = {
            labels: ['''
    
    labels = list(source_counts.keys())
    counts = [source_counts[l] for l in labels]
    
    html += ', '.join(f'"{l}"' for l in labels)
    
    html += '''],
            datasets: [{
                label: 'Articles',
                data: ['''
    html += ', '.join(str(c) for c in counts)
    
    html += '''],
                backgroundColor: [
                    '#00d4ff', '#ff6b6b', '#ffd93d', '#6bcf7f', '#ff8e53',
                    '#a0855b', '#4ecdc4', '#ff6b9d', '#c7ceea', '#b5e7a0'
                ],
                borderWidth: 1
            }]
        };

        // Bar chart
        new Chart(document.getElementById('sourceChart'), {
            type: 'bar',
            data: sourceData,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false }},
                scales: {
                    y: { beginAtZero: true, ticks: { color: '#888' }, grid: { color: '#333' }},
                    x: { ticks: { color: '#888' }, grid: { display: false }}
                }
            }
        });

        // Doughnut chart
        new Chart(document.getElementById('pieChart'), {
            type: 'doughnut',
            data: sourceData,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { position: 'right', labels: { color: '#888' }}}
            }
        });

        // Filter functionality
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                const filter = this.dataset.filter;
                document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
                this.classList.add('active');
                
                document.querySelectorAll('.news-card').forEach(card => {
                    if (filter === 'all' || card.dataset.source === filter) {
                        card.style.display = 'block';
                    } else {
                        card.style.display = 'none';
                    }
                });
            });
        });
    </script>
</body>
</html>'''

    # Save file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ Dashboard generated: {output_path}")
    print(f"   Articles: {total} from {len(source_counts)} sources")

if __name__ == "__main__":
    script_dir = Path(__file__).parent
    json_file = script_dir / 'output' / 'news.json'
    html_file = script_dir / 'output' / 'dashboard.html'
    
    # Ensure output dir exists
    html_file.parent.mkdir(exist_ok=True)
    
    data = load_news_data(str(json_file))
    generate_html(data, str(html_file))
    generate_text_summary(data, html_file)
