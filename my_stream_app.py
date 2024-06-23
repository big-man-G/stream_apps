#!/usr/bin/env python
# coding: utf-8

# In[3]:


# get_ipython().system('pip install streamlit')
# get_ipython().system('pip install yfinance')
# get_ipython().system('pip install plotly')


import sys
print(sys.version)

# get_ipython().system('pip install plotly')

import sys
print(sys.version)


# In[7]:

#!/usr/bin/env python
# coding: utf-8

import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Set page config
st.set_page_config(page_title="Trading Dashboard", layout="wide")

# Title
st.title("Trading Dashboard")

# Input for currency pairs
st.sidebar.header("Currency Pair Selection")
pair1 = st.sidebar.text_input("Enter first currency pair (e.g., GBPUSD=X)", "GBPUSD=X")
pair2 = st.sidebar.text_input("Enter second currency pair (e.g., EURUSD=X)", "EURUSD=X")
pair3 = st.sidebar.text_input("Enter third currency pair (e.g., USDJPY=X)", "USDJPY=X")

# Refresh button
if st.sidebar.button('Refresh Data', key='refresh_button'):
    st.experimental_rerun()

# Function to fetch data for a given currency pair
def get_currency_data(pair):
    ticker = yf.Ticker(pair)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=3)
    data = ticker.history(start=start_date, end=end_date, interval="5m")
    data['Return'] = data['Close'].pct_change().fillna(0)
    data['Cumulative Return'] = (1 + data['Return']).cumprod() - 1
    return data

# Function to create a price chart for multiple currency pairs
def create_price_chart(pairs_data):
    fig = go.Figure()
    for pair, data in pairs_data.items():
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data['Close'],
            mode='lines',
            name=pair
        ))
    fig.update_layout(title="Currency Pairs Price Movement", xaxis_title="Time", yaxis_title="Price")
    return fig

# Function to create a performance chart for multiple currency pairs
def create_performance_chart(pairs_data):
    fig = go.Figure()
    for pair, data in pairs_data.items():
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data['Cumulative Return'],
            mode='lines',
            name=f"{pair} Cumulative Returns"
        ))
    fig.update_layout(title="Currency Pairs Performance", xaxis_title="Time", yaxis_title="Cumulative Return")
    return fig

# Fetch data for all pairs
pairs = [pair1, pair2, pair3]
pairs_data = {pair: get_currency_data(pair) for pair in pairs}

# Create and display price chart
price_chart = create_price_chart(pairs_data)
st.plotly_chart(price_chart, use_container_width=True)

# Create and display performance chart
performance_chart = create_performance_chart(pairs_data)
st.plotly_chart(performance_chart, use_container_width=True)

# Display individual pair data
for pair in pairs:
    data = pairs_data[pair]
    current_price = data['Close'].iloc[-1]
    entry_price = 1.2500  # Replace with actual entry price or retrieve dynamically

    st.subheader(f"{pair} Data")
    st.metric("Current Price", f"{current_price:.4f}")

    # Simulated open position data
    open_position = {
        "Symbol": pair,
        "Position": 10000,
        "Entry Price": entry_price,
        "Current Price": current_price,
        "Unrealized P&L": (current_price - entry_price) * 10000
    }

    st.subheader("Open Position")
    position_df = pd.DataFrame([open_position])
    st.dataframe(position_df)

    daily_change = (current_price - data['Open'].iloc[0]) / data['Open'].iloc[0] * 100
    daily_high = data['High'].max()
    daily_low = data['Low'].min()

    col1, col2, col3 = st.columns(3)
    col1.metric("Daily Change", f"{daily_change:.2f}%")
    col2.metric("Daily High", f"{daily_high:.4f}")
    col3.metric("Daily Low", f"{daily_low:.4f}")

# Optional: Add auto-refresh using st.empty and time
# import time
# placeholder = st.empty()
# while True:
#     with placeholder.container():
#         update_data()
#     time.sleep(300)  # Refresh every 5 minutes


# In[1]:





# In[8]:




