"""
This script converts the csv dataframe into a json dictionary object
"""

import pandas as pd
import json

# Read the csv data into a dataframe
spotifyTop50 = pd.read_csv("./top50.csv", 
                            encoding = "latin",
                            skiprows = 1,
                            names = ['_id', 'Track Name', 'Artist Name', 'Genre', 'Beats Per Minute',
                                        'Energy', 'Danceability', 'Loudness dB', 'Liveness', 'Valence',
                                        'Length', 'Acousticness', 'Speechiness', 'Popularity'])

types = [int, str, str, str, float, float, float, float, float, float, float, float, float, float]

records = []

# Save the individual entries as a list of dictionaries
for idx in range(len(spotifyTop50)):
    record = spotifyTop50.iloc[idx, :].to_dict()

    for tp, (k, v) in zip(types, record.items()):
        record[k] = [x for x in map(tp, [v])][0]

    records.append(record)

# Save the dictionaries to a json file
with open("spotifyTop50.json", "w") as f:
    json.dump(records, f)
    f.close()