from datetime import datetime
from io import BytesIO
import re

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
    Image,
)


BRAND_DARK = colors.HexColor("#0f172a")
BRAND_GREEN = colors.HexColor("#047857")
BRAND_LIGHT = colors.HexColor("#f8fafc")
BORDER = colors.HexColor("#cbd5e1")


def clean_markdown(text: str) -> str:
    if not text:
        return ""

    text = text.replace("**", "")
    text = text.replace("### ", "")
    text = text.replace("## ", "")
    text = text.replace("# ", "")
    text = text.replace("–", "-")
    text = text.replace("—", "-")
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def fig_to_image(fig, width=6.2 * inch, height=3.6 * inch):
    buffer = BytesIO()
    fig.savefig(buffer, format="png", dpi=180, bbox_inches="tight")
    buffer.seek(0)
    return Image(buffer, width=width, height=height)


def section_title(text, styles):
    return Paragraph(clean_markdown(text), styles["SectionTitle"])


def body_text(text, styles):
    return Paragraph(clean_markdown(text).replace("\n", "<br/>"), styles["BodyTextCustom"])


def build_kpi_table(risk_score):
    data = [
        ["Overall Risk", risk_score.get("overall_risk_level", "Unknown")],
        ["Overall Score", f"{risk_score.get('overall_score', 0)}/100"],
        ["Likelihood", f"{risk_score.get('likelihood_score', 0)}/100"],
        ["Impact", f"{risk_score.get('impact_score', 0)}/100"],
        ["Executive Decision", risk_score.get("executive_decision", "Review required")],
    ]

    table = Table(data, colWidths=[2.2 * inch, 4.8 * inch])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), BRAND_DARK),
                ("TEXTCOLOR", (0, 0), (0, -1), colors.white),
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 11),
                ("BACKGROUND", (1, 0), (1, -1), BRAND_LIGHT),
                ("GRID", (0, 0), (-1, -1), 0.5, BORDER),
                ("PADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    return table


def parse_markdown_table(lines, start_index):
    table_lines = []
    i = start_index

    while i < len(lines) and lines[i].strip().startswith("|"):
        table_lines.append(lines[i].strip())
        i += 1

    rows = []
    for line in table_lines:
        if re.match(r"^\|\s*-+", line):
            continue

        cells = [clean_markdown(cell.strip()) for cell in line.strip("|").split("|")]
        if cells:
            rows.append(cells)

    return rows, i


def markdown_to_flowables(markdown_text, styles):
    flowables = []
    lines = markdown_text.splitlines()
    i = 0

    while i < len(lines):
        line = lines[i].strip()

        if not line:
            flowables.append(Spacer(1, 0.08 * inch))
            i += 1
            continue

        if line.startswith("|"):
            rows, next_i = parse_markdown_table(lines, i)

            if rows:
                table = Table(rows, repeatRows=1)
                table.setStyle(
                    TableStyle(
                        [
                            ("BACKGROUND", (0, 0), (-1, 0), BRAND_DARK),
                            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                            ("FONTSIZE", (0, 0), (-1, -1), 7),
                            ("GRID", (0, 0), (-1, -1), 0.35, BORDER),
                            ("VALIGN", (0, 0), (-1, -1), "TOP"),
                            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, BRAND_LIGHT]),
                            ("PADDING", (0, 0), (-1, -1), 4),
                        ]
                    )
                )
                flowables.append(table)
                flowables.append(Spacer(1, 0.18 * inch))

            i = next_i
            continue

        if line.startswith("## ") or line.startswith("### "):
            flowables.append(Spacer(1, 0.16 * inch))
            flowables.append(section_title(line.replace("#", "").strip(), styles))
            i += 1
            continue

        if line.startswith("- "):
            flowables.append(Paragraph("• " + clean_markdown(line[2:]), styles["BodyTextCustom"]))
            i += 1
            continue

        flowables.append(body_text(line, styles))
        i += 1

    return flowables


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

    styles = getSampleStyleSheet()

    styles.add(
        ParagraphStyle(
            name="CoverTitle",
            parent=styles["Title"],
            fontSize=28,
            leading=34,
            alignment=TA_CENTER,
            textColor=BRAND_DARK,
            spaceAfter=20,
        )
    )

    styles.add(
        ParagraphStyle(
            name="SectionTitle",
            parent=styles["Heading2"],
            fontSize=16,
            leading=20,
            textColor=BRAND_GREEN,
            spaceBefore=14,
            spaceAfter=8,
        )
    )

    styles.add(
        ParagraphStyle(
            name="BodyTextCustom",
            parent=styles["BodyText"],
            fontSize=9.5,
            leading=13,
            alignment=TA_LEFT,
            spaceAfter=6,
        )
    )

    elements = []

    # Cover page
    elements.append(Paragraph("AI Risk Advisory Report", styles["CoverTitle"]))
    elements.append(
        Paragraph(
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            styles["BodyTextCustom"],
        )
    )
    elements.append(Spacer(1, 0.25 * inch))
    elements.append(build_kpi_table(risk_score))
    elements.append(Spacer(1, 0.35 * inch))

    elements.append(section_title("Assessed Scenario", styles))
    elements.append(body_text(question, styles))

    elements.append(PageBreak())

    # Dashboard page
    elements.append(section_title("Executive Risk Dashboard", styles))
    elements.append(Spacer(1, 0.15 * inch))
    elements.append(fig_to_image(bar_chart_fig, width=6.5 * inch, height=3.1 * inch))
    elements.append(Spacer(1, 0.25 * inch))
    elements.append(fig_to_image(radar_chart_fig, width=5.4 * inch, height=4.0 * inch))

    elements.append(PageBreak())

    elements.append(section_title("Likelihood vs Impact Matrix", styles))
    elements.append(fig_to_image(matrix_chart_fig, width=5.3 * inch, height=4.8 * inch))

    elements.append(PageBreak())

    # Report body
    elements.append(section_title("Full Advisory Report", styles))
    elements.extend(markdown_to_flowables(report, styles))

    elements.append(PageBreak())

    # Scoring appendix
    elements.append(section_title("LLM Risk Scoring Rationale", styles))
    elements.append(body_text(risk_score.get("scoring_rationale", "No rationale returned."), styles))

    elements.append(section_title("NIST Function Scores", styles))

    score_rows = [["Function", "Score"]]
    for name, value in scores.items():
        score_rows.append([name, f"{value}/100"])

    score_table = Table(score_rows, colWidths=[2.5 * inch, 2.0 * inch])
    score_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), BRAND_DARK),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.5, BORDER),
                ("PADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )

    elements.append(score_table)

    doc.build(elements)

    buffer.seek(0)
    return buffer.getvalue()