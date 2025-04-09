# Payplug Churn Risk Dashboard

## What This Project Does

![image](https://github.com/user-attachments/assets/c16ffe1b-fc88-46b8-81c3-8a51f9b37897)

![image](https://github.com/user-attachments/assets/04ab9d23-0b45-455c-89de-16aa5784400f)

![image](https://github.com/user-attachments/assets/07310c5f-02b2-41ba-83fc-3ffdc4e02370)




The Payplug Churn Risk Dashboard is a tool that helps our company identify merchants who might stop using our payment services. It displays this information in an engaging retro-gaming style interface that makes monitoring data more enjoyable.

The dashboard shows:
- Which merchants are at high risk of leaving
- Why they might be leaving (risk factors)
- How much payment volume we might lose
- Trends in merchant behavior over time

## How This Will Help Payplug

### Immediate Benefits (Next 3-6 Months)
- **Reduce Merchant Churn**: Identify at-risk merchants before they leave, allowing our account managers to step in and address concerns.
- **Protect Revenue**: By spotting declining payment volumes early, we can take action to maintain our transaction fees.
- **Focus Resources**: Help account managers prioritize which merchants need attention first.

### Long-term Benefits (6-12 Months)
- **Identify Patterns**: Understand common reasons why merchants leave, so we can improve our services.
- **Improve Product Decisions**: See which features are most valuable to merchants who stay with us.
- **Better Forecasting**: More accurately predict revenue by understanding churn patterns.

## Key Features

1. **Risk Dashboard**: Shows key metrics and current status of merchant risks.
2. **Merchant Risk Leaderboard**: Lists all merchants sorted by their risk score.
3. **Merchant Deep Dive**: Lets you examine individual merchant profiles, including:
   - Transaction history
   - Feature usage
   - Risk factors
   - Recommended actions
4. **Historical Trend Analysis**: Shows how churn risk has changed over time.

## How to Use This Tool

This dashboard is designed for:
- **Account Managers**: To identify which of their merchants need immediate attention
- **Customer Success Team**: To develop targeted retention strategies
- **Product Team**: To understand which features drive retention
- **Executive Team**: To get an overview of churn risk and potential revenue impact

## Getting Started

1. Install requirements:
   ```
   pip install -r requirements.txt
   ```

2. Run the application:
   ```
   streamlit run app.py
   ```

3. Access the dashboard in your web browser at:
   ```
   http://localhost:8501
   ```



The current version uses mock data for demonstration purposes. In a production environment, it would connect to our merchant database for real-time insights.
