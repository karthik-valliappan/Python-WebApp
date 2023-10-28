import streamlit as st
import pandas as pd
import altair as alt
import requests

# Page layout
st.set_page_config(page_title="Analytics", page_icon="🌎", layout="wide")

# Streamlit theme
theme_plotly = None

# Title
st.title("⏱ TRADE ANALYTICS DASHBOARD")

# API URL - User input
api_url = st.text_input("Enter the API URL:", "")

# Make an API request and check for success
response = requests.get(api_url)

if response.status_code == 200:
    data = response.json()

    # Convert the JSON data to a Pandas DataFrame
    df = pd.DataFrame(data, columns=[
        "Date", "Day", "Entry Time", "Exit Time", "Ticker Symbol", "Long/Short", "Entry Price",
        "Exit Price", "Number of Shares/Contracts", "Stop-Loss Price", "Take-Profit Price",
        "Commission Paid", "Trade Duration (minutes)", "Profit/Loss", "Trade Outcome", "Strategy Used"
    ])

    # Rest of the analytics dashboard content
    # Load CSS Style
    with open('style.css') as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # Sidebar filters
    st.sidebar.header("Please filter")
    ticker_symbols = st.sidebar.multiselect(
        "Select Ticker Symbols",
        options=df["Ticker Symbol"].unique(),
        default=df["Ticker Symbol"].unique(),
    )
    strategy_used = st.sidebar.multiselect(
        "Select Strategy Used",
        options=df["Strategy Used"].unique(),
        default=df["Strategy Used"].unique(),
    )

    df_selection = df[df["Ticker Symbol"].isin(ticker_symbols) & df["Strategy Used"].isin(strategy_used)]

    # Metrics
    st.subheader('Key Performance')

    total_profit = df_selection[df_selection["Profit/Loss"] > 0]["Profit/Loss"].sum()
    total_loss = df_selection[df_selection["Profit/Loss"] < 0]["Profit/Loss"].sum()
    win_loss_ratio = abs(total_profit / total_loss) if total_loss != 0 else "Infinity"
    profit_factor = total_profit / abs(total_loss) if total_loss != 0 else "Infinity"

    col1, col2, col3, col4 = st.columns(4)
    col1.metric(label="Total Profit", value=f"{total_profit:,.2f}", delta="Total profit earned")
    col2.metric(label="Total Loss", value=f"{total_loss:,.2f}", delta="Total loss incurred")
    col3.metric(label="Win/Loss Ratio", value=win_loss_ratio, delta="Ratio of total profit to total loss")
    col4.metric(label="Profit Factor", value=profit_factor, delta="Profit factor calculation")

    # Styling
    st.markdown("""<style>.stProgress > div > div > div > div { background-image: linear-gradient(to right, #99ff99 , #FFFF00)}</style>""", unsafe_allow_html=True)

    # Bar Chart - Ticker Symbol / Profit-Loss
    st.subheader("Ticker Symbol vs. Profit-Loss")
    source = df_selection[["Ticker Symbol", "Profit/Loss"]]
    source = source.rename(columns={"Profit/Loss": "ProfitLoss"})
    bar_chart = alt.Chart(source).mark_bar().encode(
        x=alt.X("sum(ProfitLoss):Q", title="Total Profit/Loss (USD)"),
        y=alt.Y("Ticker Symbol:N", sort="-x", title="Ticker Symbol"),
    )
    st.altair_chart(bar_chart, use_container_width=True, theme=theme_plotly)

else:
    st.error("Failed to fetch data from the API. Please check the API URL.")

# Run the Streamlit app