#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  8 19:29:40 2024

@author: chrisbutler
"""
#import relevant packages
import pandas as pd
import folium 
import geopandas as gpd
from shapely.geometry import Point
import matplotlib.pyplot as plt

#read files

la = gpd.read_file('inputs/local_authority_shapefiles/pub_las.shp')

la.crs

#pm = pd.read_csv('outputs/pine_martins_sightings_clean.csv')
pm = pd.read_csv(snakemake.input[0])

meanlat = pm['Lat'].mean()
meanlon = pm['lon'].mean()

#convert the longitude and latitude points to a point geometry

points = [Point(xy) for xy in zip(pm['lon'], pm['Lat'])]

#create a geodata frame

pm_gdf = gpd.GeoDataFrame(pm, geometry = points)

#check the geometries 

# Set CRS for pm_gdf (assuming EPSG:4326 for lat/lon)
pm_gdf.set_crs("EPSG:4326", inplace = True)

# Reproject pm_gdf to match the CRS of `la`
pm_gdf = pm_gdf.to_crs(la.crs)


joined = gpd.sjoin(pm_gdf, la, predicate='within')

counts_per_county = joined.groupby('local_auth').size().reset_index(name = 'sightings_per_county')

joined_counts = pd.merge(la, counts_per_county, how = 'left', on = 'local_auth')
joined_counts = joined_counts.fillna(0)


# Create a Folium map centered around the mean latitude and longitude
m = folium.Map([meanlat, meanlon], zoom_start=7)

# Add a Choropleth layer to the map
folium.Choropleth(
    geo_data=joined_counts,              # GeoJSON data
    data=joined_counts,                 # DataFrame with the data
    columns=['local_auth', 'sightings_per_county'],  # Columns to use
    key_on='feature.properties.local_auth', # Property in GeoJSON to match DataFrame
    legend_name= 'Count of Pine Martin Sightings',
    line_width=2                        # Width of borders
).add_to(m)

# Save the map to an HTML file
m.save(snakemake.output[0])
