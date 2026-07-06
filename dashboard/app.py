import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import spacy
import sys
import os

# Fix import path
sys.path.append(os.path.abspath("."))

# Import scraper function
from scraper.news_scraper import fetch_latest_news
from reports.pdf_report import generate_report

# Load spacy model
nlp = spacy.load("en_core_web_sm")

# -------------------------
# Title
# -------------------------

st.title("Cyber Threat Intelligence Dashboard")

# -------------------------
# AUTO FETCH LATEST NEWS
# -------------------------

st.write("Fetching latest cyber threat news...")

news_df = fetch_latest_news()

st.success("Latest news fetched successfully")

# -------------------------
# Train Models
# -------------------------

train_df = pd.read_csv("data/training_data.csv")

X_train = train_df["text"]
y_label = train_df["label"]
y_severity = train_df["severity"]

vectorizer = TfidfVectorizer()

X_vectorized = vectorizer.fit_transform(X_train)

# Threat model
threat_model = MultinomialNB()
threat_model.fit(X_vectorized, y_label)

# Severity model
severity_model = MultinomialNB()
severity_model.fit(X_vectorized, y_severity)

# -------------------------
# Search Box
# -------------------------

search_term = st.text_input("Search Company or Keyword")

if search_term:
    filtered_news = news_df[
        news_df["headline"].str.contains(search_term, case=False)
    ]
else:
    filtered_news = news_df

predicted_threats = []
report_data = []

st.header("Live Cyber Threat Analysis")

# -------------------------
# Prediction Section
# -------------------------

for headline in filtered_news["headline"]:

    # Predict threat
    vector = vectorizer.transform([headline])

    threat = threat_model.predict(vector)[0]

    severity = severity_model.predict(vector)[0]

    predicted_threats.append(threat)
    report_data.append({
        "headline": headline,
        "threat": threat,
        "severity": severity
    })

    # Detect company name using spacy
    doc = nlp(headline)

    company_name = "Not Detected"

    for entity in doc.ents:
        if entity.label_ == "ORG":
            company_name = entity.text
            break

    # Alert system
    if severity == "Critical":
        st.error("CRITICAL ALERT DETECTED - Immediate Attention Required")

    # Display results
    st.write("News:", headline)
    st.write("Affected Company:", company_name)
    st.write("Threat Type:", threat)
    st.write("Severity Level:", severity)
    st.write("----------------------------------")

# -------------------------
# Threat Distribution Chart
# -------------------------

st.header("Threat Distribution Chart")

if len(predicted_threats) > 0:

    chart_data = pd.DataFrame({
        "Threat Type": predicted_threats
    })

    count_data = chart_data["Threat Type"].value_counts().reset_index()

    count_data.columns = ["Threat Type", "Count"]

    fig = px.bar(
        count_data,
        x="Threat Type",
        y="Count",
        title="Detected Cyber Threats"
    )

    st.plotly_chart(fig)

else:
    st.write("No matching results found")

# -------------------------
# Timeline Graph
# -------------------------

st.header("Attack Timeline Analysis")

# Convert timestamp
news_df["timestamp"] = pd.to_datetime(news_df["timestamp"])

# Group by minute
timeline_data = news_df.groupby(
    news_df["timestamp"].dt.strftime("%H:%M")
).size().reset_index(name="Count")

# Line graph
fig2 = px.line(
    timeline_data,
    x="timestamp",
    y="Count",
    title="Cyber Attack Trend Over Time"
)

st.plotly_chart(fig2)


# -------------------------
# PDF Report Generation
# -------------------------

st.header("Security Report")

if st.button("Generate Security Report"):

    file_path = generate_report(report_data)

    st.success("PDF Report Generated Successfully")

    st.write("Saved at:", file_path)