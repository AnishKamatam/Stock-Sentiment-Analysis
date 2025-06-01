import os
import requests
import pandas as pd
from dotenv import load_dotenv
import csv
from io import StringIO

load_dotenv()

PERPLEXITY_API_KEY = os.getenv('PERPLEXITY_API_KEY')


def fetch_perplexity_news():
    url = "https://api.perplexity.ai/chat/completions"
    headers = {
        "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
        "Content-Type": "application/json"
    }
    prompt = (
        "Return an exhaustive, comprehensive list of at least 50 unique news headlines, stories, and press releases (with dates and sources) about Apple Inc., AAPL, or any of its products (such as iPhone, MacBook, iPad, Apple Watch, iOS, App Store, etc.) from the last 30 days. Focus on key headlines and events that could affect the company as a whole. Do not include irrelevant headlines that do not provide value to the company and include any headlines related to Apple or headlines that could directly affect apple including Tim Cook or executives actions that could largely affect the brand image of Apple. Include headlines that are most likely to directly affect stock price or stock volatility. Do not let one source dominate the list. Include a mix of sources. Get the whole picture of political and economical events that directly impacts on Apple. Focus on US news sources. Get atleast one headline for each day in the last 30 days."
        "Include both positive and negative headlines, especially those discussing political and economic impacts on Apple, such as tariffs, regulations, lawsuits, supply chain issues, government actions, and global market changes. "
        "Include results from all types of sources: mainstream media, financial news, technology sites, blogs, international outlets, and press releases. "
        "Be sure to include headlines from official news outlets such as The New York Times, CNN, Reuters, Bloomberg, The Wall Street Journal, and similar. "
        "Be as thorough as possible to provide a complete overview. Format the output as a CSV with columns: date, headline, source."
    )
    data = {
        "model": "sonar-pro",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 2048,
        "temperature": 0.2
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    text = response.json()['choices'][0]['message']['content']
    # Pre-clean: keep only lines with 3 columns, skip header, remove duplicates
    lines = text.strip().split('\n')
    header = lines[0]
    clean_lines = [header]
    seen = set()
    for line in lines[1:]:
        try:
            row = next(csv.reader([line]))
            if len(row) == 3:
                row_tuple = tuple(row)
                if row_tuple not in seen:
                    clean_lines.append(line)
                    seen.add(row_tuple)
        except Exception:
            continue
    clean_csv = '\n'.join(clean_lines)
    print("Cleaned Perplexity CSV output:")
    print(clean_csv)
    try:
        df = pd.read_csv(StringIO(clean_csv))
    except Exception as e:
        print("Error reading cleaned CSV:", e)
        return None
    out_path = os.path.join(os.path.dirname(__file__), 'apify_news_headlines.csv')
    df.to_csv(out_path, index=False)
    print(f"Saved Perplexity Apple news headlines to {out_path}")
    return df

if __name__ == '__main__':
    df = fetch_perplexity_news()
    if df is not None:
        print(df.head())
        print(f"Total headlines: {len(df)}")
