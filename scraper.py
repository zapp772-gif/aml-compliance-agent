"""
Web scraping module for regulatory sources
"""

import requests
import feedparser
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import time

class RegulatoryScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def fetch_rss_feed(self, feed_url):
        """Fetch and parse RSS feed"""
        try:
            feed = feedparser.parse(feed_url)
            updates = []
            cutoff_date = datetime.now() - timedelta(days=30)
            
            for entry in feed.entries[:10]:
                pub_date = entry.get('published_parsed') or entry.get('updated_parsed')
                if pub_date:
                    entry_date = datetime(*pub_date[:6])
                    if entry_date < cutoff_date:
                        continue
                
                updates.append({
                    'title': entry.get('title', 'No title'),
                    'link': entry.get('link', ''),
                    'summary': entry.get('summary', '')[:500],
                    'date': entry.get('published', entry.get('updated', 'Recent'))
                })
            
            return updates
        except Exception as e:
            print(f"Error fetching RSS feed {feed_url}: {str(e)}")
            return []
    
    def fetch_regulator_updates(self, regulator_config):
        """Fetch all updates for a specific regulator"""
        all_updates = []
        
        for feed_url in regulator_config.get('rss_feeds', []):
            updates = self.fetch_rss_feed(feed_url)
            all_updates.extend(updates)
            time.sleep(1)
        
        seen_titles = set()
        unique_updates = []
        for update in all_updates:
            if update['title'] not in seen_titles:
                seen_titles.add(update['title'])
                unique_updates.append(update)
        
        return unique_updates[:10]
