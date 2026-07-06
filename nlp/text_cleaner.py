import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Load CSV file
df = pd.read_csv("data/news_data.csv")

# English stopwords
stop_words = set(stopwords.words("english"))

cleaned_news = []

for headline in df["headline"]:

    # Convert to lowercase
    headline = headline.lower()

    # Split into words
    words = word_tokenize(headline)

    # Remove unnecessary words
    filtered_words = []

    for word in words:
        if word.isalpha() and word not in stop_words:
            filtered_words.append(word)

    # Join back to sentence
    cleaned_text = " ".join(filtered_words)

    cleaned_news.append(cleaned_text)

# Add new column
df["cleaned_text"] = cleaned_news

# Save updated CSV
df.to_csv("data/cleaned_news.csv", index=False)

print(df)
print("\nCleaned data saved in data/cleaned_news.csv")