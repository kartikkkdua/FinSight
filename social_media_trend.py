import tweepy
import pandas as pd
import matplotlib.pyplot as plt
from textblob import TextBlob
import re  # Regular expressions for symbol extraction

# Replace these with your own Twitter API credentials
consumer_key = "YOUR_CONSUMER_KEY"
consumer_secret = "YOUR_CONSUMER_SECRET"
access_token = "YOUR_ACCESS_TOKEN"
access_token_secret = "YOUR_ACCESS_TOKEN_SECRET"

# Authenticate to Twitter API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Define search query (broader for potential company mentions)
search_query = "#StockMarket #India OR $NSEI OR $SENSEX"  # Combine relevant hashtags and stock market indices

# Function to extract stock symbols from tweet text
def extract_symbols(text):
  # Use regular expressions to find stock symbols (e.g., NSE:RELIANCE, $INFY)
  matches = re.findall(r"\$([A-Z]+)|NSE:([A-Z]+)", text)
  return [match.group(1) or match.group(2) for match in matches]  # Extract symbol part

# Number of tweets to retrieve
num_tweets = 200

# Fetch tweets
tweets = []
for tweet in tweepy.Cursor(api.search, q=search_query, lang="en", count=num_tweets).items(num_tweets):
  tweets.append(tweet.text)

# Clean and pre-process tweets (optional)
# You can add steps for removing irrelevant characters, stop words, etc.

# Analyze sentiment and extract symbols
company_sentiment = {}  # Dictionary to store sentiment per company
for tweet in tweets:
  sentiment_analysis = TextBlob(tweet)
  sentiment = sentiment_analysis.sentiment.polarity
  symbols = extract_symbols(tweet.lower())  # Convert tweet to lowercase for symbol matching
  for symbol in symbols:
    if symbol not in company_sentiment:
      company_sentiment[symbol] = []
    company_sentiment[symbol].append(sentiment)

# Analyze sentiment per company (if symbols found)
if company_sentiment:
  company_average_sentiment = {}
  for symbol, sentiment_scores in company_sentiment.items():
    company_average_sentiment[symbol] = sum(sentiment_scores) / len(sentiment_scores)

  # Sort companies by average sentiment (optional)
  sorted_companies = dict(sorted(company_average_sentiment.items(), key=lambda item: item[1], reverse=True))

  # Visualization (example) - Top 5 companies by sentiment
  top_companies = dict(list(sorted_companies.items())[:5])  # Get top 5
  company_names = [get_company_name(symbol) for symbol in top_companies.keys()]  # Replace with function to get company name by symbol (using financial data API)
  sentiment_values = list(top_companies.values())
  plt.bar(company_names, sentiment_values)
  plt.xlabel("Company")
  plt.ylabel("Average Sentiment Score")
  plt.title("Average Sentiment of Top 5 Mentioned Companies (higher is better)")
  plt.xticks(rotation=45, ha="right")  # Rotate x-axis labels for better readability
  plt.tight_layout()
  plt.show()

  print(f"Analyzed {num_tweets} tweets and found sentiment for these companies:")
  for symbol, sentiment in sorted_companies.items():
    print(f"- {get_company_name(symbol)} (Symbol: {symbol}): Average Sentiment Score = {sentiment:.2f}")  # Replace with function to get company name by symbol

else:
  print(f"No company symbols found in the analyzed tweets.")

# Function to get company name by symbol (replace with your implementation)
def get_company_name(symbol):
  # Implement logic to fetch company name using a financial data API based on the symbol
  # This example function just returns the symbol for demonstration
  return symbol

print("**Note:** Implement the 'get_company_name' function to retrieve actual company names based on symbols.")