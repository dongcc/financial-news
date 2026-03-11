#!/usr/bin/env python3
"""
Financial News Skill - Fetches news from RSS feeds and generates dashboard.
"""

import subprocess
import sys
import os
from pathlib import Path

def main():
    script_dir = Path(__file__).parent
    output_dir = script_dir / 'output'
    output_dir.mkdir(exist_ok=True)
    
    json_file = output_dir / 'news.json'
    html_file = output_dir / 'dashboard.html'
    
    print("📰 Fetching financial news...")
    fetch_script = script_dir / 'fetch_news_simple.py'
    result = subprocess.run([sys.executable, str(fetch_script)], capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Error fetching news: {result.stderr}")
        sys.exit(1)
    
    # Save fetched JSON to file for the generator
    try:
        with open(json_file, 'w', encoding='utf-8') as f:
            f.write(result.stdout)
    except Exception as e:
        print(f"Failed to write {json_file}: {e}")
        sys.exit(1)
    
    print("✅ News fetched successfully")
    print("📊 Generating dashboard...")
    gen_script = script_dir / 'generate_dashboard.py'
    result = subprocess.run([sys.executable, str(gen_script)], capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Error generating dashboard: {result.stderr}")
        sys.exit(1)
    
    print(result.stdout.strip())
    print(f"📄 Dashboard file: {html_file}")
    print("\nTo view: open", html_file)

if __name__ == "__main__":
    main()
