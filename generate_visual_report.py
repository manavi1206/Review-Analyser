#!/usr/bin/env python3
"""
Test script to generate visual PDF report with sample data
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from report_generator_visual import VisualReportGenerator

# Create sample analysis data
sample_analysis = {
    'metadata': {
        'total_reviews': 7178,
        'avg_rating': 4.12,
        'positive_pct': 68.5,
        'neutral_pct': 18.3,
        'negative_pct': 13.2,
        'date_range': {
            'start': '2025-10-22',
            'end': '2025-12-30'
        }
    },
    'themes': [
        {
            'theme': 'KYC Verification Delays',
            'percentage': 30,
            'review_count': 2153,
            'severity': 'High',
            'business_risk': 'Trust',
            'description': 'Users experiencing long wait times for account verification, some waiting 3-5 days'
        },
        {
            'theme': 'Payment Processing Issues',
            'percentage': 25,
            'review_count': 1795,
            'severity': 'High',
            'business_risk': 'Revenue',
            'description': 'Withdrawal delays and deposit failures causing user frustration and support tickets'
        },
        {
            'theme': 'App Performance & Crashes',
            'percentage': 20,
            'review_count': 1436,
            'severity': 'Medium',
            'business_risk': 'Experience',
            'description': 'App crashes during peak trading hours, slow loading times for mutual fund section'
        },
        {
            'theme': 'Customer Support Response',
            'percentage': 15,
            'review_count': 1077,
            'severity': 'Medium',
            'business_risk': 'Trust',
            'description': 'Delayed support responses, users reporting 24-48 hour wait times for ticket resolution'
        },
        {
            'theme': 'UI/UX Confusion',
            'percentage': 10,
            'review_count': 718,
            'severity': 'Low',
            'business_risk': 'Onboarding',
            'description': 'New users finding mutual fund investment flow confusing, unclear fee structure display'
        }
    ],
    'deep_dives': [
        {
            'theme': 'KYC Verification Delays',
            'quote': 'Been waiting for KYC approval for 4 days now. My friends using other apps got verified in hours. Very disappointed.',
            'segments': 'New users, first-time investors'
        },
        {
            'theme': 'Payment Processing Issues',
            'quote': 'Withdrawal stuck for 2 days with no update. This is my hard-earned money, I need better visibility on where it is.',
            'segments': 'Active traders, mutual fund investors'
        },
        {
            'theme': 'App Performance',
            'quote': 'App keeps crashing when I try to buy stocks during market open. Lost a good entry point today because of this.',
            'segments': 'Active traders, stock investors'
        },
        {
            'theme': 'UI/UX Confusion',
            'quote': 'Love the app but finding SIP options was confusing. Took me a while to figure out the interface.',
            'segments': 'First-time investors'
        }
    ],
    'recommendations': [
        {
            'action': 'Implement automated KYC verification using AI/ML document verification',
            'problem': 'Manual KYC process causing 3-5 day delays',
            'user_impact': 'Reduce verification time from days to hours, improving onboarding conversion by estimated 25%',
            'priority': 'P0'
        },
        {
            'action': 'Add real-time withdrawal tracking dashboard with status updates',
            'problem': 'Users anxious about withdrawal status with no visibility',
            'user_impact': 'Transparency reduces anxiety and support queries, builds trust',
            'priority': 'P0'
        },
        {
            'action': 'Optimize app performance with CDN caching and API response optimization',
            'problem': 'App crashes during peak trading hours',
            'user_impact': 'Smoother trading experience, no missed opportunities',
            'priority': 'P1'
        },
        {
            'action': 'Redesign mutual fund onboarding flow with guided walkthrough',
            'problem': 'New users struggling to navigate core features',
            'user_impact': 'Improve feature discovery rate by 35%',
            'priority': 'P1'
        }
    ]
}

# Generate visual report
print("\n" + "="*70)
print("📊 GENERATING VISUAL EXECUTIVE REPORT")
print("="*70 + "\n")

try:
    generator = VisualReportGenerator()
    output_path = "reports/visual_report_test.pdf"
    os.makedirs("reports", exist_ok=True)
    
    generator.generate_report(sample_analysis, output_path)
    
    print("\n" + "="*70)
    print("✅ VISUAL REPORT GENERATED SUCCESSFULLY!")
    print("="*70)
    print(f"\n📄 Report saved to: {output_path}")
    print("\nThe report includes:")
    print("  • Page 1: Executive Snapshot with KPIs and sentiment chart")
    print("  • Page 2: Key User Issues with horizontal bar chart")
    print("  • Page 3: Voice of Customer with quote cards")
    print("  • Page 4: Recommendations with priority-based actions")
    print("\n" + "="*70 + "\n")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
