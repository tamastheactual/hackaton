import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

# Read the interpolated CSV file
df = pd.read_csv('standard_stout_interpolated.csv')

# Convert time column to datetime
df['time'] = pd.to_datetime(df['time'])

# Create lag features: orders from 24 hours ago and 168 hours ago
df['orders_24h_ago'] = df['orders'].shift(24)  # 24 hours = 1 day
df['orders_168h_ago'] = df['orders'].shift(168)  # 168 hours = 7 days

# Find the index where we have both features available (first valid training point)
# This will be at index 168 (168 hours from start)
first_valid_idx = df[df['time'] == '2025-09-08 00:00:00'].index[0]

print(f"First training data point: {df.loc[first_valid_idx, 'time']}")
print(f"Index: {first_valid_idx}")

# Split data: training starts from first valid index
train_data = df[first_valid_idx:].copy()

# Remove any remaining NaN values (shouldn't be any, but just in case)
train_data = train_data.dropna()

print(f"\nTraining data size: {len(train_data)} samples")
print(f"Training period: {train_data['time'].min()} to {train_data['time'].max()}")

# Prepare features (X) and target (y)
X = train_data[['orders_24h_ago', 'orders_168h_ago']]
y = train_data['orders']

# Create and train the linear regression model
model = LinearRegression()
model.fit(X, y)

# Make predictions
y_pred = model.predict(X)

# Calculate Mean Absolute Error (MAE)
mae = mean_absolute_error(y, y_pred)

print("\n" + "=" * 60)
print("Linear Regression Model Results")
print("=" * 60)
print(f"\nModel coefficients:")
print(f"  orders_24h_ago coefficient: {model.coef_[0]:.4f}")
print(f"  orders_168h_ago coefficient: {model.coef_[1]:.4f}")
print(f"  Intercept: {model.intercept_:.4f}")
print(f"\nMean Absolute Error (MAE): {mae:.2f}")
print("=" * 60)

# Predict for 2025-09-29 23:00:00
# We need orders from 24 hours ago (2025-09-28 23:00:00) and 168 hours ago (2025-09-22 23:00:00)
target_time = pd.to_datetime('2025-09-29 23:00:00')
time_24h_ago = target_time - pd.Timedelta(hours=24)
time_168h_ago = target_time - pd.Timedelta(hours=168)

# Get the order values from the dataframe
orders_24h_ago = df[df['time'] == time_24h_ago]['orders'].values[0]
orders_168h_ago = df[df['time'] == time_168h_ago]['orders'].values[0]

print("\n" + "=" * 60)
print("Prediction for 2025-09-29 23:00:00")
print("=" * 60)
print(f"Orders at {time_24h_ago}: {orders_24h_ago}")
print(f"Orders at {time_168h_ago}: {orders_168h_ago}")

# Make prediction
X_new = np.array([[orders_24h_ago, orders_168h_ago]])
prediction = model.predict(X_new)[0]

print(f"\nPredicted orders for 2025-09-29 23:00:00: {prediction:.2f}")
print(f"Rounded prediction: {round(prediction)}")
print("=" * 60)
