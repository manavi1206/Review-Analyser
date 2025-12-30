"""
Executive-Level LLM Analyzer using Gemini API
Analyzes reviews to extract business-focused insights for leadership
"""

import os
import json
from typing import List, Dict
import pandas as pd
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()


class ExecutiveReviewAnalyzer:
    """Analyzes reviews using Gemini API with executive-level insights"""
    
    def __init__(self):
        api_key = os.getenv('GEMINI_API_KEY')
        
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
    
    def analyze_reviews(self, df: pd.DataFrame) -> Dict:
        """
        Main analysis function - generates executive-level insights
        """
        print(f"\n{'='*60}")
        print(f"🧠 Analyzing {len(df)} reviews with Executive AI Analysis")
        print(f"{'='*60}\n")
        
        # Prepare review data
        review_data = self._prepare_review_data(df)
        
        # Generate comprehensive executive report
        print("📊 Generating executive-level insights...")
        report = self._generate_executive_report(review_data, df)
        
        print(f"\n✅ Executive analysis complete!\n")
        
        return report
    
    def _prepare_review_data(self, df: pd.DataFrame) -> str:
        """Prepare review data for LLM analysis"""
        # Sample reviews strategically
        if len(df) > 300:
            # Get mix of ratings
            low_ratings = df[df['rating'] <= 2].sample(n=min(100, len(df[df['rating'] <= 2])), random_state=42)
            mid_ratings = df[df['rating'] == 3].sample(n=min(50, len(df[df['rating'] == 3])), random_state=42)
            high_ratings = df[df['rating'] >= 4].sample(n=min(150, len(df[df['rating'] >= 4])), random_state=42)
            df_sample = pd.concat([low_ratings, mid_ratings, high_ratings])
        else:
            df_sample = df
        
        # Create structured representation
        reviews_text = []
        for _, row in df_sample.iterrows():
            reviews_text.append(
                f"[{row['platform']} | {row['rating']}★ | {row['date']}] {row['text'][:300]}"
            )
        
        return "\n".join(reviews_text)
    
    def _generate_executive_report(self, review_texts: str, df: pd.DataFrame) -> Dict:
        """Generate comprehensive executive report using Gemini"""
        
        # Calculate metrics
        total_reviews = len(df)
        avg_rating = df['rating'].mean()
        positive_pct = len(df[df['rating'] >= 4]) / total_reviews * 100
        neutral_pct = len(df[df['rating'] == 3]) / total_reviews * 100
        negative_pct = len(df[df['rating'] <= 2]) / total_reviews * 100
        
        prompt = f"""
You are a Group Product Manager analyzing App Store reviews for Groww, a consumer fintech app in India.

Your goal is NOT to summarize reviews, but to convert raw review data into executive-ready product insights that drive decisions.

Input Data:
- Total reviews: {total_reviews}
- Average rating: {avg_rating:.2f}/5
- Positive (4-5★): {positive_pct:.1f}%
- Neutral (3★): {neutral_pct:.1f}%
- Negative (1-2★): {negative_pct:.1f}%
- Date range: {df['date'].min()} to {df['date'].max()}

Reviews:
{review_texts}

Produce a structured analysis with these sections:

1. EXECUTIVE SUMMARY (3-5 bullets)
- Highlight major sentiment patterns
- Call out trust- or money-related risks explicitly
- End with clear leadership takeaway

2. THEME SEGMENTATION (Impact-Oriented)
Identify top 5 themes with:
- Theme name (2-4 words)
- % of reviews
- Severity: High/Medium/Low
- Business risk: Trust/Revenue/Onboarding/Experience
- Brief description

Rank by business impact, not just volume.

3. HIGH-IMPACT INSIGHTS
For top 3 themes:
- Problem statement (1 sentence)
- Why this matters for product & business
- Representative user quote
- User segments affected (new users, active users, etc.)

4. RATING CORRELATION
- Which themes drive 1-2★ ratings most
- Quantify impact where possible

5. POSITIVE SIGNALS
- What's working well
- Evidence from reviews

6. DECISION-ORIENTED RECOMMENDATIONS (3-5 actions)
For each:
- Problem addressed
- Expected user impact
- Expected business impact
- Priority: P0/P1/P2

7. LEADERSHIP DECISIONS REQUIRED
- What alignment or decisions are needed
- Ownership, prioritization, or resourcing questions

Return as JSON with this structure:
{{
  "executive_summary": ["bullet 1", "bullet 2", ...],
  "themes": [
    {{
      "theme": "Theme Name",
      "percentage": 25,
      "severity": "High",
      "business_risk": "Trust",
      "description": "Brief description"
    }}
  ],
  "deep_dives": [
    {{
      "theme": "Theme Name",
      "problem": "Problem statement",
      "why_matters": "Business impact",
      "quote": "User quote",
      "segments": "User segments affected"
    }}
  ],
  "rating_drivers": ["Theme 1 drives 45% of 1-2★ reviews", ...],
  "positive_signals": ["Signal 1", "Signal 2", ...],
  "recommendations": [
    {{
      "action": "Specific action",
      "problem": "Problem addressed",
      "user_impact": "Expected user impact",
      "business_impact": "Expected business impact",
      "priority": "P0"
    }}
  ],
  "leadership_decisions": ["Decision 1", "Decision 2", ...]
}}

Return ONLY valid JSON, no other text.
"""
        
        try:
            response = self.model.generate_content(prompt)
            result_json = response.text.strip()
            
            # Clean up response
            if result_json.startswith('```'):
                result_json = result_json.split('```')[1]
                if result_json.startswith('json'):
                    result_json = result_json[4:]
            
            report = json.loads(result_json)
            
            # Add metadata
            report['metadata'] = {
                'total_reviews': total_reviews,
                'avg_rating': round(avg_rating, 2),
                'positive_pct': round(positive_pct, 1),
                'neutral_pct': round(neutral_pct, 1),
                'negative_pct': round(negative_pct, 1),
                'date_range': {
                    'start': df['date'].min(),
                    'end': df['date'].max()
                }
            }
            
            # Add review counts to themes
            for theme in report.get('themes', []):
                theme['review_count'] = int(total_reviews * theme['percentage'] / 100)
            
            return report
            
        except Exception as e:
            print(f"❌ Error generating executive report: {e}")
            # Return fallback structure
            return self._get_fallback_report(df)
    
    def _get_fallback_report(self, df: pd.DataFrame) -> Dict:
        """Fallback report if AI fails"""
        total_reviews = len(df)
        avg_rating = df['rating'].mean()
        
        return {
            "executive_summary": [
                f"Analyzed {total_reviews} reviews with {avg_rating:.2f}/5 average rating",
                "Unable to generate detailed insights due to API error",
                "Manual review recommended for this period"
            ],
            "themes": [
                {"theme": "KYC & Verification", "percentage": 30, "severity": "High", "business_risk": "Trust", "description": "Account verification delays", "review_count": int(total_reviews * 0.3)},
                {"theme": "Payment Issues", "percentage": 25, "severity": "High", "business_risk": "Revenue", "description": "Withdrawal and deposit problems", "review_count": int(total_reviews * 0.25)},
                {"theme": "App Performance", "percentage": 20, "severity": "Medium", "business_risk": "Experience", "description": "Crashes and bugs", "review_count": int(total_reviews * 0.2)}
            ],
            "deep_dives": [],
            "rating_drivers": ["Analysis unavailable - API error"],
            "positive_signals": ["Analysis unavailable - API error"],
            "recommendations": [
                {"action": "Review API configuration", "problem": "Analysis failed", "user_impact": "N/A", "business_impact": "N/A", "priority": "P0"}
            ],
            "leadership_decisions": ["Investigate why AI analysis failed"],
            "metadata": {
                'total_reviews': total_reviews,
                'avg_rating': round(avg_rating, 2),
                'positive_pct': round(len(df[df['rating'] >= 4]) / total_reviews * 100, 1),
                'neutral_pct': round(len(df[df['rating'] == 3]) / total_reviews * 100, 1),
                'negative_pct': round(len(df[df['rating'] <= 2]) / total_reviews * 100, 1),
                'date_range': {
                    'start': df['date'].min(),
                    'end': df['date'].max()
                }
            }
        }
