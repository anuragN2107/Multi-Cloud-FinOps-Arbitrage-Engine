import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest, RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import warnings
warnings.filterwarnings('ignore')

print("Initializing FinOps Machine Learning Engine...")

# 1. Load the Normalized Data
df = pd.read_csv('normalized_cloud_spend.csv')
df['Date'] = pd.to_datetime(df['Date'])

# ==========================================
# PART 1: ZOMBIE RESOURCE DETECTION
# ==========================================
print("\nTraining Isolation Forest to detect Zombie Resources...")

# Aggregate by ResourceID to evaluate overall efficiency
resource_stats = df.groupby(['ResourceID', 'Provider', 'ServiceCategory']).agg({
    'Cost': 'mean',
    'UsageAmount': 'mean'
}).reset_index()

# Isolation Forest isolates anomalous data points. 
# Contamination=0.05 assumes ~5% of our resources might be anomalous.
iso_forest = IsolationForest(contamination=0.05, random_state=42)
features = resource_stats[['Cost', 'UsageAmount']]
resource_stats['Anomaly_Score'] = iso_forest.fit_predict(features)

# Define a "Zombie": An anomaly (-1) where Usage is below median but Cost is above median.
median_usage = resource_stats['UsageAmount'].median()
median_cost = resource_stats['Cost'].median()

resource_stats['Is_Zombie'] = np.where(
    (resource_stats['Anomaly_Score'] == -1) & 
    (resource_stats['UsageAmount'] < median_usage) & 
    (resource_stats['Cost'] > median_cost),
    1, 0
)

zombies = resource_stats[resource_stats['Is_Zombie'] == 1]
zombies.to_csv('zombie_resources.csv', index=False)
print(f"Identified {len(zombies)} severe zombie resources costing money with negligible usage.")

# ==========================================
# PART 2: TIME-SERIES COST FORECASTING
# ==========================================
print("\nTraining Random Forest Regressor for spend forecasting...")

# Aggregate daily cost across all cloud providers
daily_spend = df.groupby('Date')['Cost'].sum().reset_index()
daily_spend = daily_spend.sort_values('Date')

# Feature Engineering: Create Lag (past days) and Rolling window features
daily_spend['Lag_1d'] = daily_spend['Cost'].shift(1)
daily_spend['Lag_7d'] = daily_spend['Cost'].shift(7)
daily_spend['Rolling_Mean_7d'] = daily_spend['Cost'].rolling(window=7).mean()

# Drop NaNs created by the shifting process
ml_df = daily_spend.dropna()

X = ml_df[['Lag_1d', 'Lag_7d', 'Rolling_Mean_7d']]
y = ml_df['Cost']

# Train/Test Split (Use the last 30 days of data for testing, do NOT shuffle time-series)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=30, shuffle=False)

rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Evaluate model accuracy
predictions = rf_model.predict(X_test)
mae = mean_absolute_error(y_test, predictions)
print(f"Forecasting Model MAE: ${mae:.2f} (Average daily prediction error)")

# Predict the next 7 days of future cloud spend
print("\nForecasting next 7 days of cloud spend...")
last_known = ml_df.iloc[-1].copy()
forecasts = []

for i in range(1, 8):
    # Build features dynamically for the next unknown day
    next_features = pd.DataFrame({
        'Lag_1d': [last_known['Cost']],
        'Lag_7d': [ml_df.iloc[-7 + i]['Cost'] if i < 7 else forecasts[i-8]],
        'Rolling_Mean_7d': [(ml_df['Cost'].iloc[-6:].sum() + last_known['Cost']) / 7]
    })
    
    pred_cost = rf_model.predict(next_features)[0]
    forecasts.append(pred_cost)
    
    # Update last known cost for the next loop iteration
    last_known['Cost'] = pred_cost

# Export the forecast for Power BI
future_dates = [daily_spend['Date'].max() + pd.Timedelta(days=i) for i in range(1, 8)]
forecast_df = pd.DataFrame({'Date': future_dates, 'Forecasted_Cost': forecasts})
forecast_df.to_csv('cost_forecast.csv', index=False)

print("Exported cost_forecast.csv. Phase 3 Complete!")