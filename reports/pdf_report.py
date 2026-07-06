from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


def generate_report(news_data):

    file_name = "reports/security_report.pdf"

    doc = SimpleDocTemplate(file_name)

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph("Cyber Threat Intelligence Report", styles["Title"])
    )

    story.append(Spacer(1, 20))

    for item in news_data:

        text = (
            f"News: {item['headline']} <br/>"
            f"Threat Type: {item['threat']} <br/>"
            f"Severity: {item['severity']} <br/><br/>"
        )

        story.append(
            Paragraph(text, styles["Normal"])
        )

    doc.build(story)

    return file_name