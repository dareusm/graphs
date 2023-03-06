from typing import OrderedDict
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from sklearn.linear_model import LinearRegression
from datetime import date
import numpy as np

# Read in bikes.csv into a pandas dataframe
### Your code here
df1 = pd.read_csv("bikes.csv")
# Read in DOX.csv into a pandas dataframe
# Be sure to parse the 'Date' column as a datetime
### Your code here
df2 = pd.read_csv("DOX.csv")
df2["Date"] = pd.to_datetime(df2["Date"])
# Divide the figure into six subplots
# Divide the figure into subplots
fig, axs = plt.subplots(3, 2, figsize=(12, 12))

# Make a pie chart
### Your code here
status_data = df1["status"]
available_count = df1["status"].value_counts()["available"]
rented_count = df1["status"].value_counts()["rented"]
broken_count = df1["status"].value_counts()["broken"]
counts = [available_count, broken_count, rented_count]
names = ["available", "broken", "rented"]
total_bikes = available_count + rented_count + broken_count
available_pecent = (available_count / total_bikes) * 100
rented_percent = (rented_count / total_bikes) * 100
broken_percent = (broken_count / total_bikes) * 100
patches, texts, pcts = axs[0, 0].pie(counts, labels=names, autopct="%1.1f%%")
for i, patch in enumerate(patches):
    texts[i].set_color(patch.get_facecolor())
plt.setp(pcts, color="white")
axs[0, 0].set_title("Current Status")


# Make a histogram with quartile lines
# There should be 20 bins
### Your code here
quant_min = df1["purchase_price"].quantile(0)
quant_25 = df1["purchase_price"].quantile(0.25)
quant_50 = df1["purchase_price"].quantile(0.5)
quant_75 = df1["purchase_price"].quantile(0.75)
quant_max = df1["purchase_price"].quantile(1)
price_data = df1["purchase_price"]
# quantiles = [quant_min, quant_25, quant_50, quant_75, quant_max]
axs[0, 1].set(
    xlabel="US Dollars", ylabel="Number of Bikes", title="Price Histogram (1000 Bikes)"
)
axs[0, 1].xaxis.set_major_formatter("${x:1.0f}")
axs[0, 1].hist(price_data, bins=20, edgecolor="blue", histtype="step", fill=None)
axs[0, 1].axvline(quant_min, linestyle="dotted", color="black")
axs[0, 1].axvline(quant_25, linestyle="dotted", color="black")
axs[0, 1].axvline(quant_50, linestyle="dotted", color="black")
axs[0, 1].axvline(quant_75, linestyle="dotted", color="black")
axs[0, 1].axvline(quant_max, linestyle="dotted", color="black")
axs[0, 1].annotate("min: $280", (quant_min, 10), rotation=90, ha="left")
axs[0, 1].annotate("25%: $494", (quant_25, 10), rotation=90, ha="left")
axs[0, 1].annotate("50%: $667", (quant_50, 10), rotation=90, ha="left")
axs[0, 1].annotate("75%: $848", (quant_75, 10), rotation=90, ha="left")
axs[0, 1].annotate("max: $1,219", (quant_max, 10), rotation=90, ha="left")

# Make a scatter plot with a trend line
### Your code here
scatter_x = df1["purchase_price"]
scatter_y = df1["weight"]
# Get data as numpy arrays
X = df1["purchase_price"].values.reshape(-1, 1)
y = df1["weight"].values.reshape(-1, 1)
# Do linear regression
reg = LinearRegression()
reg.fit(X, y)
y_predict = reg.predict(X)
# Get the parameters
slope = reg.coef_[0]
intercept = reg.intercept_
print(f"Slope: {slope}, Intercept: {intercept}")

axs[1, 0].set(xlabel="Price", ylabel="Weight", title="Price vs. Weight")
axs[1, 0].xaxis.set_major_formatter("${x:1.0f}")
axs[1, 0].yaxis.set_major_formatter("{x:1.0f} kg")
axs[1, 0].scatter(scatter_x, scatter_y, s=0.5)
axs[1, 0].plot(X, y_predict, color="red")


# Make a line plot
stock_dates = df2["Date"]
stock_price_high = df2["High"]
stock_price_low = df2["Low"]
axs[1, 1].set(title="DOX")
axs[1, 1].yaxis.set_major_formatter("${x:.2f}")
axs[1, 1].grid(True)
axs[1, 1].set_yticks(
    [65, 67.50, 70.00, 72.50, 75.00, 77.50, 80.00, 82.50, 85.00, 87.50]
)
axs[1, 1].plot(stock_dates, stock_price_high)
# Make a boxplot sorted so mean values are increasing
# Hide outliers
### Your code here
brand_data = df1["brand"]
meds = price_data
purchases_grouped = price_data.groupby(brand_data).apply(list).to_dict()


brands = ["Giant", "GT", "Canyon", "Trek", "BMC", "Cdale"]
xtick_length = len(brands)

axs[2, 0].set(title="Brand vs. Price")
axs[2, 0].yaxis.set_major_formatter("${x:1.00f}")
axs[2, 0].boxplot(
    purchases_grouped.values(),
    showfliers=False,
    patch_artist=True,
    medianprops=dict(color="green"),
    boxprops=dict(fill=None),
)
axs[2, 0].grid(True, which="both")
axs[2, 0].set_xticklabels(brands)

# Make a violin plot
### Your code here
axs[2, 1].set(title="Brand vs. Price")
axs[2, 1].yaxis.set_major_formatter("${x:1.00f}")
axs[2, 1].grid = True
axs[2, 1].violinplot(purchases_grouped.values(), showmedians=True)
axs[2, 1].set_xticklabels(["Giant", "GT", "Canyon", "Trek", "BMC", "Cdale"])
# Create some space between subplots
plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.4, hspace=0.4)

# Write out the plots as an image
plt.savefig("plots.png")
plt.show()
