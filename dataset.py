from itertools import combinations

import pandas as pd

csv = pd.read_csv(filepath_or_buffer="서울교통공사 노선별 지하철역 정보.csv", encoding="cp949", sep=",")

station_set = set(csv['전철역명'])

dataset = list(set(combinations(station_set, 2)))

n = len(dataset) // 3

taek_dataset = dataset[:n]
hwan_dataset = dataset[n+1:2*n]
sun_dataset = dataset[2*n+1:]

taek_dataFrame = pd.DataFrame(taek_dataset)
hwan_dataFrame = pd.DataFrame(hwan_dataset)
sun_dataFrame = pd.DataFrame(sun_dataset)

taek_dataFrame.to_csv('taek.csv', index=False)
hwan_dataFrame.to_csv('hwan.csv', index=False)
sun_dataFrame.to_csv('sun.csv', index=False)