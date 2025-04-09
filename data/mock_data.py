import pandas as pd
import numpy as np
import datetime
import random

def generate_mock_data(num_merchants=100):
    """
    Generate mock merchant data for the churn risk dashboard.
    
    Args:
        num_merchants (int): Number of merchant records to generate
        
    Returns:
        tuple: (merchants_df, volumes_df) - DataFrames containing merchant data and volume history
    """
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
            
        # Generate monthly volumes - Calculate the average first
        base_volume = np.random.randint(5000, 100000)
        
        # Apply risk-based trend to determine volume trend
        if risk_category == 'High':
            volume_trend = -0.15 + 0.1 * np.random.random()  # -15% to -5%
        elif risk_category == 'Medium':
            volume_trend = -0.05 + 0.1 * np.random.random()  # -5% to +5%
        else:
            volume_trend = 0.05 + 0.15 * np.random.random()  # +5% to +20%
            
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
            'monthly_volume_avg': base_volume,
            'latest_volume': int(base_volume * (1 + volume_trend/2)),  # Latest month is halfway to the trend
            'volume_trend': volume_trend
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