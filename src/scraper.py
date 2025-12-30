"""
Review Scraper for Groww App
Collects reviews from Google Play Store and Apple App Store
"""

import os
from datetime import datetime, timedelta
from typing import List, Dict
import pandas as pd
import requests
from google_play_scraper import app, Sort, reviews_all
from dotenv import load_dotenv

load_dotenv()


class ReviewScraper:
    """Scrapes reviews from App Store and Play Store"""
    
    def __init__(self, weeks_to_analyze: int = 10):
        self.weeks_to_analyze = weeks_to_analyze
        self.cutoff_date = datetime.now() - timedelta(weeks=weeks_to_analyze)
        self.android_app_id = os.getenv('GROWW_ANDROID_APP_ID', 'com.nextbillion.groww')
        self.ios_app_id = os.getenv('GROWW_IOS_APP_ID', '1404871631')
        
    def scrape_play_store(self) -> List[Dict]:
        """Scrape reviews from Google Play Store"""
        print(f"🤖 Scraping Play Store reviews for {self.android_app_id}...")
        
        try:
            # Get all reviews (will filter by date later)
            result = reviews_all(
                self.android_app_id,
                sleep_milliseconds=0,
                lang='en',
                country='in',
                sort=Sort.NEWEST
            )
            
            reviews_data = []
            for review in result:
                review_date = review['at']
                
                # Filter by date
                if review_date >= self.cutoff_date:
                    reviews_data.append({
                        'platform': 'Android',
                        'rating': review['score'],
                        'title': review.get('reviewCreatedVersion', 'N/A'),
                        'text': review['content'],
                        'date': review_date.strftime('%Y-%m-%d'),
                        'thumbs_up': review.get('thumbsUpCount', 0)
                    })
            
            print(f"✅ Collected {len(reviews_data)} Android reviews")
            return reviews_data
            
        except Exception as e:
            print(f"❌ Error scraping Play Store: {e}")
            return []
    
    def scrape_app_store(self) -> List[Dict]:
        """Scrape reviews from Apple App Store using RSS feed"""
        print(f"🍎 Scraping App Store reviews for app ID {self.ios_app_id}...")
        
        try:
            # Use RSS feed API (more reliable than app-store-scraper library)
            base_url = "https://itunes.apple.com/in/rss/customerreviews"
            all_reviews = []
            
            # Fetch multiple pages (each page has ~50 reviews)
            max_pages = 10
            
            for page in range(1, max_pages + 1):
                url = f"{base_url}/page={page}/id={self.ios_app_id}/sortby=mostrecent/json"
                
                try:
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                        'Accept': 'application/json',
                    }
                    
                    response = requests.get(url, headers=headers, timeout=10)
                    
                    if response.status_code != 200:
                        break
                    
                    data = response.json()
                    
                    # Parse reviews from feed
                    if 'feed' in data and 'entry' in data['feed']:
                        entries = data['feed']['entry']
                        
                        for entry in entries:
                            try:
                                # Extract review data
                                rating = int(entry.get('im:rating', {}).get('label', 0))
                                title = entry.get('title', {}).get('label', '')
                                content = entry.get('content', {}).get('label', '')
                                date_str = entry.get('updated', {}).get('label', '')
                                
                                # Parse date
                                try:
                                    date_obj = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S-07:00')
                                except:
                                    try:
                                        date_obj = datetime.strptime(date_str.split('T')[0], '%Y-%m-%d')
                                    except:
                                        date_obj = datetime.now()
                                
                                # Filter by date
                                if date_obj >= self.cutoff_date:
                                    all_reviews.append({
                                        'platform': 'iOS',
                                        'rating': rating,
                                        'title': title,
                                        'text': content,
                                        'date': date_obj.strftime('%Y-%m-%d'),
                                        'thumbs_up': 0  # Not available for iOS
                                    })
                                    
                            except Exception:
                                continue
                    else:
                        # No more reviews
                        break
                        
                except Exception:
                    break
            
            print(f"✅ Collected {len(all_reviews)} iOS reviews")
            return all_reviews
            
        except Exception as e:
            print(f"❌ Error scraping App Store: {e}")
            return []
    
    def scrape_all(self) -> pd.DataFrame:
        """Scrape reviews from both platforms and combine"""
        print(f"\n{'='*60}")
        print(f"📱 Starting review collection for Groww App")
        print(f"📅 Analyzing last {self.weeks_to_analyze} weeks")
        print(f"{'='*60}\n")
        
        # Scrape both platforms
        android_reviews = self.scrape_play_store()
        ios_reviews = self.scrape_app_store()
        
        # Combine all reviews
        all_reviews = android_reviews + ios_reviews
        
        if not all_reviews:
            print("⚠️  No reviews collected!")
            return pd.DataFrame()
        
        # Convert to DataFrame
        df = pd.DataFrame(all_reviews)
        
        # Sort by date (newest first)
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date', ascending=False)
        
        print(f"\n{'='*60}")
        print(f"✅ Total reviews collected: {len(df)}")
        print(f"   - Android: {len(df[df['platform'] == 'Android'])}")
        print(f"   - iOS: {len(df[df['platform'] == 'iOS'])}")
        print(f"{'='*60}\n")
        
        return df
    
    def save_to_csv(self, df: pd.DataFrame, filename: str = None) -> str:
        """Save reviews to CSV file"""
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"data/raw/groww_reviews_{timestamp}.csv"
        
        df.to_csv(filename, index=False)
        print(f"💾 Reviews saved to: {filename}")
        return filename


if __name__ == "__main__":
    # Test the scraper
    scraper = ReviewScraper(weeks_to_analyze=10)
    reviews_df = scraper.scrape_all()
    
    if not reviews_df.empty:
        csv_path = scraper.save_to_csv(reviews_df)
        print(f"\n✅ Scraping complete! File: {csv_path}")
    else:
        print("\n❌ No reviews to save")
