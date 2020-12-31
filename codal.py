import time

import requests
from selenium import webdriver


UserInput = "https://www.codal.ir/Reports/Decision.aspx?LetterSerial=rRaqRhTylppwn0S48sSphQ%3D%3D&rt=3&let=6&ct=0&ft=-1&sheetId=1"

driver = webdriver.Chrome(executable_path=r'C:\chromedriver.exe')

driver.get(UserInput)
time.sleep(5)
driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))
sell = driver.find_elements_by_css_selector(".sellColor-2qa8ZOVt")
