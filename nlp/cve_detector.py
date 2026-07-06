import re
import pandas as pd

# Load latest news
df = pd.read_csv("data/news_data.csv")

print("\nDetecting CVE IDs\n")

# CVE pattern
pattern = r"CVE-\d{4}-\d+"

for headline in df["headline"]:

    matches = re.findall(pattern, headline)

    print("NEWS:", headline)

    if matches:
        print("Detected CVE:", matches)

    else:
        print("No CVE Found")

    print("--------------------------------")