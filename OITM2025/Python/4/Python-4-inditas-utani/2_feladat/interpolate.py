import pandas as pd
import numpy as np

df = pd.read_csv('standard_stout.csv')
df['orders'] = pd.to_numeric(df['orders'], errors='coerce')
df['orders'] = df['orders'].interpolate(method='linear')
df['orders'] = df['orders'].round(0).astype(int)

df.to_csv('standard_stout_interpolated.csv', index=False)

print(f"\nStatistics:")
print(f"Min orders: {df['orders'].min()}")
print(f"Max orders: {df['orders'].max()}")
print(f"Mean orders: {df['orders'].mean():.2f}")

total_orders = df['orders'].sum()
print(f"\n--- Total Orders in 4 Weeks ---")
print(f"Total orders: {total_orders}")
