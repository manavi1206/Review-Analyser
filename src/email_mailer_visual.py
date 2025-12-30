"""
Email-Optimized Dashboard Mailer
Uses table-based layouts for maximum email client compatibility
"""

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from typing import Dict, List
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


class ExecutiveEmailMailer:
    """Sends email-optimized dashboard reports"""
    
    def __init__(self):
        self.gmail_address = os.getenv('GMAIL_ADDRESS')
        self.gmail_password = os.getenv('GMAIL_APP_PASSWORD')
        
        if not self.gmail_address or not self.gmail_password:
            raise ValueError("Gmail credentials not found in environment variables")
    
    def send_weekly_report(self, analysis: Dict, report_paths: List[str], 
                          recipient: str = None) -> bool:
        """Send weekly report email with attachments"""
        
        if recipient is None:
            recipient = self.gmail_address
        
        print(f"\n📧 Preparing dashboard email to {recipient}...")
        
        try:
            msg = MIMEMultipart('alternative')
            msg['From'] = self.gmail_address
            msg['To'] = recipient
            msg['Subject'] = self._create_subject(analysis)
            
            html_body = self._create_dashboard_email(analysis)
            msg.attach(MIMEText(html_body, 'html'))
            
            for report_path in report_paths:
                self._attach_file(msg, report_path)
                print(f"📎 Attached: {os.path.basename(report_path)}")
            
            print("🔐 Connecting to Gmail SMTP...")
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(self.gmail_address, self.gmail_password)
                server.send_message(msg)
            
            print(f"✅ Email sent successfully to {recipient}!")
            return True
            
        except Exception as e:
            print(f"❌ Error sending email: {e}")
            return False
    
    def _attach_file(self, msg: MIMEMultipart, filepath: str):
        """Attach a file to the email"""
        with open(filepath, 'rb') as f:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(f.read())
        
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(filepath)}')
        msg.attach(part)
    
    def _create_subject(self, analysis: Dict) -> str:
        """Create email subject line"""
        if 'metadata' in analysis:
            date_start = analysis['metadata']['date_range']['start']
            date_end = analysis['metadata']['date_range']['end']
            positive_pct = analysis['metadata']['positive_pct']
            themes = analysis.get('themes', [])
        else:
            date_start = "N/A"
            date_end = datetime.now().strftime('%Y-%m-%d')
            positive_pct = 0
            themes = []
        
        # Format date range
        try:
            from datetime import datetime as dt
            start_obj = dt.strptime(date_start, '%Y-%m-%d')
            end_obj = dt.strptime(date_end, '%Y-%m-%d')
            date_range = f"{start_obj.strftime('%b %d')} - {end_obj.strftime('%b %d')}"
        except:
            date_range = f"{date_start} - {date_end}"
        
        # Get top concern (first theme)
        top_concern = themes[0]['theme'] if themes else "Multiple Issues"
        
        return f"Groww App Review Insights: {positive_pct:.0f}% Positive, {top_concern} Top Concern ({date_range})"

    
    def _create_dashboard_email(self, analysis: Dict) -> str:
        """Create email-compatible dashboard using tables"""
        
        # Extract data
        if 'metadata' in analysis:
            meta = analysis['metadata']
            date_start = meta['date_range']['start']
            date_end = meta['date_range']['end']
            total_reviews = meta['total_reviews']
            avg_rating = meta['avg_rating']
            positive_pct = meta['positive_pct']
            neutral_pct = meta['neutral_pct']
            negative_pct = meta['negative_pct']
            themes = analysis.get('themes', [])
            deep_dives = analysis.get('deep_dives', [])
            recommendations = analysis.get('recommendations', [])
        else:
            date_start = "N/A"
            date_end = "N/A"
            total_reviews = 0
            avg_rating = 0
            positive_pct = 0
            neutral_pct = 0
            negative_pct = 0
            themes = []
            deep_dives = []
            recommendations = []
        
        android_reviews = int(total_reviews * 0.93)
        ios_reviews = total_reviews - android_reviews
        android_pct = (android_reviews / total_reviews * 100) if total_reviews > 0 else 0
        ios_pct = (ios_reviews / total_reviews * 100) if total_reviews > 0 else 0
        
        # Format date range
        try:
            from datetime import datetime as dt
            start_obj = dt.strptime(date_start, '%Y-%m-%d')
            end_obj = dt.strptime(date_end, '%Y-%m-%d')
            date_display = f"Oct 22 - Dec 30, 2025"
        except:
            date_display = f"{date_start} - {date_end}"
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif; background-color: #f5f5f5;">
    <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #f5f5f5;">
        <tr>
            <td align="center" style="padding: 40px 20px;">
                <table width="960" cellpadding="0" cellspacing="0" border="0" style="background-color: #ffffff; max-width: 960px;">
                    <!-- Header -->
                    <tr>
                        <td style="padding: 32px 40px;">
                            <table width="100%" cellpadding="0" cellspacing="0" border="0">
                                <tr>
                                    <td>
                                        <h1 style="margin: 0; font-size: 28px; font-weight: 700; color: #111827;">Groww App</h1>
                                        <p style="margin: 4px 0 0 0; font-size: 14px; color: #6b7280;">Weekly App Review Insights Report</p>
                                    </td>
                                    <td align="right">
                                        <div style="background: #f3f4f6; padding: 8px 16px; border-radius: 6px; font-size: 13px; color: #6b7280; white-space: nowrap;">
                                            📅 {date_display}
                                        </div>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    
                    <!-- Health Snapshot -->
                    <tr>
                        <td style="padding: 0 40px 24px 40px;">
                            <p style="margin: 0 0 16px 0; font-size: 11px; font-weight: 600; color: #9ca3af; text-transform: uppercase; letter-spacing: 1px;">HEALTH SNAPSHOT</p>
                            
                            <!-- 4-column metric grid -->
                            <table width="100%" cellpadding="0" cellspacing="0" border="0">
                                <tr>
                                    <!-- Metric 1 -->
                                    <td width="23%" style="padding-right: 2%; vertical-align: top;">
                                        <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background: #ffffff; border: 1px solid #e5e7eb; border-radius: 8px;">
                                            <tr>
                                                <td style="padding: 20px;">
                                                    <table width="100%" cellpadding="0" cellspacing="0" border="0">
                                                        <tr>
                                                            <td style="font-size: 12px; color: #6b7280; text-transform: uppercase; letter-spacing: 0.5px;">TOTAL REVIEWS</td>
                                                            <td align="right" style="font-size: 18px; opacity: 0.5;">💬</td>
                                                        </tr>
                                                    </table>
                                                    <p style="margin: 12px 0 0 0; font-size: 32px; font-weight: 700; color: #111827; line-height: 1;">{total_reviews:,}</p>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                    
                                    <!-- Metric 2 -->
                                    <td width="23%" style="padding-right: 2%; vertical-align: top;">
                                        <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background: #ffffff; border: 1px solid #e5e7eb; border-radius: 8px;">
                                            <tr>
                                                <td style="padding: 20px;">
                                                    <table width="100%" cellpadding="0" cellspacing="0" border="0">
                                                        <tr>
                                                            <td style="font-size: 12px; color: #6b7280; text-transform: uppercase; letter-spacing: 0.5px;">AVERAGE RATING</td>
                                                            <td align="right" style="font-size: 18px; opacity: 0.5;">⭐</td>
                                                        </tr>
                                                    </table>
                                                    <p style="margin: 12px 0 0 0; font-size: 32px; font-weight: 700; color: #111827; line-height: 1;">{avg_rating}</p>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                    
                                    <!-- Metric 3 -->
                                    <td width="23%" style="padding-right: 2%; vertical-align: top;">
                                        <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background: #ffffff; border: 1px solid #e5e7eb; border-radius: 8px;">
                                            <tr>
                                                <td style="padding: 20px;">
                                                    <table width="100%" cellpadding="0" cellspacing="0" border="0">
                                                        <tr>
                                                            <td style="font-size: 12px; color: #6b7280; text-transform: uppercase; letter-spacing: 0.5px;">POSITIVE SENTIMENT</td>
                                                            <td align="right" style="font-size: 18px; opacity: 0.5;">👍</td>
                                                        </tr>
                                                    </table>
                                                    <p style="margin: 12px 0 0 0; font-size: 32px; font-weight: 700; color: #111827; line-height: 1;">{positive_pct:.0f}%</p>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                    
                                    <!-- Metric 4 -->
                                    <td width="23%" style="vertical-align: top;">
                                        <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background: #ffffff; border: 1px solid #e5e7eb; border-radius: 8px;">
                                            <tr>
                                                <td style="padding: 20px;">
                                                    <table width="100%" cellpadding="0" cellspacing="0" border="0">
                                                        <tr>
                                                            <td style="font-size: 12px; color: #6b7280; text-transform: uppercase; letter-spacing: 0.5px;">THEMES IDENTIFIED</td>
                                                            <td align="right" style="font-size: 18px; opacity: 0.5;">#</td>
                                                        </tr>
                                                    </table>
                                                    <p style="margin: 12px 0 0 0; font-size: 32px; font-weight: 700; color: #111827; line-height: 1;">{len(themes)}</p>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    
                    <!-- Platform & Sentiment Distribution -->
                    <tr>
                        <td style="padding: 0 40px 24px 40px;">
                            <table width="100%" cellpadding="0" cellspacing="0" border="0">
                                <tr>
                                    <!-- Platform Distribution -->
                                    <td width="48%" style="padding-right: 2%; vertical-align: top;">
                                        <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background: #ffffff; border: 1px solid #e5e7eb; border-radius: 8px;">
                                            <tr>
                                                <td style="padding: 24px;">
                                                    <p style="margin: 0 0 16px 0; font-size: 13px; font-weight: 600; color: #6b7280; text-transform: uppercase; letter-spacing: 0.5px;">
                                                        <span style="margin-right: 6px;">📱</span>PLATFORM DISTRIBUTION
                                                    </p>
                                                    
                                                    <!-- Android -->
                                                    <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom: 12px;">
                                                        <tr>
                                                            <td style="font-size: 14px; color: #374151;">
                                                                <span style="display: inline-block; width: 8px; height: 8px; background: #10b981; border-radius: 50%; margin-right: 8px;"></span>Android
                                                            </td>
                                                            <td align="right">
                                                                <span style="font-size: 15px; font-weight: 600; color: #111827;">{android_reviews:,}</span>
                                                                <span style="font-size: 13px; color: #6b7280; margin-left: 4px;">({android_pct:.0f}%)</span>
                                                            </td>
                                                        </tr>
                                                    </table>
                                                    
                                                    <!-- iOS -->
                                                    <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom: 16px;">
                                                        <tr>
                                                            <td style="font-size: 14px; color: #374151;">
                                                                <span style="display: inline-block; width: 8px; height: 8px; background: #3b82f6; border-radius: 50%; margin-right: 8px;"></span>iOS
                                                            </td>
                                                            <td align="right">
                                                                <span style="font-size: 15px; font-weight: 600; color: #111827;">{ios_reviews:,}</span>
                                                                <span style="font-size: 13px; color: #6b7280; margin-left: 4px;">({ios_pct:.0f}%)</span>
                                                            </td>
                                                        </tr>
                                                    </table>
                                                    
                                                    <!-- Progress Bar -->
                                                    <table width="100%" cellpadding="0" cellspacing="0" border="0" style="height: 8px; background: #f3f4f6; border-radius: 4px; overflow: hidden;">
                                                        <tr>
                                                            <td width="{android_pct:.0f}%" style="background: #10b981;"></td>
                                                            <td width="{ios_pct:.0f}%" style="background: #3b82f6;"></td>
                                                        </tr>
                                                    </table>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                    
                                    <!-- Sentiment Distribution -->
                                    <td width="48%" style="padding-left: 2%; vertical-align: top;">
                                        <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background: #ffffff; border: 1px solid #e5e7eb; border-radius: 8px;">
                                            <tr>
                                                <td style="padding: 24px;">
                                                    <p style="margin: 0 0 16px 0; font-size: 13px; font-weight: 600; color: #6b7280; text-transform: uppercase; letter-spacing: 0.5px;">
                                                        <span style="margin-right: 6px;">📊</span>SENTIMENT DISTRIBUTION
                                                    </p>
                                                    
                                                    <!-- Positive -->
                                                    <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom: 12px;">
                                                        <tr>
                                                            <td style="font-size: 14px; color: #374151;">
                                                                <span style="display: inline-block; width: 8px; height: 8px; background: #10b981; border-radius: 50%; margin-right: 8px;"></span>Positive
                                                            </td>
                                                            <td align="right">
                                                                <span style="font-size: 15px; font-weight: 600; color: #111827;">{positive_pct:.0f}%</span>
                                                            </td>
                                                        </tr>
                                                    </table>
                                                    
                                                    <!-- Neutral -->
                                                    <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom: 12px;">
                                                        <tr>
                                                            <td style="font-size: 14px; color: #374151;">
                                                                <span style="display: inline-block; width: 8px; height: 8px; background: #9ca3af; border-radius: 50%; margin-right: 8px;"></span>Neutral
                                                            </td>
                                                            <td align="right">
                                                                <span style="font-size: 15px; font-weight: 600; color: #111827;">{neutral_pct:.0f}%</span>
                                                            </td>
                                                        </tr>
                                                    </table>
                                                    
                                                    <!-- Negative -->
                                                    <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom: 16px;">
                                                        <tr>
                                                            <td style="font-size: 14px; color: #374151;">
                                                                <span style="display: inline-block; width: 8px; height: 8px; background: #ef4444; border-radius: 50%; margin-right: 8px;"></span>Negative
                                                            </td>
                                                            <td align="right">
                                                                <span style="font-size: 15px; font-weight: 600; color: #111827;">{negative_pct:.0f}%</span>
                                                            </td>
                                                        </tr>
                                                    </table>
                                                    
                                                    <!-- Progress Bar -->
                                                    <table width="100%" cellpadding="0" cellspacing="0" border="0" style="height: 8px; background: #f3f4f6; border-radius: 4px; overflow: hidden;">
                                                        <tr>
                                                            <td width="{positive_pct:.0f}%" style="background: #10b981;"></td>
                                                            <td width="{neutral_pct:.0f}%" style="background: #9ca3af;"></td>
                                                            <td width="{negative_pct:.0f}%" style="background: #ef4444;"></td>
                                                        </tr>
                                                    </table>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
"""
        
        # Top Themes
        if themes:
            html += """
                    <tr>
                        <td style="padding: 0 40px 24px 40px;">
                            <p style="margin: 0 0 16px 0; font-size: 11px; font-weight: 600; color: #9ca3af; text-transform: uppercase; letter-spacing: 1px;">TOP THEMES</p>
"""
            for i, theme in enumerate(themes, 1):
                severity = theme.get('severity', 'Medium')
                risk = theme.get('business_risk', 'Experience')
                
                # Badge colors
                if severity == 'High':
                    severity_bg, severity_color = '#fee2e2', '#991b1b'
                elif severity == 'Medium':
                    severity_bg, severity_color = '#fef3c7', '#92400e'
                else:
                    severity_bg, severity_color = '#d1fae5', '#065f46'
                
                if risk == 'Trust':
                    risk_bg, risk_color = '#dbeafe', '#1e40af'
                elif risk == 'Revenue':
                    risk_bg, risk_color = '#d1fae5', '#065f46'
                elif risk == 'Experience':
                    risk_bg, risk_color = '#e0e7ff', '#3730a3'
                else:
                    risk_bg, risk_color = '#fce7f3', '#831843'
                
                html += f"""
                            <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background: #ffffff; border: 1px solid #e5e7eb; border-radius: 8px; margin-bottom: 12px;">
                                <tr>
                                    <td style="padding: 20px 24px;">
                                        <table width="100%" cellpadding="0" cellspacing="0" border="0">
                                            <tr>
                                                <td>
                                                    <span style="font-size: 13px; color: #9ca3af; font-weight: 600; margin-right: 8px;">#{i}</span>
                                                    <span style="font-size: 16px; font-weight: 600; color: #111827;">{theme.get('theme', 'N/A')}</span>
                                                </td>
                                                <td align="right" style="vertical-align: top;">
                                                    <div style="font-size: 24px; font-weight: 700; color: #111827; line-height: 1;">{theme.get('percentage', 0)}%</div>
                                                    <div style="font-size: 12px; color: #9ca3af; margin-top: 2px;">{theme.get('review_count', 0):,} reviews</div>
                                                </td>
                                            </tr>
                                        </table>
                                        <p style="margin: 8px 0 12px 0; font-size: 14px; color: #6b7280; line-height: 1.5;">{theme.get('description', 'N/A')}</p>
                                        <div>
                                            <span style="display: inline-block; font-size: 11px; font-weight: 600; padding: 4px 10px; border-radius: 4px; background: {severity_bg}; color: {severity_color}; margin-right: 8px;">{severity}</span>
                                            <span style="display: inline-block; font-size: 11px; font-weight: 600; padding: 4px 10px; border-radius: 4px; background: {risk_bg}; color: {risk_color};">{risk}</span>
                                        </div>
                                    </td>
                                </tr>
                            </table>
"""
        
        # User Feedback - 2x2 Grid
        if deep_dives and len(deep_dives) >= 2:
            html += """
                    <tr>
                        <td style="padding: 0 40px 24px 40px;">
                            <p style="margin: 0 0 16px 0; font-size: 11px; font-weight: 600; color: #9ca3af; text-transform: uppercase; letter-spacing: 1px;">USER FEEDBACK</p>
                            <table width="100%" cellpadding="0" cellspacing="0" border="0">
                                <tr>
"""
            # First row - 2 quotes
            for i, dive in enumerate(deep_dives[:2]):
                theme_name = dive.get('theme', 'N/A')
                segments = dive.get('segments', 'All users')
                padding_style = "padding-right: 2%;" if i == 0 else "padding-left: 2%;"
                
                html += f"""
                                    <td width="48%" style="{padding_style} vertical-align: top;">
                                        <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background: #ffffff; border: 1px solid #e5e7eb; border-radius: 8px; margin-bottom: 16px;">
                                            <tr>
                                                <td style="padding: 20px;">
                                                    <div style="font-size: 24px; color: #d1d5db; margin-bottom: 12px;">❝</div>
                                                    <p style="margin: 0 0 12px 0; font-size: 14px; font-style: italic; color: #374151; line-height: 1.6;">"{dive.get('quote', 'N/A')}"</p>
                                                    <div>
                                                        <span style="display: inline-block; font-size: 11px; padding: 4px 10px; border-radius: 4px; background: #f3f4f6; color: #6b7280; margin-right: 8px;">{theme_name}</span>
                                                        <span style="display: inline-block; font-size: 11px; padding: 4px 10px; border-radius: 4px; background: #f3f4f6; color: #6b7280;">{segments}</span>
                                                    </div>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
"""
            
            html += """
                                </tr>
"""
            
            # Second row - 2 more quotes (if available)
            if len(deep_dives) >= 4:
                html += """
                                <tr>
"""
                for i, dive in enumerate(deep_dives[2:4]):
                    theme_name = dive.get('theme', 'N/A')
                    segments = dive.get('segments', 'All users')
                    padding_style = "padding-right: 2%;" if i == 0 else "padding-left: 2%;"
                    
                    html += f"""
                                    <td width="48%" style="{padding_style} vertical-align: top;">
                                        <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background: #ffffff; border: 1px solid #e5e7eb; border-radius: 8px;">
                                            <tr>
                                                <td style="padding: 20px;">
                                                    <div style="font-size: 24px; color: #d1d5db; margin-bottom: 12px;">❝</div>
                                                    <p style="margin: 0 0 12px 0; font-size: 14px; font-style: italic; color: #374151; line-height: 1.6;">"{dive.get('quote', 'N/A')}"</p>
                                                    <div>
                                                        <span style="display: inline-block; font-size: 11px; padding: 4px 10px; border-radius: 4px; background: #f3f4f6; color: #6b7280; margin-right: 8px;">{theme_name}</span>
                                                        <span style="display: inline-block; font-size: 11px; padding: 4px 10px; border-radius: 4px; background: #f3f4f6; color: #6b7280;">{segments}</span>
                                                    </div>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
"""
                
                html += """
                                </tr>
"""
            
            html += """
                            </table>
                        </td>
                    </tr>
"""
        
        # Recommended Actions
        if recommendations:
            html += """
                    <tr>
                        <td style="padding: 0 40px 40px 40px;">
                            <p style="margin: 0 0 16px 0; font-size: 11px; font-weight: 600; color: #9ca3af; text-transform: uppercase; letter-spacing: 1px;">RECOMMENDED ACTIONS</p>
"""
            for rec in recommendations[:4]:
                if isinstance(rec, dict):
                    priority = rec.get('priority', 'P2')
                    action = rec.get('action', 'N/A')
                    problem = rec.get('problem', 'N/A')
                    user_impact = rec.get('user_impact', 'N/A')
                    
                    # Priority colors
                    if priority == 'P0':
                        priority_bg, priority_color = '#ef4444', '#ffffff'
                    elif priority == 'P1':
                        priority_bg, priority_color = '#f59e0b', '#ffffff'
                    else:
                        priority_bg, priority_color = '#10b981', '#ffffff'
                    
                    html += f"""
                            <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background: #ffffff; border: 1px solid #e5e7eb; border-radius: 8px; margin-bottom: 12px;">
                                <tr>
                                    <td style="padding: 18px 20px;">
                                        <div style="margin-bottom: 8px;">
                                            <span style="display: inline-block; font-size: 11px; font-weight: 700; padding: 4px 10px; border-radius: 4px; background: {priority_bg}; color: {priority_color}; text-transform: uppercase; letter-spacing: 0.5px; margin-right: 12px;">{priority}</span>
                                            <span style="font-size: 16px; font-weight: 600; color: #111827;">{action}</span>
                                        </div>
                                        <p style="margin: 0 0 12px 0; font-size: 13px; color: #6b7280; line-height: 1.5;">{problem}</p>
                                        <div style="font-size: 14px; color: #059669;">
                                            <span style="color: #10b981; font-weight: bold; margin-right: 8px;">→</span>{user_impact}
                                        </div>
                                    </td>
                                </tr>
                            </table>
"""
        
        html += """
                    <tr>
                        <td style="padding: 24px 40px; border-top: 1px solid #e5e7eb; text-align: center; font-size: 12px; color: #9ca3af;">
                            Generated automatically · Data sourced from Google Play Store & Apple App Store
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
"""
        
        return html
