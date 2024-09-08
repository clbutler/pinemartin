#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 22:55:08 2024

@author: chrisbutler
"""

import folium
import pandas as pd 


#pm_map = pd.read_csv('../outputs/pine_martins_sightings_clean.csv')

pm_map = pd.read_csv(snakemake.input[0])

pm_map['Year'] = pd.to_datetime(pm_map['Year'])
pm_map['label'] = pm_map['Year'].dt.year.astype(str)




#add the midpoints

lat_midpoint = pm_map['Lat'].mean()
lon_midpoint = pm_map['lon'].mean()

#create first map centred on midpoints

m = folium.Map(location = (lat_midpoint,lon_midpoint), zoom_start = 7)


#Take the last 100 sightings 
pm_map = pm_map.sort_values(by = 'Year', ascending = False)


for i, row in pm_map.iterrows():
    folium.Marker(
        location = [row['Lat'], row['lon']],
        icon=folium.Icon(color='green', prefix = 'fa', icon='binoculars'), 
                         tooltip = row['label']).add_to(m)


#

m.save(snakemake.output[0])



