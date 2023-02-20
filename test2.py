import pandas as pd

from itertools import combinations


# csv_input = pd.read_csv(filepath_or_buffer="서울교통공사 노선별 지하철역 정보.csv", encoding="cp949", sep=",")
#
# stations = list(csv_input['전철역명'])
#
# com = list(combinations(stations, 2))
#
# n = len(com)//3
#
# teak_com = com[:n]
# sun_com = com[n+1:2*n]
# hwan_com = com[2*n+1:]
#
# # taek_frame = pd.DataFrame(teak_com, columns=['start', 'end'])
# sun_frame = pd.DataFrame(sun_com, columns=['start', 'end'])
# hwan_frame = pd.DataFrame(hwan_com, columns=['start', 'end'])
#
# # taek = taek_frame.to_csv('taek.csv', index=False, encoding='cp949')
# sun = sun_frame.to_csv('sum.csv', index=False, encoding='cp949')
# hwan = hwan_frame.to_csv('hwan.csv', index=False, encoding='cp949')

def getDateset():
    return pd.read_csv(filepath_or_buffer="taek.csv", encoding="cp949", sep=",")


def test(start, end):
    print(start, ', ', end)


def run():
    dataset = getDateset()
    dataset = dataset[1]
    for row in dataset.itertuples():
        test(row[0], row[1])


run()



