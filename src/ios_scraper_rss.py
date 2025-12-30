"""
Working iOS Review Scraper using iTunes RSS Feed
"""

import requests
import json
from datetime import datetime, timedelta
from typing import List, Dict
import pandas as pd

class iOSReviewScraperRSS:
    """Scrapes iOS reviews using iTunes RSS feed"""
    
    def __init__(self, app_id: str, country: str = 'in'):
        self.app_id = app_id
        self.country = country
        self.base_url = f"https://itunes.apple.com/{country}/rss/customerreviews"
        
    def scrape_reviews(self, max_pages: int = 10) -> List[Dict]:
        """
        Scrape reviews from iTunes RSS feed
        
        Args:
            max_pages: Number of pages to fetch (each page ~50 reviews)
            
        Returns:
            List of review dictionaries
        """
        all_reviews = []
        
        print(f"🍎 Scraping iOS reviews using RSS feed...")
        print(f"   App ID: {self.app_id}")
        print(f"   Country: {self.country}\n")
        
        for page in range(1, max_pages + 1):
            print(f"   Fetching page {page}...")
            
            reviews = self._fetch_page(page)
            
            if not reviews:
                print(f"   No more reviews on page {page}")
                break
            
            all_reviews.extend(reviews)
            print(f"   ✅ Got {len(reviews)} reviews from page {page}")
            
        print(f"\n✅ Total iOS reviews collected: {len(all_reviews)}")
        return all_reviews
    
    def _fetch_page(self, page: int) -> List[Dict]:
        """Fetch a single page of reviews"""
        
        # RSS feed URL with pagination
        url = f"{self.base_url}/page={page}/id={self.app_id}/sortby=mostrecent/json"
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                'Accept': 'application/json',
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code != 200:
                return []
            
            data = response.json()
            
            # Parse reviews from feed
            if 'feed' in data and 'entry' in data['feed']:
                return self._parse_reviews(data['feed']['entry'])
            
            return []
            
        except Exception as e:
            print(f"   ⚠️  Error fetching page {page}: {e}")
            return []
    
    def _parse_reviews(self, entries: List[Dict]) -> List[Dict]:
        """Parse review entries from RSS feed"""
        reviews = []
        
        for entry in entries:
            try:
                # Extract review data
                rating = int(entry.get('im:rating', {}).get('label', 0))
                title = entry.get('title', {}).get('label', '')
                content = entry.get('content', {}).get('label', '')
                author = entry.get('author', {}).get('name', {}).get('label', 'Anonymous')
                date_str = entry.get('updated', {}).get('label', '')
                version = entry.get('im:version', {}).get('label', '')
                
                # Parse date
                try:
                    date_obj = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S-07:00')
                except:
                    try:
                        date_obj = datetime.strptime(date_str.split('T')[0], '%Y-%m-%d')
                    except:
                        date_obj = datetime.now()
                
                reviews.append({
                    'platform': 'iOS',
                    'rating': rating,
                    'title': title,
                    'text': content,
                    'date': date_obj,
                    'author': author,
                    'version': version,
                    'thumbs_up': 0  # Not available in RSS
                })
                
            except Exception as e:
                continue
        
        return reviews
    
    def scrape_and_filter(self, weeks: int = 10, max_pages: int = 10) -> pd.DataFrame:
        """Scrape reviews and filter by date"""
        
        cutoff_date = datetime.now() - timedelta(weeks=weeks)
        
        # Get all reviews
        all_reviews = self.scrape_reviews(max_pages=max_pages)
        
        # Filter by date
        filtered_reviews = [
            r for r in all_reviews 
            if r['date'] >= cutoff_date
        ]
        
        print(f"\n📊 Reviews from last {weeks} weeks: {len(filtered_reviews)}")
        
        # Convert to DataFrame
        if filtered_reviews:
            df = pd.DataFrame(filtered_reviews)
            df['date'] = df['date'].dt.strftime('%Y-%m-%d')
            return df
        
        return pd.DataFrame()


if __name__ == "__main__":
    # Test the scraper
    scraper = iOSReviewScraperRSS(app_id='1404871703', country='in')
    
    # Scrape reviews from last 10 weeks
    df = scraper.scrape_and_filter(weeks=10, max_pages=10)
    
    if not df.empty:
        print(f"\n{'='*70}")
        print(f"SUCCESS! Collected {len(df)} iOS reviews")
        print(f"{'='*70}")
        print(f"\nSample reviews:")
        print(df[['rating', 'title', 'text', 'date']].head(3))
        print(f"\nAverage rating: {df['rating'].mean():.2f}/5")
        print(f"Date range: {df['date'].min()} to {df['date'].max()}")
    else:
        print("\n❌ No reviews collected")
