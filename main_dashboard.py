# main_dashboard.py
# Tech Giants Financial Analysis Dashboard.

import streamlit as st
from data_loader import TECH_LIST, get_company_data, get_all_company_data
from analysis import plot_stock_performance, plot_financial_growth, plot_metric_comparison
import pandas as pd

# ----------------------------
# APP SETUP
# ----------------------------
st.set_page_config(page_title="Tech Giants Analysis", page_icon="💻", layout="wide")
st.title("💻 Global Tech Giants Financial Analysis (2019-2024)")
st.markdown("Analyzing and comparing the world's largest technology companies.")

# ----------------------------
# SIDEBAR - USER CONTROLS
# ----------------------------
st.sidebar.header("Controls")
selected_ticker = st.sidebar.selectbox(
    "Select a Company to Analyze:",
    options=list(TECH_LIST.keys()),
    format_func=lambda x: f"{x} - {TECH_LIST[x]['name']}"
)

# ----------------------------
# FETCH DATA
# ----------------------------
if 'all_data' not in st.session_state:
    with st.spinner('Downloading data for all companies... This may take a minute.'):
        st.session_state.all_data = get_all_company_data()

# Check if we have any data at all
if not st.session_state.all_data:
    st.error("Could not load data for any companies. Please check your internet connection and try again.")
    st.stop()

# Get data for the selected company
company_data = st.session_state.all_data.get(selected_ticker)
if not company_data:
    st.error(f"Could not load data for {selected_ticker}. Please select another company.")
    st.stop()

company_name = TECH_LIST[selected_ticker]['name']
info = company_data['info']
stock_history = company_data['stock_history']
financials = company_data['financials']

# ----------------------------
# MAIN DASHBOARD LAYOUT - TABS
# ----------------------------
tab1, tab2 = st.tabs(["🏢 Company Analysis", "📊 Peer Comparison"])

with tab1:
    st.header(f"Analysis for {company_name}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Display key metrics
        st.subheader("Key Metrics")
        current_price = info.get('currentPrice', 'N/A')
        market_cap = info.get('marketCap', 'N/A')
        pe_ratio = info.get('trailingPE', 'N/A')
        profit_margin = info.get('profitMargins', 'N/A')
        
        st.metric("Current Price", f"${current_price:.2f}" if isinstance(current_price, float) else current_price)
        st.metric("Market Cap", f"${market_cap:,.2f}" if isinstance(market_cap, (int, float)) else market_cap)
        st.metric("P/E Ratio", f"{pe_ratio:.2f}" if isinstance(pe_ratio, (int, float)) else pe_ratio)
        if isinstance(profit_margin, (int, float)):
            st.metric("Profit Margin", f"{profit_margin * 100:.2f}%")
        else:
            st.metric("Profit Margin", profit_margin)
        st.metric("Sector", TECH_LIST[selected_ticker]['sector'])
    
    with col2:
        # Stock Performance Chart
        st.plotly_chart(plot_stock_performance(stock_history, company_name), use_container_width=True)
    
    # Financial Growth Chart (if data is available)
    financial_chart = plot_financial_growth(financials, company_name)
    if financial_chart:
        st.plotly_chart(financial_chart, use_container_width=True)
    else:
        st.info("Detailed financial statement data not available for this view.")

with tab2:
    st.header("Peer Comparison")
    
    metric_choice = st.selectbox("Select Metric to Compare:", 
                                ["Market Cap", "P/E Ratio", "Profit Margin"])
    
    comparison_fig = plot_metric_comparison(st.session_state.all_data, metric_choice)
    if comparison_fig:
        st.plotly_chart(comparison_fig, use_container_width=True)
    else:
        st.warning("Not enough data available for this comparison.")

# ----------------------------
# FOOTER
# ----------------------------
st.sidebar.markdown("---")
st.sidebar.caption("Data sourced from Yahoo Finance. For educational purposes.")
st.sidebar.write(f"Companies loaded: {len(st.session_state.all_data)}/{len(TECH_LIST)}")