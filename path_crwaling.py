import ast
import datetime
import json
import os
import time
from random import uniform

import pandas as pd
import requests

SKIP_ROWS = 97050

cookies = {
    'NNB': 'SX7OOPZCUPQGG',
    'nx_ssl': '2',
    'nid_inf': '1108721644',
    'NID_AUT': 'dOQU/s9qAxw/MpWU9/zqnani0MuzpR/6zVir2BP2DMt/dSxuP2YHJf2u9xm1M7u/',
    'NID_JKL': 'rfufteyRJQ/9vY21VDfODy2srktLmpP4t/2dghcDiBY=',
    'NID_SES': 'AAABi3d7bpKO42ldT/mkBq4BilQnL2rXxo6OJ9vBiAo6+k+rCw3rVtkvTn6Tc+9tGK5UKylwHrcUKj8FC812m9X/jcTrq7gElOOKyDLKKlo+4kA25byIPTcNm+gaz3M9t+ymiVNklVuCnyEFNOB5z8acsxTw7oD7cMaNrU97oDMgV2gSbgX6vodOhZFcSe+aQm78VAOU6SC2t5oxMEm1TET2/76WAI6TWRvPmxp6YqD/Izfxhs1Z8bht1ZBWSwe0tPM5zSV6lQnAokA099VzamGkhMx8Nl2Ap/WQkvy9Ih2v8PYWvrSFr0kb4anzDhIpdV9c1AtmQcvo49/7mtutWSqd8YCQqIIjv6Zg6Xh9liseeq464lDxqmKOWY6txVLqGOYoZfvOKTCdATMVCSmMLxI9SLEC3JHbTXEKyQhAEZfYqSdEL04RYDCm47MCMV2Uc4UOIgxzyMuH5cOeFm0jlu6myAIcHKM8wsovXWlXdpiYOLbcLx5p0aEM9vqEV+UZO0K87C4nOeA5sloPaq/rweGSqRg=',
    'page_uid': '8a1d209f-7216-4f9f-8cb6-6eb8d32b9bc7',
    'csrf_token': '74e00d82594d87cde744f8fe18077b5ed7cdbc3ea75dbb3f9ee1aeb2442bd76da341cf81644487d7f7cb3c14623aea0051dfe61ba5dc28091c91d966d70ecb47',
    'BMR': 's=1677168324802&r=https%3A%2F%2Fm.blog.naver.com%2FPostView.naver%3FisHttpsRedirect%3Dtrue%26blogId%3Dbkpark94%26logNo%3D220226951442&r2=https%3A%2F%2Fwww.google.com%2F',
}

headers = {
    'authority': 'map.naver.com',
    'accept': '*/*',
    'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7,de-AT;q=0.6,de;q=0.5,zh-CN;q=0.4,zh-TW;q=0.3,zh;q=0.2',
    'referer': 'https://map.naver.com/',
    'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
}

if SKIP_ROWS == 0:
    csv = pd.read_csv(filepath_or_buffer="taek.csv", encoding="utf-8", sep=",")
else:
    csv = pd.read_csv(filepath_or_buffer="taek.csv", encoding="utf-8", sep=",", skiprows=SKIP_ROWS)

tuples = csv.values
flag = True

for idx, t in enumerate(tuples):
    start_json = ast.literal_eval(t[0])
    goal_json = ast.literal_eval(t[1])
    start = int(start_json['id'])
    start_name = start_json['name']
    goal = int(goal_json['id'])
    goal_name = goal_json['name']

    if start == goal:
        continue

    if os.path.exists('path.csv'):
        result = pd.read_csv(filepath_or_buffer="path.csv", encoding="utf-8", sep=",")
        saved_length = len(result) + 1
        print(start, ', ', goal)

        if saved_length != 0 and idx + SKIP_ROWS < saved_length:
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

    time.sleep(0.05)

    short_paths = response.json()['paths'][0]

    arrival_time = datetime.datetime.strptime(short_paths['arrivalTime'], '%Y-%m-%dT%H:%M:%S')
    departure_time = datetime.datetime.strptime(short_paths['departureTime'], '%Y-%m-%dT%H:%M:%S')
    steps_json = short_paths['legs'][0]['steps']
    stations = []
    for step in steps_json:
        stations_json = step['stations']
        for station in stations_json:
            stations.append(station['displayName'])

    start_station = stations[0]
    end_station = stations[-1]
    path = "-".join(stations)
    r_path = "-".join(reversed(stations))
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

    rand_value = uniform(0.01, 0.2)
    time.sleep(rand_value)