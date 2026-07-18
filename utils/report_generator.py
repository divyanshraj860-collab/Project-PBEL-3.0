from io import BytesIO
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


def generate_pdf(statement, prediction, confidence):
    """
    Generate a professional PDF report.
    """

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()

    title = styles["Heading1"]
    title.alignment = TA_CENTER
    title.textColor = colors.HexColor("#2563EB")

    heading = styles["Heading2"]
    heading.textColor = colors.HexColor("#1F2937")

    normal = styles["BodyText"]

    story = []

    # --------------------------------------------------
    # TITLE
    # --------------------------------------------------

    story.append(Paragraph("🧠 MindCare AI", title))
    story.append(
        Paragraph(
            "<b>Mental Health Assessment Report</b>",
            styles["Heading2"],
        )
    )

    story.append(Spacer(1, 20))

    # --------------------------------------------------
    # REPORT DETAILS
    # --------------------------------------------------

    report_id = datetime.now().strftime("MH-%Y%m%d-%H%M%S")

    details = [
        ["Report ID", report_id],
        ["Date", datetime.now().strftime("%d %B %Y")],
        ["Time", datetime.now().strftime("%I:%M %p")],
    ]

    table = Table(details, colWidths=[120, 280])

    table.setStyle(
        TableStyle(
            [
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#EAF2FF")),
                ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )

    story.append(table)
    story.append(Spacer(1, 20))

    # --------------------------------------------------
    # RESULT
    # --------------------------------------------------

    story.append(Paragraph("Assessment Result", heading))

    result_table = Table(
        [
            ["Prediction", str(prediction)],
            ["Confidence", f"{confidence:.2f}%"],
        ],
        colWidths=[120, 280],
    )

    result_table.setStyle(
        TableStyle(
            [
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#F3F4F6")),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )

    story.append(result_table)
    story.append(Spacer(1, 20))

    # --------------------------------------------------
    # RISK LEVEL
    # --------------------------------------------------

    if confidence >= 90:
        risk = "High"
    elif confidence >= 75:
        risk = "Moderate"
    else:
        risk = "Low"

    story.append(Paragraph("Risk Level", heading))
    story.append(Paragraph(f"<b>{risk}</b>", normal))
    story.append(Spacer(1, 20))

    # --------------------------------------------------
    # USER STATEMENT
    # --------------------------------------------------

    story.append(Paragraph("Your Statement", heading))
    story.append(Paragraph(statement.replace("\n", "<br/>"), normal))
    story.append(Spacer(1, 20))

    # --------------------------------------------------
    # RECOMMENDATIONS
    # --------------------------------------------------

    recommendation_map = {
        "Anxiety": [
            "Practice mindfulness or meditation.",
            "Reduce caffeine intake.",
            "Maintain a healthy sleep routine.",
        ],
        "Depression": [
            "Stay connected with supportive people.",
            "Exercise regularly.",
            "Seek professional guidance if symptoms persist.",
        ],
        "Stress": [
            "Take regular breaks during work or study.",
            "Practice deep breathing exercises.",
            "Stay hydrated.",
        ],
        "Normal": [
            "Maintain your healthy lifestyle.",
            "Continue regular physical activity.",
            "Get sufficient sleep.",
        ],
        "Suicidal": [
            "Seek immediate professional help.",
            "Contact a trusted family member or friend.",
            "Reach out to emergency mental health services if needed.",
        ],
        "Bipolar": [
            "Follow your prescribed treatment plan.",
            "Keep regular appointments with your healthcare provider.",
        ],
        "Personality disorder": [
            "Consider psychotherapy.",
            "Maintain a structured daily routine.",
        ],
    }

    story.append(Paragraph("Personalized Recommendations", heading))

    for item in recommendation_map.get(
        prediction,
        ["Consult a qualified mental health professional."]
    ):
        story.append(Paragraph(f"• {item}", normal))

    story.append(Spacer(1, 20))

    # --------------------------------------------------
    # DISCLAIMER
    # --------------------------------------------------

    story.append(Paragraph("Important Disclaimer", heading))

    story.append(
        Paragraph(
            "This report is generated using a Machine Learning model for educational purposes only. "
            "It is <b>not</b> a medical diagnosis and should not replace consultation with a qualified "
            "mental health professional.",
            normal,
        )
    )

    story.append(Spacer(1, 25))

    # --------------------------------------------------
    # FOOTER
    # --------------------------------------------------

    footer = styles["BodyText"]
    footer.alignment = TA_CENTER
    footer.textColor = colors.grey

    story.append(
        Paragraph(
            "MindCare AI<br/>"
            "Contact Health Professional in case of Emergency<br/>"
            
            "Divyansh Raj • All Rights Reserved • 2026 • email: divyanshraj860@gmail.com",
            footer,
        )
    )

    doc.build(story)

    pdf = buffer.getvalue()
    buffer.close()

    return pdf


# Compatibility alias
generate_report = generate_pdf