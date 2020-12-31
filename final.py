import requests
import urllib
import json
import driver as driver
from flask import Flask, request
import time
from unidecode import unidecode
import random
import driver as driver
import pandas as pd
import time
from persiantools import digits

n = 6001
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

xc = 'غپینو'
date = '139907'

d = requests.get(
    'http://sourcearena.ir/api/codalBridges/b1.php?name=' + xc)
letter = d.json()
out = []
om = []

for i in range(len(letter)):
    url = letter[i]['Url']
    title = letter[i]['Title']
    out.insert(i, {'title': title, 'link': 'http://codal.ir' + url})

driver = webdriver.Chrome('C:\chromedriver.exe', options=chrome_options)


def negative(a):
    if a.isnumeric():
        if '(' in a:
            return int('-' + a.replace('(', '').replace(')', ''))
        else:
            return a
    return a
def negative2(a):
    if '(' in a:
        return int('-' + a.replace('(', '').replace(')', ''))
    else:
        return a





for t in range(len(out)):
    url = out[t]['link']
    title = out[t]['title']

    if date in digits.fa_to_en(title).replace('/', ''):

        driver.get(url)
        time.sleep(0.5)

        if 'rayanDynamicStatement' in driver.find_element_by_tag_name('html').get_attribute('innerHTML'):
            A = driver.find_element_by_css_selector('.rayanDynamicStatement').get_attribute(
                'outerHTML')
            table = pd.read_html(A.replace(
                'nan',
                '0'), encoding='utf8')

            head = table[0].head()
            body = table[0]
            m = True

        else:
            A = driver.find_element_by_tag_name('html').get_attribute('innerHTML').replace(',', '')
            table = pd.read_html(A.replace(
                'nan',
                '0'), encoding='utf8')
            m = False

            head = table[0]
            body = table[1]

        oi = []
        returned = 0
        off = 0
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

                pro_count = digits.fa_to_en(str(body[q][u])).replace(',', '').replace('nan', '0')
                sale_count = digits.fa_to_en(str(body[w][u])).replace(',', '').replace('nan', '0')
                sale_price = digits.fa_to_en(str(body[e][u])).replace(',', '').replace('nan', '0')
                sale_income = digits.fa_to_en(str(body[r][u])).replace(',', '').replace('nan', '0')
                pro_count = negative2(pro_count)
                sale_price = negative2(sale_price)
                sale_income = negative2(sale_income)
                sale_count = negative2(sale_count)

                if int(sale_price) > 0 and (int(sale_income) > 0 or int(sale_income) < 0):
                    pro_name = str(body[t][u])
                    if pro_name == 'جمع':
                        sum = sale_income
                    if pro_name == 'جمع برگشت از فروش':
                        returned = sale_income
                    if pro_name == 'تخفیفات':
                        off = sale_income
                    if 'جمع' not in pro_name:
                        find = False
                        for mn in range(len(oi)):

                            if pro_name == str(oi[mn]["product_name"]):
                                find = True
                                gh = mn

                        if find:

                            oi[gh] = {"product_name": pro_name,
                                      "produce_count": int(oi[gh]["produce_count"]) + int(pro_count),
                                      "sale_count": int(oi[gh]["sale_count"]) + int(sale_count),
                                      "sale_price": oi[gh]["sale_price"],
                                      "sale_income": int(oi[gh]["sale_income"]) + int(sale_income)}

                        else:
                            oi.insert(i, {"product_name": pro_name,
                                          "produce_count": int(pro_count),
                                          "sale_count": int(sale_count),
                                          "sale_price": int(sale_price),
                                          "sale_income": int(sale_income)})



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

            print(url)
            for u in range(len(head)):

                pro_count = digits.fa_to_en(str(head[KEY - 3][u])).replace(',', '').replace('nan', '0')
                sale_count = digits.fa_to_en(str(head[KEY - 2][u])).replace(',', '').replace('nan', '0')
                sale_price = digits.fa_to_en(str(head[KEY - 1][u])).replace(',', '').replace('nan', '0')
                sale_income = digits.fa_to_en(str(head[KEY][u])).replace(',', '').replace('nan', '0')
                sale_count = negative(sale_count)
                pro_count = negative(pro_count)
                sale_price = negative(sale_price)
                sale_income = negative(sale_income)
                if sale_income.isnumeric():
                    if int(sale_income) > 0 or int(sale_income) < 0:
                        pro_name = head[0][u]
                        if pro_name == 'جمع':
                            sum = sale_income
                        if pro_name == 'جمع برگشت از فروش':
                            returned = sale_income
                        if pro_name == 'تخفیفات':
                            off = sale_income
                        if 'جمع' not in pro_name:
                            find = False
                            for mn in range(len(oi)):

                                if pro_name == str(oi[mn]["product_name"]):
                                    find = True
                                    gh = mn

                            if find:
                                oi.insert(gh, {"product_name": pro_name,
                                               "produce_count": int(oi[gh]["produce_count"]) + int(pro_count),
                                               "sale_count": int(oi[gh]["sale_count"]) + int(sale_count),
                                               "sale_price": int(oi[gh]["sale_price"]) + int(sale_price),
                                               "sale_income": int(oi[gh]["sale_income"]) + int(sale_income)})
                            else:

                                oi.insert(i, {"product_name": pro_name,
                                              "produce_count": int(pro_count),
                                              "sale_count": int(sale_count),
                                              "sale_price": int(sale_price),
                                              "sale_income": int(sale_income)})



        os = {"name": xc, "period": date,  "items": oi}

        print(json.dumps(os, ensure_ascii=False))


