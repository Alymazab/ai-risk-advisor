"""
PDF report generator for AI Risk Advisor.
"""

from io import BytesIO
import tempfile
from pathlib import Path
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
    PageBreak,
)


def _clean_text(text: str) -> str:
    return (
        text.replace("•", "-")
        .replace("–", "-")
        .replace("—", "-")
        .replace("✔", "-")
        .replace("→", "->")
    )


def _add_markdown_to_story(report_text: str, story: list, styles):
    lines = _clean_text(report_text).splitlines()
    table_buffer = []

    def flush_table():
        nonlocal table_buffer

        if not table_buffer:
            return

        rows = []
        for line in table_buffer:
            parts = [p.strip() for p in line.strip("|").split("|")]
            if all(set(p) <= {"-", " "} for p in parts):
                continue
            rows.append(parts)

        if rows:
            table = Table(rows, repeatRows=1)
            table.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f172a")),
                        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#cbd5e1")),
                        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                        ("FONTSIZE", (0, 0), (-1, -1), 7),
                        ("VALIGN", (0, 0), (-1, -1), "TOP"),
                        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
                    ]
                )
            )
            story.append(table)
            story.append(Spacer(1, 0.18 * inch))

        table_buffer = []

    for line in lines:
        line = line.strip()

        if not line:
            flush_table()
            story.append(Spacer(1, 0.08 * inch))
            continue

        if line.startswith("|"):
            table_buffer.append(line)
            continue

        flush_table()

        if line.startswith("# "):
            story.append(Paragraph(line[2:], styles["TitleCustom"]))
            story.append(Spacer(1, 0.15 * inch))

        elif line.startswith("## "):
            story.append(Spacer(1, 0.12 * inch))
            story.append(Paragraph(line[3:], styles["Heading2Custom"]))

        elif line.startswith("### "):
            story.append(Paragraph(line[4:], styles["Heading3Custom"]))

        elif line.startswith("- "):
            story.append(Paragraph("• " + line[2:], styles["BodyCustom"]))

        elif line[:2].isdigit() and ". " in line[:5]:
            story.append(Paragraph(line, styles["BodyCustom"]))

        else:
            story.append(Paragraph(line, styles["BodyCustom"]))

    flush_table()


def _save_chart(fig, filename: str) -> str:
    path = Path(tempfile.gettempdir()) / filename
    fig.savefig(path, bbox_inches="tight", dpi=180)
    return str(path)


def generate_pdf_report(
    question: str,
    report: str,
    risk_score: dict,
    scores: dict,
    bar_chart_fig,
    radar_chart_fig,
    matrix_chart_fig,
) -> bytes:
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=0.55 * inch,
        leftMargin=0.55 * inch,
        topMargin=0.55 * inch,
        bottomMargin=0.55 * inch,
    )

    base_styles = getSampleStyleSheet()

    styles = {
        "TitleCustom": ParagraphStyle(
            "TitleCustom",
            parent=base_styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=22,
            leading=26,
            textColor=colors.HexColor("#0f172a"),
            spaceAfter=10,
        ),
        "Heading2Custom": ParagraphStyle(
            "Heading2Custom",
            parent=base_styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=15,
            leading=18,
            textColor=colors.HexColor("#14532d"),
            spaceBefore=8,
            spaceAfter=6,
        ),
        "Heading3Custom": ParagraphStyle(
            "Heading3Custom",
            parent=base_styles["Heading3"],
            fontName="Helvetica-Bold",
            fontSize=12,
            leading=15,
            textColor=colors.HexColor("#166534"),
            spaceBefore=6,
            spaceAfter=4,
        ),
        "BodyCustom": ParagraphStyle(
            "BodyCustom",
            parent=base_styles["BodyText"],
            fontName="Helvetica",
            fontSize=9,
            leading=12,
            textColor=colors.HexColor("#111827"),
            spaceAfter=4,
        ),
        "Small": ParagraphStyle(
            "Small",
            parent=base_styles["BodyText"],
            fontName="Helvetica",
            fontSize=8,
            leading=10,
            textColor=colors.HexColor("#475569"),
        ),
    }

    story = []

    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M")

    story.append(Paragraph("AI Risk Advisory Report", styles["TitleCustom"]))
    story.append(Paragraph(f"Generated: {generated_at}", styles["Small"]))
    story.append(Spacer(1, 0.2 * inch))

    summary_data = [
        ["Overall Risk", risk_score.get("overall_risk_level", "Unknown")],
        ["Overall Score", f"{risk_score.get('overall_score', 0)}/100"],
        ["Likelihood", f"{risk_score.get('likelihood_score', 0)}/100"],
        ["Impact", f"{risk_score.get('impact_score', 0)}/100"],
        ["Executive Decision", risk_score.get("executive_decision", "Review required")],
    ]

    summary_table = Table(summary_data, colWidths=[1.8 * inch, 4.6 * inch])
    summary_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#0f172a")),
                ("TEXTCOLOR", (0, 0), (0, -1), colors.white),
                ("BACKGROUND", (1, 0), (1, -1), colors.HexColor("#f8fafc")),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#cbd5e1")),
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )

    story.append(summary_table)
    story.append(Spacer(1, 0.25 * inch))

    story.append(Paragraph("Assessed Scenario", styles["Heading2Custom"]))
    story.append(Paragraph(_clean_text(question), styles["BodyCustom"]))
    story.append(PageBreak())

    story.append(Paragraph("Enterprise Risk Dashboard", styles["Heading2Custom"]))

    chart_paths = [
        _save_chart(bar_chart_fig, "ai_risk_bar_chart.png"),
        _save_chart(radar_chart_fig, "ai_risk_radar_chart.png"),
        _save_chart(matrix_chart_fig, "ai_risk_matrix_chart.png"),
    ]

    for chart_path in chart_paths:
        story.append(Image(chart_path, width=6.4 * inch, height=3.8 * inch))
        story.append(Spacer(1, 0.18 * inch))

    story.append(PageBreak())

    story.append(Paragraph("Full Advisory Report", styles["Heading2Custom"]))
    _add_markdown_to_story(report, story, styles)

    story.append(PageBreak())
    story.append(Paragraph("LLM Risk Scoring Rationale", styles["Heading2Custom"]))
    story.append(Paragraph(_clean_text(risk_score.get("scoring_rationale", "No rationale returned.")), styles["BodyCustom"]))

    story.append(Paragraph("NIST Function Scores", styles["Heading2Custom"]))
    score_rows = [["Function", "Score"]]
    for key, value in scores.items():
        score_rows.append([key, f"{value}/100"])

    score_table = Table(score_rows, colWidths=[3 * inch, 2 * inch])
    score_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f172a")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#cbd5e1")),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
            ]
        )
    )
    story.append(score_table)

    doc.build(story)

    pdf = buffer.getvalue()
    buffer.close()
    return pdf