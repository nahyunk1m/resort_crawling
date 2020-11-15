import os
import time
import json
import enum
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from datetime import datetime, timedelta, date


# 오늘 날짜 구하기
TodayDate = date.today()
CURRENT_DIR = os.getcwd()
MAINPAGE = "https://www.sonohotelsresorts.com/mv.dp/dmparse.dm?menuCd=5560000"
RESORTPAGE = "https://www.sonohotelsresorts.com/reservation.online.roomUseTotCalSts.dp/dmparse.dm?fastYN=Y"
BACKSPACE='/ue003'
ENTER='/ue007'
TAB='/ue004'
options = Options()
options.add_experimental_option("prefs", {
     "download.default_directory": CURRENT_DIR,
     "download.prompt_for_download": False,
     "download.directory_upgrade": True,
     "safebrowsing.enabled": True
})


class Resort:
    def __init__(self, name):
        self.name = name
        self.accom = {}

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"{self.name}"


class Accomondation:
    def __init__(self, name):
        pass


def get_account(info):
    with open('secrets.json', 'r') as f:
        data = json.loads(f.read())
    return data[info]


def remove_file(extension="xls"):
    pass


try:
    driver = webdriver.Chrome(options=options)
except:
    pass


driver.implicitly_wait(5)
driver.get(MAINPAGE)
id_curs = driver.find_element_by_css_selector('#_id')
id_curs.click()
id_curs.send_keys(get_account('ID'))
time.sleep(2)
password_curs = driver.find_element_by_css_selector('#_password')
password_curs.send_keys(get_account('PW'))
time.sleep(1)
password_curs.send_keys(Keys.ENTER)
time.sleep(2)

driver.get(RESORTPAGE)
html = driver.page_source
# driver.find_element_by_xpath('//*[@id="contents"]/div[2]/a[2]').click()

soup = BeautifulSoup(html, 'html.parser')

resort_list = []
for inner in soup.select('.room_state .inner'):
    resort_name = inner.select_one('.first')
    resort = Resort(resort_name.text)
    
    # 숙소별로 구하기
    for tbody in inner.select('table tbody'):
        for tr_idx, tr in enumerate(tbody.select('tr')[1:]):
            if tr_idx == 0:
                accom_name = tr.select_one('th').text
                resort.accom[accom_name] = {}
            day = TodayDate
            for td_idx, td in enumerate(tr.select('td')):
                if td_idx == 0:
                    accom_type = '/'.join(td.select_one('.r_name').text.strip().split())
                    resort.accom[accom_name][accom_type] = {}
                else:
                    resort.accom[accom_name][accom_type][day.strftime('%Y-%m-%d')] = td.text.strip('\n\t ')
                    day = day + timedelta(days=1)
    resort_list.append(resort)

print(resort_list)

time.sleep(3)
driver.quit()


while True:
    try:
        choice = int(input('원하는 메뉴를 선택해주세요. 1. 조회  0. 종료'))
    except ValueError:
        print('숫자만 입력 가능합니다.')
        continue

    if choice == 1:
        pass