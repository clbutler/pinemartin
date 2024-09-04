######## snakemake preamble start (automatically inserted, do not edit) ########
import sys;sys.path.extend(['/Users/chrisbutler/anaconda3/envs/pine_martin/lib/python3.12/site-packages', '/Users/chrisbutler/Documents/pine_martin', '/Users/chrisbutler/anaconda3/envs/pine_martin/bin', '/Users/chrisbutler/anaconda3/envs/pine_martin/lib/python3.12', '/Users/chrisbutler/anaconda3/envs/pine_martin/lib/python3.12/lib-dynload', '/Users/chrisbutler/anaconda3/envs/pine_martin/lib/python3.12/site-packages', '/Users/chrisbutler/anaconda3/envs/pine_martin/lib/python3.12/site-packages/setuptools/_vendor', '/Users/chrisbutler/Library/Caches/snakemake/snakemake/source-cache/runtime-cache/tmpdofgee4_/file/Users/chrisbutler/Documents/pine_martin/scripts', '/Users/chrisbutler/Documents/pine_martin/scripts']);import pickle;from snakemake import script;script.snakemake = pickle.loads(b'\x80\x04\x95\xb6\x03\x00\x00\x00\x00\x00\x00\x8c\x10snakemake.script\x94\x8c\tSnakemake\x94\x93\x94)\x81\x94}\x94(\x8c\x05input\x94\x8c\x0csnakemake.io\x94\x8c\nInputFiles\x94\x93\x94)\x81\x94\x8c"outputs/pine_martins_sightings.csv\x94a}\x94(\x8c\x06_names\x94}\x94\x8c\x12_allowed_overrides\x94]\x94(\x8c\x05index\x94\x8c\x04sort\x94eh\x10h\x06\x8c\x0eAttributeGuard\x94\x93\x94)\x81\x94}\x94\x8c\x04name\x94h\x10sbh\x11h\x13)\x81\x94}\x94h\x16h\x11sbub\x8c\x06output\x94h\x06\x8c\x0bOutputFiles\x94\x93\x94)\x81\x94\x8cOoutputs/pine_martins_sightings_clean.csvoutputs/pine_martins_sightings_plot.pdf\x94a}\x94(h\x0c}\x94h\x0e]\x94(h\x10h\x11eh\x10h\x13)\x81\x94}\x94h\x16h\x10sbh\x11h\x13)\x81\x94}\x94h\x16h\x11sbub\x8c\x06params\x94h\x06\x8c\x06Params\x94\x93\x94)\x81\x94}\x94(h\x0c}\x94h\x0e]\x94(h\x10h\x11eh\x10h\x13)\x81\x94}\x94h\x16h\x10sbh\x11h\x13)\x81\x94}\x94h\x16h\x11sbub\x8c\twildcards\x94h\x06\x8c\tWildcards\x94\x93\x94)\x81\x94}\x94(h\x0c}\x94h\x0e]\x94(h\x10h\x11eh\x10h\x13)\x81\x94}\x94h\x16h\x10sbh\x11h\x13)\x81\x94}\x94h\x16h\x11sbub\x8c\x07threads\x94K\x01\x8c\tresources\x94h\x06\x8c\tResources\x94\x93\x94)\x81\x94(K\x01K\x01\x8c0/var/folders/1z/9q2sbs594sj783bxhkj9gfl80000gn/T\x94e}\x94(h\x0c}\x94(\x8c\x06_cores\x94K\x00N\x86\x94\x8c\x06_nodes\x94K\x01N\x86\x94\x8c\x06tmpdir\x94K\x02N\x86\x94uh\x0e]\x94(h\x10h\x11eh\x10h\x13)\x81\x94}\x94h\x16h\x10sbh\x11h\x13)\x81\x94}\x94h\x16h\x11sbhCK\x01hEK\x01hGh@ub\x8c\x03log\x94h\x06\x8c\x03Log\x94\x93\x94)\x81\x94}\x94(h\x0c}\x94h\x0e]\x94(h\x10h\x11eh\x10h\x13)\x81\x94}\x94h\x16h\x10sbh\x11h\x13)\x81\x94}\x94h\x16h\x11sbub\x8c\x06config\x94}\x94\x8c\x04rule\x94\x8c\x1bclean_pine_martin_sightings\x94\x8c\x0fbench_iteration\x94N\x8c\tscriptdir\x94\x8c0/Users/chrisbutler/Documents/pine_martin/scripts\x94ub.');del script;from snakemake.logging import logger;from snakemake.script import snakemake; logger.printshellcmds = False;__real_file__ = __file__; __file__ = '/Users/chrisbutler/Documents/pine_martin/scripts/pm_api_collect.py';
######## snakemake preamble end #########
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

