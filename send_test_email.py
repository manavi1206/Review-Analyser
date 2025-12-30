#!/usr/bin/env python3
"""
Test script to send visual email using last scraped data
"""

import sys
import os
import pandas as pd

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from email_mailer_visual import ExecutiveEmailMailer

# Create sample analysis data (simulating executive analyzer output)
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
    'executive_summary': [
        "68.5% positive sentiment indicates strong overall user satisfaction with the Groww platform",
        "KYC verification delays remain the top pain point, affecting 30% of reviews and driving trust concerns",
        "Payment processing issues (25% of reviews) directly impact revenue and require immediate attention",
        "App performance improvements in recent updates showing positive user response",
        "Critical: Address verification and withdrawal delays to prevent user churn"
    ],
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
            'problem': 'Manual verification process creating 3-5 day delays for new users',
            'why_matters': 'Delays in onboarding directly impact user acquisition and first-time investor conversion rates',
            'quote': 'Been waiting for KYC approval for 4 days now. My friends using other apps got verified in hours. Very disappointed.',
            'segments': 'New users, first-time investors'
        },
        {
            'theme': 'Payment Processing Issues',
            'problem': 'Withdrawal processing taking 2-3 business days, causing anxiety for users',
            'why_matters': 'Money-related delays erode trust and increase support burden, directly affecting retention',
            'quote': 'Withdrawal stuck for 2 days with no update. This is my hard-earned money, I need better visibility on where it is.',
            'segments': 'Active traders, mutual fund investors'
        },
        {
            'theme': 'App Performance',
            'problem': 'App crashes during market hours when trading volume is high',
            'why_matters': 'Performance issues during critical trading windows can lead to missed opportunities and user churn',
            'quote': 'App keeps crashing when I try to buy stocks during market open. Lost a good entry point today because of this.',
            'segments': 'Active traders, stock investors'
        },
        {
            'theme': 'UI/UX Confusion',
            'problem': 'Confusing navigation for mutual fund investments',
            'why_matters': 'Poor onboarding experience leads to user drop-off and lower conversion rates',
            'quote': 'Love the app but finding SIP options was confusing. Took me a while to figure out the interface.',
            'segments': 'First-time investors'
        }
    ],
    'rating_drivers': [
        'KYC verification delays contribute to 45% of 1-2★ reviews',
        'Payment processing issues drive 35% of negative ratings',
        'App crashes during trading hours account for 20% of low ratings'
    ],
    'positive_signals': [
        'Recent UI improvements for mutual fund section receiving positive feedback',
        'New users praising educational content and beginner-friendly interface',
        'Instant deposit feature (UPI) highly appreciated by users',
        'Stock screener and research tools getting consistent 5★ mentions'
    ],
    'recommendations': [
        {
            'action': 'Implement automated KYC verification using AI/ML document verification',
            'problem': 'Manual KYC process causing 3-5 day delays',
            'user_impact': 'Reduce verification time from days to hours, improving onboarding conversion by estimated 25%',
            'business_impact': 'Faster user activation, reduced support load, competitive advantage in acquisition',
            'priority': 'P0'
        },
        {
            'action': 'Add real-time withdrawal tracking dashboard with status updates',
            'problem': 'Users anxious about withdrawal status with no visibility',
            'user_impact': 'Transparency reduces anxiety and support queries, builds trust',
            'business_impact': 'Reduce withdrawal-related support tickets by 40%, improve retention',
            'priority': 'P0'
        },
        {
            'action': 'Optimize app performance with CDN caching and API response optimization',
            'problem': 'App crashes during peak trading hours',
            'user_impact': 'Smoother trading experience, no missed opportunities',
            'business_impact': 'Reduce churn during high-value trading windows, increase trading volume',
            'priority': 'P1'
        }
    ],
    'leadership_decisions': [
        'Prioritize KYC automation vs other Q1 roadmap items - requires engineering allocation',
        'Approve budget for third-party KYC verification API integration',
        'Decide on withdrawal tracking feature ownership (Product vs Engineering)',
        'Review infrastructure scaling plan for handling peak trading hours'
    ]
}

# Report paths (use existing reports if available)
report_paths = [
    'reports/executive_report_20251231.md',
    'reports/executive_report_20251231.pdf'
]

# Check if reports exist
import os
existing_reports = [p for p in report_paths if os.path.exists(p)]

if not existing_reports:
    print("⚠️  No existing reports found. Using sample data only.")
    report_paths = []
else:
    report_paths = existing_reports
    print(f"✅ Found {len(existing_reports)} existing reports to attach")

# Send test email
print("\n" + "="*70)
print("📧 SENDING TEST EMAIL WITH VISUAL DESIGN")
print("="*70 + "\n")

try:
    mailer = ExecutiveEmailMailer()
    success = mailer.send_weekly_report(
        analysis=sample_analysis,
        report_paths=report_paths
    )
    
    if success:
        print("\n" + "="*70)
        print("✅ TEST EMAIL SENT SUCCESSFULLY!")
        print("="*70)
        print("\nCheck your inbox to see the new visual email design!")
        print("It includes:")
        print("  • Pastel color scheme")
        print("  • Platform split (Android vs iOS)")
        print("  • Sentiment bar charts")
        print("  • Severity badges")
        print("  • Priority tags")
        print("  • Executive summary")
        print("\n📧 Email sent to:", mailer.gmail_address)
    else:
        print("\n❌ Failed to send test email")
        
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
