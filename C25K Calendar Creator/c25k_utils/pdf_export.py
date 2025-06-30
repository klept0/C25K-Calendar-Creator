"""
c25k_utils/pdf_export.py
Handles printable PDF export of the plan.
Fully implements visually rich, accessible PDF export using reportlab.
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.units import inch
import datetime


def export_to_pdf(plan, user, filename):
    """
    Export the workout plan as a visually rich, accessible PDF.
    Includes user info, personal goal, summary, resource links, accessibility options,
    and a table for each session (week, day, workout, tip, weather, motivational quote, rest day).
    """
    # Choose page size and font based on accessibility
    page_size = A4
    large_font = user.get("large_font", False)
    dyslexia_font = user.get("dyslexia_font", False)
    high_contrast = user.get("high_contrast", False)
    font_name = "Helvetica"
    if dyslexia_font:
        font_name = "Comic-Sans"  # fallback, as OpenDyslexic is not standard
    font_size = 12 if not large_font else 16
    heading_font_size = 18 if not large_font else 24
    # Document setup
    doc = SimpleDocTemplate(
        filename,
        pagesize=page_size,
        rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36,
        title="Couch to 5K Plan",
        author="C25K Calendar Generator",
    )
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="CenterTitle", alignment=TA_CENTER, fontSize=heading_font_size, fontName=font_name, spaceAfter=18, textColor=colors.yellow if high_contrast else colors.darkblue, leading=heading_font_size+2))
    styles.add(ParagraphStyle(name="NormalBig", fontSize=font_size, fontName=font_name, leading=font_size+2, textColor=colors.yellow if high_contrast else colors.black))
    styles.add(ParagraphStyle(name="SectionHeader", fontSize=font_size+2, fontName=font_name, spaceAfter=8, textColor=colors.yellow if high_contrast else colors.darkred, leading=font_size+4, alignment=TA_LEFT))
    styles.add(ParagraphStyle(name="RestDay", fontSize=font_size, fontName=font_name, textColor=colors.red, backColor=colors.whitesmoke, leading=font_size+2, leftIndent=12))
    styles.add(ParagraphStyle(name="Motivation", fontSize=font_size, fontName=font_name, textColor=colors.green, leading=font_size+2, leftIndent=12, italic=True))
    # High-contrast background (simulate with table background)
    bg_color = colors.black if high_contrast else colors.whitesmoke
    fg_color = colors.yellow if high_contrast else colors.black
    # Build document
    elements = []
    # Cover/title
    elements.append(Paragraph("Couch to 5K Personalized Plan", styles["CenterTitle"]))
    elements.append(Spacer(1, 0.2*inch))
    # User info
    user_info = f"""
    <b>Name:</b> {user['name']}<br/>
    <b>Age:</b> {user['age']}<br/>
    <b>Start Date:</b> {user.get('start_day').strftime('%Y-%m-%d') if user.get('start_day') else 'default'}<br/>
    <b>Personal Goal:</b> {user.get('goal', 'N/A')}<br/>
    <b>Accessibility:</b> {'High-contrast ' if high_contrast else ''}{'Large font ' if large_font else ''}{'Dyslexia-friendly font' if dyslexia_font else ''}<br/>
    <b>Resource:</b> <a href='https://www.nhs.uk/live-well/exercise/couch-to-5k-week-by-week/'>C25K Guide</a>
    """
    elements.append(Paragraph(user_info, styles["NormalBig"]))
    elements.append(Spacer(1, 0.2*inch))
    # Summary
    summary = f"This plan covers <b>{user.get('weeks', 10)}</b> weeks, <b>{user.get('days_per_week', 3)}</b> days per week. Each session includes a workout, tip, weather, and motivational quote."
    elements.append(Paragraph(summary, styles["NormalBig"]))
    elements.append(Spacer(1, 0.2*inch))
    # Table header
    table_data = [[
        "Week", "Day", "Date", "Workout", "Tip", "Weather", "Motivation", "Rest Day?"
    ]]
    # Add each session
    for session in plan:
        is_rest = session["duration"] == 0 or "rest" in session["description"].lower()
        table_data.append([
            session["week"],
            session["day"],
            session["date"],
            session["workout"],
            session["tip"],
            session.get("weather", ""),
            session.get("motivation", ""),
            "Yes" if is_rest else ""
        ])
    # Table style
    tbl_style = TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue if not high_contrast else colors.black),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white if not high_contrast else colors.yellow),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, -1), font_name),
        ("FONTSIZE", (0, 0), (-1, -1), font_size),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [bg_color, colors.white]),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
    ])
    # Highlight rest days
    for i, row in enumerate(table_data[1:], start=1):
        if row[-1] == "Yes":
            tbl_style.add("BACKGROUND", (0, i), (-1, i), colors.lightgrey if not high_contrast else colors.darkgrey)
            tbl_style.add("TEXTCOLOR", (0, i), (-1, i), colors.red if not high_contrast else colors.yellow)
    # Build table
    table = Table(table_data, repeatRows=1, hAlign="LEFT")
    table.setStyle(tbl_style)
    elements.append(table)
    elements.append(Spacer(1, 0.3*inch))
    # Add motivational section
    elements.append(Paragraph("Stay motivated!", styles["SectionHeader"]))
    motivational_quotes = [
        "You are stronger than you think!",
        "Every step counts. Keep going!",
        "Progress, not perfection.",
        "Believe in yourself and all that you are.",
        "Small steps lead to big changes.",
        "You’re doing great—don’t stop now!",
        "Consistency is key.",
        "Your only limit is you.",
        "Celebrate every victory, no matter how small.",
        "The journey is just as important as the destination.",
    ]
    for quote in motivational_quotes:
        elements.append(Paragraph(f"• {quote}", styles["Motivation"]))
    elements.append(Spacer(1, 0.2*inch))
    # Add summary and privacy note
    elements.append(Paragraph(
        f"<b>Generated on:</b> {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}<br/>"
        "<b>Privacy:</b> Your data is only used to generate this plan and is not stored.",
        styles["NormalBig"]
    ))
    # Build PDF
    doc.build(elements)
    print(f"PDF file '{filename}' created successfully.")
