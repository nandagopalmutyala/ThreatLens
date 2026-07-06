from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

def generate_pdf(results, stats, filename="ThreatVision_Report.pdf"):

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    elements = []

    elements.append(Paragraph("<b>ThreatVision</b>", styles["Title"]))
    elements.append(Paragraph("Cyber Threat Intelligence Report", styles["Heading2"]))

    elements.append(Paragraph("<br/>", styles["Normal"]))

    elements.append(
        Paragraph(
            f"""
            Critical Alerts : {stats['critical']}<br/>
            High Threats : {stats['high']}<br/>
            Companies : {stats['companies']}<br/>
            CVEs : {stats['cves']}
            """,
            styles["BodyText"],
        )
    )

    elements.append(Paragraph("<br/>", styles["Normal"]))

    data = [["Time", "Company", "Threat", "Severity"]]

    for item in results:

        data.append([
            item["timestamp"],
            item["company"],
            item["threat"],
            item["severity"]
        ])

    table = Table(data)

    table.setStyle(TableStyle([

        ("BACKGROUND",(0,0),(-1,0),colors.darkblue),

        ("TEXTCOLOR",(0,0),(-1,0),colors.white),

        ("GRID",(0,0),(-1,-1),1,colors.black),

        ("BACKGROUND",(0,1),(-1,-1),colors.beige),

        ("FONTSIZE",(0,0),(-1,-1),9)

    ]))

    elements.append(table)

    doc.build(elements)

    return filename