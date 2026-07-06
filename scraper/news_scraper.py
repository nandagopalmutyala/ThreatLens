import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime


def fetch_latest_news():

    url = "https://thehackernews.com"

    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")

    headlines = soup.find_all("h2")

    news_list = []

    for headline in headlines[:10]:

        text = headline.text.strip()

        news_list.append({
            "headline": text,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    df = pd.DataFrame(news_list)

    df.to_csv("data/news_data.csv", index=False)

    return df


if __name__ == "__main__":

    fetch_latest_news()

    print("Latest news fetched successfully")