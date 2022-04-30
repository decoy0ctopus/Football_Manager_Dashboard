# -*- coding: utf-8 -*-
"""
Created on Wed 08 Dec 21 

@author: Patrick Robinson
"""
# Importing the initial libraries

import numpy as np
import pandas as pd
import certifi
import ssl
import geopy.geocoders
from geopy.geocoders import Nominatim, GoogleV3
from geopy.exc import GeocoderTimedOut
import googlemaps 
from meteostat import Point, Daily

# Importing the excel dataset

init_dataset = pd.read_excel('C:/Users/pater/OneDrive/Education/STT/Ronseal football league dataset.xlsx')

# Remove spaces from columns

init_dataset.columns = init_dataset.columns.str.replace(' ', '_')

# Remove rows with na or 0 in games played, as there's no useful data if a game hasn't been played

dataset = init_dataset
dataset['Games_Played'] = dataset['Games_Played'].replace(0, np.nan)
dataset = dataset.dropna(subset=['Games_Played'])

#Replace incorrect spelling of Ipswich

dataset['Team'] = dataset['Team'].replace("Ipswitch", "Ipswich")

# Add columns for games won, net goals, goals scored per match and goals conceded per match, net games won

dataset['Games_Won'] = dataset['Games_Played'] - dataset['Games_Against']
dataset['Net_Goals'] = dataset['Goals_Scored'] - dataset['Goals_Against']
dataset['Goals_For_Per_Match'] = dataset['Goals_Scored'] / dataset['Games_Played']
dataset['Goals_Against_Per_Match'] = dataset['Goals_Against'] / dataset['Games_Played']
dataset['Net_Games_Won'] = dataset['Games_Won'] - dataset['Games_Against']
dataset['address'] = dataset['Team']+", "+dataset["County"]+", "+dataset["Country"]

# Group by team and count the sum of wins, losses, goals against and goals scored

group_by_team = dataset.groupby("Team")[
    "Team", "Games_Won", "Games_Against", "Goals_Against", 'Goals_Scored'].sum()

#GEOVISUALISATION : 

#Set up Google Maps Client

gmaps = googlemaps.Client(key='AIzaSyDffa_ftCQ0jMX_13j6zbNwxHaWu4Ri7KQ')  

#Set up Nominatim Geocoding API

ctx = ssl.create_default_context(cafile=certifi.where())
geopy.geocoders.options.default_ssl_context = ctx
Nom = Nominatim(scheme = 'http', user_agent='Test Application2')

# Geocode team names to get location data iot plot on a map

geolocator = GoogleV3(api_key='AIzaSyDffa_ftCQ0jMX_13j6zbNwxHaWu4Ri7KQ')

#Add address column to assist wth geocoding

dataset['address'] = dataset['Team']+", "+dataset["County"]+", "+dataset["Country"]

#function 'my_geocoder' for calling Google geocoding API on a row, returning the Latitude and Longitude

def my_geocoder(row):
    try:
        point = geolocator.geocode(row, timeout=None).point
        return pd.Series({'Latitude': point.latitude, 'Longitude': point.longitude})
    except GeocoderTimedOut as e:
        print("Error: geocode failed on input %s with message %s"%(row, str(e)))

# Apply my_geocoder function on address column for all rows in dataset
        
dataset[['Latitude', 'Longitude']] = dataset.apply(lambda x: my_geocoder(x['address']), axis=1)

#drop locations that haven't been able to be found

dataset = dataset.loc[~np.isnan(dataset["Latitude"])]

# Our home location
hereford_united_loc = (52, -2.7)

# Consult Google Maps API to get distance and duration from Hereford for each Lat and Long

# Blank list to append API output dictionary to

distance_list = [] 

# Iterate through rows, calling Google Maps API getting distance and duration from Hereford, then append to dictionary

for index, row in dataset.iterrows():
    distance_dict_new = gmaps.distance_matrix((row['Latitude'], row['Longitude']),
                                              hereford_united_loc, mode='driving')['rows'][0]['elements'][0]
    distance_list.append(distance_dict_new)
 
# Expand dictionary to get data into dataframe
    
distance_df = pd.DataFrame(distance_list)
distance_df = distance_df.apply(pd.Series)
distance_df = distance_df.apply(pd.Series)

# Reset index to merge two dataframes

dataset.reset_index(drop=True, inplace=True)

# Concat the two dataframes horizontally

dataset = pd.concat([dataset, distance_df], axis=1)
dataset = pd.concat([dataset.drop(['distance'], axis=1), dataset['distance'].apply(pd.Series)], axis=1)
dataset = pd.concat([dataset.drop(['duration'], axis=1), dataset['duration'].apply(pd.Series)], axis=1)

# WEATHER DATA

# Blank list to append Weather API output dictionary to

wx_dict = []

# Iterate through rows, calling MeteoStat API 'daily' getting Wx and Temp data for the given point at the given date

for index, row in dataset.iterrows():
    wx_dict_new = Daily(Point(row['Latitude'], row['Longitude']), start = row['Date'],
                        end = row['Date']).fetch()
    wx_dict.append(wx_dict_new)
    
# Turn list of dictionaries into a dataset
    
wx_dict = pd.concat(wx_dict)

# Reset indexes and then merge the Weather API dataframe with our original dataset

dataset.reset_index(drop=True, inplace=True)
wx_dict.reset_index(drop=True, inplace=True)
dataset_inc_wx = pd.concat([dataset, wx_dict], axis = 1)

#Get correlation dataframe using corr() function

corr = dataset.corr()




