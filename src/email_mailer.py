"""
Email Mailer
Sends weekly reports via Gmail
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from datetime import datetime
from typing import Dict, List
from dotenv import load_dotenv

load_dotenv()


class EmailMailer:
    """Sends email reports via Gmail"""
    
    def __init__(self):
        self.gmail_address = os.getenv('GMAIL_ADDRESS')
        self.gmail_password = os.getenv('GMAIL_APP_PASSWORD')
        
        if not self.gmail_address or not self.gmail_password:
            raise ValueError("Gmail credentials not found in environment variables")
    
    def send_weekly_report(self, analysis: Dict, report_paths: List[str], 
                          recipient: str = None) -> bool:
        """
        Send weekly report email with attachments
        
        Args:
            analysis: Analysis results dictionary
            report_paths: List of file paths to attach (markdown, PDF)
            recipient: Email recipient (defaults to sender)
        """
        
        if recipient is None:
            recipient = self.gmail_address
        
        print(f"\n📧 Preparing email to {recipient}...")
        
        # Create email
        msg = MIMEMultipart()
        msg['From'] = self.gmail_address
        msg['To'] = recipient
        msg['Subject'] = self._create_subject(analysis)
        
        # Email body
        body = self._create_email_body(analysis)
        msg.attach(MIMEText(body, 'html'))
        
        # Attach files
        for file_path in report_paths:
            if os.path.exists(file_path):
                self._attach_file(msg, file_path)
        
        # Send email
        try:
            print("🔐 Connecting to Gmail SMTP...")
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(self.gmail_address, self.gmail_password)
                server.send_message(msg)
            
            print(f"✅ Email sent successfully to {recipient}!")
            return True
            
        except Exception as e:
            print(f"❌ Error sending email: {e}")
            print("\n💡 Troubleshooting tips:")
            print("   1. Make sure you're using an App Password, not your regular Gmail password")
            print("   2. Enable 2-factor authentication on your Google account")
            print("   3. Generate an App Password at: https://myaccount.google.com/apppasswords")
            return False
    
    def _create_subject(self, analysis: Dict) -> str:
        """Create email subject line"""
        # Handle both old and new analyzer formats
        if 'metadata' in analysis:
            # New executive analyzer format
            date_end = analysis['metadata']['date_range']['end']
            avg_rating = analysis['metadata']['avg_rating']
        else:
            # Old analyzer format (fallback)
            date_end = analysis.get('date_range', {}).get('end', datetime.now().strftime('%Y-%m-%d'))
            avg_rating = analysis.get('avg_rating', 0)
        
        return f"📊 Groww App Weekly Insights — {date_end} (Avg Rating: {avg_rating}/5)"
    
    def _create_email_body(self, analysis: Dict) -> str:
        """Create HTML email body"""
        
        # Handle both old and new analyzer formats
        if 'metadata' in analysis:
            # New executive analyzer format
            meta = analysis['metadata']
            date_range = f"{meta['date_range']['start']} to {meta['date_range']['end']}"
            total_reviews = meta['total_reviews']
            avg_rating = meta['avg_rating']
            themes = analysis.get('themes', [])
            quotes = analysis.get('deep_dives', [])  # Executive format uses deep_dives
            actions = analysis.get('recommendations', [])
        else:
            # Old analyzer format (fallback)
            date_range = f"{analysis.get('date_range', {}).get('start', 'N/A')} to {analysis.get('date_range', {}).get('end', 'N/A')}"
            total_reviews = analysis.get('total_reviews', 0)
            avg_rating = analysis.get('avg_rating', 0)
            themes = analysis.get('themes', [])
            quotes = analysis.get('quotes', [])
            actions = analysis.get('actions', [])
        
        # Build themes HTML
        themes_html = ""
        for i, theme in enumerate(themes[:3], 1):
            severity = theme.get('severity', 'N/A')
            risk = theme.get('business_risk', 'N/A')
            themes_html += f"""
            <tr>
                <td style="padding: 10px; border-bottom: 1px solid #eee;">
                    <strong>{i}. {theme['theme']}</strong> ({theme['percentage']}%)<br/>
                    <span style="color: #666;">{theme['description']}</span><br/>
                    <em style="color: #999; font-size: 12px;">~{theme['review_count']} reviews | Severity: {severity} | Risk: {risk}</em>
                </td>
            </tr>
            """
        
        
        # Build quotes HTML (handle both formats)
        quotes_html = ""
        for i, quote_data in enumerate(quotes[:3], 1):
            if 'quote' in quote_data:
                # Old format
                sentiment_emoji = "😊" if quote_data.get('sentiment') == 'positive' else "😞" if quote_data.get('sentiment') == 'negative' else "😐"
                quote_text = quote_data['quote']
                theme_name = quote_data.get('theme', 'N/A')
            else:
                # New executive format (deep_dives)
                sentiment_emoji = "💡"
                quote_text = quote_data.get('quote', 'N/A')
                theme_name = quote_data.get('theme', 'N/A')
            
            quotes_html += f"""
            <tr>
                <td style="padding: 10px; border-bottom: 1px solid #eee;">
                    {sentiment_emoji} <em>"{quote_text}"</em><br/>
                    <span style="color: #999; font-size: 12px;">— Related to: {theme_name}</span>
                </td>
            </tr>
            """
        
        
        # Build actions HTML (handle both formats)
        actions_html = ""
        for i, action_data in enumerate(actions[:3], 1):
            if isinstance(action_data, str):
                # Old format (simple string)
                action_text = action_data
            else:
                # New executive format (dict with priority)
                priority = action_data.get('priority', 'P2')
                action_text = f"[{priority}] {action_data.get('action', 'N/A')}"
            
            actions_html += f"""
            <tr>
                <td style="padding: 10px; border-bottom: 1px solid #eee;">
                    <strong>{i}.</strong> {action_text}
                </td>
            </tr>
            """
        
        # Complete HTML email
        html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #1a73e8; color: white; padding: 20px; text-align: center; border-radius: 5px; }}
                .section {{ margin: 20px 0; }}
                .section-title {{ color: #1a73e8; font-size: 18px; margin-bottom: 10px; }}
                table {{ width: 100%; border-collapse: collapse; }}
                .footer {{ text-align: center; color: #999; font-size: 12px; margin-top: 30px; }}
                .stats {{ background-color: #f5f5f5; padding: 15px; border-radius: 5px; margin: 15px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>📊 Groww App Weekly Review Insights</h1>
                </div>
                
                <div class="stats">
                    <strong>Report Period:</strong> {date_range}<br/>
                    <strong>Total Reviews Analyzed:</strong> {total_reviews}<br/>
                    <strong>Average Rating:</strong> {avg_rating}/5 ⭐
                </div>
                
                <div class="section">
                    <div class="section-title">🔍 Top 3 Themes</div>
                    <table>
                        {themes_html}
                    </table>
                </div>
                
                <div class="section">
                    <div class="section-title">💬 User Voices</div>
                    <table>
                        {quotes_html}
                    </table>
                </div>
                
                <div class="section">
                    <div class="section-title">💡 Recommended Actions</div>
                    <table>
                        {actions_html}
                    </table>
                </div>
                
                <div class="footer">
                    <p>Report generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
                    <p>Attached: Full report in Markdown and PDF formats</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html
    
    def _attach_file(self, msg: MIMEMultipart, file_path: str):
        """Attach a file to the email"""
        
        filename = os.path.basename(file_path)
        
        with open(file_path, 'rb') as f:
            file_data = f.read()
        
        # Determine MIME type
        if file_path.endswith('.pdf'):
            attachment = MIMEApplication(file_data, _subtype='pdf')
        else:
            attachment = MIMEApplication(file_data, _subtype='octet-stream')
        
        attachment.add_header('Content-Disposition', 'attachment', filename=filename)
        msg.attach(attachment)
        
        print(f"📎 Attached: {filename}")


if __name__ == "__main__":
    # Test email (won't actually send without proper credentials)
    sample_analysis = {
        'themes': [
            {'theme': 'KYC Issues', 'description': 'Users facing delays in verification', 'percentage': 35, 'review_count': 70},
            {'theme': 'Payment Problems', 'description': 'Withdrawal and deposit issues', 'percentage': 28, 'review_count': 56},
            {'theme': 'App Performance', 'description': 'Crashes and slow loading', 'percentage': 22, 'review_count': 44}
        ],
        'quotes': [
            {'quote': 'KYC verification taking too long', 'theme': 'KYC Issues', 'sentiment': 'negative'},
            {'quote': 'Great app for beginners', 'theme': 'User Experience', 'sentiment': 'positive'},
            {'quote': 'Withdrawal stuck for 3 days', 'theme': 'Payment Problems', 'sentiment': 'negative'}
        ],
        'actions': [
            'Implement automated KYC verification to reduce processing time',
            'Add real-time withdrawal tracking dashboard',
            'Optimize app performance with caching and lazy loading'
        ],
        'total_reviews': 200,
        'avg_rating': 3.8,
        'date_range': {'start': '2024-11-01', 'end': '2024-12-30'}
    }
    
    print("Email body preview:")
    mailer = EmailMailer()
    body = mailer._create_email_body(sample_analysis)
    print(body)
