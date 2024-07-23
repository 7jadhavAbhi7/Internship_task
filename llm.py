import os
from constant import openai_key
from langchain_openai import OpenAI

import streamlit as st
import yfinance as yf

# Set the OpenAI API key
os.environ["OPENAI_API_KEY"] = openai_key

# Streamlit app setup
st.title('Langchain and Finance Demo')

# Sample list of tickers (you can expand this list as needed)
tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']

# Dropdown menu for selecting a ticker
selected_ticker = st.selectbox('Select a stock ticker', tickers)

llm = OpenAI(temperature=0.8)

def fetch_stock_data(symbol):
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        return {
            "name": info.get("longName", "N/A"),
            "sector": info.get("sector", "N/A"),
            "price": info.get("regularMarketPrice", "N/A"),
            "previousClose": info.get("regularMarketPreviousClose", "N/A"),
            "marketCap": info.get("marketCap", "N/A")
        }
    except Exception as e:
        return {"error": str(e)}

if selected_ticker:
    stock_data = fetch_stock_data(selected_ticker)
    st.write(stock_data)