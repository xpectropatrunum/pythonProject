import requests
import urllib
import json
import driver as driver
from flask import Flask, request
import time
from persiantools import digits
import random
import driver as driver
import pandas as pd
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

app = Flask(__name__)


@app.route('/product/<name>&<date>')
def getName(name,date):
    xc = (name)
    d = requests.get(
        'http://sourcearena.ir/api/bridge.php?name=' + xc)
    letter = d.json()['Letters']
    out = []

    for i in range(len(letter)):
        url = letter[i]['Url']
        title = letter[i]['Title']
        out.insert(i, {'title': title, 'link': 'http://codal.ir' + url})

    driver = webdriver.Chrome('/usr/bin/chromedriver', options=chrome_options)
    url = out[0]['link']
    title = out[0]['title']
    driver.get(url)
    time.sleep(0.5)

    for t in range(len(out)):
        url = out[t]['link']
        title = out[t]['title']

        if date in digits.fa_to_en(title).replace('/', ''):

            driver.get(url)
            time.sleep(0.5)

            if 'rayanDynamicStatement' in driver.find_element_by_tag_name('html').get_attribute('innerHTML'):
                A = driver.find_element_by_css_selector('.rayanDynamicStatement').get_attribute('outerHTML').replace(
                    ',',
                    '')
                table = pd.read_html(A, encoding='utf8')

                head = table[0].head()
                body = table[0]
                m = True

            else:
                A = driver.find_element_by_tag_name('html').get_attribute('innerHTML').replace(',', '')
                table = pd.read_html(A, encoding='utf8')
                m = False

                head = table[0]
                body = table[1]

            oi = []

            if m:

                for y in range(len(head.keys())):

                    date_ = digits.fa_to_en(head.keys()[y][0].replace('/', ''))
                    if 'یک ماهه' in date_:
                        KEY = y
                        q = body.keys()[y - 3]
                        w = body.keys()[y - 2]
                        e = body.keys()[y - 1]
                        r = body.keys()[y]
                        t = body.keys()[0]

                for u in range(len(body)):

                    pro_count = digits.fa_to_en(str(body[q][u]))
                    sale_count = digits.fa_to_en(str(body[w][u]))
                    sale_price = digits.fa_to_en(str(body[e][u]))
                    sale_income = digits.fa_to_en(str(body[r][u]))
                    if str(sale_count).isnumeric():
                        oi.insert(i, {"product_name": body[t][u],
                                      "produce_count": pro_count,
                                      "sale_count": sale_count,
                                      "sale_price": sale_price,
                                      "sale_income": sale_income})
            else:
                for y in range(len(body.keys())):
                    date_ = body.keys()[y][0]

                    if 'یک ماهه' in date_:
                        KEY = y
                        q = body.keys()[y + 3]
                        w = body.keys()[y + 2]
                        e = body.keys()[y + 1]
                        r = body.keys()[y]
                        t = body.keys()[0]

                for u in range(len(head)):

                    pro_count = digits.fa_to_en(str(head[KEY - 3][u]))
                    sale_count = digits.fa_to_en(str(head[KEY - 2][u]))
                    sale_price = digits.fa_to_en(str(head[KEY - 1][u]))
                    sale_income = digits.fa_to_en(str(head[KEY][u]))
                    if str(sale_count).isnumeric():
                        pro_name = head[0][u]
                        for g in range(len(oi)):
                            if pro_name == oi[g]["product_name"]:
                                oi.insert(g, {"product_name": pro_name,
                                              "produce_count": oi[g]["produce_count"]+pro_count,
                                              "sale_count": oi[g]["sale_count"]+sale_count,
                                              "sale_price": oi[g]["sale_price"]+sale_price,
                                              "sale_income": oi[g]["sale_income"]+sale_income})
                            else:
                                oi.insert(i, {"product_name": pro_name,
                                              "produce_count": pro_count,
                                              "sale_count": sale_count,
                                              "sale_price": sale_price,
                                              "sale_income": sale_income})
                        if len(oi) == 0:
                            oi.insert(i, {"product_name": pro_name,
                                          "produce_count": pro_count,
                                          "sale_count": sale_count,
                                          "sale_price": sale_price,
                                          "sale_income": sale_income})





            os = {"name": xc, "period": date, "items": oi}

            print(json.dumps(os, ensure_ascii=False))

            return os


app.run(host='185.8.174.140', port=7500)





