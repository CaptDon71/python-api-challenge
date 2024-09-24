#!/usr/bin/env python
# coding: utf-8

# # WeatherPy
# 
# ---
# 
# ## Starter Code to Generate Random Geographic Coordinates and a List of Cities

# In[2]:


# Dependencies and Setup
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import requests
import time
from scipy.stats import linregress

# Impor the OpenWeatherMap API key
from api_keys import weather_api_key

# Import citipy to determine the cities based on latitude and longitude
from citipy import citipy


# ### Generate the Cities List by Using the `citipy` Library

# In[3]:


# Empty list for holding the latitude and longitude combinations
lat_lngs = []

# Empty list for holding the cities names
cities = []

# Range of latitudes and longitudes
lat_range = (-90, 90)
lng_range = (-180, 180)

# Create a set of random lat and lng combinations
lats = np.random.uniform(lat_range[0], lat_range[1], size=1500)
lngs = np.random.uniform(lng_range[0], lng_range[1], size=1500)
lat_lngs = zip(lats, lngs)

# Identify nearest city for each lat, lng combination
for lat_lng in lat_lngs:
    city = citipy.nearest_city(lat_lng[0], lat_lng[1]).city_name

    # If the city is unique, then add it to a our cities list
    if city not in cities:
        cities.append(city)

# Print the city count to confirm sufficient count
print(f"Number of cities in the list: {len(cities)}")


# ---

# ## Requirement 1: Create Plots to Showcase the Relationship Between Weather Variables and Latitude
# 
# ### Use the OpenWeatherMap API to retrieve weather data from the cities list generated in the started code

# In[4]:


# Set the API base URL
url = "http://api.openweathermap.org/data/2.5/weather?"

# Define an empty list to fetch the weather data for each city
city_data = []

# Print to logger
print("Beginning Data Retrieval     ")
print("-----------------------------")

# Create counters
record_count = 1
set_count = 1

# Loop through all the cities in our list to fetch weather data
for i, city in enumerate(cities):

    # Group cities in sets of 50 for logging purposes
    if (i % 50 == 0 and i >= 50):
        set_count += 1
        record_count = 0

    # Create endpoint URL with each city
    city_url = f"{url}q={city}&appid={weather_api_key}&units=metric"


    # Log the url, record, and set numbers
    print("Processing Record %s of Set %s | %s" % (record_count, set_count, city))

    # Add 1 to the record count
    record_count += 1

    # Run an API request for each of the cities
    try:
        # Make the API request
        response = requests.get(city_url)
        city_weather = response.json()
        city_weather
        # Parse the JSON and retrieve data
        if response.status_code == 200:
            # Parse out latitude, longitude, max temp, humidity, cloudiness, wind speed, country, and date
            city_lat = city_weather['coord']['lat']
            city_lng = city_weather['coord']['lon']
            city_max_temp = city_weather['main']['temp_max']
            city_humidity = city_weather['main']['humidity']
            city_clouds = city_weather['clouds']['all']
            city_wind = city_weather['wind']['speed']
            city_country = city_weather['sys']['country']
            city_date = city_weather['dt']

            # Append the city information into city_data list
            city_data.append({
                "City": city,
                "Lat": city_lat,
                "Lng": city_lng,
                "Max Temp": city_max_temp,
                "Humidity": city_humidity,
                "Cloudiness": city_clouds,
                "Wind Speed": city_wind,
                "Country": city_country,
                "Date": city_date
            })

        else:
            print(f"City not found. Skipping {city_url}...")

    # If an error is experienced, skip the city
    except Exception as e:
        print(f"Error occurred for city {city}: {e}")
        pass

    # Pause to avoid hitting API rate limits (1 second pause)
    time.sleep(1)

# Indicate that Data Loading is complete
print("-----------------------------")
print("Data Retrieval Complete      ")
print("-----------------------------")


# In[5]:


# Convert the cities weather data into a Pandas DataFrame
city_data_df = pd.DataFrame(city_data)

# Show Record Count
city_data_df.count()


# In[6]:


# Display sample data
city_data_df.head()


# In[7]:


# Export the City_Data into a csv
city_data_df.to_csv("output_data/cities.csv", index_label="City_ID")


# In[8]:


# Read saved data
city_data_df = pd.read_csv("output_data/cities.csv", index_col="City_ID")

# Display sample data
city_data_df.head()


# ### Create the Scatter Plots Requested
# 
# #### Latitude Vs. Temperature

# In[10]:


# Build scatter plot for latitude vs. temperature
plt.scatter(city_data_df['Lat'], city_data_df['Max Temp'], edgecolor='black', marker='o')

# Incorporate the other graph properties
plt.title('City Max Latitude vs. Temperature (2024-09-24)')
plt.xlabel('Latitude')
plt.ylabel('Max Temperature (C)')
plt.grid()


# Save the figure
plt.savefig("output_data/Fig1.png")

# Show plot
plt.show()


# #### Latitude Vs. Humidity

# In[11]:


# Build the scatter plots for latitude vs. humidity
plt.scatter(city_data_df['Lat'], city_data_df['Humidity'], edgecolor='black', marker='o')

# Incorporate the other graph properties
plt.title('City Max Latitude vs. Humidity (2024-09-24)')
plt.xlabel('Latitude')
plt.ylabel('Humidity (%)')
plt.grid()


# Save the figure
plt.savefig("output_data/Fig2.png")

# Show plot
plt.show()


# #### Latitude Vs. Cloudiness

# In[13]:


# Build the scatter plots for latitude vs. cloudiness
plt.scatter(city_data_df['Lat'], city_data_df['Cloudiness'], edgecolor='black', marker='o')

# Incorporate the other graph properties
plt.title('City Max Latitude vs. Cloudiness (2024-09-24)')
plt.xlabel('Latitude')
plt.ylabel('Cloudiness (%)')
plt.grid()


# Save the figure
plt.savefig("output_data/Fig3.png")

# Show plot
plt.show()


# #### Latitude vs. Wind Speed Plot

# In[14]:


# Build the scatter plots for latitude vs. wind speed
plt.scatter(city_data_df['Lat'], city_data_df['Wind Speed'], edgecolor='black', marker='o')

# Incorporate the other graph properties
plt.title('City Max Latitude vs. Wind Speed (2024-09-24)')
plt.xlabel('Latitude')
plt.ylabel('Wind Speed (m/s)')
plt.grid()


# Save the figure
plt.savefig("output_data/Fig4.png")

# Show plot
plt.show()


# ---
# 
# ## Requirement 2: Compute Linear Regression for Each Relationship
# 

# In[16]:


# Define a function to create Linear Regression plots
def create_linear_regression_plot(x, y, ann_x, ann_y, x_label='X-axis', y_label='Y-axis', title='Linear Regression Plot'):
    # Perform linear regression using arguments 
    slope, intercept, r_value, p_value, std_err = linregress(x, y)
    value = 12345.6789
    np.set_printoptions(suppress=True)
    print(f'The r^2-value is: {r_value**2}')
    # Calculate predicted y values
    y_pred = slope * np.array(x) + intercept
    line_eq = "y = " + str(round(slope,2)) + "x + " + str(round(intercept,2))
    # Create the scatter plot
    plt.scatter(x, y, color='blue', edgecolor='black', label='Data Points')
    plt.plot(x, y_pred, color='red', linewidth=2, label='Regression Line')
    plt.annotate(line_eq,(ann_x,ann_y),fontsize=15,color="red")
    # Add titles and labels
    # title: Title of the plot (str)
    plt.title(title)
    # x_label: Label for the x-axis (str)
    plt.xlabel(x_label)
    # y_label: Label for the y-axis (str)
    plt.ylabel(y_label)
    plt.legend()
    plt.grid()

    # Show the plot
    plt.show()


# In[17]:


# Create a DataFrame with the Northern Hemisphere data (Latitude >= 0)
northern_hemi_df = city_data_df[city_data_df['Lat'] >= 0]

# Display sample data
northern_hemi_df.head()


# In[18]:


# Create a DataFrame with the Southern Hemisphere data (Latitude < 0)
southern_hemi_df = city_data_df[city_data_df['Lat'] <= 0]


# Display sample data
southern_hemi_df.head()


# ###  Temperature vs. Latitude Linear Regression Plot

# In[19]:


# Linear regression on Northern Hemisphere
create_linear_regression_plot(
    northern_hemi_df['Lat'],
    northern_hemi_df['Max Temp'],
    ann_x = 5.8, 
    ann_y = 0.1,
    x_label='Latitude',
    y_label='Max Temperature (°C)',
    title='Max Temperature vs. Latitude in the Northern Hemisphere'
)


# In[20]:


# Linear regression on Southern Hemisphere
create_linear_regression_plot(
    southern_hemi_df['Lat'],
    southern_hemi_df['Max Temp'],
    ann_x = -25, 
    ann_y = 5.8,
    x_label='Latitude',
    y_label='Max Temperature (°C)',
    title='Max Temperature vs. Latitude in the Southern Hemisphere'
)


# **Discussion about the linear relationship:** Our analysis supports that temperature decreases as one moves away from the equator, but other factors may can cause deviations from the expected linear relationship.

# ### Humidity vs. Latitude Linear Regression Plot

# In[21]:


# Northern Hemisphere
create_linear_regression_plot(
    northern_hemi_df['Lat'],
    northern_hemi_df['Humidity'],
    ann_x = 45, 
    ann_y = 20,
    x_label='Latitude',
    y_label='Humidity (%)',
    title='Humidity vs. Latitude in the Northern Hemisphere'
)


# In[22]:


# Southern Hemisphere
create_linear_regression_plot(
    southern_hemi_df['Lat'],
    southern_hemi_df['Humidity'],
    ann_x = -55, 
    ann_y = 45,
    x_label='Latitude',
    y_label='Humidity (%)',
    title='Humidity vs. Latitude in the Southern Hemisphere'
)


# **Discussion about the linear relationship:** While latitude plays a significant role in determining temperature, its impact on humidity is far less direct and more heavily moderated by local and regional factors. This leads to a weaker linear relationship between humidity and latitude in comparison to temperature and latitude.

# ### Cloudiness vs. Latitude Linear Regression Plot

# In[23]:


# Northern Hemisphere
create_linear_regression_plot(
    northern_hemi_df['Lat'],
    northern_hemi_df['Cloudiness'],
    ann_x = 46, 
    ann_y = 20,
    x_label='Latitude',
    y_label='Cloudiness (%)',
    title='Cloudiness vs. Latitude in the Northern Hemisphere'
)


# In[219]:


# Southern Hemisphere
create_linear_regression_plot(
    southern_hemi_df['Lat'],
    southern_hemi_df['Cloudiness'],
    ann_x = -55, 
    ann_y = 20,
    x_label='Latitude',
    y_label='Cloudiness (%)',
    title='Cloudiness vs. Latitude in the Southern Hemisphere'
)


# **Discussion about the linear relationship:** The linear regression analysis between cloudiness and latitude often shows little to no clear relationship. Proximity to large bodies of water or humid regions can increase cloudiness, while dry inland areas, regardless of latitude, often have less cloud cover.

# ### Wind Speed vs. Latitude Linear Regression Plot

# In[24]:


# Northern Hemisphere
create_linear_regression_plot(
    northern_hemi_df['Lat'],
    northern_hemi_df['Wind Speed'],
    ann_x = 2, 
    ann_y = 9.5,
    x_label='Latitude',
    y_label='Wind Speed m/s',
    title='Wind Speed vs. Latitude in the Northern Hemisphere'
)


# In[25]:


# Southern Hemisphere
create_linear_regression_plot(
    southern_hemi_df['Lat'],
    southern_hemi_df['Wind Speed'],
    ann_x = -55, 
    ann_y = 9,
    x_label='Latitude',
    y_label='Wind Speed m/s',
    title='Wind Speed vs. Latitude in the Southern Hemisphere'
)


# **Discussion about the linear relationship:** Global atmospheric circulation does create some regional wind patterns based on latitude, the relationship between wind speed and latitude is weak due to the strong influence of other factors. 
