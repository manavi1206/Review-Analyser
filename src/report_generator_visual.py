"""
Visual Executive Report Generator
Creates leadership-grade PDF reports with charts and clean design
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from datetime import datetime
import os
from typing import Dict, List
import io


class VisualReportGenerator:
    """Generates visual executive reports with charts"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        # Page title
        self.styles.add(ParagraphStyle(
            name='PageTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=12,
            fontName='Helvetica-Bold'
        ))
        
        # Section header
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#6b7280'),
            spaceAfter=8,
            fontName='Helvetica-Bold',
            textTransform='uppercase'
        ))
        
        # Metric value
        self.styles.add(ParagraphStyle(
            name='MetricValue',
            fontSize=32,
            textColor=colors.HexColor('#111827'),
            fontName='Helvetica-Bold',
            alignment=TA_CENTER
        ))
        
        # Metric label
        self.styles.add(ParagraphStyle(
            name='MetricLabel',
            fontSize=10,
            textColor=colors.HexColor('#6b7280'),
            fontName='Helvetica',
            alignment=TA_CENTER,
            spaceAfter=0
        ))
        
        # Quote text
        self.styles.add(ParagraphStyle(
            name='QuoteText',
            fontSize=14,
            textColor=colors.HexColor('#374151'),
            fontName='Helvetica-Oblique',
            leading=20,
            leftIndent=20,
            rightIndent=20
        ))
    
    def generate_report(self, analysis: Dict, output_path: str):
        """Generate visual PDF report"""
        
        # Create PDF
        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch
        )
        
        story = []
        
        # Extract data
        if 'metadata' in analysis:
            meta = analysis['metadata']
            total_reviews = meta['total_reviews']
            avg_rating = meta['avg_rating']
            positive_pct = meta['positive_pct']
            neutral_pct = meta['neutral_pct']
            negative_pct = meta['negative_pct']
            date_range = meta['date_range']
            themes = analysis.get('themes', [])
            deep_dives = analysis.get('deep_dives', [])
            recommendations = analysis.get('recommendations', [])
        else:
            return
        
        # Page 1: Executive Snapshot
        story.extend(self._create_page1_snapshot(
            total_reviews, avg_rating, positive_pct, neutral_pct, negative_pct, date_range
        ))
        story.append(PageBreak())
        
        # Page 2: Key User Issues
        story.extend(self._create_page2_issues(themes))
        story.append(PageBreak())
        
        # Page 3: Voice of Customer
        story.extend(self._create_page3_quotes(deep_dives))
        story.append(PageBreak())
        
        # Page 4: Recommendations
        story.extend(self._create_page4_recommendations(recommendations, themes))
        
        # Build PDF
        doc.build(story)
        print(f"✅ Visual report generated: {output_path}")
    
    def _create_page1_snapshot(self, total_reviews, avg_rating, positive_pct, 
                                neutral_pct, negative_pct, date_range):
        """Page 1: Executive Snapshot with KPIs and chart"""
        elements = []
        
        # Header
        elements.append(Paragraph("Groww App", self.styles['PageTitle']))
        elements.append(Paragraph("EXECUTIVE INSIGHTS REPORT", self.styles['SectionHeader']))
        
        # Report metadata
        date_str = f"{date_range['start']} to {date_range['end']}"
        timestamp = datetime.now().strftime("%B %d, %Y at %I:%M %p IST")
        
        meta_data = [
            ['Report Period:', date_str],
            ['Generated:', timestamp]
        ]
        meta_table = Table(meta_data, colWidths=[1.5*inch, 4*inch])
        meta_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#6b7280')),
            ('TEXTCOLOR', (1, 0), (1, -1), colors.HexColor('#111827')),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        elements.append(meta_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # KPI Cards
        elements.append(Paragraph("HEALTH SNAPSHOT", self.styles['SectionHeader']))
        elements.append(Spacer(1, 0.2*inch))
        
        kpi_data = [
            [
                self._create_kpi_cell("Total Reviews", f"{total_reviews:,}"),
                self._create_kpi_cell("Average Rating", f"{avg_rating}/5"),
                self._create_kpi_cell("Positive Sentiment", f"{positive_pct:.0f}%")
            ]
        ]
        
        kpi_table = Table(kpi_data, colWidths=[2.2*inch, 2.2*inch, 2.2*inch])
        kpi_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f9fafb')),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#e5e7eb')),
            ('INNERGRID', (0, 0), (-1, -1), 1, colors.HexColor('#e5e7eb')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 16),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 16),
        ]))
        elements.append(kpi_table)
        elements.append(Spacer(1, 0.4*inch))
        
        # Sentiment Chart
        elements.append(Paragraph("SENTIMENT DISTRIBUTION", self.styles['SectionHeader']))
        elements.append(Spacer(1, 0.2*inch))
        
        chart_img = self._create_sentiment_chart(positive_pct, neutral_pct, negative_pct)
        elements.append(chart_img)
        
        return elements
    
    def _create_kpi_cell(self, label, value):
        """Create a KPI cell with label and value"""
        return [
            Paragraph(label.upper(), self.styles['MetricLabel']),
            Spacer(1, 0.1*inch),
            Paragraph(value, self.styles['MetricValue'])
        ]
    
    def _create_sentiment_chart(self, positive_pct, neutral_pct, negative_pct):
        """Create sentiment distribution donut chart"""
        fig, ax = plt.subplots(figsize=(6, 3.5))
        
        sizes = [positive_pct, neutral_pct, negative_pct]
        labels = [f'Positive\n{positive_pct:.0f}%', f'Neutral\n{neutral_pct:.0f}%', f'Negative\n{negative_pct:.0f}%']
        colors_list = ['#10b981', '#9ca3af', '#ef4444']
        
        # Create donut chart
        wedges, texts, autotexts = ax.pie(
            sizes, 
            labels=labels,
            colors=colors_list,
            autopct='',
            startangle=90,
            wedgeprops=dict(width=0.4, edgecolor='white', linewidth=2)
        )
        
        # Style text
        for text in texts:
            text.set_fontsize(11)
            text.set_fontweight('bold')
            text.set_color('#1a1a1a')
        
        ax.axis('equal')
        
        # Save to buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=150, bbox_inches='tight', facecolor='white')
        buf.seek(0)
        plt.close()
        
        return Image(buf, width=4.5*inch, height=2.5*inch)
    
    def _create_page2_issues(self, themes):
        """Page 2: Key User Issues with bar chart"""
        elements = []
        
        elements.append(Paragraph("Key User Issues", self.styles['PageTitle']))
        elements.append(Paragraph("TOP THEMES RANKED BY IMPACT", self.styles['SectionHeader']))
        elements.append(Spacer(1, 0.3*inch))
        
        # Themes bar chart
        if themes:
            chart_img = self._create_themes_chart(themes[:5])
            elements.append(chart_img)
            elements.append(Spacer(1, 0.3*inch))
            
            # Themes table
            elements.append(Paragraph("THEME DETAILS", self.styles['SectionHeader']))
            elements.append(Spacer(1, 0.2*inch))
            
            theme_data = [['Theme', '% Reviews', 'Severity', 'Impact']]
            
            for theme in themes[:5]:
                severity = theme.get('severity', 'Medium')
                risk = theme.get('business_risk', 'N/A')
                
                theme_data.append([
                    theme['theme'],
                    f"{theme['percentage']}%",
                    severity,
                    risk
                ])
            
            theme_table = Table(theme_data, colWidths=[2.8*inch, 1*inch, 1.2*inch, 1.6*inch])
            theme_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f3f4f6')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#1a1a1a')),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('TOPPADDING', (0, 1), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e5e7eb')),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))
            elements.append(theme_table)
        
        return elements
    
    def _create_themes_chart(self, themes):
        """Create horizontal bar chart for themes"""
        fig, ax = plt.subplots(figsize=(6.5, 4))
        
        theme_names = [t['theme'] for t in themes]
        percentages = [t['percentage'] for t in themes]
        severities = [t.get('severity', 'Medium') for t in themes]
        
        # Color by severity
        colors_map = {'High': '#ef4444', 'Medium': '#f59e0b', 'Low': '#10b981'}
        bar_colors = [colors_map.get(s, '#9ca3af') for s in severities]
        
        # Create horizontal bars
        y_pos = range(len(theme_names))
        bars = ax.barh(y_pos, percentages, color=bar_colors, height=0.6)
        
        # Customize
        ax.set_yticks(y_pos)
        ax.set_yticklabels(theme_names, fontsize=10)
        ax.set_xlabel('% of Reviews', fontsize=10, fontweight='bold')
        ax.set_xlim(0, max(percentages) * 1.15)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.grid(axis='x', alpha=0.3, linestyle='--')
        
        # Add percentage labels
        for i, (bar, pct) in enumerate(zip(bars, percentages)):
            ax.text(pct + 1, i, f'{pct}%', va='center', fontsize=9, fontweight='bold')
        
        # Legend
        high_patch = mpatches.Patch(color='#ef4444', label='High Severity')
        med_patch = mpatches.Patch(color='#f59e0b', label='Medium Severity')
        low_patch = mpatches.Patch(color='#10b981', label='Low Severity')
        ax.legend(handles=[high_patch, med_patch, low_patch], loc='lower right', fontsize=8)
        
        plt.tight_layout()
        
        # Save to buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=150, bbox_inches='tight', facecolor='white')
        buf.seek(0)
        plt.close()
        
        return Image(buf, width=6*inch, height=3.5*inch)
    
    def _create_page3_quotes(self, deep_dives):
        """Page 3: Voice of Customer with quote cards"""
        elements = []
        
        elements.append(Paragraph("Voice of the Customer", self.styles['PageTitle']))
        elements.append(Paragraph("REPRESENTATIVE USER FEEDBACK", self.styles['SectionHeader']))
        elements.append(Spacer(1, 0.3*inch))
        
        for dive in deep_dives[:4]:
            # Quote card
            quote_data = [[
                Paragraph(f'"{dive.get("quote", "N/A")}"', self.styles['QuoteText'])
            ]]
            
            quote_table = Table(quote_data, colWidths=[6.5*inch])
            quote_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f9fafb')),
                ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#e5e7eb')),
                ('LEFTPADDING', (0, 0), (-1, -1), 20),
                ('RIGHTPADDING', (0, 0), (-1, -1), 20),
                ('TOPPADDING', (0, 0), (-1, -1), 16),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 16),
            ]))
            elements.append(quote_table)
            
            # Tags
            theme = dive.get('theme', 'N/A')
            segments = dive.get('segments', 'All users')
            
            tag_style = ParagraphStyle(
                name='TagStyle',
                fontSize=9,
                textColor=colors.HexColor('#6b7280'),
                fontName='Helvetica'
            )
            
            tags = Paragraph(f"<b>Theme:</b> {theme} • <b>User Type:</b> {segments}", tag_style)
            elements.append(Spacer(1, 0.05*inch))
            elements.append(tags)
            elements.append(Spacer(1, 0.25*inch))
        
        return elements
    
    def _create_page4_recommendations(self, recommendations, themes):
        """Page 4: Recommendations & Next Actions"""
        elements = []
        
        elements.append(Paragraph("Recommendations & Next Actions", self.styles['PageTitle']))
        elements.append(Paragraph("PRIORITY-BASED ACTION PLAN", self.styles['SectionHeader']))
        elements.append(Spacer(1, 0.3*inch))
        
        for i, rec in enumerate(recommendations[:4], 1):
            if isinstance(rec, dict):
                priority = rec.get('priority', 'P2')
                action = rec.get('action', 'N/A')
                problem = rec.get('problem', 'N/A')
                user_impact = rec.get('user_impact', 'N/A')
                
                # Priority badge color
                if priority == 'P0':
                    badge_color = colors.HexColor('#ef4444')
                elif priority == 'P1':
                    badge_color = colors.HexColor('#f59e0b')
                else:
                    badge_color = colors.HexColor('#10b981')
                
                # Action card
                action_style = ParagraphStyle(
                    name=f'Action{i}',
                    fontSize=12,
                    textColor=colors.HexColor('#111827'),
                    fontName='Helvetica-Bold',
                    spaceAfter=6
                )
                
                detail_style = ParagraphStyle(
                    name=f'Detail{i}',
                    fontSize=10,
                    textColor=colors.HexColor('#6b7280'),
                    fontName='Helvetica',
                    leading=14
                )
                
                impact_style = ParagraphStyle(
                    name=f'Impact{i}',
                    fontSize=10,
                    textColor=colors.HexColor('#059669'),
                    fontName='Helvetica',
                    leading=14
                )
                
                card_content = [
                    [Paragraph(f"<b>{priority}</b>", ParagraphStyle(name='Priority', fontSize=10, textColor=colors.white, fontName='Helvetica-Bold'))],
                    [Paragraph(action, action_style)],
                    [Paragraph(f"<b>Problem:</b> {problem}", detail_style)],
                    [Paragraph(f"→ <b>Expected Outcome:</b> {user_impact}", impact_style)]
                ]
                
                card_table = Table(card_content, colWidths=[6.5*inch])
                card_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (0, 0), badge_color),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#ffffff')),
                    ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#e5e7eb')),
                    ('LEFTPADDING', (0, 0), (-1, -1), 16),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 16),
                    ('TOPPADDING', (0, 0), (0, 0), 6),
                    ('BOTTOMPADDING', (0, 0), (0, 0), 6),
                    ('TOPPADDING', (0, 1), (-1, -1), 10),
                    ('BOTTOMPADDING', (0, 1), (-1, -1), 10),
                ]))
                
                elements.append(card_table)
                elements.append(Spacer(1, 0.2*inch))
        
        return elements
