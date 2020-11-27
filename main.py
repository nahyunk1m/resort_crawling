import os
import time
import json
import enum
from collections import OrderedDict
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
    resort_list = []
    resort_number = 0
    html = ""

    def __init__(self, name):
        self.name = name
        self.accom = {}

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"{self.name}"

    @classmethod
    def crawling(cls):
        try:
            driver = webdriver.Chrome(options=options)
        except:
            pass
        driver.implicitly_wait(5)
        driver.get(MAINPAGE)
        id_curs = driver.find_element_by_css_selector('#_id')
        id_curs.click()
        id_curs.send_keys(cls.get_account('ID'))
        time.sleep(2)
        password_curs = driver.find_element_by_css_selector('#_password')
        password_curs.send_keys(cls.get_account('PW'))
        time.sleep(1)
        password_curs.send_keys(Keys.ENTER)
        time.sleep(2)

        driver.get(RESORTPAGE)
        cls.html = driver.page_source

        soup = BeautifulSoup(cls.html, 'html.parser')

        for inner in soup.select('.room_state .inner'):
            resort_name = inner.select_one('.first')
            resort = cls(resort_name.text)

            # 숙소별로 구하기
            for tbody in inner.select('table tbody'):
                for tr_idx, tr in enumerate(tbody.select('tr')[1:]):
                    if tr_idx == 0:
                        accom_name = tr.select_one('th').text
                        resort.accom[accom_name] = OrderedDict()
                    day = TodayDate
                    for td_idx, td in enumerate(tr.select('td')):
                        if td_idx == 0:
                            accom_type = '/'.join(td.select_one('.r_name').text.strip().split())
                            resort.accom[accom_name][accom_type] = OrderedDict()
                        else:
                            resort.accom[accom_name][accom_type][day.strftime('%Y-%m-%d')] = td.text.strip('\n\t ')
                            day = day + timedelta(days=1)
            cls.resort_list.append(resort)
        time.sleep(3)
        cls.driver = driver

    @staticmethod
    def get_account(info):
        with open('secrets.json', 'r') as f:
            data = json.loads(f.read())
        return data[info]

    @staticmethod
    def remove_file(extension="xls"):
        pass

    @classmethod
    def choice_resort(cls):
        cls.choice = choice_number(cls.resort_list, msg="조회하실 리조트를 골라주세요.")
        if cls.choice == 0:
            return
        return cls.resort_list[cls.choice-1]

    def show(self, d="", indent=0):
        if not isinstance(d, dict):
            d = self.accom
        for key, value in d.items():
        # print('\t' * indent + str(key))
            if indent == 2:
                print(key, self.resort_number, end='')
                self.resort_number += 1
            else:
                print(key)
            if isinstance(value, dict):
                self.show(value, indent+1)
            else:
                print('\t' * (indent+1) + str(value))

    def show_detail(self, number):
        soup = BeautifulSoup(self.html, 'html.parser')
        for inner in soup.select('.room_state .inner'):
            if inner.select_one('h3.first').text != self.name:
                 continue
            for idx, div in enumerate(inner.select('td div')):
                if idx == number:
                    try:
                        selector = div['onclick']
                        break
                    except:
                        return "예약 불가입니다."
        if self.driver.current_url != RESORTPAGE:
            self.driver.back()
        self.driver.find_element_by_css_selector(""".inner td div[onclick="{}"]""".format(selector)).click()


def choice_number(choice_list, msg=""):
    while True:
        print(msg)
        for num, i in enumerate(choice_list, 1):
            print(f"{num}.{i}", end="\t")
        print("0. 종료")
        try:
            choice = int(input(''))
            if choice > len(choice_list):
                raise Exception()
        except:
            print("정해진 범위와 숫자만 입력해주세요.")
            continue
        else:
            return choice


if __name__ == "__main__":
    choice_list = ["조회"]
    Resort.crawling()
    msg = "리조트 크롤링 프로그램입니다. 메뉴를 선택해주세요."

    while True:
        choice = choice_number(choice_list, msg)
        if choice == 1:
            resort = Resort.choice_resort() # 리조트 인스턴스 받기
            resort.show()
            resort_number = int(input('조회하실 항목을 골라주세요.'))
            resort.show_detail(resort_number)

        elif choice == 0:
            input("종료. 아무키나 눌러주세요.")
            break
