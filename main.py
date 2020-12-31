import requests
import time

from selenium import webdriver
import json

UserInput = "http://sourcearena.ir/signal.php"

driver = webdriver.Chrome(executable_path=r'C:\chromedriver.exe')

driver.get(UserInput)
time.sleep(5)


for i in range(1000):
    driver.refresh()
    time.sleep(5)
    driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))
    sell = driver.find_elements_by_css_selector(".sellColor-2qa8ZOVt")

    buy = driver.find_elements_by_css_selector(".buyColor-4BaoBngr")
    print(buy[0].text)
    res =0
    if buy[0].text == 'STRONG BUY':
        res = 200
    if sell[0].text == "STRONG SELL":
        res = -200
    elif len(sell) == 2:
        res = -100
    elif len(buy) == 2:
        res = 100

    x = requests.get('https://sourcearena.ir/mql/save.php?code=' + str(res))
    print(res)
    time.sleep(60)



