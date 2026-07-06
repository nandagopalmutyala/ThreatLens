import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# -----------------------------
# Train model using training data
# -----------------------------
train_df = pd.read_csv("data/training_data.csv")

X_train = train_df["text"]
y_train = train_df["label"]

vectorizer = TfidfVectorizer()
X_train_vectorized = vectorizer.fit_transform(X_train)

model = MultinomialNB()
model.fit(X_train_vectorized, y_train)

print("Model trained successfully\n")

# -----------------------------
# Load real scraped news
# -----------------------------
news_df = pd.read_csv("data/news_data.csv")

print("Real Time Threat Predictions:\n")

# Predict each headline
for headline in news_df["headline"]:

    headline_vector = vectorizer.transform([headline])

    prediction = model.predict(headline_vector)

    print("NEWS:", headline)
    print("Predicted Threat Type:", prediction[0])
    print("----------------------------------")