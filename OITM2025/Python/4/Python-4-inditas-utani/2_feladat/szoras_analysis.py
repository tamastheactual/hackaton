import pandas as pd
import numpy as np

# Read the interpolated CSV file
df = pd.read_csv('standard_stout_interpolated.csv')

# Calculate standard deviation (szórás) of the original hourly data
original_std = df['orders'].std()

# Calculate 24-hour moving average
df['smoothed'] = df['orders'].rolling(window=24, center=True).mean()

# Remove NaN values from smoothed data for std calculation
smoothed_data = df['smoothed'].dropna()

# Calculate standard deviation (szórás) of the smoothed data
smoothed_std = smoothed_data.std()

print("=" * 60)
print("Standard Deviation (Szórás) Analysis")
print("=" * 60)
print(f"\nOriginal hourly data szórás: {original_std:.2f}")
print(f"Smoothed (24h moving avg) szórás: {smoothed_std:.2f}")
print(f"\nReduction in szórás: {original_std - smoothed_std:.2f}")
print(f"Reduction percentage: {((original_std - smoothed_std) / original_std * 100):.2f}%")
print("=" * 60)
