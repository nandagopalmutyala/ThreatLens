import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# Load training dataset
df = pd.read_csv("data/training_data.csv")

# Input text and labels
X = df["text"]
y = df["label"]

# Convert text to numbers
vectorizer = TfidfVectorizer()
X_vectorized = vectorizer.fit_transform(X)

# Train model
model = MultinomialNB()
model.fit(X_vectorized, y)

print("Model trained successfully")

# Test prediction
sample = ["hackers launched ransomware attack affecting systems"]

sample_vector = vectorizer.transform(sample)

prediction = model.predict(sample_vector)

print("Prediction:", prediction[0])