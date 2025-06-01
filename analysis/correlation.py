import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr, spearmanr

# Load stock data
stock_path = os.path.join(os.path.dirname(__file__), '../data/stock_data.py')
from importlib.util import spec_from_file_location, module_from_spec
spec = spec_from_file_location("stock_data", stock_path)
stock_data = module_from_spec(spec)
spec.loader.exec_module(stock_data)
stock_df = stock_data.fetch_aapl_stock_data()

# Load sentiment data
sentiment_path = os.path.join(os.path.dirname(__file__), '../data/apify_news_headlines_with_sentiment.csv')
sentiment_df = pd.read_csv(sentiment_path)
sentiment_df['date'] = pd.to_datetime(sentiment_df['date']).dt.date

# Aggregate daily average sentiment
daily_sentiment = sentiment_df.groupby('date')['sentiment'].mean().reset_index()

# Merge with stock data
stock_df['date'] = pd.to_datetime(stock_df['date']).dt.date
merged = pd.merge(stock_df, daily_sentiment, on='date', how='inner')

# Correlation analysis
pearson_corr, pearson_p = pearsonr(merged['sentiment'], merged['daily_return'])
spearman_corr, spearman_p = spearmanr(merged['sentiment'], merged['daily_return'])

print(f"Pearson correlation (sentiment vs daily return): {pearson_corr:.3f} (p={pearson_p:.3g})")
print(f"Spearman correlation (sentiment vs daily return): {spearman_corr:.3f} (p={spearman_p:.3g})")

# Plot: Stock price line graph (top) and daily average sentiment bar graph (bottom), sharing x-axis
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True, gridspec_kw={'height_ratios': [2, 1]})

# Top: AAPL Close Price line
ax1.plot(merged['date'], merged['close'], color='tab:blue', label='AAPL Close Price')
ax1.set_ylabel('AAPL Close Price', color='tab:blue')
ax1.set_title('AAPL Close Price and Daily Average News Sentiment')
ax1.legend(loc='upper left')

# Bottom: Daily average sentiment bar graph
ax2.bar(merged['date'], merged['sentiment'], color='tab:orange', label='Avg Sentiment')
ax2.set_ylabel('Avg Sentiment Score', color='tab:orange')
ax2.set_xlabel('Date')
ax2.legend(loc='upper left')

fig.autofmt_xdate()
fig.tight_layout()
plt.show() 