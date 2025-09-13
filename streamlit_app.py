"""
Gold SIP Calculator - Streamlit Dashboard
Interactive dashboard for calculating and visualizing Gold SIP returns
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime
import sys
import os

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from gold_sip_calculator import GoldSIPCalculator, GoldPriceAPI

# Page configuration
st.set_page_config(
    page_title="Gold SIP Calculator Dashboard",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize calculator
@st.cache_resource
def get_calculator():
    return GoldSIPCalculator()

calculator = get_calculator()

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #FFD700, #FFA500);
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #FFD700;
    }
    .result-positive {
        color: #28a745;
    }
    .result-negative {
        color: #dc3545;
    }
    .sidebar-info {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e9ecef;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🏆 Gold SIP Calculator Dashboard</h1>
    <p>Calculate and visualize your Gold SIP investment returns</p>
</div>
""", unsafe_allow_html=True)

# Sidebar inputs
st.sidebar.markdown("## 📊 Investment Parameters")

# Input fields
monthly_amount = st.sidebar.number_input(
    "💰 Monthly SIP Amount (₹)",
    min_value=100,
    max_value=1000000,
    value=10000,
    step=500,
    help="Amount to invest every month in Gold SIP"
)

duration_months = st.sidebar.number_input(
    "📅 Investment Duration (Months)",
    min_value=1,
    max_value=360,
    value=24,
    step=1,
    help="How many months you want to invest"
)

st.sidebar.markdown("---")

# Gold price inputs
st.sidebar.markdown("### 💎 Gold Price Details")

# Fetch current gold price
current_live_price = calculator.get_live_gold_price()

col1, col2 = st.sidebar.columns(2)
with col1:
    if st.button("🔄 Refresh Price"):
        current_live_price = calculator.get_live_gold_price()
        st.rerun()

with col2:
    st.markdown(f"**Live Price:** ₹{current_live_price:.0f}")

average_gold_price = st.sidebar.number_input(
    "📊 Average Gold Price (₹/gram)",
    min_value=1000,
    max_value=20000,
    value=8000,  # Realistic average for 12.5% CAGR
    step=50,
    help="Average gold price during your investment period (use lower values for historical scenarios)"
)

current_gold_price = st.sidebar.number_input(
    "💎 Current Gold Price (₹/gram)",
    min_value=1000,
    max_value=20000,
    value=int(current_live_price),
    step=50,
    help="Current market price of gold"
)

# Advanced options
st.sidebar.markdown("---")
show_advanced = st.sidebar.expander("🔧 Advanced Options")

with show_advanced:
    start_date = st.date_input(
        "Start Date",
        value=datetime.date.today() - datetime.timedelta(days=duration_months*30),
        help="When did you start your SIP"
    )
    
    show_monthly_breakdown = st.checkbox("Show Monthly Breakdown", value=True)
    show_price_projection = st.checkbox("Show Price Projection", value=False)

# Information panel
st.sidebar.markdown("---")
st.sidebar.markdown("""
<div class="sidebar-info">
    <h4>💡 Quick Tips</h4>
    <ul>
        <li>Gold SIP is great for long-term wealth creation</li>
        <li>Gold delivered ~12.5% CAGR over last 10 years</li>
        <li>Use lower average prices for historical scenarios</li>
        <li>Recent SIP: ₹9,000 avg | Long-term: ₹6,000 avg</li>
    </ul>
    
    <h4>📈 Historical Context</h4>
    <ul>
        <li>2015: ₹2,600/gram | 2025: ₹10,500/gram</li>
        <li>10-year CAGR: ~12.5% per annum</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# Calculate results
if st.sidebar.button("🚀 Calculate Returns", type="primary", use_container_width=True):
    # Perform calculations
    results = calculator.calculate_sip_returns(
        monthly_amount=monthly_amount,
        duration_months=duration_months,
        average_gold_price=average_gold_price,
        current_gold_price=current_gold_price,
        start_date=start_date
    )
    
    # Store in session state
    st.session_state.results = results
    st.session_state.show_results = True

# Display results if available
if hasattr(st.session_state, 'show_results') and st.session_state.show_results:
    results = st.session_state.results
    
    # Key metrics
    st.markdown("## 📈 Investment Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="💰 Total Invested",
            value=f"₹{results['total_investment']:,.0f}",
            help="Total amount invested over the period"
        )
    
    with col2:
        st.metric(
            label="⚖️ Gold Purchased",
            value=f"{results['total_grams']:.2f}g",
            help="Total grams of gold purchased"
        )
    
    with col3:
        st.metric(
            label="💎 Current Value",
            value=f"₹{results['current_value']:,.0f}",
            delta=f"₹{results['profit_loss']:,.0f}",
            help="Current market value of your gold"
        )
    
    with col4:
        st.metric(
            label="📊 Returns (CAGR)",
            value=f"{results['cagr']:.1f}%",
            delta=f"{results['profit_loss_percentage']:.1f}%",
            help="Compound Annual Growth Rate"
        )
    
    # Profit/Loss indicator
    if results['profit_loss'] > 0:
        st.success(f"🎉 Congratulations! Your investment is in profit by ₹{results['profit_loss']:,.0f} ({results['profit_loss_percentage']:.2f}%)")
    else:
        st.warning(f"📉 Your investment is currently at a loss of ₹{abs(results['profit_loss']):,.0f} ({abs(results['profit_loss_percentage']):.2f}%). Gold is a long-term investment!")
    
    st.markdown("---")
    
    # Charts section
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        st.markdown("### 📊 Investment Breakdown")
        
        # Pie chart for investment vs current value
        fig_pie = go.Figure(data=[
            go.Pie(
                labels=['Total Invested', 'Profit/Loss'],
                values=[results['total_investment'], abs(results['profit_loss'])],
                hole=0.4,
                colors=['#FFD700', '#32CD32' if results['profit_loss'] > 0 else '#FF6B6B']
            )
        ])
        fig_pie.update_layout(
            title="Investment vs Returns",
            height=400,
            showlegend=True
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with chart_col2:
        st.markdown("### 💰 Value Comparison")
        
        # Bar chart comparing invested vs current value
        comparison_data = {
            'Category': ['Amount Invested', 'Current Value'],
            'Value': [results['total_investment'], results['current_value']],
            'Color': ['#FFA500', '#32CD32' if results['current_value'] > results['total_investment'] else '#FF6B6B']
        }
        
        fig_bar = px.bar(
            comparison_data,
            x='Category',
            y='Value',
            color='Color',
            color_discrete_map="identity",
            text='Value'
        )
        fig_bar.update_traces(texttemplate='₹%{text:,.0f}', textposition='outside')
        fig_bar.update_layout(
            title="Invested vs Current Value",
            height=400,
            showlegend=False,
            yaxis_title="Amount (₹)"
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # Monthly breakdown
    if show_monthly_breakdown:
        st.markdown("---")
        st.markdown("### 📅 Monthly Investment Breakdown")
        
        breakdown = calculator.calculate_monthly_breakdown(
            monthly_amount=monthly_amount,
            duration_months=min(duration_months, 60),  # Limit for performance
            start_date=start_date
        )
        
        # Convert to DataFrame
        df_breakdown = pd.DataFrame(breakdown)
        df_breakdown['Date'] = pd.to_datetime(df_breakdown['date'])
        df_breakdown['Cumulative Value'] = df_breakdown['cumulative_grams'] * current_gold_price
        
        # Create subplot with secondary y-axis
        fig_monthly = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Monthly Gold Purchase', 'Cumulative Investment Value'),
            vertical_spacing=0.12
        )
        
        # Monthly purchase chart
        fig_monthly.add_trace(
            go.Bar(
                x=df_breakdown['Date'],
                y=df_breakdown['grams_bought'],
                name='Gold Purchased (g)',
                marker_color='#FFD700'
            ),
            row=1, col=1
        )
        
        # Cumulative value chart
        fig_monthly.add_trace(
            go.Scatter(
                x=df_breakdown['Date'],
                y=df_breakdown['Cumulative Value'],
                mode='lines+markers',
                name='Portfolio Value',
                line=dict(color='#32CD32', width=3),
                marker=dict(size=6)
            ),
            row=2, col=1
        )
        
        fig_monthly.add_trace(
            go.Scatter(
                x=df_breakdown['Date'],
                y=df_breakdown['cumulative_investment'],
                mode='lines+markers',
                name='Amount Invested',
                line=dict(color='#FFA500', width=2),
                marker=dict(size=4)
            ),
            row=2, col=1
        )
        
        fig_monthly.update_layout(
            height=700,
            title="Monthly SIP Performance Analysis",
            showlegend=True
        )
        
        fig_monthly.update_xaxes(title_text="Date", row=2, col=1)
        fig_monthly.update_yaxes(title_text="Grams", row=1, col=1)
        fig_monthly.update_yaxes(title_text="Value (₹)", row=2, col=1)
        
        st.plotly_chart(fig_monthly, use_container_width=True)
        
        # Monthly data table
        with st.expander("📋 View Monthly Data Table"):
            display_df = df_breakdown[['month', 'Date', 'investment_amount', 'gold_price', 
                                     'grams_bought', 'cumulative_grams', 'cumulative_investment']].copy()
            display_df.columns = ['Month', 'Date', 'Investment (₹)', 'Gold Price (₹/g)', 
                                'Gold Bought (g)', 'Total Gold (g)', 'Total Invested (₹)']
            
            # Format the dataframe
            display_df['Investment (₹)'] = display_df['Investment (₹)'].apply(lambda x: f"₹{x:,.0f}")
            display_df['Gold Price (₹/g)'] = display_df['Gold Price (₹/g)'].apply(lambda x: f"₹{x:,.0f}")
            display_df['Gold Bought (g)'] = display_df['Gold Bought (g)'].apply(lambda x: f"{x:.3f}g")
            display_df['Total Gold (g)'] = display_df['Total Gold (g)'].apply(lambda x: f"{x:.3f}g")
            display_df['Total Invested (₹)'] = display_df['Total Invested (₹)'].apply(lambda x: f"₹{x:,.0f}")
            display_df['Date'] = display_df['Date'].dt.strftime('%Y-%m-%d')
            
            st.dataframe(display_df, use_container_width=True, hide_index=True)

# Investment advice and tips
st.markdown("---")
st.markdown("## 💡 Gold Investment Tips & Advice")

tip_col1, tip_col2, tip_col3 = st.columns(3)

with tip_col1:
    st.markdown("""
    #### ✅ Best Practices
    - **Consistency is Key**: Invest the same amount monthly regardless of gold prices
    - **Long-term Focus**: Gold SIP works best for 3+ years investment horizon
    - **Diversification**: Keep gold allocation to 5-15% of your portfolio
    - **Digital Gold**: Consider digital gold for lower costs and easy liquidity
    """)

with tip_col2:
    st.markdown("""
    #### ⚠️ Important Points
    - **No Income**: Gold doesn't provide dividends or interest
    - **Volatility**: Short-term price fluctuations are normal
    - **Costs**: Physical gold has making charges and GST
    - **Storage**: Digital gold eliminates storage concerns
    """)

with tip_col3:
    st.markdown("""
    #### 📈 When to Invest
    - **Market Uncertainty**: Gold acts as a hedge during volatile times
    - **Inflation**: Historically performs well during high inflation
    - **Portfolio Balance**: As part of a diversified investment strategy
    - **Goal-based**: For long-term goals like weddings, retirement
    """)

# Price analysis section
st.markdown("---")
st.markdown("## 📊 Gold Price Analysis")

price_col1, price_col2 = st.columns(2)

with price_col1:
    st.markdown("### 📈 Price Sensitivity Analysis")
    
    # Calculate returns for different current prices
    price_scenarios = []
    base_current_price = current_gold_price
    
    for price_change in [-20, -15, -10, -5, 0, 5, 10, 15, 20]:
        scenario_price = base_current_price * (1 + price_change/100)
        scenario_results = calculator.calculate_sip_returns(
            monthly_amount=monthly_amount,
            duration_months=duration_months,
            average_gold_price=average_gold_price,
            current_gold_price=scenario_price
        )
        
        price_scenarios.append({
            'Price Change (%)': price_change,
            'Gold Price (₹/g)': scenario_price,
            'Returns (%)': scenario_results['profit_loss_percentage'],
            'Profit/Loss (₹)': scenario_results['profit_loss']
        })
    
    df_scenarios = pd.DataFrame(price_scenarios)
    
    # Price sensitivity chart
    fig_sensitivity = px.line(
        df_scenarios,
        x='Price Change (%)',
        y='Returns (%)',
        markers=True,
        title="Returns vs Gold Price Changes"
    )
    fig_sensitivity.update_traces(line=dict(color='#FFD700', width=3), marker=dict(size=8))
    fig_sensitivity.update_layout(height=400)
    fig_sensitivity.add_hline(y=0, line_dash="dash", line_color="red", opacity=0.7)
    
    st.plotly_chart(fig_sensitivity, use_container_width=True)

with price_col2:
    st.markdown("### 💰 Investment Amount Impact")
    
    # Calculate returns for different SIP amounts
    amount_scenarios = []
    base_amount = monthly_amount
    
    for amount_multiplier in [0.5, 0.75, 1.0, 1.25, 1.5, 2.0]:
        scenario_amount = base_amount * amount_multiplier
        scenario_results = calculator.calculate_sip_returns(
            monthly_amount=scenario_amount,
            duration_months=duration_months,
            average_gold_price=average_gold_price,
            current_gold_price=current_gold_price
        )
        
        amount_scenarios.append({
            'Monthly Amount (₹)': scenario_amount,
            'Total Investment (₹)': scenario_results['total_investment'],
            'Current Value (₹)': scenario_results['current_value'],
            'Gold Purchased (g)': scenario_results['total_grams']
        })
    
    df_amounts = pd.DataFrame(amount_scenarios)
    
    # Amount impact chart
    fig_amounts = px.bar(
        df_amounts,
        x='Monthly Amount (₹)',
        y='Current Value (₹)',
        title="Portfolio Value vs Monthly SIP Amount",
        color='Current Value (₹)',
        color_continuous_scale='YlOrRd'
    )
    fig_amounts.update_layout(height=400)
    
    st.plotly_chart(fig_amounts, use_container_width=True)

# Download results
if hasattr(st.session_state, 'show_results') and st.session_state.show_results:
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        # Create summary report
        summary_text = calculator.generate_summary_text(st.session_state.results)
        
        st.download_button(
            label="📄 Download Investment Report",
            data=summary_text,
            file_name=f"gold_sip_report_{datetime.date.today().strftime('%Y%m%d')}.txt",
            mime="text/plain",
            use_container_width=True
        )

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p>💛 <strong>Gold SIP Calculator Dashboard</strong> | Built with Streamlit & ❤️</p>
    <p><small>Disclaimer: This tool is for educational purposes. Please consult a financial advisor for investment decisions.</small></p>
</div>
""", unsafe_allow_html=True)