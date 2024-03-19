import streamlit as st
import requests
from bs4 import BeautifulSoup

def get_financial_news(target_url):
  """Fetches and parses financial news from a given URL.

  Args:
      target_url (str): The URL of the financial news website.

  Returns:
      list: A list of dictionaries containing extracted news data (headline, summary, link).
  """
  try:
    response = requests.get(target_url)
    response.raise_for_status()  # Raise exception for unsuccessful requests
    soup = BeautifulSoup(response.content, "html.parser")
    return extract_news_data(soup)
  except requests.exceptions.RequestException as e:
    st.error(f"Error: An error occurred while fetching the website: {e}")
    return []

def extract_news_data(soup):
  """Extracts news data from the parsed HTML content.

  Args:
      soup (BeautifulSoup): The parsed HTML content.

  Returns:
      list: A list of dictionaries containing extracted news data.
  """
  # Replace with actual selectors based on the target website's structure
  article_container = "div.article-item"  # Placeholder, adjust as needed
  news_data = []
  for article in soup.find_all(article_container):
    try:
      headline = article.find("h3").text.strip()  # Adjust tag for headline
      summary = article.find("p").text.strip()  # Adjust tag for summary
      link = article.find("a", href=True)["href"]
      news_data.append({"headline": headline, "summary": summary, "link": link})
    except AttributeError:
      # Handle cases where elements might not be found
      pass
  return news_data

def display_news(news_data):
  """Displays extracted news data in a user-friendly format within Streamlit.

  Args:
      news_data (list): A list of dictionaries containing news data.
  """
  if not news_data:
    st.info("No news found.")
    return
  for item in news_data:
    st.subheader(item['headline'])
    st.write(item['summary'])
    st.write(f"[Full Article]({item['link']})")  # Link with markdown

if __name__ == "__main__":
  # Streamlit app layout and functionality
  st.title("Financial News Scraper")
  target_url = st.text_input("Enter the URL of the financial news website:")

  if target_url:
    # Display 'Loading...' message while fetching data
    with st.spinner("Fetching news..."):
      news_data = get_financial_news(target_url)
    display_news(news_data)
