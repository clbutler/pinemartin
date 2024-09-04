#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 21:39:19 2024

@author: chrisbutler
"""

#import packages 
import pandas as pd
import matplotlib.pyplot as plt

pm_unclean = pd.read_csv(snakemake.input[0])

#step 1 only keep certain columns
#print(pm_unclean.columns)

pm_unclean = pm_unclean[['year','decimalLatitude', 'decimalLongitude', 'identificationVerificationStatus', 'vitality', 'basisOfRecord']]

#step 2 - only keep alive sightings 
#print(pm_unclean['vitality'].unique())

pm_unclean = pm_unclean[pm_unclean['vitality'] != 'dead' ]

#step 3 - only keep human sightings
#print(pm_unclean['basisOfRecord'].unique())
pm_unclean = pm_unclean[pm_unclean['basisOfRecord'] == 'HumanObservation' ]

#step 4 - only keep verified sightings
#print(pm_unclean['identificationVerificationStatus'].unique())
pm_unclean = pm_unclean[~pm_unclean['identificationVerificationStatus'].isin(['Unconfirmed', 'Unconfirmed - plausible'])]

#step 5 - sort out dates

pm_unclean['year'] = pd.to_datetime(pm_unclean['year'], format = '%Y')
pm_unclean = pm_unclean.dropna(subset = 'year')


#set up final clean

pm_clean = pm_unclean[['year', 'decimalLongitude', 'decimalLatitude']]
pm_clean = pm_clean.rename({'year' : 'Year', 'decimalLatitude' : 'Lat',  'decimalLongitude' : 'lon'}, axis = 1)
pm_clean.to_csv(snakemake.output[0])


#initial plot
pm_plot = pm_clean.set_index('Year')
pm_plot = pm_plot.resample('Y').count()
pm_plot = pm_plot[pm_plot.index > '2000']


fix, ax = plt.subplots(figsize = (10,10))
plt.plot(pm_plot.index, pm_plot['lon'])
ax.set_xlabel('\nYear', fontsize = 15)
ax.set_ylabel('Pine Martin Sightings\n', fontsize = 15)
ax.set_title('Verified Pine Martin Sightings Since 2020', fontsize = 30)
plt.savefig(snakemake.output[1])
plt.show()









