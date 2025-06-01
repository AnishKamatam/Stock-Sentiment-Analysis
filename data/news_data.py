import os
import requests
import pandas as pd
import time
from dotenv import load_dotenv

load_dotenv()

APIFY_API_KEY = os.getenv('APIFY_API_KEY')
APIFY_ACTOR_ID = 'X81PxOydfbSEcYmNx'  # Fast News Scraper
APIFY_BASE_URL = 'https://api.apify.com/v2'


def fetch_apify_news(search_query='"Apple Inc" OR "AAPL stock"', max_items=100):
    # 1. Trigger the actor
    trigger_url = f'{APIFY_BASE_URL}/acts/{APIFY_ACTOR_ID}/runs'
    payload = {
        'searchQuery': search_query,
        'maxItems': max_items,
        'lang': 'en',
        'proxy': { 'useApifyProxy': True }
    }
    response = requests.post(trigger_url, json=payload, params={'token': APIFY_API_KEY})
    if not response.ok:
        print('Error triggering Apify actor:')
        print('Status code:', response.status_code)
        print('Response:', response.text)
        response.raise_for_status()
    run = response.json()
    run_id = run['data']['id']
    print(f"Triggered Apify actor, run id: {run_id}")

    # 2. Poll for run to finish
    status_url = f'{APIFY_BASE_URL}/actor-runs/{run_id}'
    while True:
        status_resp = requests.get(status_url, params={'token': APIFY_API_KEY})
        status_resp.raise_for_status()
        status = status_resp.json()['data']['status']
        print(f"Run status: {status}")
        if status in ['SUCCEEDED', 'FAILED', 'ABORTED', 'TIMED-OUT']:
            break
        time.sleep(5)
    if status != 'SUCCEEDED':
        raise RuntimeError(f"Apify run did not succeed: {status}")

    # 3. Get dataset items (results)
    dataset_id = status_resp.json()['data']['defaultDatasetId']
    dataset_url = f'{APIFY_BASE_URL}/datasets/{dataset_id}/items'
    items_resp = requests.get(dataset_url, params={'token': APIFY_API_KEY, 'format': 'json'})
    items_resp.raise_for_status()
    items = items_resp.json()

    # 4. Parse results into DataFrame
    records = []
    for item in items:
        records.append({
            'date': item.get('publishedAt', '')[:10],
            'headline': item.get('title', ''),
            'source': item.get('source', ''),
            'url': item.get('url', '')
        })
    df = pd.DataFrame(records)
    if not df.empty:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
    # 5. Save to CSV
    out_path = os.path.join(os.path.dirname(__file__), 'apify_news_headlines.csv')
    df.to_csv(out_path, index=False)
    print(f"Saved Apify news headlines to {out_path}")
    return df

if __name__ == '__main__':
    df = fetch_apify_news()
    print(df.head())
    print(f"Total headlines: {len(df)}") 