import os
import time
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

MAINPAGE = "https://www.sonohotelsresorts.com/mv.dp/dmparse.dm?menuCd=5560000"
BACKSPACE='/ue003'
ENTER='/ue007'
TAB='/ue004'

def get_account(info):
    with open('secrets.json', 'r') as f:
        data = json.loads(f.read())
    return data[info]

try:
    driver = webdriver.Chrome()
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
driver.quit()