#!/usr/bin/env python
# coding: utf-8

# # VacationPy
# ---
# 
# ## Import Libraries and Load the Weather and Coordinates Data

# In[1]:


# Dependencies and Setup
import hvplot.pandas
import json

import pandas as pd
import requests
from requests.structures import CaseInsensitiveDict

# Import API key
from api_keys import geoapify_key


# In[2]:


# Load the CSV file created in Part 1 into a Pandas DataFrame
city_data_df = pd.read_csv("output_data/cities.csv")

# Display sample data
city_data_df.head()


# ---
# 
# ### Step 1: Create a map that displays a point for every city in the `city_data_df` DataFrame. The size of the point should be the humidity in each city.

# In[4]:


get_ipython().run_cell_magic('capture', '--no-display', "\n# Configure the map plot\n# Activate the Geo extension\nhvplot.extension('bokeh')\n# Configure the map plot_1\nmap_plot = city_data_df.hvplot.points(\n    'Lng', 'Lat', \n    geo=True,\n    color='City', \n    size='Humidity', \n    tiles='OSM', \n    hover_cols=['City', 'Humidity']\n\n)\n# Display the map\nmap_plot\n")


# ### Step 2: Narrow down the `city_data_df` DataFrame to find your ideal weather condition

# In[5]:


# Narrow down cities that fit criteria and drop any results with null values
# Filter cities based on the given criteria
filtered_cities = city_data_df[
    (city_data_df['Max Temp'] > 21) & (city_data_df['Max Temp'] < 27) &
    (city_data_df['Wind Speed'] < 4.5) &
    (city_data_df['Cloudiness'] == 0)
]


# Drop any rows with null values
filtered_cities = filtered_cities.dropna()


# Display sample data
filtered_cities


# ### Step 3: Create a new DataFrame called `hotel_df`.

# In[6]:


# Use the Pandas copy function to create DataFrame called hotel_df to store the city, country, coordinates, and humidity
# Create a new DataFrame 'hotel_df' using the copy function
hotel_df = filtered_cities[['City', 'Country', 'Lat', 'Lng', 'Humidity']].copy()

# Add an empty column, "Hotel Name," to the DataFrame so you can store the hotel found using the Geoapify API
hotel_df['Hotel Name'] = ""

# Display sample data
hotel_df


# ### Step 4: For each city, use the Geoapify API to find the first hotel located within 10,000 metres of your coordinates.

# In[7]:


# Set parameters to search for a hotelimport requests
radius = 10000  # Set radius in meters

# Prepare the params dictionary outside of the loop
params = {
    "categories": "accommodation.hotel",
    "limit": 1,  # Limit to one result for simplicity
    "apiKey": geoapify_key  # Your API key
}

# Print a message to follow up the hotel search
print("Starting hotel search")

# Iterate through the hotel_df DataFrame
for index, row in hotel_df.iterrows():
    # Get latitude and longitude from the DataFrame
    lat = row['Lat']  # Get latitude from the 'Lat' column
    lng = row['Lng']  # Get longitude from the 'Lng' column

    # Add the current city's latitude and longitude to the params dictionary
    params["filter"] = f"circle:{lng},{lat},{radius}"  # Circle around coordinates with the radius
    params["bias"] = f"proximity:{lng},{lat}"  # Bias the results towards the specified coordinates

    # Set base URL
    base_url = "https://api.geoapify.com/v2/places"

    # Make an API request using the params dictionary
    response = requests.get(base_url, params=params)

    # Convert the API response to JSON format
    name_address = response.json()

    # Grab the first hotel from the results and store the name in the hotel_df DataFrame
    try:
        hotel_df.loc[index, "Hotel Name"] = name_address["features"][0]["properties"]["name"]
    except (KeyError, IndexError):
        # If no hotel is found, set the hotel name as "No hotel found".
        hotel_df.loc[index, "Hotel Name"] = "No hotel found"

    # Log the search results
    print(f"{hotel_df.loc[index, 'City']} - nearest hotel: {hotel_df.loc[index, 'Hotel Name']}")

# Display sample data
hotel_df


# ### Step 5: Add the hotel name and the country as additional information in the hover message for each city in the map.

# In[8]:


get_ipython().run_cell_magic('capture', '--no-display', "\n# Configure the map plot\n# Create the city map with hover information\ncity_map = hotel_df.hvplot.points(\n    'Lng', 'Lat',\n    geo=True,\n    tiles='OSM',\n    size='Humidity',  # Size of the points based on humidity\n    color='City',\n    hover_cols=['City', 'Country', 'Hotel Name'],  # Hover information\n    title='City Map with Hotels'\n)\n\n# Display the map\ncity_map\n")


# In[ ]:




