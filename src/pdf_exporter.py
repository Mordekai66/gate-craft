
"""Export logic circuit questions to a formatted multi-question PDF."""

from pathlib import Path

from PIL import Image
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image as PDFImage,
    Table,
    TableStyle,
    KeepTogether,
)

NAVY = colors.HexColor("#17324D")
BLUE = colors.HexColor("#2F6690")
PALE_BLUE = colors.HexColor("#EEF5FA")
LIGHT_GRAY = colors.HexColor("#F4F6F8")
MID_GRAY = colors.HexColor("#667085")
BORDER = colors.HexColor("#D8E1E8")
GREEN = colors.HexColor("#287D5A")


def _question_card(question, include_answers, styles):
    """Build a compact, consistently formatted question card."""

    image_path = Path(question["image"])

    if not image_path.is_file():
        raise FileNotFoundError(
            f"Circuit image not found: {image_path}"
        )

    with Image.open(image_path) as img:
        image_width, image_height = img.size

    max_width = 165 * mm
    max_height = 35 * mm

    scale = min(
        max_width / image_width,
        max_height / image_height,
    )

    circuit = PDFImage(
        str(image_path),
        width=image_width * scale,
        height=image_height * scale,
    )
    circuit.hAlign = "CENTER"

    heading = Table(
        [[
            Paragraph(
                f"<b>QUESTION {question['number']:02d}</b>",
                styles["QuestionNumber"],
            ),
            Paragraph(
                f"{len(question['inputs'])} input(s)",
                styles["SmallRight"],
            ),
        ]],
        colWidths=[100 * mm, 65 * mm],
    )
    heading.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), PALE_BLUE),
        ("BOX", (0, 0), (-1, -1), 0.5, BORDER),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))

    content = [
        heading,
        Spacer(1, 2 * mm),
        Paragraph(
            "Find the Boolean expression for output Y.",
            styles["QuestionText"],
        ),
        Paragraph(
            "Inputs: " + ", ".join(question["inputs"]),
            styles["InputText"],
        ),
        Spacer(1, 2 * mm),
        circuit,
    ]

    if include_answers:
        content.extend([
            Spacer(1, 2 * mm),
            Paragraph(
                f"<b>Answer:</b> Y = {question['answer']}",
                styles["AnswerText"],
            ),
        ])

    card = Table(
        [[content]],
        colWidths=[174 * mm],
    )
    card.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.white),
        ("BOX", (0, 0), (-1, -1), 0.8, BORDER),
        ("LEFTPADDING", (0, 0), (-1, -1), 4 * mm),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4 * mm),
        ("TOPPADDING", (0, 0), (-1, -1), 3 * mm),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3 * mm),
    ]))

    return card


def _draw_page(canvas, doc, title, include_answers):
    """Draw the repeating page header and footer."""

    canvas.saveState()
    page_width, page_height = A4

    canvas.setFillColor(NAVY)
    canvas.rect(
        0,
        page_height - 17 * mm,
        page_width,
        17 * mm,
        fill=1,
        stroke=0,
    )

    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica-Bold", 10)
    canvas.drawString(
        18 * mm,
        page_height - 10.5 * mm,
        title,
    )

    mode = "ANSWER EDITION" if include_answers else "PRACTICE COPY"
    canvas.setFont("Helvetica", 7.5)
    canvas.drawRightString(
        page_width - 18 * mm,
        page_height - 10.5 * mm,
        mode,
    )

    canvas.setStrokeColor(BORDER)
    canvas.line(
        18 * mm, 14 * mm,
        page_width - 18 * mm, 14 * mm,
    )

    canvas.setFillColor(MID_GRAY)
    canvas.setFont("Helvetica", 8)
    canvas.drawString(
        18 * mm, 8.5 * mm,
        "DIGITAL LOGIC | BOOLEAN EXPRESSIONS",
    )
    canvas.drawRightString(
        page_width - 18 * mm,
        8.5 * mm,
        f"Page {doc.page}",
    )

    canvas.restoreState()


def create_pdf(
    questions,
    output_path,
    include_answers=True,
    title="Digital Logic - Circuit Practice",
):
    """Create a formatted PDF with multiple circuits per page.

    Args:
        questions: List of question dictionaries.
        output_path: Destination PDF path.
        include_answers: Show answers when True.
        title: Title shown in the page header.
    """

    if not questions:
        raise ValueError("At least one question is required.")

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name="QuestionNumber",
        fontName="Helvetica-Bold",
        fontSize=9,
        leading=11,
        textColor=BLUE,
    ))
    styles.add(ParagraphStyle(
        name="SmallRight",
        fontName="Helvetica",
        fontSize=8,
        leading=10,
        textColor=MID_GRAY,
        alignment=2,
    ))
    styles.add(ParagraphStyle(
        name="QuestionText",
        fontName="Helvetica-Bold",
        fontSize=9,
        leading=12,
        textColor=NAVY,
    ))
    styles.add(ParagraphStyle(
        name="InputText",
        fontName="Helvetica",
        fontSize=8,
        leading=11,
        textColor=MID_GRAY,
    ))
    styles.add(ParagraphStyle(
        name="AnswerText",
        fontName="Helvetica",
        fontSize=9,
        leading=12,
        textColor=GREEN,
        backColor=colors.HexColor("#EAF5EF"),
        borderPadding=5,
    ))

    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=23 * mm,
        bottomMargin=19 * mm,
        title=title,
        author="Digital Logic Practice Generator",
    )

    story = [
        Paragraph(
            "Solve each circuit and write its Boolean expression."
            if not include_answers
            else "Review each circuit and compare your work with the answer.",
            styles["Normal"],
        ),
        Spacer(1, 4 * mm),
    ]

    for question in questions:
        story.append(
            KeepTogether([
                _question_card(question, include_answers, styles),
                Spacer(1, 4 * mm),
            ])
        )

    def decorate(canvas, doc):
        _draw_page(canvas, doc, title, include_answers)

    doc.build(
        story,
        onFirstPage=decorate,
        onLaterPages=decorate,
    )

    return output_path
