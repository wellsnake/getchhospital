#!/usr/bin/env python
# coding: utf-8
__author__ = 'well snake'

from bs4 import BeautifulSoup as BS
from string import strip
import urllib2
import sqlite3 as db

#获得普通门诊号表
response=urllib2.urlopen('http://www.chhospital.com.cn/news_show/?cid=97')
html=response.read()
#开始读入BeautifulSoup
soup = BS(html)

#读取门诊号表内容，整理成形如：
#[["中医门诊",0,1,1,1,1,1,1,1,1,1,1,1,0,0],["儿科门诊",,0,1,1,1,1,1,1,1,1,1,1,1,0,0]]
#其中第一列表示科室名称，后面 1-开诊 0-不开诊
#因为一周开诊分上下午，所以一共有14列分别对应不同的开诊时间
clinic = []
a = []
i = 1
for x in soup('td'):
    #如果是科室直接写入科室
    if  x.text != u"★" and x.text != u'':
        a.append(strip(x.text))
        i = 1
    #如果当日开诊，并且不是一周最后一天
    elif x.text == u"★" and i != 14:
        a.append(1)
        i += 1
    #如果当日不开诊，并且不是一周最后一天
    elif x.text == u'' and i != 14:
        a.append(0)
        i +=1
    #如果是最后一天并且当日开诊
    elif x.text == u"★" and i == 14:
        a.append(1)
        clinic.append(a)
        a = []
    #如果是最后一天并且当日不开诊
    elif x.text == u'' and i == 14:
        a.append(0)
        clinic.append(a)
        a = []
    else:
        break

#循环打印clinic
for x in clinic:
    print x[0],x[1:]

#将数据写入数据库
conn = db.connect("clinic.db")
for x in clinic:
    sql = "INSERT INTO %s VALUES('%s',%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d)"% ("clinic_schedule_common",x[0],x[1],x[2],x[3],x[4],x[5],x[6],x[7],x[8],x[9],x[10],x[11],x[12],x[13],x[14])
    c = conn.cursor()
    c.execute(sql)
conn.commit()

