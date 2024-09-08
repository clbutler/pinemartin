

import requests
import pandas as pd

#User Input

i_year =  input('What year do you wish to investgate?').strip()

if len(i_year) != 4:
    print('Please ensure you put your year in YYYY format')
else:
    
    # Base URL
    base_url = 'https://records-ws.nbnatlas.org/occurrences/search'

    # Initial parameters
    params = {
        'q': 'lsid:NHMSYS0000080190',
        'fq': 'year:' + str(i_year),
        'qc': 'state:Scotland',
        'limit': 100  # Number of records per page
    }
    
    # Initialize
    all_records = []
    offset = 0
    total_records = None
    
    while True:
        # Update the offset parameter
        params['offset'] = offset
    
        # Fetch data
        response = requests.get(base_url, params=params)
        data = response.json()
    
        # Extract records
        occurrences = data.get('occurrences', [])
        if not occurrences:
            break  # Exit loop if no more records are returned
    
        all_records.extend(occurrences)
    
        # Update offset and total_records
        offset += len(occurrences)
    
        # Check if we have fetched all records
        if total_records is None:
            total_records = data.get('totalRecords')
    
        # Check if we have fetched all the records
        if len(all_records) >= total_records:
            break
    
    # Convert to DataFrame
    df = pd.DataFrame(all_records)
    
    df.to_csv(snakemake.output[0])
    
    
    
    print(f"Total records fetched: {len(df)}")
