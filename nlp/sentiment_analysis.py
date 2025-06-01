import os
import pandas as pd
import openai
import time
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
openai.api_key = OPENAI_API_KEY

INPUT_CSV = os.path.join(os.path.dirname(__file__), '../data/apify_news_headlines.csv')
OUTPUT_CSV = os.path.join(os.path.dirname(__file__), '../data/apify_news_headlines_with_sentiment.csv')

MODEL = 'gpt-4.1'  # GPT-4.1

SYSTEM_PROMPT = (
    "You are a financial news sentiment analysis assistant. "
    "Given a news headline, return a single sentiment score from -1.0 (very negative) to +1.0 (very positive). "
    "Be as objective as possible. Only output the score as a number."
)


def analyze_sentiment(headline):
    for attempt in range(3):
        try:
            response = openai.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": headline}
                ],
                max_tokens=4,
                temperature=0.0,
            )
            score_str = response.choices[0].message.content.strip()
            score = float(score_str)
            return score
        except Exception as e:
            print(f"Error analyzing: {headline[:60]}... | {e}")
            time.sleep(2)
    return None


def main():
    df = pd.read_csv(INPUT_CSV)
    if 'sentiment' in df.columns:
        print('Sentiment column already exists. Skipping analysis.')
        return
    sentiments = []
    for i, row in df.iterrows():
        headline = row['headline']
        score = analyze_sentiment(headline)
        sentiments.append(score)
        print(f"{i+1}/{len(df)} | {score} | {headline}")
        # Optional: Save progress every 10 headlines
        if (i+1) % 10 == 0:
            df.loc[:i, 'sentiment'] = sentiments
            df.to_csv(OUTPUT_CSV, index=False)
    df['sentiment'] = sentiments
    df.to_csv(OUTPUT_CSV, index=False)
    print(f"Saved with sentiment to {OUTPUT_CSV}")

if __name__ == '__main__':
    main() 