import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup

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

start = '역곡'
end = '강남'

driver = webdriver.Chrome()
driver.get('https://map.naver.com/v5/subway/1000/-/-/-?c=16,0,0,0,dh')
time.sleep(1)
assert '지하철 - 네이버 지도' in driver.title

driver.find_element(By.ID, 'input_search_0').send_keys(start)
time.sleep(STATION_INPUT_DELAY)
driver.find_element(By.XPATH, START_STATION_BUTTON_XPATH).send_keys(Keys.ENTER)

driver.find_element(By.ID, 'input_search_1').click()
driver.find_element(By.ID, 'input_search_1').send_keys(end)
time.sleep(STATION_INPUT_DELAY)
driver.find_element(By.XPATH, END_STATION_BUTTON_XPATH).send_keys(Keys.ENTER)
time.sleep(2)

driver.find_element(By.XPATH, DETAIL_VIEW_XPATH).send_keys(Keys.ENTER)

source = driver.page_source
soup = BeautifulSoup(source, 'html.parser')


required_time = soup.select_one(REQUIRED_TIME_SELECTOR).text.strip('분')
print("소요 시간 ", required_time)

# route = soup.select_one(ROUTE_SELECTOR)
# route_page = route.prettify()
#
# print(route_page)

find_all = soup.find_all('li', class_='item_line ng-star-inserted')

for find in find_all:
    print(find.text)