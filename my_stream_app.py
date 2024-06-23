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

# Define the list of currency pairs to watch
currency_pairs = ["GBPUSD=X", "EURUSD=X", "USDJPY=X"]

# Add a selectbox for currency pair selection
selected_pair = st.selectbox("Select Currency Pair", currency_pairs)

# Refresh button
if st.button('Refresh Data', key='refresh_button'):
    st.experimental_rerun()

# Function to fetch data for a given currency pair
def get_currency_data(pair):
    ticker = yf.Ticker(pair)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=3)
    data = ticker.history(start=start_date, end=end_date, interval="5m")
    data['Return'] = data['Close'].pct_change().fillna(0)  # Calculate percentage change and fill NaN with 0
    data['Cumulative Return'] = (1 + data['Return']).cumprod() - 1  # Calculate cumulative return
    return data

# Function to update and display data for a given currency pair
def update_data(pair):
    data = get_currency_data(pair)
    current_price = data['Close'].iloc[-1]
    entry_price = 1.2500  # Replace with actual entry price or retrieve dynamically

    st.subheader(f"{pair} Data")
    st.metric("Current Price", f"{current_price:.4f}")

    # Plot price data
    fig_price = go.Figure()
    fig_price.add_trace(go.Candlestick(
        x=data.index,
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close'],
        name=pair
    ))
    fig_price.update_layout(title=f"{pair} Price Movement", xaxis_title="Time", yaxis_title="Price")
    st.plotly_chart(fig_price, use_container_width=True)

    # Plot return data with entry price line
    fig_return = go.Figure()
    fig_return.add_trace(go.Scatter(
        x=data.index,
        y=data['Cumulative Return'],
        mode='lines',
        name=f"{pair} Cumulative Returns"
    ))
    fig_return.add_shape(
        type="line",
        x0=data.index[0],
        y0=data['Cumulative Return'].iloc[0],
        x1=data.index[-1],
        y1=data['Cumulative Return'].iloc[-1],
        line=dict(
            color="black",
            width=1,
            dash="dashdot",
        ),
        name=f"Entry Price ({entry_price})"
    )
    fig_return.update_layout(title=f"{pair} Performance", xaxis_title="Time", yaxis_title="Cumulative Return")
    st.plotly_chart(fig_return, use_container_width=True)

    # Simulated open position data (replace this with actual data from your trading account)
    open_position = {
        "Symbol": pair,
        "Position": 10000,  # Assuming a long position of 10,000 units
        "Entry Price": entry_price,
        "Current Price": current_price,
        "Unrealized P&L": (current_price - entry_price) * 10000  # Update entry price accordingly
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

# Display data for the selected currency pair
update_data(selected_pair)




# Optional: Add auto-refresh using st.empty and time
# import time
# placeholder = st.empty()
# while True:
#     with placeholder.container():
#         update_data()
#     time.sleep(300)  # Refresh every 5 minutes


# In[1]:





# In[8]:




