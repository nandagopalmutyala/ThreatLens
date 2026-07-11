from reports.pdf_report import generate_report

sample_data = [
    {
        "headline": "Microsoft vulnerability detected",
        "threat": "Malware",
        "severity": "High"
    },
    {
        "headline": "New ransomware attack spreading",
        "threat": "Ransomware",
        "severity": "Critical"
    }
]

generate_report(sample_data)

print("PDF Generated Successfully")