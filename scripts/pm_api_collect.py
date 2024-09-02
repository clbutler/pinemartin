# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

#import packages 
import requests
import pandas as pd

#extract data
base_url = 'https://records-ws.nbnatlas.org/occurrences/search?q=lsid%3ANHMSYS0000080190&fq=occurrence_status%3Apresent&qc=state%3AScotland'
# Make a GET request to the API

page_size = 100  # Number of items per page
total_items = 8915  # Total number of items to retrieve
items_fetched = 0  # Counter for items fetched

# To store all items
all_items = []

while items_fetched < total_items:
    # Construct the request URL with pagination parameters
    params = {
        'limit': page_size,
        'offset': items_fetched  # Use the number of items already fetched to set offset
    }
    
    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        items = data.get('occurrences', [])  # Adjust the key based on the actual API response
        
        if not items:
            break  # Exit loop if no more items are returned

        all_items.extend(items)  # Add the new items to the list
        items_fetched += len(items)  # Update the counter
        
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        break  # Exit loop in case of failure

print(f"Total items fetched: {len(all_items)}")

df = pd.DataFrame(all_items)
df.to_csv(snakemake.output[0])

