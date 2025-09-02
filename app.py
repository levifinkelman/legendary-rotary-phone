import streamlit as st
import pandas as pd
import requests

# --- Fetch BTC price from CoinGecko ---
def fetch_btc_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    try:
        response = requests.get(url)
        data = response.json()
        return data["bitcoin"]["usd"]
    except Exception as e:
        st.error(f"Error fetching BTC price: {e}")
        return None

# --- Portfolio Metrics ---
def calculate_metrics(btc_price, btc_owned, cost_basis):
    current_value = btc_price * btc_owned
    profit_loss = current_value - cost_basis
    roi = (profit_loss / cost_basis) * 100 if cost_basis else 0
    return current_value, profit_loss, roi

# --- Streamlit UI ---
st.title("📊 Bitcoin Portfolio Dashboard")

btc_price = fetch_btc_price()
btc_owned = st.number_input("BTC Owned", value=0.5, step=0.01)
cost_basis = st.number_input("Total Cost Basis (USD)", value=10000)

if btc_price:
    st.metric("Live BTC Price (USD)", f"${btc_price:,.2f}")
    current_value, profit_loss, roi = calculate_metrics(btc_price, btc_owned, cost_basis)
    st.metric("Current Value", f"${current_value:,.2f}")
    st.metric("Profit / Loss", f"${profit_loss:,.2f}")
    st.metric("ROI", f"{roi:.2f}%")

# --- Notes Section ---
try:
    with open("notes.txt", "r") as f:
        notes = f.read()
        st.text_area("📝 Project Notes", value=notes, height=200)
except FileNotFoundError:
    st.warning("notes.txt not found. Add it to your repo to display notes.")
