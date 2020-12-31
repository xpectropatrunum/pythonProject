import driver as driver
import pandas as pd
import time
from seaercher import *

import json


if 'rayanDynamicStatement' in driver.find_element_by_tag_name('html'):
    A = driver.find_element_by_css_selector('.rayanDynamicStatement').get_attribute('outerHTML')
    table = pd.read_html(A, encoding='utf8')

    df_GDP = table[0].head()
    df_body = table[0]
    m = True

else:
    A = driver.find_element_by_tag_name('html').get_attribute('innerHTML')
    table = pd.read_html(A, encoding='utf8')
    m = False

    df_GDP = table[0]
    df_body = table[1]

oi = []

if m:
    for i in range(len(df_body)):

        val1 = str(df_body[(df_body).keys()[1]][i])

        if '(' in val1:
            val1 = '-' + val1.replace('(', '').replace(')', '')
        val2 = str(df_body[(df_body).keys()[2]][i])
        if '(' in val2:
            val2 = '-' + val2.replace('(', '').replace(')', '')
        val3 = str(df_body[(df_body).keys()[3]][i])

        if '(' in val3:
            val3 = '-' + val3.replace('(', '').replace(')', '')

        if (len((df_body).keys()) > 4):

            col1 = (df_body).keys()[1][0]
            col2 = (df_body).keys()[2][0]
            col4 = (df_body).keys()[3][0]
            col3 = (df_body).keys()[3][0]
            val4 = str(df_body[(df_body).keys()[4]][i])
            row = str(df_body[(df_body).keys()[0]][i])

            if '(' in val4:
                val4 = '-' + val4.replace('(', '').replace(')', '')

            if 'تغییر' in col3:
                col4_ = col3
                val4_ = val3
                col3_ = col4
                val3_ = val4
            else:
                col3_ = col4
                val3_ = val4
                col4_ = col3
                val4_ = val3

            oi.insert(i, {'row': row,
                          'items': [
                              {'column': col1,
                               'value': (val1)},
                              {'column': col2,
                               'value': (val2)
                               }, {'column': col3_,
                                   'value': (val3_)
                                   }], 'change': (val4_)})





        else:
            oi.insert(i, {'row': row,
                          'items': [
                              {'column': col1,
                               'value': (val1)},
                              {'column': col2,
                               'value': (val2)
                               }], 'change': (val4)})








else:
    for i in range(len(df_body)):

        val1 = str(df_body[2][i])
        if '(' in val1:
            val1 = '-' + val1.replace('(', '').replace(')', '')
        val2 = str(df_body[3][i])
        if '(' in val2:
            val2 = '-' + val2.replace('(', '').replace(')', '')
        val3 = str(df_body[4][i])
        if '(' in val3:
            val3 = '-' + val3.replace('(', '').replace(')', '')

        if (len(df_GDP.columns) > 4):

            if m:
                col1 = df_GDP.columns[1][0]
                col2 = df_GDP.columns[2][0]
                col3 = df_GDP.columns[3][0]
                col4 = df_GDP.columns[4][0]
            else:
                col1 = df_GDP.columns[1]
                col2 = df_GDP.columns[2]
                col3 = df_GDP.columns[3]
                col4 = df_GDP.columns[4]
            val4 = str(df_body[5][i])

            if '(' in val4:
                val4 = '-' + val4.replace('(', '').replace(')', '')

            if 'درصد' in col4:

                col3_ = col4
                val3_ = val4
                col4_ = col3
                val4_ = val3
            else:
                col3_ = col4
                val3_ = val4
                col4_ = col3
                val4_ = val3
            oi.insert(i, {'row': str(df_body[1][i]),
                          'items': [{'column': col1,
                                     'value': (val1)},
                                    {'column': col2,
                                     'value': (val2)
                                     }, {'column': col3_,
                                         'value': (val3_)
                                         }], 'change': (val4_)})
        else:
            if m:
                col1 = df_GDP.columns[1][0]
                col2 = df_GDP.columns[2][0]

            else:
                col1 = df_GDP.columns[1]
                col2 = df_GDP.columns[2]

            oi.insert(i, {'row': str(df_body[1][i]),
                          'items': [
                              {'row': str(df_body[1][i]), 'column': col1, 'period': (df_body[2][5]),
                               'value': (val1)},
                              {'row': str(df_body[1][i]), 'column': col2, 'period': (df_body[3][5]),
                               'value': (val2)
                               }], 'change': (val3)})

ui = (json.dumps(oi, ensure_ascii=False).replace('nan', 'null'))
print(ui)
oi = []

