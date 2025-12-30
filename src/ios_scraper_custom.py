"""
Custom iOS App Store Review Scraper
Uses iTunes Store web endpoint to fetch reviews
"""

import requests
import json
import re
from datetime import datetime, timedelta
from typing import List, Dict
from bs4 import BeautifulSoup

class iOSReviewScraper:
    """Custom scraper for iOS App Store reviews"""
    
    def __init__(self, app_id: str, country: str = 'in'):
        self.app_id = app_id
        self.country = country
        self.base_url = "https://itunes.apple.com"
        
    def scrape_reviews(self, max_pages: int = 10) -> List[Dict]:
        """
        Scrape reviews from App Store
        
        Args:
            max_pages: Maximum number of pages to scrape
            
        Returns:
            List of review dictionaries
        """
        all_reviews = []
        
        print(f"🍎 Scraping iOS reviews for app ID {self.app_id}...")
        
        for page in range(1, max_pages + 1):
            print(f"   Fetching page {page}...")
            
            reviews = self._fetch_page(page)
            
            if not reviews:
                print(f"   No more reviews found at page {page}")
                break
                
            all_reviews.extend(reviews)
            print(f"   ✅ Got {len(reviews)} reviews from page {page}")
            
        print(f"✅ Total iOS reviews collected: {len(all_reviews)}")
        return all_reviews
    
    def _fetch_page(self, page_number: int) -> List[Dict]:
        """Fetch a single page of reviews"""
        
        # Try multiple endpoint formats
        urls = [
            # Format 1: Web store endpoint
            f"{self.base_url}/WebObjects/MZStore.woa/wa/viewContentsUserReviews",
            # Format 2: Customer reviews endpoint  
            f"{self.base_url}/{self.country}/customer-reviews/id{self.app_id}",
        ]
        
        params = {
            'id': self.app_id,
            'pageNumber': page_number - 1,
            'sortOrdering': 2,  # Most recent
            'type': 'Purple Software',
            'mt': 8
        }
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Apple-Store-Front': '143467-2,32',  # India store front
        }
        
        for url in urls:
            try:
                response = requests.get(url, params=params, headers=headers, timeout=15)
                
                if response.status_code == 200:
                    # Try to parse as JSON first
                    try:
                        data = response.json()
                        return self._parse_json_reviews(data)
                    except json.JSONDecodeError:
                        # Parse as HTML
                        return self._parse_html_reviews(response.text)
                        
            except Exception as e:
                continue
        
        return []
    
    def _parse_json_reviews(self, data: dict) -> List[Dict]:
        """Parse reviews from JSON response"""
        reviews = []
        
        # Try different JSON structures
        if 'userReviewList' in data:
            for review in data.get('userReviewList', []):
                reviews.append({
                    'rating': review.get('rating', 0),
                    'title': review.get('title', ''),
                    'text': review.get('body', ''),
                    'author': review.get('name', 'Anonymous'),
                    'date': review.get('date', ''),
                })
        
        return reviews
    
    def _parse_html_reviews(self, html: str) -> List[Dict]:
        """Parse reviews from HTML response"""
        reviews = []
        
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # Look for review containers
            review_divs = soup.find_all('div', class_=re.compile('customer-review|review'))
            
            for div in review_divs:
                try:
                    # Extract rating
                    rating_elem = div.find('div', class_=re.compile('rating|stars'))
                    rating = 0
                    if rating_elem:
                        rating_text = rating_elem.get_text()
                        rating_match = re.search(r'(\d+)', rating_text)
                        if rating_match:
                            rating = int(rating_match.group(1))
                    
                    # Extract title
                    title_elem = div.find(['h3', 'h4', 'span'], class_=re.compile('title'))
                    title = title_elem.get_text().strip() if title_elem else ''
                    
                    # Extract review text
                    text_elem = div.find('p', class_=re.compile('review-text|body'))
                    text = text_elem.get_text().strip() if text_elem else ''
                    
                    # Extract date
                    date_elem = div.find('time') or div.find('span', class_=re.compile('date'))
                    date_str = date_elem.get_text().strip() if date_elem else ''
                    
                    if text:  # Only add if we got review text
                        reviews.append({
                            'rating': rating,
                            'title': title,
                            'text': text,
                            'date': date_str,
                        })
                        
                except Exception:
                    continue
            
        except Exception as e:
            print(f"   ⚠️  HTML parsing error: {e}")
        
        return reviews


if __name__ == "__main__":
    # Test the scraper
    scraper = iOSReviewScraper(app_id='1404871631', country='in')
    reviews = scraper.scrape_reviews(max_pages=5)
    
    print(f"\n{'='*70}")
    print(f"Test Results:")
    print(f"Total reviews: {len(reviews)}")
    
    if reviews:
        print(f"\nFirst review:")
        print(f"  Rating: {reviews[0].get('rating', 'N/A')}")
        print(f"  Title: {reviews[0].get('title', 'N/A')}")
        print(f"  Text: {reviews[0].get('text', 'N/A')[:100]}...")
    print(f"{'='*70}")
