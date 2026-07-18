from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.colors import HexColor
from datetime import datetime
from io import BytesIO

styles = getSampleStyleSheet()

title_style = styles["Title"]
title_style.alignment = TA_CENTER
title_style.textColor = HexColor("#2563EB")

heading = styles["Heading2"]
heading.textColor = HexColor("#2563EB")

normal = styles["BodyText"]


def generate_pdf(statement, prediction, confidence):

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    story = []

    story.append(Paragraph("🧠 MindCare AI", title_style))
    story.append(Paragraph("Mental Health Assessment Report", heading))
    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            f"<b>Date:</b> {datetime.now().strftime('%d-%m-%Y %H:%M')}",
            normal,
        )
    )

    story.append(Spacer(1, 15))

    story.append(Paragraph("<b>User Statement</b>", heading))
    story.append(Paragraph(statement, normal))

    story.append(Spacer(1, 15))

    story.append(Paragraph("<b>Prediction</b>", heading))
    story.append(Paragraph(prediction, normal))

    story.append(Spacer(1, 15))

    story.append(Paragraph("<b>Confidence</b>", heading))
    story.append(Paragraph(f"{confidence:.2f}%", normal))

    story.append(Spacer(1, 20))

    recommendations = {
        "Normal": "Maintain a healthy lifestyle.",
        "Stress": "Practice meditation and maintain work-life balance.",
        "Anxiety": "Practice deep breathing and mindfulness.",
        "Depression": "Consult a mental health professional.",
        "Bipolar": "Seek psychiatric evaluation.",
        "Personality disorder": "Consult a psychologist.",
        "Suicidal": "Seek immediate professional help."
    }

    story.append(Paragraph("<b>Recommendation</b>", heading))
    story.append(
        Paragraph(
            recommendations.get(
                prediction,
                "Consult a qualified mental health professional."
            ),
            normal,
        )
    )

    story.append(Spacer(1, 20))

    story.append(Paragraph("<b>Disclaimer</b>", heading))
    story.append(
        Paragraph(
            "This report is generated for educational purposes only and is not a medical diagnosis.",
            normal,
        )
    )

    doc.build(story)

    pdf = buffer.getvalue()
    buffer.close()

    return pdf


# Backward compatibility
generate_report = generate_pdf