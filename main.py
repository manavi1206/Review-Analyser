#!/usr/bin/env python3
"""
Groww App Review Insights Analyzer
Main orchestrator script that runs the complete workflow
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from scraper import ReviewScraper
from analyzer_executive import ExecutiveReviewAnalyzer
from report_generator_executive import ExecutiveReportGenerator
from email_mailer import EmailMailer


def main():
    """Main workflow orchestrator"""
    
    print("\n" + "="*70)
    print("🚀 GROWW APP REVIEW INSIGHTS ANALYZER")
    print("="*70 + "\n")
    
    # Load environment variables
    load_dotenv()
    
    # Configuration
    weeks_to_analyze = int(os.getenv('WEEKS_TO_ANALYZE', 10))
    max_themes = int(os.getenv('MAX_THEMES', 5))
    
    try:
        # Step 1: Scrape Reviews
        print("📱 STEP 1: Scraping Reviews")
        print("-" * 70)
        scraper = ReviewScraper(weeks_to_analyze=weeks_to_analyze)
        reviews_df = scraper.scrape_all()
        
        if reviews_df.empty:
            print("❌ No reviews collected. Exiting.")
            return
        
        # Save reviews to CSV
        csv_path = scraper.save_to_csv(reviews_df)
        
        # Step 2: Analyze Reviews
        print("\n" + "="*70)
        print("🧠 STEP 2: Analyzing Reviews with Gemini AI")
        print("-" * 70)
        analyzer = ExecutiveReviewAnalyzer()
        analysis_results = analyzer.analyze_reviews(reviews_df)
        
        # Step 3: Generate Reports
        print("\n" + "="*70)
        print("📄 STEP 3: Generating Reports")
        print("-" * 70)
        generator = ExecutiveReportGenerator()
        
        # Generate both markdown and PDF
        md_path = generator.generate_markdown(analysis_results)
        pdf_path = generator.generate_pdf(analysis_results)
        
        # Step 4: Send Email
        print("\n" + "="*70)
        print("📧 STEP 4: Sending Email Report")
        print("-" * 70)
        
        mailer = EmailMailer()
        email_sent = mailer.send_weekly_report(
            analysis=analysis_results,
            report_paths=[md_path, pdf_path]
        )
        
        # Summary
        print("\n" + "="*70)
        print("✅ WORKFLOW COMPLETE!")
        print("="*70)
        print(f"\n📊 Summary:")
        print(f"   • Reviews analyzed: {analysis_results['total_reviews']}")
        print(f"   • Average rating: {analysis_results['avg_rating']}/5")
        print(f"   • Date range: {analysis_results['date_range']['start']} to {analysis_results['date_range']['end']}")
        print(f"\n📁 Generated files:")
        print(f"   • CSV: {csv_path}")
        print(f"   • Markdown: {md_path}")
        print(f"   • PDF: {pdf_path}")
        print(f"\n📧 Email: {'Sent ✅' if email_sent else 'Failed ❌'}")
        print("\n" + "="*70 + "\n")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
