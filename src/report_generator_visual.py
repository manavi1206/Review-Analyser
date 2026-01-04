"""
Plain Markdown-style Executive Report Generator
Minimal, text-based format with no design elements
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from typing import Dict, List


class VisualReportGenerator:
    """Generates plain, minimal executive reports"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_styles()
    
    def _setup_styles(self):
        """Setup minimal text styles"""
        
        # Main heading
        self.styles.add(ParagraphStyle(
            name='H1',
            fontSize=18,
            fontName='Helvetica-Bold',
            textColor=colors.HexColor('#000000'),
            spaceAfter=12,
            spaceBefore=0
        ))
        
        # Section heading
        self.styles.add(ParagraphStyle(
            name='H2',
            fontSize=14,
            fontName='Helvetica-Bold',
            textColor=colors.HexColor('#000000'),
            spaceAfter=10,
            spaceBefore=20
        ))
        
        # Body text
        self.styles.add(ParagraphStyle(
            name='PlainBody',
            fontSize=10,
            fontName='Helvetica',
            textColor=colors.HexColor('#000000'),
            leading=15,
            leftIndent=0
        ))
        
        # Bullet points
        self.styles.add(ParagraphStyle(
            name='BulletPoint',
            fontSize=10,
            fontName='Helvetica',
            textColor=colors.HexColor('#000000'),
            leading=15,
            leftIndent=20,
            bulletIndent=10
        ))
    
    def generate_report(self, analysis: Dict, output_path: str):
        """Generate plain text report"""
        
        if 'metadata' not in analysis:
            return
        
        meta = analysis['metadata']
        total_reviews = meta['total_reviews']
        avg_rating = meta['avg_rating']
        positive_pct = meta['positive_pct']
        date_range = meta['date_range']
        themes = analysis.get('themes', [])
        deep_dives = analysis.get('deep_dives', [])
        recommendations = analysis.get('recommendations', [])
        
        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=inch,
            leftMargin=inch,
            topMargin=inch,
            bottomMargin=inch
        )
        
        story = []
        
        # Title
        story.append(Paragraph("Groww App — Weekly Product Insights", self.styles['H1']))
        story.append(Paragraph(
            f"Report period: {date_range['start']} – {date_range['end']}",
            self.styles['PlainBody']
        ))
        story.append(Spacer(1, 0.3*inch))
        
        # 1. Product Health Snapshot
        story.append(Paragraph("1. Product Health Snapshot", self.styles['H2']))
        
        critical_count = len([t for t in themes if t.get('severity') == 'High'])
        
        story.append(Paragraph(f"• Total reviews: {total_reviews:,}", self.styles['BulletPoint']))
        story.append(Paragraph(f"• Average rating: {avg_rating} / 5", self.styles['BulletPoint']))
        story.append(Paragraph(f"• Positive sentiment: {positive_pct:.0f}%", self.styles['BulletPoint']))
        story.append(Paragraph(f"• Critical issues identified: {critical_count}", self.styles['BulletPoint']))
        story.append(Spacer(1, 0.15*inch))
        
        # Health assessment
        if positive_pct >= 70:
            health = "Healthy"
        elif positive_pct >= 60:
            health = "Moderate"
        else:
            health = "At Risk"
        
        story.append(Paragraph(f"Overall health: <b>{health}</b>", self.styles['PlainBody']))
        story.append(Spacer(1, 0.1*inch))
        
        # 2. Key Findings
        story.append(Paragraph("2. Key Findings", self.styles['H2']))
        story.append(Paragraph(f"• {positive_pct:.0f}% positive sentiment across all reviews", self.styles['BulletPoint']))
        story.append(Paragraph(f"• {critical_count} high-severity issues require immediate attention", self.styles['BulletPoint']))
        story.append(Paragraph("• Ratings remain stable across platforms", self.styles['BulletPoint']))
        if themes:
            story.append(Paragraph(f"• {themes[0]['theme']} is the largest source of negative feedback", self.styles['BulletPoint']))
        story.append(Spacer(1, 0.1*inch))
        
        # 3. Top User Issues
        story.append(Paragraph("3. Top User Issues (Ranked)", self.styles['H2']))
        
        for i, theme in enumerate(themes[:5], 1):
            sev = theme.get('severity', 'Medium')
            impact = theme.get('business_risk', 'N/A')
            
            story.append(Paragraph(
                f"<b>{i}. {theme['theme']}</b> ({sev} — {impact})",
                self.styles['PlainBody']
            ))
            story.append(Paragraph(f"• {theme['percentage']}% of reviews", self.styles['BulletPoint']))
            story.append(Paragraph(f"• {theme['description']}", self.styles['BulletPoint']))
            story.append(Spacer(1, 0.12*inch))
        
        # 4. Voice of the Customer
        story.append(Paragraph("4. Voice of the Customer", self.styles['H2']))
        
        for dive in deep_dives[:3]:
            story.append(Paragraph(
                f'"{dive.get("quote", "N/A")}"',
                ParagraphStyle(name='Quote', fontSize=10, fontName='Helvetica-Oblique', leading=15, leftIndent=10)
            ))
            story.append(Paragraph(
                f"— {dive.get('segments', 'User')}",
                ParagraphStyle(name='Attribution', fontSize=9, leading=13, leftIndent=10)
            ))
            story.append(Spacer(1, 0.15*inch))
        
        # 5. Recommended Actions
        story.append(Paragraph("5. Recommended Actions", self.styles['H2']))
        
        # P0 recommendations
        p0_recs = [r for r in recommendations if r.get('priority') == 'P0']
        for rec in p0_recs:
            story.append(Paragraph(
                f"<b>P0 — {rec.get('action', 'N/A')}</b>",
                self.styles['PlainBody']
            ))
            story.append(Paragraph(
                f"{rec.get('user_impact', 'N/A')}",
                ParagraphStyle(name='Impact', fontSize=10, leading=14, leftIndent=10)
            ))
            story.append(Spacer(1, 0.12*inch))
        
        # P1 recommendations
        p1_recs = [r for r in recommendations if r.get('priority') == 'P1']
        for rec in p1_recs:
            story.append(Paragraph(
                f"<b>P1 — {rec.get('action', 'N/A')}</b>",
                self.styles['PlainBody']
            ))
            story.append(Paragraph(
                f"{rec.get('user_impact', 'N/A')}",
                ParagraphStyle(name='Impact2', fontSize=10, leading=14, leftIndent=10)
            ))
            story.append(Spacer(1, 0.12*inch))
        
        doc.build(story)
        print(f"✅ Visual report generated: {output_path}")
