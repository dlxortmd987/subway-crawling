import datetime
import os
import time
from random import uniform

import pandas as pd
import requests

SKIP_ROWS = 0

csv = pd.read_csv(filepath_or_buffer="taek.csv", encoding="utf-8", sep=",", skiprows=SKIP_ROWS)


tuples = csv.itertuples()
flag = True

for idx, t in enumerate(tuples):
    start = t[1]
    goal = t[2]

    if start == goal:
        continue

    if os.path.exists('path.csv'):
        result = pd.read_csv(filepath_or_buffer="path.csv", encoding="utf-8", sep=",")
        saved_length = len(result)
        print(start, ', ', goal)

        if saved_length != 0 and idx + 1 + SKIP_ROWS < saved_length:
            continue

    params = {
        'start': start,
        'goal': goal,
        'lang': 'ko',
        'includeDetailOperation': 'true',
        'departureTime': '2023-03-30T19:00:00',
    }

    response = requests.get('https://map.naver.com/v5/api/transit/directions/subway', params=params, cookies=cookies,
                            headers=headers)

    short_paths = response.json()['paths'][0]

    arrival_time = datetime.datetime.strptime(short_paths['arrivalTime'], '%Y-%m-%dT%H:%M:%S')
    departure_time = datetime.datetime.strptime(short_paths['departureTime'], '%Y-%m-%dT%H:%M:%S')
    steps_json = short_paths['legs'][0]['steps']
    stations = []
    for step in steps_json:
        stations_json = step['stations']
        for station in stations_json:
            stations.append(station['displayName'])

    no_dup_stations = list(dict.fromkeys(stations))

    start_station = no_dup_stations[0]
    end_station = no_dup_stations[-1]
    path = "-".join(no_dup_stations)
    r_path = "-".join(reversed(no_dup_stations))
    split_time = str(arrival_time - departure_time).split(':')
    required_time = int(split_time[1]) + int(split_time[0])*60
    data = {
        "start": [start_station],
        "end": [end_station],
        "required_time": [required_time],
        "path": [path]
    }
    r_data = {
        "start": [end_station],
        "end": [start_station],
        "required_time": [required_time],
        "path": [r_path]
    }
    df = pd.DataFrame(data)
    r_df = pd.DataFrame(r_data)
    if not os.path.exists('path.csv'):
        df.to_csv('path.csv', index=False, mode='w', encoding='utf-8', header=False)
        r_df.to_csv('r_path.csv', index=False, mode='a', encoding='utf-8', header=False)
    else:
        df.to_csv('path.csv', index=False, mode='a', encoding='utf-8', header=False)
        r_df.to_csv('r_path.csv', index=False, mode='a', encoding='utf-8', header=False)
    print(df)

    rand_value = uniform(1, 2)
    time.sleep(rand_value)
