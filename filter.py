import json
import time
import re
import selenium
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from flask import Flask, request
from selenium.webdriver.common.keys import Keys

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
url = 'http://www.tsetmc.com/Loader.aspx?ParTree=15131F#'
driver = webdriver.Chrome('C:\chromedriver.exe')
driver.get(url)

data = """true==function() {
    var period = 20;
    var multi = 2;
    var addToday = true;
    
    var candle = function(a) {
        return {c: a.PDrCotVal, h: a.PriceMax, l: a.PriceMin, o: a.PriceFirst};
    }
    
    var getCandles = function() {
        var cs = [];
        for(var i = 0; i < [ih].length; i++)
            ([ih][i].ZTotTran > 0) && cs.push(candle([ih][i]));
        if(addToday && (tno) > 0) {
            var t = {c: (pl), h: (pmax), l: (pmin), o: (pf)};
            if(t.c != cs[0].c || t.h != cs[0].h || t.l != cs[0].l || t.o != cs[0].o)
                cs.unshift(t);
        }
        return (cs.length > 30) ? cs : false;
    }
    
    var BB = function(a) {
        var dvma, i, j;
        for(i = a.length-period; i >= 0; i--) {
            var sum = 0;
            for(j = 0; j < period; j++)
                sum += a[i+j].c;
            a[i].BBM = sum/period;
            var sumdv = 0;
            for(j = 0; j < period; j++)
                sumdv += Math.pow(a[i+j].c - a[i].BBM, 2);
            dvma = Math.sqrt(sumdv/period);
            a[i].BBH = a[i].BBM + 2*dvma;
            a[i].BBL = a[i].BBM - 2*dvma;
        }
    }
        var c = getCandles();
    if(c) {
        BB(c);
        if(c[0].l <= c[0].BBL) 
{
            return true;
        }
}
}()&&(tvol)> [is5] && (tvol)>2*[is6]"""
driver.execute_script('mw.ShowAllSettings()')
driver.execute_script('mw.Settings.LoadClientType=1-mw.Settings.LoadClientType;mw.SaveParams();HideAllWindow();mw.LoadClientType();')
driver.execute_script('mw.ShowAllSettings();')
driver.execute_script('mw.Settings.LoadInstStat=1-mw.Settings.LoadInstStat;mw.SaveParams();HideAllWindow();mw.LoadInstStat();')
driver.execute_script('mw.ShowAllSettings();')
driver.execute_script('mw.Settings.LoadInstHistory=1-mw.Settings.LoadInstHistory;mw.SaveParams();HideAllWindow();mw.LoadInstHistory();')

driver.execute_script('mw.QueryWindow();')
driver.execute_script('mw.QueryWindowNewFilter();')
driver.execute_script('mw.QueryWindowFilterNames();')
driver.execute_script('mw.SelectFilter('
                      '0);')
driver.execute_script('mw.ShowSettings();')
driver.execute_script('mw.SaveParams();')
driver.execute_script('mw.QueryWindowFilterNames();')
elem = driver.find_element_by_id('InputFilterCode')
for part in data.split('\n'):
    elem.send_keys(part)
    ActionChains(driver).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.SHIFT).key_up(Keys.ENTER).perform()
#driver.execute_script("document.getElementById('InputFilterCode').value ='" + (data) + "'")
driver.execute_script("mw.QueryWindowSaveFilter()")

time.sleep(5)
mk = driver.find_element_by_css_selector('#main')
tr = mk.find_elements_by_css_selector('.inst')

dict = []

for i in range(len(tr)):
    if i % 2 == 0:
        try:
            er = tr[i].get_attribute('innerHTML')
        except StaleElementReferenceException:
            er = 0
        dict.insert(int(i / 2), er)
driver.close()
print(json.dumps(dict, ensure_ascii=False))
