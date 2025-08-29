import pandas as pd

# Step 1: Read all 3 CSV files
data0 = pd.read_csv("data/daily_sales_data_0.csv")
data1 = pd.read_csv("data/daily_sales_data_1.csv")
data2 = pd.read_csv("data/daily_sales_data_2.csv")

# Step 2: Combine them into one dataset
all_data = pd.concat([data0, data1, data2])

# Step 3: Filter only "pink morsel" product
pink_data = all_data[all_data["product"] == "pink morsel"]

# Step 4: Convert price (remove $ sign and convert to float)
pink_data["price"] = pink_data["price"].replace('[\$,]', '', regex=True).astype(float)

# Step 5: Calculate revenue (price × quantity)
pink_data["sales"] = pink_data["price"] * pink_data["quantity"]

# Step 6: Keep only useful columns
final_data = pink_data[["date", "region", "sales"]]

# Step 7: Save to CSV
final_data.to_csv("output.csv", index=False)

print("✅ Task completed! Filtered data saved as output.csv")
