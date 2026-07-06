from flask import Flask, render_template, request, jsonify
import pandas as pd
import spacy
import re
from flask import send_file
from reports.pdf_generator import generate_pdf

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

from scraper.news_scraper import fetch_latest_news

app = Flask(__name__)

# Load NLP model once
nlp = spacy.load("en_core_web_sm")


# ===========================================
# PROCESS NEWS
# ===========================================

def process_news(search=""):

    # Fetch latest news
    news_df = fetch_latest_news()

    # Load training data
    train_df = pd.read_csv("data/training_data.csv")

    X_train = train_df["text"]

    y_label = train_df["label"]

    y_severity = train_df["severity"]

    # Train Vectorizer
    vectorizer = TfidfVectorizer()

    X_vectorized = vectorizer.fit_transform(X_train)

    # Threat Model
    threat_model = MultinomialNB()

    threat_model.fit(X_vectorized, y_label)

    # Severity Model
    severity_model = MultinomialNB()

    severity_model.fit(X_vectorized, y_severity)

    # ==========================
    # Process Headlines
    # ==========================

    results = []


    for _, row in news_df.iterrows():

        headline = row["headline"]

        timestamp = row["timestamp"]

        vector = vectorizer.transform([headline])

        threat = str(threat_model.predict(vector)[0])

        severity = str(severity_model.predict(vector)[0])

        # Company Detection

        doc = nlp(headline)

        company = "Not Detected"

        for entity in doc.ents:

            if entity.label_ == "ORG":

                company = entity.text

                break

        results.append({

            "timestamp": timestamp,

            "headline": headline,

            "company": company,

            "threat": threat,

            "severity": severity

        })

    # ==========================
    # Search Filter
    # ==========================

    if search:

        search = search.lower()

        results = [

            item

            for item in results

            if (

                search in item["headline"].lower()

                or search in item["company"].lower()

                or search in item["threat"].lower()

                or search in item["severity"].lower()

            )

        ]

    # ==========================
    # Dashboard Statistics
    # ==========================

    critical_count = sum(

        1

        for item in results

        if item["severity"] == "Critical"

    )

    high_count = sum(

        1

        for item in results

        if item["severity"] == "High"

    )

    company_count = len(

        set(

            item["company"]

            for item in results

            if item["company"] != "Not Detected"

        )

    )

    cve_pattern = r"CVE-\d{4}-\d+"

    cves = []

    for item in results:

        found = re.findall(

            cve_pattern,

            item["headline"]

        )

        cves.extend(found)

    cve_count = len(set(cves))

    # ==========================
    # Threat Distribution
    # ==========================

    threat_counts = {}

    for item in results:

        threat_counts[item["threat"]] = (

            threat_counts.get(item["threat"], 0)

            + 1

        )
        # ==========================
    # Timeline Data
    # ==========================

        timeline = {}

        for item in results:

            date = str(item["timestamp"])[:10]

            timeline[date] = timeline.get(date, 0) + 1
            # ==========================
    # Threat Distribution
    # ==========================

    threat_counts = {}

    for item in results:
        threat_counts[item["threat"]] = (
            threat_counts.get(item["threat"], 0)
            + 1
        )

   # ==========================
    # Cumulative Threat Timeline
    # ==========================

    timeline_labels = []
    timeline_values = []

    total_threats = 0

    for i, item in enumerate(results, start=1):

        total_threats += 1

        timeline_labels.append(f"T{i}")

        timeline_values.append(total_threats)

    # ==========================
    # Return
    # ==========================

    return {

            "results": results,

            "critical": critical_count,

            "high": high_count,

            "companies": company_count,

            "cves": cve_count,

            "labels": list(threat_counts.keys()),

            "values": list(threat_counts.values()),
            
            "timeline_labels": timeline_labels,
            
            "timeline_values": timeline_values

        }
    

# ===========================================
# HOME PAGE
# ===========================================

@app.route("/")
@app.route("/dashboard")
def home():

    search = request.args.get("search", "").strip()

    data = process_news(search)

    return render_template(
    "dashboard.html",
    news_data=data["results"],
    critical_count=data["critical"],
    high_count=data["high"],
    company_count=data["companies"],
    cve_count=data["cves"],
    threat_labels=data["labels"],
    threat_values=data["values"],
    timeline_labels=data["timeline_labels"],
    timeline_values=data["timeline_values"]
)


# ===========================================
# API : NEWS
# ===========================================

@app.route("/api/news")
def api_news():

    search = request.args.get("search", "").strip()

    data = process_news(search)

    return jsonify(data["results"])


# ===========================================
# API : DASHBOARD STATS
# ===========================================

@app.route("/api/stats")
def api_stats():

    data = process_news()

    return jsonify({

        "critical": data["critical"],

        "high": data["high"],

        "companies": data["companies"],

        "cves": data["cves"]

    })


# ===========================================
# API : THREAT DISTRIBUTION
# ===========================================

@app.route("/api/threats")
def api_threats():

    data = process_news()

    return jsonify({

        "labels": data["labels"],

        "values": data["values"]

    })


# ===========================================
# RUN APP
# ===========================================
@app.route("/download-report")
def download_report():

    data = process_news()

    filename = generate_pdf(

        data["results"],

        {

            "critical": data["critical"],

            "high": data["high"],

            "companies": data["companies"],

            "cves": data["cves"]

        }

    )

    return send_file(

        filename,

        as_attachment=True

    )

if __name__ == "__main__":

    app.run(debug=True)