# Zomato Data Analytics Project

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
dataframe = pd.read_csv("Zomato-data-.csv")

# Display initial rows
print("Initial Dataset Preview:")
print(dataframe.head())

# --- Data Cleaning ---
# Convert 'rate' from '4.1/5' to float

def handleRate(value):
    try:
        value = str(value).split('/')[0].strip()
        return float(value)
    except:
        return np.nan

# Apply conversion and drop NA
dataframe['rate'] = dataframe['rate'].apply(handleRate)
dataframe.dropna(subset=['rate'], inplace=True)

# Clean approx cost

def clean_cost(value):
    try:
        return int(str(value).replace(',', ''))
    except:
        return np.nan

dataframe['approx_cost(for two people)'] = dataframe['approx_cost(for two people)'].apply(clean_cost)
dataframe.dropna(subset=['approx_cost(for two people)'], inplace=True)

# --- EDA and Visualizations ---

# 1. Countplot for restaurant types
plt.figure(figsize=(10,5))
sns.countplot(x='listed_in(type)', data=dataframe)
plt.title("Number of Restaurants by Type")
plt.xlabel("Type of Restaurant")
plt.ylabel("Count")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 2. Total votes per restaurant type
plt.figure(figsize=(10,5))
grouped_data = dataframe.groupby('listed_in(type)')['votes'].sum().sort_values(ascending=False)
plt.plot(grouped_data.index, grouped_data.values, marker='o', color='green')
plt.xticks(rotation=45)
plt.title("Votes by Restaurant Type")
plt.xlabel("Type of Restaurant")
plt.ylabel("Total Votes")
plt.tight_layout()
plt.show()

# 3. Restaurant with max votes
max_votes = dataframe['votes'].max()
restaurant_with_max_votes = dataframe.loc[dataframe['votes'] == max_votes, 'name']
print("\nRestaurant(s) with the maximum votes:")
print(restaurant_with_max_votes.values)

# 4. Online order count
plt.figure(figsize=(5,4))
sns.countplot(x='online_order', data=dataframe)
plt.title("Online Order Availability")
plt.xlabel("Online Order")
plt.ylabel("Count")
plt.tight_layout()
plt.show()

# 5. Ratings distribution
plt.figure(figsize=(6,4))
plt.hist(dataframe['rate'], bins=10, color='skyblue', edgecolor='black')
plt.title("Ratings Distribution")
plt.xlabel("Rating")
plt.ylabel("Frequency")
plt.tight_layout()
plt.show()

# 6. Cost for two people
plt.figure(figsize=(6,4))
sns.boxplot(x='online_order', y='rate', data=dataframe)
plt.title("Rating vs Online Order")
plt.tight_layout()
plt.show()

# 7. Heatmap: Restaurant Type vs Online Order
plt.figure(figsize=(8,6))
pivot_table = dataframe.pivot_table(index='listed_in(type)', columns='online_order', aggfunc='size', fill_value=0)
sns.heatmap(pivot_table, annot=True, cmap='YlGnBu', fmt='d')
plt.title('Restaurant Type vs Online Order Availability')
plt.xlabel('Online Order')
plt.ylabel('Restaurant Type')
plt.tight_layout()
plt.show()
