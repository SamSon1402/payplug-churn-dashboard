import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import datetime
from PIL import Image
import base64
from io import BytesIO
import random

# Set page configuration
st.set_page_config(
    page_title="Payplug Churn Risk Radar",
    page_icon="🕹️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for retro gaming aesthetic
def local_css():
    st.markdown("""
    <style>
    /* Main theme colors */
    :root {
        --primary: #FF355E;        /* Hot pink */
        --secondary: #01EDED;      /* Cyan */
        --tertiary: #50FC00;       /* Bright green */
        --dark: #120458;           /* Dark blue */
        --light: #F5F5F5;          /* White-ish */
        --warning: #FF9933;        /* Orange */
        --danger: #FF0000;         /* Red */
        --background: #FFDD00;     /* Bright yellow */
    }
    
    /* Fonts */
    @import url('https://fonts.googleapis.com/css2?family=VT323&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Space+Mono&display=swap');
    
    /* Base styles */
    .main {
        background-color: var(--background);
        color: var(--dark);
    }
    
    /* Override Streamlit's default background */
    .stApp {
        background-color: var(--background);
    }
    
    h1, h2, h3 {
        font-family: 'Press Start 2P', cursive;
        text-transform: uppercase;
        color: var(--secondary);
        text-shadow: 3px 3px 0 var(--dark);
        margin: 1.5rem 0;
    }
    
    h1 {
        color: var(--primary);
        font-size: 2.5rem;
        letter-spacing: 2px;
        text-align: center;
        padding: 20px 0;
        border-bottom: 4px solid var(--primary);
        margin-bottom: 30px;
    }
    
    .stDataFrame {
        border: 4px solid var(--secondary);
        box-shadow: 8px 8px 0 var(--dark);
    }
    
    /* Metric cards */
    .metric-card {
        background-color: var(--dark);
        border: 3px solid var(--secondary);
        border-radius: 0;
        padding: 10px;
        text-align: center;
        margin: 5px;
        box-shadow: 5px 5px 0 rgba(0,0,0,0.5);
        transition: all 0.2s;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 7px 7px 0 #000;
    }
    
    .metric-value {
        font-family: 'Press Start 2P', cursive;
        font-size: 2rem;
        margin: 10px 0;
    }
    
    .metric-label {
        font-family: 'VT323', monospace;
        font-size: 1.3rem;
        color: var(--light);
    }
    
    /* Risk levels */
    .high-risk {
        color: var(--danger);
        font-weight: bold;
    }
    
    .medium-risk {
        color: var(--warning);
        font-weight: bold;
    }
    
    .low-risk {
        color: var(--tertiary);
        font-weight: bold;
    }
    
    /* Button styles */
    .stButton button {
        font-family: 'Press Start 2P', cursive;
        background-color: var(--secondary);
        color: var(--dark);
        border: 3px solid var(--dark);
        border-radius: 0;
        box-shadow: 5px 5px 0 rgba(0,0,0,0.5);
        transition: all 0.2s;
        text-transform: uppercase;
        padding: 10px 20px;
        margin: 10px 0;
    }
    
    .stButton button:hover {
        background-color: var(--primary);
        color: white;
        transform: translateY(-2px);
        box-shadow: 7px 7px 0 rgba(0,0,0,0.5);
    }
    
    /* Select box styling */
    .stSelectbox div[data-baseweb="select"] > div {
        font-family: 'VT323', monospace;
        background-color: var(--dark);
        border: 3px solid var(--secondary);
        border-radius: 0;
        color: white;
    }
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background-color: var(--dark);
        border-right: 4px solid var(--secondary);
    }
    
    [data-testid="stSidebar"] {
        background-color: var(--dark);
    }
    
    .sidebar h2 {
        font-size: 1.5rem;
        color: var(--primary);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    
    .stTabs [data-baseweb="tab"] {
        font-family: 'Press Start 2P', cursive;
        font-size: 0.8rem;
        background-color: var(--dark);
        border: 2px solid var(--secondary);
        border-radius: 0;
        color: var(--light);
        padding: 10px;
        box-shadow: 3px 3px 0 #000;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: var(--secondary);
        color: var(--dark);
    }
    
    /* Dataframe styling */
    .dataframe {
        font-family: 'Space Mono', monospace;
    }
    
    /* Footer */
    .footer {
        font-family: 'VT323', monospace;
        text-align: center;
        color: var(--light);
        padding: 20px 0;
        border-top: 2px solid var(--primary);
        margin-top: 50px;
    }
    
    /* Progress bar styling */
    .stProgress > div > div {
        background-color: var(--primary);
    }
    
    /* Arcade marquee effect */
    .marquee {
        background-color: var(--dark);
        overflow: hidden;
        position: relative;
        border: 3px solid var(--primary);
        box-shadow: 0 0 10px var(--primary);
        margin: 20px 0;
        padding: 10px;
    }
    
    .marquee-content {
        font-family: 'Press Start 2P', cursive;
        font-size: 1.2rem;
        color: var(--primary);
        white-space: nowrap;
        animation: marquee 15s linear infinite;
    }
    
    @keyframes marquee {
        0% { transform: translateX(100%); }
        100% { transform: translateX(-100%); }
    }
    
    /* High-score table style */
    .high-score {
        font-family: 'VT323', monospace;
        font-size: 1.2rem;
        margin-bottom: 10px;
    }
    
    .high-score-name {
        color: var(--secondary);
        display: inline-block;
        width: 70%;
    }
    
    .high-score-value {
        color: var(--tertiary);
        display: inline-block;
        width: 30%;
        text-align: right;
    }
    </style>
    """, unsafe_allow_html=True)

# Generate mock data
def generate_mock_data(num_merchants=100):
    # Random seed for reproducibility
    np.random.seed(42)
    
    # Industries
    industries = ['E-commerce', 'Retail', 'SaaS', 'Hospitality', 'Healthcare', 'Education', 'Finance']
    
    # Segments
    segments = ['Small Business', 'Mid-Market', 'Enterprise']
    
    # Account Managers
    account_managers = ['Alex Thompson', 'Samantha Lee', 'Marcus Johnson', 'Rachel Chen', 'David Kim']
    
    # Risk Factors
    risk_factors = [
        'Volume Drop >30%', 
        'Low Feature Adoption', 
        'Payment Failures', 
        'Support Tickets Increase', 
        'Competitor Integration',
        'Contract End Approaching',
        'Price Sensitivity',
        'Account Inactivity'
    ]
    
    # Generate data
    merchants = []
    current_date = datetime.datetime.now()
    
    for i in range(1, num_merchants + 1):
        # Basic merchant info
        merchant_id = f'M{i:04d}'
        merchant_name = f'Merchant {i}'
        industry = np.random.choice(industries)
        segment = np.random.choice(segments)
        account_manager = np.random.choice(account_managers)
        
        # Tenure (1-36 months)
        tenure = np.random.randint(1, 37)
        onboarding_date = current_date - datetime.timedelta(days=tenure*30)
        
        # Risk calculation
        base_risk = np.random.beta(2, 5)  # Skewed toward lower risk
        
        # Adjust risk based on some factors
        if tenure < 3:
            base_risk += 0.2  # New merchants have higher churn risk
        elif tenure > 24:
            base_risk -= 0.1  # Loyal merchants have lower risk
            
        if segment == 'Small Business':
            base_risk += 0.05  # Small businesses have slightly higher risk
        elif segment == 'Enterprise':
            base_risk -= 0.05  # Enterprise has slightly lower risk
            
        # Ensure risk is between 0 and 1
        risk_score = max(0, min(base_risk, 1))
        
        # Determine risk category
        if risk_score >= 0.7:
            risk_category = 'High'
        elif risk_score >= 0.4:
            risk_category = 'Medium'
        else:
            risk_category = 'Low'
            
        # Generate random monthly volume for the past 12 months
        monthly_volumes = []
        base_volume = np.random.randint(5000, 100000)
        
        for month in range(12):
            if risk_category == 'High' and month >= 9:
                # High risk merchants show declining volume in recent months
                decline_factor = 1 - 0.1 * (month - 8)
                volume = int(base_volume * max(0.5, decline_factor))
            elif risk_category == 'Medium' and month >= 10:
                # Medium risk merchants show slight decline in very recent months
                volume = int(base_volume * 0.9)
            else:
                # Normal variation
                variation = np.random.normal(0, 0.1)
                volume = int(base_volume * (1 + variation))
                
            month_date = current_date - datetime.timedelta(days=(11-month)*30)
            monthly_volumes.append({
                'merchant_id': merchant_id,
                'month': month_date.strftime('%Y-%m'),
                'volume': volume
            })
        
        # Select risk factors for this merchant
        num_risk_factors = 0
        if risk_category == 'High':
            num_risk_factors = np.random.randint(2, 5)
        elif risk_category == 'Medium':
            num_risk_factors = np.random.randint(1, 3)
        elif risk_category == 'Low' and np.random.random() < 0.3:
            num_risk_factors = 1
            
        merchant_risk_factors = np.random.choice(risk_factors, size=num_risk_factors, replace=False).tolist()
        
        # Feature usage (0-100%)
        one_click_usage = np.random.randint(0, 101)
        subscription_api_usage = np.random.randint(0, 101)
        fraud_tools_usage = np.random.randint(0, 101)
        mobile_sdk_usage = np.random.randint(0, 101)
        
        # Lower feature usage correlates with higher risk
        if risk_category == 'High':
            one_click_usage = min(one_click_usage, 50)
            subscription_api_usage = min(subscription_api_usage, 40)
            fraud_tools_usage = min(fraud_tools_usage, 30)
            mobile_sdk_usage = min(mobile_sdk_usage, 20)
        
        # Support tickets (more for high risk)
        if risk_category == 'High':
            support_tickets = np.random.randint(5, 15)
        elif risk_category == 'Medium':
            support_tickets = np.random.randint(2, 7)
        else:
            support_tickets = np.random.randint(0, 3)
            
        merchants.append({
            'merchant_id': merchant_id,
            'merchant_name': merchant_name,
            'industry': industry,
            'segment': segment,
            'account_manager': account_manager,
            'tenure': tenure,
            'onboarding_date': onboarding_date.strftime('%Y-%m-%d'),
            'risk_score': risk_score,
            'risk_category': risk_category,
            'risk_factors': merchant_risk_factors,
            'one_click_usage': one_click_usage,
            'subscription_api_usage': subscription_api_usage,
            'fraud_tools_usage': fraud_tools_usage,
            'mobile_sdk_usage': mobile_sdk_usage,
            'support_tickets': support_tickets,
            'monthly_volume_avg': int(sum(mv['volume'] for mv in monthly_volumes) / len(monthly_volumes)),
            'latest_volume': monthly_volumes[-1]['volume'],
            'volume_trend': monthly_volumes[-1]['volume'] / monthly_volumes[-6]['volume'] - 1  # 6-month trend
        })
    
    # Convert to DataFrames
    merchants_df = pd.DataFrame(merchants)
    
    # Flatten monthly volumes for all merchants
    all_volumes = []
    for merchant in merchants:
        for month in range(12):
            month_date = current_date - datetime.timedelta(days=(11-month)*30)
            if month < 6:
                vol_base = merchant['monthly_volume_avg'] * (0.85 + 0.3 * random.random())
            else:
                # Use the volume trend to inform later months
                trend_factor = 1 + (month - 5) * (merchant['volume_trend'] / 6)
                vol_base = merchant['monthly_volume_avg'] * max(0.5, trend_factor)
            
            all_volumes.append({
                'merchant_id': merchant['merchant_id'],
                'month': month_date.strftime('%Y-%m'),
                'volume': int(vol_base)
            })
    
    volumes_df = pd.DataFrame(all_volumes)
    
    return merchants_df, volumes_df

# Create a pixel art version of the merchant icon
def create_pixel_merchant_icon(color='cyan'):
    colors = {
        'cyan': (1, 237, 237),
        'pink': (255, 53, 94),
        'green': (80, 252, 0),
        'yellow': (255, 218, 0),
        'orange': (255, 153, 51),
        'red': (255, 0, 0),
    }
    
    rgb_color = colors.get(color, colors['cyan'])
    
    # Create a 16x16 image with transparent background
    img = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
    pixels = img.load()
    
    # Draw a simple store/shop icon
    # Roof
    for x in range(3, 13):
        pixels[x, 3] = rgb_color
    for x in range(2, 14):
        pixels[x, 4] = rgb_color
    
    # Building
    for y in range(5, 13):
        for x in range(4, 12):
            pixels[x, y] = rgb_color
    
    # Door
    for y in range(9, 13):
        for x in range(6, 10):
            pixels[x, y] = (0, 0, 0, 255)
    
    # Door handle
    pixels[8, 11] = (255, 255, 255, 255)
    
    # Convert to base64 for HTML display
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    
    return f"data:image/png;base64,{img_str}"

# Create a pixelated data visualization
def create_pixel_chart(data, color='cyan', height=100, width=200):
    # Create an empty image
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    pixels = img.load()
    
    # Normalize data to fit the height
    max_val = max(data)
    min_val = min(data)
    range_val = max_val - min_val
    
    if range_val == 0:  # Handle flat data
        normalized = [height // 2 for _ in data]
    else:
        normalized = [int((height - 10) * (1 - (val - min_val) / range_val)) + 5 for val in data]
    
    # Get RGB color
    colors = {
        'cyan': (1, 237, 237),
        'pink': (255, 53, 94),
        'green': (80, 252, 0),
        'yellow': (255, 218, 0),
        'orange': (255, 153, 51),
        'red': (255, 0, 0),
    }
    
    rgb_color = colors.get(color, colors['cyan'])
    
    # Draw the line
    step = width / (len(data) - 1) if len(data) > 1 else width
    
    for i in range(len(data) - 1):
        x1, y1 = int(i * step), normalized[i]
        x2, y2 = int((i + 1) * step), normalized[i + 1]
        
        # Draw a thick pixel line
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy
        
        while x1 != x2 or y1 != y2:
            # Draw a 2x2 pixel at this point
            for ox in range(2):
                for oy in range(2):
                    if 0 <= x1+ox < width and 0 <= y1+oy < height:
                        pixels[x1+ox, y1+oy] = rgb_color
            
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy
                
        # Draw the endpoint
        for ox in range(2):
            for oy in range(2):
                if 0 <= x2+ox < width and 0 <= y2+oy < height:
                    pixels[x2+ox, y2+oy] = rgb_color
    
    # Convert to base64 for HTML display
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    
    return f"data:image/png;base64,{img_str}"

# Main application
def main():
    local_css()
    
    # Generate mock data
    merchants_df, volumes_df = generate_mock_data(100)
    
    # Application title
    st.markdown("<h1>PAYPLUG CHURN RISK RADAR 🕹️</h1>", unsafe_allow_html=True)
    
    # Arcade marquee
    st.markdown("""
    <div class="marquee">
        <div class="marquee-content">
            ALERT! 15 MERCHANTS AT HIGH RISK • ACCOUNT MANAGERS ACTIVATE RETENTION PROTOCOLS • NEW HIGH SCORE: SAMANTHA LEE - 98% RETENTION RATE
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar with filters
    st.sidebar.markdown("<h2>CONTROL PANEL</h2>", unsafe_allow_html=True)
    
    # Time filter
    st.sidebar.markdown("### 📅 TIME PERIOD")
    time_period = st.sidebar.selectbox(
        "Select Period:",
        ["Current Month", "Last 3 Months", "Last 6 Months", "Year To Date", "All Time"]
    )
    
    # Segment filters
    st.sidebar.markdown("### 🏢 MERCHANT SEGMENTS")
    
    selected_industries = st.sidebar.multiselect(
        "Industry:",
        options=merchants_df['industry'].unique(),
        default=merchants_df['industry'].unique()
    )
    
    selected_segments = st.sidebar.multiselect(
        "Size Segment:",
        options=merchants_df['segment'].unique(),
        default=merchants_df['segment'].unique()
    )
    
    # Account Manager filter
    st.sidebar.markdown("### 👥 ACCOUNT MANAGERS")
    selected_managers = st.sidebar.multiselect(
        "Account Manager:",
        options=merchants_df['account_manager'].unique(),
        default=merchants_df['account_manager'].unique()
    )
    
    # Risk level filter
    st.sidebar.markdown("### ⚠️ RISK LEVEL")
    selected_risk = st.sidebar.multiselect(
        "Risk Category:",
        options=["High", "Medium", "Low"],
        default=["High", "Medium", "Low"]
    )
    
    # Apply filters to data
    filtered_df = merchants_df[
        merchants_df['industry'].isin(selected_industries) &
        merchants_df['segment'].isin(selected_segments) &
        merchants_df['account_manager'].isin(selected_managers) &
        merchants_df['risk_category'].isin(selected_risk)
    ]
    
    # Dashboard metrics
    st.markdown("## CURRENT STATUS")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        high_risk_count = len(filtered_df[filtered_df['risk_category'] == 'High'])
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">HIGH RISK MERCHANTS</div>
            <div class="metric-value high-risk">{high_risk_count}</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        medium_risk_count = len(filtered_df[filtered_df['risk_category'] == 'Medium'])
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">MEDIUM RISK MERCHANTS</div>
            <div class="metric-value medium-risk">{medium_risk_count}</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        at_risk_volume = filtered_df[filtered_df['risk_category'].isin(['High', 'Medium'])]['monthly_volume_avg'].sum()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">AT-RISK VOLUME</div>
            <div class="metric-value">${at_risk_volume:,}</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col4:
        avg_risk_score = filtered_df['risk_score'].mean()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">AVG RISK SCORE</div>
            <div class="metric-value">{avg_risk_score:.2f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Risk factors bar chart
    st.markdown("## TOP RISK FACTORS")
    
    # Extract all risk factors and count occurrences
    all_factors = []
    for factors in filtered_df['risk_factors']:
        all_factors.extend(factors)
    
    if all_factors:
        factor_counts = pd.Series(all_factors).value_counts().reset_index()
        factor_counts.columns = ['Risk Factor', 'Count']
        
        fig = px.bar(
            factor_counts.head(5), 
            x='Count', 
            y='Risk Factor',
            orientation='h',
            color_discrete_sequence=['#01EDED'],
            labels={'Count': 'Number of Merchants'}
        )
        
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family="VT323", size=16, color="#F5F5F5"),
            yaxis_title=None,
            xaxis_title=None,
            margin=dict(l=0, r=10, t=10, b=0),
            height=300
        )
        
        fig.update_traces(marker_line_width=2, marker_line_color="#120458")
        fig.update_xaxes(gridcolor='#333333', gridwidth=0.5)
        fig.update_yaxes(gridcolor='#333333', gridwidth=0.5)
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No risk factors found with current filters.")
    
    # Merchant list with risk scoring
    st.markdown("## MERCHANT RISK LEADERBOARD")
    
    # Sort by risk score (descending)
    sorted_merchants = filtered_df.sort_values('risk_score', ascending=False).reset_index(drop=True)
    
    # Add styling to the table based on risk category
    def color_risk(val):
        if val == 'High':
            return 'color: #FF0000; font-weight: bold'
        elif val == 'Medium':
            return 'color: #FF9933; font-weight: bold'
        else:
            return 'color: #50FC00; font-weight: bold'
    
    # Select columns to display
    display_cols = ['merchant_name', 'risk_category', 'risk_score', 'account_manager', 
                    'industry', 'segment', 'tenure', 'monthly_volume_avg']
    
    # Format and display the table
    display_df = sorted_merchants[display_cols].copy()
    display_df.columns = ['Merchant Name', 'Risk Level', 'Risk Score', 'Account Manager', 
                         'Industry', 'Segment', 'Tenure (Months)', 'Avg Monthly Volume ($)']
    
    # Format the risk score and volume columns
    display_df['Risk Score'] = display_df['Risk Score'].map(lambda x: f"{x:.2f}")
    display_df['Avg Monthly Volume ($)'] = display_df['Avg Monthly Volume ($)'].map(lambda x: f"${x:,}")
    
    # Apply styling and display
    styled_df = display_df.style.applymap(color_risk, subset=['Risk Level'])
    st.dataframe(styled_df, use_container_width=True, height=400)
    
    # Merchant detail view
    st.markdown("## MERCHANT DEEP DIVE")
    
    selected_merchant = st.selectbox(
        "Select Merchant to Analyze:",
        options=sorted_merchants['merchant_name'].tolist()
    )
    
    # Get the selected merchant data
    merchant_data = sorted_merchants[sorted_merchants['merchant_name'] == selected_merchant].iloc[0]
    
    # Display merchant profile in tabs
    tab1, tab2, tab3 = st.tabs(["PROFILE", "RISK ANALYSIS", "TRANSACTION HISTORY"])
    
    with tab1:
        col1, col2 = st.columns([1, 2])
        
        with col1:
            # Merchant info card
            risk_color = "red" if merchant_data['risk_category'] == 'High' else "orange" if merchant_data['risk_category'] == 'Medium' else "green"
            
            st.markdown(f"""
            <div style="border: 3px solid var(--secondary); padding: 15px; margin-bottom: 20px; background-color: var(--dark);">
                <div style="text-align: center; margin-bottom: 15px;">
                    <img src="{create_pixel_merchant_icon(risk_color)}" style="width: 64px; height: 64px;">
                </div>
                <div style="font-family: 'VT323', monospace; font-size: 1.5rem; text-align: center; color: var(--secondary); margin-bottom: 10px;">
                    {merchant_data['merchant_name']}
                </div>
                <div style="font-family: 'VT323', monospace; font-size: 1.2rem; margin-bottom: 5px;">
                    <span style="color: var(--light);">Industry:</span> {merchant_data['industry']}
                </div>
                <div style="font-family: 'VT323', monospace; font-size: 1.2rem; margin-bottom: 5px;">
                    <span style="color: var(--light);">Segment:</span> {merchant_data['segment']}
                </div>
                <div style="font-family: 'VT323', monospace; font-size: 1.2rem; margin-bottom: 5px;">
                    <span style="color: var(--light);">Account Manager:</span> {merchant_data['account_manager']}
                </div>
                <div style="font-family: 'VT323', monospace; font-size: 1.2rem; margin-bottom: 5px;">
                    <span style="color: var(--light);">Onboarded:</span> {merchant_data['onboarding_date']}
                </div>
                <div style="font-family: 'VT323', monospace; font-size: 1.2rem; margin-bottom: 5px;">
                    <span style="color: var(--light);">Tenure:</span> {merchant_data['tenure']} months
                </div>
                <div style="font-family: 'VT323', monospace; font-size: 1.2rem; margin-bottom: 5px;">
                    <span style="color: var(--light);">Support Tickets:</span> {merchant_data['support_tickets']}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            # Feature usage section
            st.markdown("### FEATURE USAGE LEVELS")
            
            # One-click payment usage
            st.markdown(f"""
            <div style="margin-bottom: 15px;">
                <div style="font-family: 'VT323', monospace; font-size: 1.2rem; margin-bottom: 5px; display: flex; justify-content: space-between;">
                    <span>One-Click Payment</span>
                    <span>{merchant_data['one_click_usage']}%</span>
                </div>
                <div style="height: 20px; width: 100%; background-color: #333; border: 2px solid var(--secondary);">
                    <div style="height: 100%; width: {merchant_data['one_click_usage']}%; background-color: var(--tertiary);"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Subscription API usage
            st.markdown(f"""
            <div style="margin-bottom: 15px;">
                <div style="font-family: 'VT323', monospace; font-size: 1.2rem; margin-bottom: 5px; display: flex; justify-content: space-between;">
                    <span>Subscription API</span>
                    <span>{merchant_data['subscription_api_usage']}%</span>
                </div>
                <div style="height: 20px; width: 100%; background-color: #333; border: 2px solid var(--secondary);">
                    <div style="height: 100%; width: {merchant_data['subscription_api_usage']}%; background-color: var(--tertiary);"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Fraud Tools usage
            st.markdown(f"""
            <div style="margin-bottom: 15px;">
                <div style="font-family: 'VT323', monospace; font-size: 1.2rem; margin-bottom: 5px; display: flex; justify-content: space-between;">
                    <span>Fraud Tools</span>
                    <span>{merchant_data['fraud_tools_usage']}%</span>
                </div>
                <div style="height: 20px; width: 100%; background-color: #333; border: 2px solid var(--secondary);">
                    <div style="height: 100%; width: {merchant_data['fraud_tools_usage']}%; background-color: var(--tertiary);"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Mobile SDK usage
            st.markdown(f"""
            <div style="margin-bottom: 15px;">
                <div style="font-family: 'VT323', monospace; font-size: 1.2rem; margin-bottom: 5px; display: flex; justify-content: space-between;">
                    <span>Mobile SDK</span>
                    <span>{merchant_data['mobile_sdk_usage']}%</span>
                </div>
                <div style="height: 20px; width: 100%; background-color: #333; border: 2px solid var(--secondary);">
                    <div style="height: 100%; width: {merchant_data['mobile_sdk_usage']}%; background-color: var(--tertiary);"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Volume info
            st.markdown("### TRANSACTION VOLUME")
            st.markdown(f"""
            <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                <div style="font-family: 'VT323', monospace; font-size: 1.2rem;">
                    <span style="color: var(--light);">Average Monthly:</span> 
                    <span style="color: var(--tertiary); font-weight: bold;">${merchant_data['monthly_volume_avg']:,}</span>
                </div>
                <div style="font-family: 'VT323', monospace; font-size: 1.2rem;">
                    <span style="color: var(--light);">Latest Month:</span> 
                    <span style="color: var(--tertiary); font-weight: bold;">${merchant_data['latest_volume']:,}</span>
                </div>
                <div style="font-family: 'VT323', monospace; font-size: 1.2rem;">
                    <span style="color: var(--light);">6-Month Trend:</span> 
                    <span style="color: {'var(--tertiary)' if merchant_data['volume_trend'] >= 0 else 'var(--danger)'}; font-weight: bold;">
                        {'+' if merchant_data['volume_trend'] >= 0 else ''}{merchant_data['volume_trend']*100:.1f}%
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
    with tab2:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # Risk score gauge chart
            risk_score = merchant_data['risk_score']
            risk_gauge = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = risk_score,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "RISK SCORE", 'font': {'family': "Press Start 2P", 'size': 16}},
                gauge = {
                    'axis': {'range': [0, 1], 'tickwidth': 2, 'tickcolor': "#F5F5F5"},
                    'bar': {'color': "#01EDED"},
                    'bgcolor': "black",
                    'borderwidth': 2,
                    'bordercolor': "#01EDED",
                    'steps': [
                        {'range': [0, 0.4], 'color': '#50FC00'},
                        {'range': [0.4, 0.7], 'color': '#FF9933'},
                        {'range': [0.7, 1], 'color': '#FF0000'}
                    ],
                    'threshold': {
                        'line': {'color': "white", 'width': 4},
                        'thickness': 0.75,
                        'value': risk_score
                    }
                },
                number = {'font': {'family': "Press Start 2P", 'size': 24}}
            ))
            
            risk_gauge.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(family="VT323", size=16, color="#F5F5F5"),
                margin=dict(l=20, r=20, t=50, b=20),
                height=300
            )
            
            st.plotly_chart(risk_gauge, use_container_width=True)
            
        with col2:
            # Risk factors list
            st.markdown("### ACTIVE RISK FACTORS")
            
            if merchant_data['risk_factors']:
                for i, factor in enumerate(merchant_data['risk_factors']):
                    severity = random.randint(70, 100) if merchant_data['risk_category'] == 'High' else random.randint(40, 70)
                    
                    st.markdown(f"""
                    <div style="margin-bottom: 15px;">
                        <div style="font-family: 'VT323', monospace; font-size: 1.2rem; margin-bottom: 5px; display: flex; justify-content: space-between;">
                            <span>{factor}</span>
                            <span>Severity: {severity}%</span>
                        </div>
                        <div style="height: 20px; width: 100%; background-color: #333; border: 2px solid var(--secondary);">
                            <div style="height: 100%; width: {severity}%; background-color: {'var(--danger)' if severity >= 70 else 'var(--warning)'};"></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="font-family: 'VT323', monospace; font-size: 1.5rem; text-align: center; color: var(--tertiary); padding: 50px 0;">
                    NO ACTIVE RISK FACTORS DETECTED
                </div>
                """, unsafe_allow_html=True)
        
        # Recommendations section
        st.markdown("### RECOMMENDED ACTIONS")
        
        if merchant_data['risk_category'] == 'High':
            st.markdown("""
            <div style="border: 3px solid var(--danger); padding: 15px; margin-bottom: 20px; background-color: rgba(255, 0, 0, 0.1);">
                <div style="font-family: 'Press Start 2P', cursive; font-size: 1.2rem; color: var(--danger); margin-bottom: 10px;">
                    HIGH PRIORITY INTERVENTION REQUIRED
                </div>
                <ul style="font-family: 'VT323', monospace; font-size: 1.2rem; color: var(--light); list-style-type: square;">
                    <li>Schedule urgent executive meeting within 48 hours</li>
                    <li>Perform complete contract review and offer renewal incentives</li>
                    <li>Address specific pain points: volume drop, feature adoption</li>
                    <li>Assign dedicated support specialist for next 30 days</li>
                    <li>Create custom retention package with targeted discounts</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        elif merchant_data['risk_category'] == 'Medium':
            st.markdown("""
            <div style="border: 3px solid var(--warning); padding: 15px; margin-bottom: 20px; background-color: rgba(255, 153, 51, 0.1);">
                <div style="font-family: 'Press Start 2P', cursive; font-size: 1.2rem; color: var(--warning); margin-bottom: 10px;">
                    INCREASED MONITORING RECOMMENDED
                </div>
                <ul style="font-family: 'VT323', monospace; font-size: 1.2rem; color: var(--light); list-style-type: square;">
                    <li>Schedule account review within 2 weeks</li>
                    <li>Create feature adoption plan to boost engagement</li>
                    <li>Check for competitive pressures in the market</li>
                    <li>Offer complimentary optimization consultation</li>
                    <li>Monitor transaction volume weekly for next 30 days</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="border: 3px solid var(--tertiary); padding: 15px; margin-bottom: 20px; background-color: rgba(80, 252, 0, 0.1);">
                <div style="font-family: 'Press Start 2P', cursive; font-size: 1.2rem; color: var(--tertiary); margin-bottom: 10px;">
                    STABLE ACCOUNT - GROWTH OPPORTUNITY
                </div>
                <ul style="font-family: 'VT323', monospace; font-size: 1.2rem; color: var(--light); list-style-type: square;">
                    <li>Maintain regular quarterly check-ins</li>
                    <li>Consider for early access to new features</li>
                    <li>Explore upsell opportunities for premium services</li>
                    <li>Request case study or testimonial opportunity</li>
                    <li>Include in customer advisory board invitations</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
    with tab3:
        # Generate some mock monthly volume data
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        
        # Create data with trend based on risk category
        base_volume = merchant_data['monthly_volume_avg']
        monthly_data = []
        
        for i in range(12):
            if merchant_data['risk_category'] == 'High' and i >= 8:
                # High risk merchants show declining volume in recent months
                decline_factor = 1 - 0.1 * (i - 7)
                volume = int(base_volume * max(0.6, decline_factor))
            elif merchant_data['risk_category'] == 'Medium' and i >= 9:
                # Medium risk merchants show slight decline in very recent months
                volume = int(base_volume * 0.9)
            else:
                # Normal variation
                variation = np.random.normal(0, 0.1)
                volume = int(base_volume * (1 + variation))
            
            monthly_data.append(volume)
        
        # Create a Plotly figure for the transaction volume
        fig = go.Figure()
        
        # Add volume bars
        fig.add_trace(go.Bar(
            x=months,
            y=monthly_data,
            marker_color='#01EDED',
            marker_line_color='#120458',
            marker_line_width=2,
            opacity=0.8,
            name="Monthly Volume"
        ))
        
        # Customize layout
        fig.update_layout(
            title={
                'text': "MONTHLY TRANSACTION VOLUME",
                'font': {'family': "Press Start 2P", 'size': 18, 'color': "#01EDED"},
                'y': 0.95
            },
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family="VT323", size=16, color="#F5F5F5"),
            xaxis_title=None,
            yaxis_title="Volume ($)",
            margin=dict(l=40, r=40, t=80, b=40),
            height=400
        )
        
        fig.update_xaxes(gridcolor='#333333', gridwidth=0.5)
        fig.update_yaxes(gridcolor='#333333', gridwidth=0.5)
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Transaction trends insights
        col1, col2 = st.columns(2)
        
        with col1:
            # Calculate volume metrics
            recent_trend = (monthly_data[-1] / monthly_data[-3] - 1) * 100
            overall_trend = (monthly_data[-1] / monthly_data[0] - 1) * 100
            peak_volume = max(monthly_data)
            peak_month = months[monthly_data.index(peak_volume)]
            
            st.markdown("### VOLUME TRENDS")
            st.markdown(f"""
            <div style="border: 3px solid var(--secondary); padding: 15px; margin-bottom: 20px; background-color: var(--dark);">
                <div class="high-score">
                    <span class="high-score-name">Recent 3-Month Trend:</span>
                    <span class="high-score-value" style="color: {'var(--tertiary)' if recent_trend >= 0 else 'var(--danger)'};">
                        {'+' if recent_trend >= 0 else ''}{recent_trend:.1f}%
                    </span>
                </div>
                <div class="high-score">
                    <span class="high-score-name">Annual Trend:</span>
                    <span class="high-score-value" style="color: {'var(--tertiary)' if overall_trend >= 0 else 'var(--danger)'};">
                        {'+' if overall_trend >= 0 else ''}{overall_trend:.1f}%
                    </span>
                </div>
                <div class="high-score">
                    <span class="high-score-name">Peak Volume Month:</span>
                    <span class="high-score-value">{peak_month}</span>
                </div>
                <div class="high-score">
                    <span class="high-score-name">Peak Volume Amount:</span>
                    <span class="high-score-value">${peak_volume:,}</span>
                </div>
                <div class="high-score">
                    <span class="high-score-name">Average Transaction Size:</span>
                    <span class="high-score-value">${random.randint(50, 500)}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            # Transaction success rates
            st.markdown("### TRANSACTION SUCCESS")
            
            # Generate mock success rate data
            success_rate = 0.94 if merchant_data['risk_category'] == 'Low' else 0.9 if merchant_data['risk_category'] == 'Medium' else 0.85
            authorization_rate = 0.96 if merchant_data['risk_category'] == 'Low' else 0.93 if merchant_data['risk_category'] == 'Medium' else 0.88
            fraud_rate = 0.01 if merchant_data['risk_category'] == 'Low' else 0.03 if merchant_data['risk_category'] == 'Medium' else 0.05
            
            st.markdown(f"""
            <div style="border: 3px solid var(--secondary); padding: 15px; margin-bottom: 20px; background-color: var(--dark);">
                <div style="margin-bottom: 15px;">
                    <div style="font-family: 'VT323', monospace; font-size: 1.2rem; margin-bottom: 5px; display: flex; justify-content: space-between;">
                        <span>Transaction Success Rate</span>
                        <span>{success_rate*100:.1f}%</span>
                    </div>
                    <div style="height: 20px; width: 100%; background-color: #333; border: 2px solid var(--secondary);">
                        <div style="height: 100%; width: {success_rate*100}%; background-color: var(--tertiary);"></div>
                    </div>
                </div>
                
                <div style="margin-bottom: 15px;">
                    <div style="font-family: 'VT323', monospace; font-size: 1.2rem; margin-bottom: 5px; display: flex; justify-content: space-between;">
                        <span>Authorization Rate</span>
                        <span>{authorization_rate*100:.1f}%</span>
                    </div>
                    <div style="height: 20px; width: 100%; background-color: #333; border: 2px solid var(--secondary);">
                        <div style="height: 100%; width: {authorization_rate*100}%; background-color: var(--tertiary);"></div>
                    </div>
                </div>
                
                <div style="margin-bottom: 15px;">
                    <div style="font-family: 'VT323', monospace; font-size: 1.2rem; margin-bottom: 5px; display: flex; justify-content: space-between;">
                        <span>Fraud Detection Rate</span>
                        <span>{fraud_rate*100:.1f}%</span>
                    </div>
                    <div style="height: 20px; width: 100%; background-color: #333; border: 2px solid var(--secondary);">
                        <div style="height: 100%; width: {fraud_rate*100}%; background-color: var(--danger);"></div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
    # Historical trend analysis
    st.markdown("## CHURN RISK HISTORICAL TRENDS")
    
    # Generate mock historical data
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    
    # Risk distribution over time (stacked area chart)
    high_risk_data = [10, 12, 14, 13, 15, 18, 16, 17, 15, 16, 14, 15]
    medium_risk_data = [22, 24, 25, 28, 26, 25, 27, 28, 30, 32, 28, 26]
    low_risk_data = [68, 64, 61, 59, 59, 57, 57, 55, 55, 52, 58, 59]
    
    # Create figure
    fig = go.Figure()
    
    # Add traces
    fig.add_trace(go.Scatter(
        x=months, y=high_risk_data,
        mode='lines',
        line=dict(width=0, color='#FF0000'),
        stackgroup='one',
        fillcolor='#FF0000',
        name='High Risk'
    ))
    
    fig.add_trace(go.Scatter(
        x=months, y=medium_risk_data,
        mode='lines',
        line=dict(width=0, color='#FF9933'),
        stackgroup='one',
        fillcolor='#FF9933',
        name='Medium Risk'
    ))
    
    fig.add_trace(go.Scatter(
        x=months, y=low_risk_data,
        mode='lines',
        line=dict(width=0, color='#50FC00'),
        stackgroup='one',
        fillcolor='#50FC00',
        name='Low Risk'
    ))
    
    # Customize layout
    fig.update_layout(
        title={
            'text': "MERCHANT RISK DISTRIBUTION OVER TIME",
            'font': {'family': "Press Start 2P", 'size': 18, 'color': "#01EDED"},
            'y': 0.95
        },
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="VT323", size=16, color="#F5F5F5"),
        xaxis_title=None,
        yaxis_title="Percentage of Merchants",
        margin=dict(l=40, r=40, t=80, b=40),
        legend=dict(
            font=dict(family="VT323", size=16, color="#F5F5F5"),
            bgcolor="rgba(0,0,0,0.5)",
            bordercolor="#01EDED",
            borderwidth=2
        ),
        height=400
    )
    
    fig.update_xaxes(gridcolor='#333333', gridwidth=0.5)
    fig.update_yaxes(gridcolor='#333333', gridwidth=0.5)
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Footer
    st.markdown("""
    <div class="footer">
        PAYPLUG CHURN RISK RADAR - DEMO VERSION 1.0 | © 2025 PAYPLUG | PRESS START TO SAVE YOUR MERCHANTS
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()