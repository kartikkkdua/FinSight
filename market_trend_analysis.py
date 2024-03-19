# Data Reteriving and pre processing
# Module 1
import talib

import yfinance as yf
import ta
#from ta.trend import rsi
import ta.momentum
# from pandas talib id

def download_indian_data(tickers, period):
    """Downloads historical stock price data for Indian companies.

    Args:
        tickers (list): List of NSE or BSE stock tickers of Indian companies.
        period (str, optional): Period for which to download data (e.g., "1y", "max"). Defaults to "1y".

    Returns:
        pandas.DataFrame: DataFrame containing historical stock price data
                          for the specified companies.

    Raises:
        ValueError: If no valid tickers are provided.
        yf.DownloadError: If there's an error downloading data from yfinance.
    """

    if not tickers:
        raise ValueError("Please provide a list of stock tickers.")

    # Option 1: Iterate
    # for ticker in tickers:
    #     if not ticker.endswith(".NS") and not ticker.endswith(".BO"):
    #         # Add ".NS" or ".BO" extension based on exchange

    # Option 2: List comprehension with check
    #tickers_with_exchange = [ticker + ".swith((".NS", ".BO")) else ticker for ticker in tickersf

    try:
        data = yf.download(tickers, period=period, auto_adjust=True)
    except (yf.DownloadError, ValueError) as e:
        print(f"Error downloading data: {e}")
        return None

    # Handle potential missing data
    data.dropna(axis=0, inplace=True)  # Drop rows with missing values (adjust as needed)
    return data

# Technical Analysis Function
import matplotlib.pyplot as plt

def calculate_sma(data, window):
    """Calculates Simple Moving Average (SMA) for closing prices."""
    data["SMA_" + str(window)] = data["Close"].rolling(window=window).mean()
    return data

def calculate_ema(data, window):
    """Calculates Exponential Moving Average (EMA) for closing prices."""
    data["EMA_" + str(window)] = data["Close"].ewm(span=window, min_periods=window).mean()
    return data

def plot_closing_prices(data, title="Closing Prices"):
    """Plots the historical closing prices for each company."""
    data["Close"].plot(figsize=(12, 6))
    plt.xlabel("Date")
    plt.ylabel("Closing Price")
    plt.title(title)
    plt.legend()
    plt.show()

def plot_indicators(data, window_sma=20, window_ema=50):
    """Plots closing prices, SMA, and EMA."""
    data = calculate_sma(data.copy(), window_sma)
    data = calculate_ema(data.copy(), window_ema)
    plot_closing_prices(data, title="Closing Prices, SMA, and EMA")

# Adanced Analysis

#1 Technical Indicators with ta :
# import ta

def calculate_rsi(data, window=14):
  """Calculates Relative Strength Index (RSI)."""
  data["RSI"] = ta.momentum.rsi(data.Close, window=window)
  return data

def calculate_macd(data, slow=26, fast=12, signal=9):
  """Calculates Moving Average Convergence Divergence (MACD)."""
  macd = talib.MACD(data.Close, fastperiod=fast, slowperiod=slow, signalperiod=signal)
  data["MACD"] = macd[0]  # Extract MACD line
  data["MACD_Signal"] = macd[1]  # Extract Signal line
  data["MACD_Hist"] = macd[2]  # Extract MACD Histogram
  return data

def calculate_bollinger_bands(data, window=20, std=2):
  """Calculates Bollinger Bands (Upper Band, Middle Band, Lower Band)."""
  bollinger = talib.BBANDS(data.Close, timeperiod=window, nbdevup=std, nbdevdn=std)
  data["BB_Upper"] = bollinger[0]
  data["BB_Middle"] = bollinger[1]
  data["BB_Lower"] = bollinger[2]
  return data

# 2 Fundamental Analysis

def get_fundamental_data(ticker):
  """Fetches basic fundamental data from yfinance (limited example)."""
  try:
    company_info = yf.download(ticker, period="1d", auto_adjust=True)["info"]
    return {
      "sector": company_info.get("sector"),
      "marketCap": company_info.get("marketCap"),
      "peRatio": company_info.get("peRatio"),
    }
  except Exception as e:
      print("Error downloading fundamental data")
  # except (ValueError) as e:
  #   print(f"Error downloading fundamental data for {ticker}: {e}")
  #   return None

# 3 Integrating ta  with Fundamental data
def analyze_company(ticker, period="1y", window_sma=20, window_ema=50):
  """Downloads data, calculates indicators, and retrieves basic fundamentals."""
  data = download_indian_data([ticker], period)
  if data is None:
    return None

  data = calculate_sma(data.copy(), window_sma)
  data = calculate_ema(data.copy(), window_ema)
  data = calculate_rsi(data.copy())
  data = calculate_macd(data.copy())
  data = calculate_bollinger_bands(data.copy())

  fundamentals = get_fundamental_data(ticker)

  return data, fundamentals  # Combine technical and fundamental data

# User interaction
import  streamlit as st
if __name__ == "__main__":
  st.title("Indian Stock Market Trend Analysis")

  # User Input Widgets (modify as needed)
  tickers = st.text_input("Enter comma separated stock tickers (e.g., INFY.NS, RELIANCE.NS)")
  period = st.selectbox("Select analysis period", ["1y", "2y", "5y", "max"])
  window_sma = st.number_input("SMA window size", min_value=1, value=20)
  window_ema = st.number_input("EMA window size", min_value=1, value=50)
  show_fundamentals = st.checkbox("Show fundamental data (optional)")
  # Analyze and Display Results
  if st.button("Analyze"):
    data, fundamentals = analyze_company(tickers, period, window_sma, window_ema)
    if data is not None:
      st.write("## Closing Prices")
      plot_closing_prices(data.copy())

      st.write("## Technical Indicators")
      plot_indicators(data.copy(), window_sma, window_ema)

      if show_fundamentals and fundamentals:
        st.write("## Fundamental Data")
        st.json(fundamentals)
    else:
      st.error("Error downloading data. Please check tickers and try again.")