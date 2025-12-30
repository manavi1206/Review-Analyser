"""
Executive Report Generator
Creates comprehensive executive-level reports from analysis results
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


class ExecutiveReportGenerator:
    """Generates executive-level reports"""
    
    def generate_markdown(self, analysis: Dict, output_path: str = None) -> str:
        """Generate executive markdown report"""
        
        if output_path is None:
            timestamp = datetime.now().strftime('%Y%m%d')
            output_path = f"reports/executive_report_{timestamp}.md"
        
        md_content = self._build_executive_markdown(analysis)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        print(f"📄 Executive markdown report saved: {output_path}")
        return output_path
    
    def generate_pdf(self, analysis: Dict, output_path: str = None) -> str:
        """Generate executive PDF report"""
        
        if output_path is None:
            timestamp = datetime.now().strftime('%Y%m%d')
            output_path = f"reports/executive_report_{timestamp}.pdf"
        
        doc = SimpleDocTemplate(output_path, pagesize=letter,
                                rightMargin=72, leftMargin=72,
                                topMargin=72, bottomMargin=18)
        
        story = self._build_executive_pdf(analysis)
        doc.build(story)
        
        print(f"📄 Executive PDF report saved: {output_path}")
        return output_path
    
    def _build_executive_markdown(self, analysis: Dict) -> str:
        """Build executive markdown content"""
        
        meta = analysis.get('metadata', {})
        date_range = f"{meta.get('date_range', {}).get('start', 'N/A')} to {meta.get('date_range', {}).get('end', 'N/A')}"
        
        md = f"""# 📊 Groww App — Executive Review Insights

**Report Period:** {date_range}  
**Total Reviews:** {meta.get('total_reviews', 0):,}  
**Average Rating:** {meta.get('avg_rating', 0)}/5 ⭐  
**Sentiment:** {meta.get('positive_pct', 0):.1f}% Positive | {meta.get('neutral_pct', 0):.1f}% Neutral | {meta.get('negative_pct', 0):.1f}% Negative

---

## 🎯 Executive Summary

"""
        
        for bullet in analysis.get('executive_summary', []):
            md += f"- {bullet}\n"
        
        md += "\n---\n\n## 📊 Theme Segmentation (Impact-Oriented)\n\n"
        md += "| Theme | % | Count | Severity | Business Risk | Description |\n"
        md += "|-------|---|-------|----------|---------------|-------------|\n"
        
        for theme in analysis.get('themes', [])[:5]:
            md += f"| **{theme.get('theme', 'N/A')}** | {theme.get('percentage', 0)}% | {theme.get('review_count', 0)} | {theme.get('severity', 'N/A')} | {theme.get('business_risk', 'N/A')} | {theme.get('description', 'N/A')} |\n"
        
        md += "\n---\n\n## 🔍 High-Impact Insights\n\n"
        
        for i, dive in enumerate(analysis.get('deep_dives', [])[:3], 1):
            md += f"### {i}. {dive.get('theme', 'N/A')}\n\n"
            md += f"**Problem:** {dive.get('problem', 'N/A')}\n\n"
            md += f"**Why This Matters:** {dive.get('why_matters', 'N/A')}\n\n"
            md += f"**User Voice:** \"{dive.get('quote', 'N/A')}\"\n\n"
            md += f"**Segments Affected:** {dive.get('segments', 'N/A')}\n\n"
        
        md += "---\n\n## ⚠️ Rating Correlation Analysis\n\n"
        
        for driver in analysis.get('rating_drivers', []):
            md += f"- {driver}\n"
        
        md += "\n---\n\n## ✅ Positive Signals\n\n"
        
        for signal in analysis.get('positive_signals', []):
            md += f"- {signal}\n"
        
        md += "\n---\n\n## 💡 Decision-Oriented Recommendations\n\n"
        
        for i, rec in enumerate(analysis.get('recommendations', []), 1):
            md += f"### {i}. {rec.get('action', 'N/A')} [{rec.get('priority', 'P2')}]\n\n"
            md += f"- **Problem Addressed:** {rec.get('problem', 'N/A')}\n"
            md += f"- **User Impact:** {rec.get('user_impact', 'N/A')}\n"
            md += f"- **Business Impact:** {rec.get('business_impact', 'N/A')}\n\n"
        
        md += "---\n\n## 🎯 Leadership Decisions Required\n\n"
        
        for decision in analysis.get('leadership_decisions', []):
            md += f"- {decision}\n"
        
        md += f"\n---\n\n*Report generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}*\n"
        
        return md
    
    def _build_executive_pdf(self, analysis: Dict):
        """Build executive PDF content"""
        
        story = []
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=20,
            textColor=colors.HexColor('#1a73e8'),
            spaceAfter=20,
            alignment=TA_CENTER
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#1a73e8'),
            spaceAfter=10,
            spaceBefore=10
        )
        
        # Title
        story.append(Paragraph("📊 Groww App — Executive Review Insights", title_style))
        story.append(Spacer(1, 0.2*inch))
        
        # Metadata
        meta = analysis.get('metadata', {})
        date_range = f"{meta.get('date_range', {}).get('start', 'N/A')} to {meta.get('date_range', {}).get('end', 'N/A')}"
        
        meta_data = [
            ['Report Period:', date_range],
            ['Total Reviews:', f"{meta.get('total_reviews', 0):,}"],
            ['Average Rating:', f"{meta.get('avg_rating', 0)}/5 ⭐"],
            ['Sentiment:', f"{meta.get('positive_pct', 0):.1f}% Pos | {meta.get('neutral_pct', 0):.1f}% Neu | {meta.get('negative_pct', 0):.1f}% Neg"]
        ]
        
        meta_table = Table(meta_data, colWidths=[2*inch, 4*inch])
        meta_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.grey),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        
        story.append(meta_table)
        story.append(Spacer(1, 0.2*inch))
        
        # Executive Summary
        story.append(Paragraph("🎯 Executive Summary", heading_style))
        for bullet in analysis.get('executive_summary', []):
            story.append(Paragraph(f"• {bullet}", styles['Normal']))
            story.append(Spacer(1, 0.1*inch))
        
        story.append(Spacer(1, 0.15*inch))
        
        # Themes
        story.append(Paragraph("📊 Top Themes", heading_style))
        
        theme_data = [['Theme', '%', 'Severity', 'Risk']]
        for theme in analysis.get('themes', [])[:5]:
            theme_data.append([
                theme.get('theme', 'N/A'),
                f"{theme.get('percentage', 0)}%",
                theme.get('severity', 'N/A'),
                theme.get('business_risk', 'N/A')
            ])
        
        theme_table = Table(theme_data, colWidths=[2.5*inch, 0.7*inch, 1*inch, 1.3*inch])
        theme_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a73e8')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        story.append(theme_table)
        story.append(Spacer(1, 0.2*inch))
        
        # Recommendations
        story.append(Paragraph("💡 Key Recommendations", heading_style))
        for i, rec in enumerate(analysis.get('recommendations', [])[:3], 1):
            rec_text = f"<b>{i}. [{rec.get('priority', 'P2')}] {rec.get('action', 'N/A')}</b><br/>{rec.get('user_impact', 'N/A')}"
            story.append(Paragraph(rec_text, styles['Normal']))
            story.append(Spacer(1, 0.1*inch))
        
        # Footer
        story.append(Spacer(1, 0.2*inch))
        footer_text = f"<i>Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</i>"
        story.append(Paragraph(footer_text, styles['Normal']))
        
        return story
