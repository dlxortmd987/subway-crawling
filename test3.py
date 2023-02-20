import os
import re
import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup

LAST_SUBWAY_RADIO_BUTTON_XPATH = '//*[@id="container"]/shrinkable-layout/div/subway-layout/subway-home-layout/div[1]/div/subway-directions-list/subway-directions-options/div/ul/li[2]/label'

FIRST_SUBWAY_RADIO_BUTTON_XPATH = '//*[@id="container"]/shrinkable-layout/div/subway-layout/subway-home-layout/div[1]/div/subway-directions-list/subway-directions-options/div/ul/li[1]/label'

STATIONS_SELECTOR = '#container > shrinkable-layout > div > subway-layout > subway-home-layout > div.sub > subway-directions-details > div > div > ul > li.item_route.type_subway1.ng-star-inserted > ul > li:nth-child'

DETAIL_VIEW_XPATH = '//*[@id="container"]/shrinkable-layout/div/subway-layout/subway-home-layout/div[1]/div/subway-directions-list/div/div[1]/div[2]/button'

ROUTE_SELECTOR = '#container > shrinkable-layout > div > subway-layout > subway-home-layout > div.sub > subway-directions-details > div > div > ul'

REQUIRED_TIME_SELECTOR = "#container > shrinkable-layout > div > subway-layout > subway-home-layout > div.main > div > subway-directions-list > div > div.direction_summary_area.active.ng-star-inserted > div.summary_area > div > strong"

ROUTE_XPATH = '//*[@id="container"]/shrinkable-layout/div/subway-layout/subway-home-layout/div[2]/subway-directions-details/div/div/ul'

REQUIRED_TIME_XPATH = '//*[@id="container"]/shrinkable-layout/div/subway-layout/subway-home-layout/div[2]/subway-directions-details/div/div/div/div/strong'

END_STATION_BUTTON_XPATH = '//*[@id="container"]/shrinkable-layout/div/subway-layout/subway-home-layout/div[1]/subway-control-panel/div/subway-input-control/div[1]/ul/li[2]/subway-input-control-item/div/subway-search-list/div/ul/li[1]/a'

START_STATION_BUTTON_XPATH = '//*[@id="container"]/shrinkable-layout/div/subway-layout/subway-home-layout/div[1]/subway-control-panel/div/subway-input-control/div[1]/ul/li[1]/subway-input-control-item/div/subway-search-list/div/ul/li/a'

STATION_INPUT_DELAY = 1

DIRECTION_SEC = 0.5


def convert_to_minute(required_time_str):  # 예: 2시간 4분
    if "시간" in required_time_str:
        temp = required_time_str.strip("분").split("시간")
        return int(temp[0]) * 60 + int(temp[1])
    return int(required_time_str.strip("분"))


def calc_stations(array):
    count = 0
    stations = []  # 출발역 ~ 도착역 (환승역 포함)

    for element in array:
        text = element.text.strip()

        if start in text:
            count += 1

        if count == 4:  # 4 고정
            if "정차역" in text or \
                    "방면" in text or \
                    "역 이동" in text:
                continue
            else:
                split_ = text.split(" ")[0]
                if split_ not in stations:
                    stations.append(split_)

        if end in text and count == 4:
            break

    return stations


def set_start_station(start_station, chrome_driver):
    chrome_driver.find_element(By.ID, 'input_search_0').send_keys(start_station)
    time.sleep(STATION_INPUT_DELAY)
    chrome_driver.find_element(By.XPATH, START_STATION_BUTTON_XPATH).send_keys(Keys.ENTER)


### main
def set_end_station(end_station, chrome_driver):
    chrome_driver.find_element(By.ID, 'input_search_1').click()
    chrome_driver.find_element(By.ID, 'input_search_1').send_keys(end_station)
    time.sleep(STATION_INPUT_DELAY)
    chrome_driver.find_element(By.XPATH, END_STATION_BUTTON_XPATH).send_keys(Keys.ENTER)
    time.sleep(2)


def get_soup(chrome_driver):
    chrome_driver.find_element(By.XPATH, DETAIL_VIEW_XPATH).send_keys(Keys.ENTER)
    source = chrome_driver.page_source
    return BeautifulSoup(source, 'html.parser')


def get_required_time(beautiful_soup):
    required_time_str = beautiful_soup.select_one(REQUIRED_TIME_SELECTOR).text
    print(required_time_str)
    # required_time_str = required_time_str.split("시간")
    return convert_to_minute(required_time_str)


def get_stations(beautiful_soup):
    temp_arr = beautiful_soup.find_all(string=re.compile('역'))
    return calc_stations(temp_arr)


def getDataset():
    return pd.read_csv(filepath_or_buffer="taek.csv", encoding="cp949", sep=",")


driver = webdriver.Chrome()
driver.get('https://map.naver.com/v5/subway/1000/-/-/-?c=16,0,0,0,dh')
time.sleep(1)

assert '지하철 - 네이버 지도' in driver.title

dataset = getDataset()


def clear(driver):
    driver.find_element(By.ID, 'input_search_0').clear()
    driver.find_element(By.ID, 'input_search_1').clear()


def set_first_subway(driver):
    driver.find_element(By.XPATH, LAST_SUBWAY_RADIO_BUTTON_XPATH).click()
    driver.find_element(By.XPATH, FIRST_SUBWAY_RADIO_BUTTON_XPATH).click()
    time.sleep(1)


def append_data(path_arr, required_time):
    end1 = path_arr[0]
    end2 = path_arr[-1]
    route = '-'.join(path_arr)
    data = {
        "end1": [end1],
        "end2": [end2],
        "required_time": [required_time],
        "route": [route]
    }
    df = pd.DataFrame(data)
    if not os.path.exists('result.csv'):
        df.to_csv('result.csv', index=False, mode='w', encoding='utf-8')
    else:
        df.to_csv('result.csv', index=False, mode='a', encoding='utf-8', header=False)

flag = True

for row in dataset.itertuples():

    start = row[1]
    end = row[2]

    csv = pd.read_csv(filepath_or_buffer="result.csv", encoding="utf-8", sep=",")

    if len(csv) != 0 and flag:
        last_row = csv.iloc[-1]
        print(last_row)
        if not (start in last_row[0] and end in last_row[1]):
            continue
        else:
            flag = False

    set_start_station(start, driver)
    set_end_station(end, driver)
    set_first_subway(driver)

    soup = get_soup(driver)
    required_time = get_required_time(soup)
    path_arr = get_stations(soup)

    print(required_time)
    for path in path_arr:
        print(path)

    clear(driver)

    time.sleep(1)

    append_data(path_arr, required_time)