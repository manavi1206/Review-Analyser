"""
Report Generator
Creates weekly one-page reports from analysis results
"""

import os
from datetime import datetime
from typing import Dict
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT


class ReportGenerator:
    """Generates weekly one-page reports"""
    
    def __init__(self, word_limit: int = 250):
        self.word_limit = word_limit
    
    def generate_markdown(self, analysis: Dict, output_path: str = None) -> str:
        """Generate markdown report"""
        
        if output_path is None:
            timestamp = datetime.now().strftime('%Y%m%d')
            output_path = f"reports/weekly_report_{timestamp}.md"
        
        # Build markdown content
        md_content = self._build_markdown_content(analysis)
        
        # Save to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        print(f"📄 Markdown report saved: {output_path}")
        return output_path
    
    def generate_pdf(self, analysis: Dict, output_path: str = None) -> str:
        """Generate PDF report"""
        
        if output_path is None:
            timestamp = datetime.now().strftime('%Y%m%d')
            output_path = f"reports/weekly_report_{timestamp}.pdf"
        
        # Create PDF
        doc = SimpleDocTemplate(output_path, pagesize=letter,
                                rightMargin=72, leftMargin=72,
                                topMargin=72, bottomMargin=18)
        
        # Build PDF content
        story = self._build_pdf_content(analysis)
        
        # Generate PDF
        doc.build(story)
        
        print(f"📄 PDF report saved: {output_path}")
        return output_path
    
    def _build_markdown_content(self, analysis: Dict) -> str:
        """Build markdown content for report"""
        
        date_range = f"{analysis['date_range']['start']} to {analysis['date_range']['end']}"
        
        md = f"""# 📊 Groww App Weekly Review Insights

**Report Period:** {date_range}  
**Total Reviews Analyzed:** {analysis['total_reviews']}  
**Average Rating:** {analysis['avg_rating']}/5 ⭐

---

## 🔍 Top 3 Themes

"""
        
        # Add top 3 themes
        for i, theme in enumerate(analysis['themes'][:3], 1):
            md += f"### {i}. {theme['theme']} ({theme['percentage']}%)\n"
            md += f"{theme['description']}\n"
            md += f"*~{theme['review_count']} reviews*\n\n"
        
        md += "---\n\n## 💬 User Voices\n\n"
        
        # Add quotes
        for i, quote in enumerate(analysis['quotes'], 1):
            sentiment_emoji = "😊" if quote['sentiment'] == 'positive' else "😞" if quote['sentiment'] == 'negative' else "😐"
            md += f"{i}. {sentiment_emoji} \"{quote['quote']}\"\n"
            md += f"   *— Related to: {quote['theme']}*\n\n"
        
        md += "---\n\n## 💡 Recommended Actions\n\n"
        
        # Add recommendations
        for i, action in enumerate(analysis['actions'], 1):
            md += f"{i}. **{action}**\n\n"
        
        md += "---\n\n"
        md += f"*Report generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}*\n"
        
        return md
    
    def _build_pdf_content(self, analysis: Dict):
        """Build PDF content"""
        
        story = []
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a73e8'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#1a73e8'),
            spaceAfter=12,
            spaceBefore=12
        )
        
        # Title
        story.append(Paragraph("📊 Groww App Weekly Review Insights", title_style))
        story.append(Spacer(1, 0.2*inch))
        
        # Metadata
        date_range = f"{analysis['date_range']['start']} to {analysis['date_range']['end']}"
        meta_data = [
            ['Report Period:', date_range],
            ['Total Reviews:', str(analysis['total_reviews'])],
            ['Average Rating:', f"{analysis['avg_rating']}/5 ⭐"]
        ]
        
        meta_table = Table(meta_data, colWidths=[2*inch, 4*inch])
        meta_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.grey),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        story.append(meta_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Top 3 Themes
        story.append(Paragraph("🔍 Top 3 Themes", heading_style))
        
        for i, theme in enumerate(analysis['themes'][:3], 1):
            theme_text = f"<b>{i}. {theme['theme']} ({theme['percentage']}%)</b><br/>{theme['description']}<br/><i>~{theme['review_count']} reviews</i>"
            story.append(Paragraph(theme_text, styles['Normal']))
            story.append(Spacer(1, 0.15*inch))
        
        story.append(Spacer(1, 0.2*inch))
        
        # User Quotes
        story.append(Paragraph("💬 User Voices", heading_style))
        
        for i, quote in enumerate(analysis['quotes'], 1):
            sentiment_emoji = "😊" if quote['sentiment'] == 'positive' else "😞" if quote['sentiment'] == 'negative' else "😐"
            quote_text = f"{sentiment_emoji} \"{quote['quote']}\"<br/><i>— Related to: {quote['theme']}</i>"
            story.append(Paragraph(quote_text, styles['Normal']))
            story.append(Spacer(1, 0.15*inch))
        
        story.append(Spacer(1, 0.2*inch))
        
        # Recommendations
        story.append(Paragraph("💡 Recommended Actions", heading_style))
        
        for i, action in enumerate(analysis['actions'], 1):
            action_text = f"<b>{i}.</b> {action}"
            story.append(Paragraph(action_text, styles['Normal']))
            story.append(Spacer(1, 0.15*inch))
        
        # Footer
        story.append(Spacer(1, 0.3*inch))
        footer_text = f"<i>Report generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</i>"
        story.append(Paragraph(footer_text, styles['Normal']))
        
        return story


if __name__ == "__main__":
    # Test with sample data
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
    
    generator = ReportGenerator()
    generator.generate_markdown(sample_analysis)
    generator.generate_pdf(sample_analysis)
    print("✅ Test reports generated!")
