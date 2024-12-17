import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from io import StringIO

# Streamlit Title
st.title("Zomato Data Analysis")

# Load the dataset
dataframe = pd.read_csv("Zomato data .csv")

# Function to handle the 'rate' column
def handleRate(value):
    value = str(value).split('/')
    value = value[0]
    try:
        return float(value)
    except ValueError:
        return np.nan  # Handle invalid values

dataframe['rate'] = dataframe['rate'].apply(handleRate)

# Display the dataset
st.write("### Dataset Preview")
st.dataframe(dataframe.head())

# Capture and display dataset info
st.write("### Dataset Info")
buffer = StringIO()  # Create a buffer to capture the output
dataframe.info(buf=buffer)  # Redirect info output to the buffer
info_output = buffer.getvalue()  # Get the string from the buffer
st.text(info_output)  # Display the info output in Streamlit

# Count plot for 'listed_in(type)'
st.write("### Type of Restaurants")
plt.figure(figsize=(10, 5))
sns.countplot(x=dataframe['listed_in(type)'])
plt.xlabel("Type of Restaurant")
plt.xticks(rotation=45)
st.pyplot(plt)

# Group by 'listed_in(type)' and sum votes
st.write("### Total Votes by Type of Restaurant")
grouped_data = dataframe.groupby('listed_in(type)')['votes'].sum()
result = pd.DataFrame({'votes': grouped_data})
plt.figure(figsize=(10, 5))
plt.plot(result, c="green", marker="o")
plt.xlabel("Type of Restaurant", c="red", size=20)
plt.ylabel("Votes", c="red", size=20)
plt.xticks(rotation=45)
st.pyplot(plt)

# Find restaurant(s) with the maximum votes
max_votes = dataframe['votes'].max()
restaurant_with_max_votes = dataframe.loc[dataframe['votes'] == max_votes, 'name']
st.write("### Restaurant(s) with the Maximum Votes:")
st.write(restaurant_with_max_votes)

# Count plot for 'online_order'
st.write("### Online Order Distribution")
plt.figure(figsize=(6, 6))
sns.countplot(x=dataframe['online_order'])
plt.title("Online Order Count")
st.pyplot(plt)

# Histogram for 'rate'
st.write("### Ratings Distribution")
plt.figure(figsize=(6, 6))
plt.hist(dataframe['rate'].dropna(), bins=5)  # Drop NaN values
plt.title("Ratings Distribution")
st.pyplot(plt)

# Count plot for 'approx_cost(for two people)'
st.write("### Approximate Cost for Two People")
plt.figure(figsize=(10, 5))
sns.countplot(x=dataframe['approx_cost(for two people)'])
plt.title("Cost Distribution")
plt.xticks(rotation=45)
st.pyplot(plt)

# Box plot for 'rate' vs 'online_order'
st.write("### Rate vs Online Order")
plt.figure(figsize=(6, 6))
sns.boxplot(x='online_order', y='rate', data=dataframe)
plt.title("Rate vs Online Order")
st.pyplot(plt)

# Heatmap for pivot table
st.write("### Heatmap of Online Order vs Type of Restaurant")
pivot_table = dataframe.pivot_table(index='listed_in(type)', columns='online_order', aggfunc='size', fill_value=0)
plt.figure(figsize=(8, 6))
sns.heatmap(pivot_table, annot=True, cmap="YlGnBu", fmt='d')
plt.title("Heatmap")
plt.xlabel("Online Order")
plt.ylabel("Listed In (Type)")
st.pyplot(plt)
