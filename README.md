# Apple News Sentiment & Stock Price Analysis

This project analyzes the relationship between news sentiment and Apple (AAPL) stock price movements over the past 30 days, using only API-based data and no machine learning models.

## Pipeline Overview

1. **Fetch AAPL Stock Data**
   - Uses Alpha Vantage API to get the last 30 days of daily closing prices and returns for Apple Inc. (AAPL).

2. **Fetch Apple News Headlines**
   - Uses the Perplexity API to retrieve a comprehensive set of news headlines about Apple Inc., AAPL, and its products from the last 30 days, including both positive and negative headlines and a wide range of sources.

3. **Sentiment Analysis**
   - Uses OpenAI GPT-4.1 to assign a sentiment score (-1.0 to +1.0) to each headline.
   - Aggregates daily average sentiment scores.

4. **Analysis & Visualization**
   - Merges daily sentiment with stock price data.
   - Computes Pearson and Spearman correlation coefficients between sentiment and daily returns.
   - Visualizes stock price and sentiment trends day by day.

## Setup

1. **Clone the repository**
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure API keys**
   - Copy `.env.example` to `.env` and fill in your API keys for Alpha Vantage, Perplexity, OpenAI, etc.

4. **Run the pipeline**
   - Fetch news headlines:
     ```bash
     python data/news_data.py
     ```
   - Run sentiment analysis:
     ```bash
     python nlp/sentiment_analysis.py
     ```
   - Analyze and visualize:
     ```bash
     python analysis/correlation.py
     ```

## Results & Limitations

- The pipeline successfully fetches, analyzes, and visualizes the relationship between Apple news sentiment and AAPL stock price.
- **However, the observed correlation between daily news sentiment and daily stock returns was not strong or statistically significant in this analysis.**
- This may be due to the complexity of market dynamics, the limitations of headline-level sentiment, or the relatively short time window.

## Notes
- All API keys are loaded from `.env` (never hardcoded).
- The project is backend-only and does not use machine learning models for prediction.
- You can tune the Perplexity prompt or sentiment model for further experimentation.

---

**Author:** [Your Name] 