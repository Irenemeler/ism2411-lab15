
# ISM2411 Lab 15 — Aggregate & Chart
# Irene Meler

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

# Load the cleaned sales data
df = pd.read_csv("data/clean_sales.csv")

# Convert order_date into datetime format
df["order_date"] = pd.to_datetime(df["order_date"])

# Display the first five rows
print(df.head())

# Display information about the dataset
print(df.info())


# ==========================================
# EXERCISE 1 — Revenue by Region
# Business question: Which region generates the most revenue?
# ==========================================

# Calculate total revenue for each region
revenue_by_region = df.groupby("region")["revenue"].sum().reset_index()

# Sort revenue from highest to lowest
revenue_by_region = revenue_by_region.sort_values(
    by="revenue", ascending=False
)

# Print the results
print("\nQ1: Revenue by Region")
print(revenue_by_region)


# Create the bar chart using Seaborn
plt.figure(figsize=(10, 6))

sns.barplot(
    data=revenue_by_region,
    x="region",
    y="revenue",
    color="steelblue"
)

# Seaborn provides a different default visual style
# and makes it easy to work directly with DataFrames.
# Difference: Seaborn works directly with DataFrames
# and provides a cleaner default chart appearance.

# Add chart title and labels
plt.title("Total Revenue by Region")
plt.xlabel("Region")
plt.ylabel("Total Revenue ($)")

# Save the chart
plt.tight_layout()
plt.savefig("charts/q1_revenue_by_region.png")
plt.close()

# State the top-performing region
top_region = revenue_by_region.iloc[0]

print(
    f"{top_region['region']} generated the highest revenue "
    f"at ${top_region['revenue']:,.2f}."
)

# ==========================================
# EXERCISE 2 — Monthly Revenue Trend
# Business question: Which month generates the most revenue?
# ==========================================

# Create a month column
df["month"] = df["order_date"].dt.month

# Calculate total revenue for each month
monthly_revenue = df.groupby("month")["revenue"].sum()

# Calculate average monthly revenue
average_revenue = monthly_revenue.mean()

# Find the peak month
peak_month = monthly_revenue.idxmax()
peak_revenue = monthly_revenue.max()

# Calculate percentage above average
percentage_above_average = (
    (peak_revenue - average_revenue) / average_revenue
) * 100

# Print the results
print("\nQ2: Monthly Revenue Trend")
print(monthly_revenue)

# Create the line chart
plt.figure(figsize=(10, 6))
plt.plot(
    monthly_revenue.index,
    monthly_revenue.values,
    marker="o",
    color="darkorange"
)

# Show all 12 months
plt.xticks(range(1, 13))

# Add title and labels
plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Total Revenue ($)")

# Save the chart
plt.tight_layout()
plt.savefig("charts/q2_monthly_trend.png")
plt.close()

print(
    f"Month {peak_month} had the highest revenue at "
    f"${peak_revenue:,.2f}, which is "
    f"{percentage_above_average:.2f}% above the monthly average."
)


# ==========================================
# EXERCISE 3 — Order Size Distribution
# Business question: How are order sizes distributed?
# ==========================================

# Calculate mean and median
mean_order = df["revenue"].mean()
median_order = df["revenue"].median()

# Calculate skewness
order_skewness = df["revenue"].skew()

# Print results
print("\nQ3: Order Size Distribution")
print(f"Mean order size: ${mean_order:,.2f}")
print(f"Median order size: ${median_order:,.2f}")
print(f"Skewness: {order_skewness:.2f}")

# Create histogram
plt.figure(figsize=(10, 6))
plt.hist(df["revenue"], bins=20, color="teal", edgecolor="black")

# Add title and labels
plt.title("Distribution of Order Sizes")
plt.xlabel("Order Revenue ($)")
plt.ylabel("Number of Orders")

# Save chart
plt.tight_layout()
plt.savefig("charts/q3_order_distribution.png")
plt.close()

# Describe the distribution
if order_skewness > 0.5:
    print("The distribution is right-skewed.")
elif order_skewness < -0.5:
    print("The distribution is left-skewed.")
else:
    print("The distribution is approximately symmetric.")

# The distribution is right-skewed because a few large orders
# increase the mean above the median. A business analyst should
# use the median to understand a typical order size.


# ==========================================
# EXERCISE 4 — Custom Business Question
# Business question: Which product category generates the most revenue?
# ==========================================

# Calculate revenue by product category
revenue_by_category = (
    df.groupby("product_category")["revenue"]
    .sum()
    .sort_values(ascending=False)
)

# Print the results
print("\nQ4: Revenue by Product Category")
print(revenue_by_category)

# Create a bar chart
# A bar chart is appropriate because it makes category comparisons easy.
plt.figure(figsize=(10, 6))
plt.bar(
    revenue_by_category.index,
    revenue_by_category.values,
    color="slateblue"
)

# Add title and labels
plt.title("Total Revenue by Product Category")
plt.xlabel("Product Category")
plt.ylabel("Total Revenue ($)")
plt.xticks(rotation=30)

# Save chart
plt.tight_layout()
plt.savefig("charts/q4_custom.png")
plt.close()

# Identify the top category
top_category = revenue_by_category.idxmax()
top_category_revenue = revenue_by_category.max()

print(
    f"{top_category} generated the most revenue "
    f"at ${top_category_revenue:,.2f}."
)

# ==========================================
# EXERCISE 6 — Multiple Aggregations
# Business question: Which region has the most orders
# and the highest average order value?
# ==========================================

# Calculate revenue and order count by region
region_summary = df.groupby("region").agg(
    total_revenue=("revenue", "sum"),
    order_count=("order_id", "count")
).reset_index()

# Calculate average order value
region_summary["average_order_value"] = (
    region_summary["total_revenue"] / region_summary["order_count"]
)

# Print the results
print("\nQ6: Multiple Aggregations")
print(region_summary)

# Find the region with the most orders
most_orders_region = region_summary.loc[
    region_summary["order_count"].idxmax()
]

# Find the region with the highest average order value
highest_aov_region = region_summary.loc[
    region_summary["average_order_value"].idxmax()
]

# Answer the business questions
# The region with the most orders is the region with the highest order_count.
# The region with the highest average order value has the highest total_revenue / order_count.

print(
    f"Most orders: {most_orders_region['region']} "
    f"({most_orders_region['order_count']} orders)"
)

print(
    f"Highest average order value: {highest_aov_region['region']} "
    f"(${highest_aov_region['average_order_value']:,.2f})"
)

# ==========================================
# LAB 15 — SELF-ASSESSMENT
# ==========================================

# 1. The charts clearly show the main findings.
# The titles and labels explain what each chart represents.
# The charts make it easy to compare revenue and order sizes.

# 2. Business findings:
# The South region generated $605,454.95 in revenue.
# December generated $203,267.75, which was 27.38% above
# the average monthly revenue.
# The order distribution was right-skewed, with a mean
# of $409.32 and a median of $144.99.

# 3. The most difficult part was creating the charts and
# understanding how to group and aggregate the data.
# I learned how to use pandas, Matplotlib, and Seaborn
# to answer business questions using data.
