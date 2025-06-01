import os
import requests
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')
BASE_URL = 'https://www.alphavantage.co/query'

def fetch_aapl_stock_data():
    params = {
        'function': 'TIME_SERIES_DAILY',
        'symbol': 'AAPL',
        'outputsize': 'compact',
        'apikey': ALPHA_VANTAGE_API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    data = response.json()
    time_series = data.get('Time Series (Daily)', {})
    
    if not time_series:
        print('Error: No time series data found. Full response:')
        print(data)
        return pd.DataFrame(columns=['date', 'close', 'daily_return'])
    
    # Parse and clean data
    records = []
    for date_str, daily_data in time_series.items():
        records.append({
            'date': date_str,
            'close': float(daily_data['4. close'])
        })
    df = pd.DataFrame(records)
    if 'date' not in df.columns:
        print('Error: "date" column missing after parsing records. Records:')
        print(records)
        return pd.DataFrame(columns=['date', 'close', 'daily_return'])
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')
    
    # Filter last 30 days
    last_30 = df.tail(30).copy()
    last_30['daily_return'] = last_30['close'].pct_change() * 100  # percent return
    last_30 = last_30.reset_index(drop=True)
    return last_30[['date', 'close', 'daily_return']]

if __name__ == '__main__':
    df = fetch_aapl_stock_data()
    print(df) 