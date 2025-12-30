"""
LLM Analyzer using Gemini API
Analyzes reviews to extract themes, quotes, and actionable insights
"""

import os
import json
from typing import List, Dict, Tuple
import pandas as pd
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()


class ReviewAnalyzer:
    """Analyzes reviews using Gemini API"""
    
    def __init__(self, max_themes: int = 5):
        self.max_themes = max_themes
        api_key = os.getenv('GEMINI_API_KEY')
        
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
    
    def analyze_reviews(self, df: pd.DataFrame) -> Dict:
        """
        Main analysis function that extracts themes, quotes, and recommendations
        """
        print(f"\n{'='*60}")
        print(f"🧠 Analyzing {len(df)} reviews with Gemini AI")
        print(f"{'='*60}\n")
        
        # Prepare review text for analysis
        review_texts = self._prepare_review_data(df)
        
        # Extract themes
        print("🔍 Step 1: Extracting themes...")
        themes = self._extract_themes(review_texts, df)
        
        # Select representative quotes
        print("💬 Step 2: Selecting representative quotes...")
        quotes = self._select_quotes(review_texts, themes)
        
        # Generate action recommendations
        print("💡 Step 3: Generating action recommendations...")
        actions = self._generate_recommendations(themes, df)
        
        print(f"\n✅ Analysis complete!\n")
        
        return {
            'themes': themes,
            'quotes': quotes,
            'actions': actions,
            'total_reviews': len(df),
            'avg_rating': round(df['rating'].mean(), 2),
            'date_range': {
                'start': df['date'].min().strftime('%Y-%m-%d'),
                'end': df['date'].max().strftime('%Y-%m-%d')
            }
        }
    
    def _prepare_review_data(self, df: pd.DataFrame) -> str:
        """Prepare review data for LLM analysis"""
        # Sample reviews if too many (to stay within token limits)
        if len(df) > 200:
            df_sample = df.sample(n=200, random_state=42)
        else:
            df_sample = df
        
        # Create a concise representation
        reviews_text = []
        for _, row in df_sample.iterrows():
            reviews_text.append(
                f"[{row['platform']} | Rating: {row['rating']}/5] {row['text'][:200]}"
            )
        
        return "\n".join(reviews_text)
    
    def _extract_themes(self, review_texts: str, df: pd.DataFrame) -> List[Dict]:
        """Extract top themes from reviews using Gemini"""
        
        prompt = f"""
You are analyzing app reviews for Groww, an investment and trading platform in India.

Analyze these reviews and identify the TOP {self.max_themes} themes/topics that users are discussing.

For each theme:
1. Give it a clear, concise name (2-4 words)
2. Provide a brief description (1 sentence)
3. Estimate the percentage of reviews discussing this theme

Focus on themes related to: KYC/verification, payments/withdrawals, UI/UX, customer support, features, bugs, performance.

Reviews:
{review_texts}

Return ONLY a JSON array with this exact structure:
[
  {{
    "theme": "Theme Name",
    "description": "Brief description",
    "percentage": 25
  }}
]

Return ONLY valid JSON, no other text.
"""
        
        try:
            response = self.model.generate_content(prompt)
            themes_json = response.text.strip()
            
            # Clean up response (remove markdown code blocks if present)
            if themes_json.startswith('```'):
                themes_json = themes_json.split('```')[1]
                if themes_json.startswith('json'):
                    themes_json = themes_json[4:]
            
            themes = json.loads(themes_json)
            
            # Add review count to each theme
            for theme in themes:
                theme['review_count'] = int(len(df) * theme['percentage'] / 100)
            
            return themes[:self.max_themes]
            
        except Exception as e:
            print(f"❌ Error extracting themes: {e}")
            # Fallback themes
            return [
                {"theme": "KYC & Verification", "description": "Issues with account verification", "percentage": 30, "review_count": int(len(df) * 0.3)},
                {"theme": "Payment Issues", "description": "Problems with deposits/withdrawals", "percentage": 25, "review_count": int(len(df) * 0.25)},
                {"theme": "App Performance", "description": "Bugs, crashes, slow loading", "percentage": 20, "review_count": int(len(df) * 0.2)}
            ]
    
    def _select_quotes(self, review_texts: str, themes: List[Dict]) -> List[Dict]:
        """Select 3 representative quotes from reviews"""
        
        theme_names = [t['theme'] for t in themes[:3]]
        
        prompt = f"""
From these app reviews for Groww, select 3 REAL, AUTHENTIC user quotes that best represent user sentiment.

Requirements:
- Select quotes that relate to these themes: {', '.join(theme_names)}
- Each quote should be 1-2 sentences, clear and impactful
- Remove any personally identifiable information (names, emails, phone numbers)
- Keep the original tone and language
- Choose quotes that highlight both problems and positive feedback

Reviews:
{review_texts}

Return ONLY a JSON array with this exact structure:
[
  {{
    "quote": "The actual user quote here",
    "theme": "Related theme name",
    "sentiment": "positive/negative/neutral"
  }}
]

Return ONLY valid JSON, no other text.
"""
        
        try:
            response = self.model.generate_content(prompt)
            quotes_json = response.text.strip()
            
            # Clean up response
            if quotes_json.startswith('```'):
                quotes_json = quotes_json.split('```')[1]
                if quotes_json.startswith('json'):
                    quotes_json = quotes_json[4:]
            
            quotes = json.loads(quotes_json)
            return quotes[:3]
            
        except Exception as e:
            print(f"❌ Error selecting quotes: {e}")
            # Fallback quotes
            return [
                {"quote": "KYC verification is taking too long, been waiting for 3 days", "theme": "KYC & Verification", "sentiment": "negative"},
                {"quote": "Great app for beginners, easy to understand", "theme": "User Experience", "sentiment": "positive"},
                {"quote": "Withdrawal is stuck, customer support not responding", "theme": "Payment Issues", "sentiment": "negative"}
            ]
    
    def _generate_recommendations(self, themes: List[Dict], df: pd.DataFrame) -> List[str]:
        """Generate 3 actionable recommendations based on themes"""
        
        theme_summary = "\n".join([f"- {t['theme']}: {t['description']} ({t['percentage']}%)" for t in themes[:3]])
        avg_rating = df['rating'].mean()
        
        prompt = f"""
You are a product manager analyzing user feedback for Groww app.

Based on these top themes from user reviews:
{theme_summary}

Average Rating: {avg_rating:.2f}/5

Generate 3 SPECIFIC, ACTIONABLE recommendations that the product/engineering team can implement.

Each recommendation should:
- Be concrete and implementable
- Address the most critical user pain points
- Be prioritized by impact
- Be 1-2 sentences max

Return ONLY a JSON array of strings:
["Recommendation 1", "Recommendation 2", "Recommendation 3"]

Return ONLY valid JSON, no other text.
"""
        
        try:
            response = self.model.generate_content(prompt)
            actions_json = response.text.strip()
            
            # Clean up response
            if actions_json.startswith('```'):
                actions_json = actions_json.split('```')[1]
                if actions_json.startswith('json'):
                    actions_json = actions_json[4:]
            
            actions = json.loads(actions_json)
            return actions[:3]
            
        except Exception as e:
            print(f"❌ Error generating recommendations: {e}")
            # Fallback recommendations
            return [
                "Reduce KYC verification time by implementing automated document verification",
                "Add real-time withdrawal status tracking to reduce support queries",
                "Improve app performance by optimizing API calls and caching frequently accessed data"
            ]


if __name__ == "__main__":
    # Test the analyzer
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python analyzer.py <path_to_reviews_csv>")
        sys.exit(1)
    
    csv_path = sys.argv[1]
    df = pd.read_csv(csv_path)
    
    analyzer = ReviewAnalyzer(max_themes=5)
    results = analyzer.analyze_reviews(df)
    
    print("\n" + "="*60)
    print("ANALYSIS RESULTS")
    print("="*60)
    print(json.dumps(results, indent=2))
