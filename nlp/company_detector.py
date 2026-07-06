import pandas as pd
import spacy

# Load spacy model
nlp = spacy.load("en_core_web_sm")

# Load latest news
df = pd.read_csv("data/news_data.csv")

print("\nDetecting Affected Companies\n")

for headline in df["headline"]:

    doc = nlp(headline)

    print("NEWS:", headline)

    found = False

    for entity in doc.ents:

        # ORG = organization/company
        if entity.label_ == "ORG":

            print("Affected Company:", entity.text)

            found = True

    if not found:

        print("No Company Detected")

    print("--------------------------------") 