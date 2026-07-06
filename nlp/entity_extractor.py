import pandas as pd
import spacy

# Load English model
nlp = spacy.load("en_core_web_sm")

# Load cleaned CSV
df = pd.read_csv("data/cleaned_news.csv")

print("\nDetected Entities:\n")

# Check each cleaned headline
for text in df["cleaned_text"]:

    doc = nlp(text)

    print("TEXT:", text)

    for entity in doc.ents:
        print(entity.text, " --> ", entity.label_)

    print("---------------------------")