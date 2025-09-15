# analysis.py
# Creates visualizations for tech company data.

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# 1. Function to plot stock price performance
def plot_stock_performance(stock_history, company_name):
    """Creates a line chart for the historical stock price."""
    fig = px.line(stock_history, 
                  x=stock_history.index, 
                  y='Close',
                  title=f"{company_name} - Stock Price (2019-2024)")
    fig.update_layout(yaxis_title="Price (USD)", showlegend=False)
    return fig

# 2. Function to plot revenue and income growth
def plot_financial_growth(financials_df, company_name):
    """Creates a line chart for Revenue and Net Income over time."""
    if financials_df.empty or 'Total Revenue' not in financials_df.columns:
        return None
        
    fig = go.Figure()
    
    # Add Revenue trace
    fig.add_trace(go.Scatter(
        x=financials_df.index, 
        y=financials_df['Total Revenue'] / 1e9, # Convert to billions
        mode='lines+markers',
        name='Total Revenue',
        line=dict(color='#1f77b4')
    ))
    
    # Add Net Income trace if available
    if 'Net Income' in financials_df.columns:
        fig.add_trace(go.Scatter(
            x=financials_df.index, 
            y=financials_df['Net Income'] / 1e9, # Convert to billions
            mode='lines+markers',
            name='Net Income',
            line=dict(color='#ff7f0e')
        ))
    
    fig.update_layout(
        title=f"{company_name} - Financial Performance (Billion USD)",
        xaxis_title="Fiscal Year",
        yaxis_title="Amount (USD Billion)",
        hovermode='x unified'
    )
    return fig

# 3. Function to create a comparison chart
def plot_metric_comparison(all_companies_data, metric_name):
    """Creates a bar chart comparing one metric for all tech firms."""
    data_for_chart = []
    
    for ticker, data_dict in all_companies_data.items():
        company_name = data_dict['info'].get('shortName', ticker)
        info = data_dict['info']
        
        # Get the metric from the info dictionary
        metric_value = None
        
        if metric_name == "Market Cap":
            metric_value = info.get('marketCap')
            format_as_billions = True
        elif metric_name == "P/E Ratio":
            metric_value = info.get('trailingPE')
            format_as_billions = False
        elif metric_name == "Profit Margin":
            metric_value = info.get('profitMargins')
            if metric_value is not None:
                metric_value = metric_value * 100  # Convert to percentage
            format_as_billions = False
        
        if metric_value is not None and not np.isnan(metric_value):
            data_for_chart.append({
                'Company': company_name,
                'Value': metric_value,
                'Metric': metric_name
            })
    
    if not data_for_chart:
        return None
        
    df = pd.DataFrame(data_for_chart)
    
    # Format the value
    if metric_name == "Market Cap":
        df['Value'] = df['Value'] / 1e9  # Convert to billions
        y_title = "Billions USD"
        title = f"Comparison: Market Capitalization (Billions USD)"
    elif metric_name == "P/E Ratio":
        y_title = "P/E Ratio"
        title = f"Comparison: P/E Ratio"
    else:  # Profit Margin
        y_title = "Percent (%)"
        title = f"Comparison: Profit Margin (%)"
    
    # Sort by value for better visualization
    df = df.sort_values('Value', ascending=False)
    
    fig = px.bar(df, x='Company', y='Value', 
                 title=title,
                 text_auto='.2s')
    fig.update_layout(xaxis_title="", yaxis_title=y_title,
                     xaxis_tickangle=-45)
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    return fig