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
        date_end = analysis['date_range']['end']
        avg_rating = analysis['avg_rating']
        return f"📊 Groww App Weekly Insights — {date_end} (Avg Rating: {avg_rating}/5)"
    
    def _create_email_body(self, analysis: Dict) -> str:
        """Create HTML email body"""
        
        date_range = f"{analysis['date_range']['start']} to {analysis['date_range']['end']}"
        
        # Build themes HTML
        themes_html = ""
        for i, theme in enumerate(analysis['themes'][:3], 1):
            themes_html += f"""
            <tr>
                <td style="padding: 10px; border-bottom: 1px solid #eee;">
                    <strong>{i}. {theme['theme']}</strong> ({theme['percentage']}%)<br/>
                    <span style="color: #666;">{theme['description']}</span><br/>
                    <em style="color: #999; font-size: 12px;">~{theme['review_count']} reviews</em>
                </td>
            </tr>
            """
        
        # Build quotes HTML
        quotes_html = ""
        for i, quote in enumerate(analysis['quotes'], 1):
            sentiment_emoji = "😊" if quote['sentiment'] == 'positive' else "😞" if quote['sentiment'] == 'negative' else "😐"
            quotes_html += f"""
            <tr>
                <td style="padding: 10px; border-bottom: 1px solid #eee;">
                    {sentiment_emoji} <em>"{quote['quote']}"</em><br/>
                    <span style="color: #999; font-size: 12px;">— Related to: {quote['theme']}</span>
                </td>
            </tr>
            """
        
        # Build actions HTML
        actions_html = ""
        for i, action in enumerate(analysis['actions'], 1):
            actions_html += f"""
            <tr>
                <td style="padding: 10px; border-bottom: 1px solid #eee;">
                    <strong>{i}.</strong> {action}
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
                    <strong>Total Reviews Analyzed:</strong> {analysis['total_reviews']}<br/>
                    <strong>Average Rating:</strong> {analysis['avg_rating']}/5 ⭐
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
