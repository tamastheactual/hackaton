import pandas as pd

# Read the interpolated CSV file
df = pd.read_csv('standard_stout_interpolated.csv')

# Convert time column to datetime
df['time'] = pd.to_datetime(df['time'])

# Extract just the date (day) from the datetime
df['date'] = df['time'].dt.date

# Group by date and sum the orders for each day
daily_orders = df.groupby('date')['orders'].sum().reset_index()

# Sort by orders descending and get top 5
top_5_days = daily_orders.sort_values('orders', ascending=False).head(5)

print("Top 5 Most Popular Days:")
print("=" * 50)
for idx, row in top_5_days.iterrows():
    print(f"{row['date']}: {row['orders']} orders")

print("\n" + "=" * 50)
print(f"Total orders across all days: {daily_orders['orders'].sum()}")

# Sum the total beer for the top 5 days
top_5_total = top_5_days['orders'].sum()
print(f"\nTotal orders for the top 5 days: {top_5_total}")
