import json
from itertools import combinations

import pandas as pd

with open("station_id.json", "r", encoding="utf-8") as f:
    contents = f.read()
    json_data = json.loads(contents)

stations = []
undefined_stations = []

for station in json_data:
    stations.append(station['id'])
print(stations)

dataset = list(combinations(stations, 2))

final = []

for data in dataset:
    if data[0] != data[1]:
        final.append(data)

n = len(final) // 3

taek_dataset = dataset[:n]
hwan_dataset = dataset[n+1:2*n]
sun_dataset = dataset[2*n+1:]

taek_dataFrame = pd.DataFrame(taek_dataset)
hwan_dataFrame = pd.DataFrame(hwan_dataset)
sun_dataFrame = pd.DataFrame(sun_dataset)

taek_dataFrame.to_csv('taek.csv', encoding='utf-8', index=False)
hwan_dataFrame.to_csv('hwan.csv', encoding='utf-8', index=False)
sun_dataFrame.to_csv('sun.csv', encoding='utf-8', index=False)