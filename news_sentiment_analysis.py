import requests
from bs4 import BeautifulSoup  # Not used in this update, but kept for potential future use
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
import streamlit as st
from plotly.express import pie

# Download NLTK resources (sentiment lexicon) if not already installed
nltk.download('vader_lexicon')


def news_sentiment_analysis(company_name, api_key):
  """Analyzes news sentiment for a given Indian company using News API (preferred) or web scraping (fallback).

  Args:
      company_name (str): Name of the Indian company.


  Returns:
      pandas.DataFrame: DataFrame containing extracted news articles with sentiment scores, or None if no articles found.
  """

  # Try fetching data using News API (preferred)
  if api_key:
    url = f"https://newsapi.org/v2/everything?q={company_name}&sortBy=publishedAt&apiKey={api_key}"
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for non-200 status codes
    data = response.json()

    if data["status"] == "ok":
      articles = []
      for article in data["articles"]:
        articles.append({
          "title": article["title"],
          "description": article["description"]
        })
      return process_articles(articles)  # Process and analyze articles

  # Fallback to web scraping (with caution) if News API fails or no key is provided
  print("News API failed or no key provided. Falling back to web scraping (for educational purposes only).")
  articles = scrape_news_articles(company_name)  # Implement scrape_news_articles function responsibly
  if articles:
    return process_articles(articles)  # Process and analyze scraped articles
  else:
    print(f"No articles found for {company_name}.")
    st.info(f"No articles found for {company_name}. Try a different company name or consider obtaining a News API key.")
    return None


def process_articles(articles):
  """Processes and analyzes news articles.

  Args:
      articles (list): List of dictionaries containing news article information (title, description).

  Returns:
      pandas.DataFrame: DataFrame containing extracted news articles with sentiment scores.
  """

  sentiment_analyzer = SentimentIntensityAnalyzer()
  sentiment_scores = []

  for article in articles:
    title = article.get("title", "")
    description = article.get("description", "")
    content = title + " " + description  # Combine title and description for analysis

    # Preprocess text (optional, adjust as needed)
    # tokens = nltk.word_tokenize(content.lower())  # Tokenization
    # stopwords = nltk.corpus.stopwords.words('english')
    # filtered_tokens = [w for w in tokens if w not in stopwords]  # Stop word removal

    sentiment = sentiment_analyzer.polarity_scores(content)
    sentiment_scores.append({
      "title": title,
      "description": description,
      "compound": sentiment["compound"],
      "pos": sentiment["pos"],
      "neg": sentiment["neg"],
      "neu": sentiment["neu"]
    })

  df = pd.DataFrame(sentiment_scores)
  df["sentiment"] = df["compound"].apply(
    lambda score: "positive" if score > 0.05 else ("negative" if score < -0.05 else "neutral"))
  return df


# Function to scrape news articles from a website (replace with your implementation)
# Ensure responsible scraping practices (delays, respect robots.txt)
def scrape_news_articles(company_name):
  # Implement scraping logic here, returning a list of dictionaries containing title and description
  # Replace with your actual scraping code, considering website structure and responsible practices
  print("Scraping not implemented yet. Please replace with your scraping logic.")
  return []  # Placeholder, replace with actual scraped articles


# Streamlit App
st.title("News Sentiment Analysis for Indian Companies")

# Input field for company name
company_name = st.text_input("Enter Indian Company Name:")

# Input field for News API key (optional)
api_key = st.text_input("Enter News API Key")
# Button to trigger analysis