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
clinic_name = ''
clinic_desc = ''
i = 1
for x in soup('td'):
    #如果是科室直接写入科室
    if  x.text != u"★" and x.text != u'':
        clinic_name = strip(x.text)
        i = 1
    #如果当日开诊，并且不是一周最后一天
    elif x.text == u"★" and i != 14:
        clinic_desc += '1,'
        i += 1
    #如果当日不开诊，并且不是一周最后一天
    elif x.text == u'' and i != 14:
        clinic_desc += '0,'
        i += 1
    #如果是最后一天并且当日开诊
    elif x.text == u"★" and i == 14:
        clinic_desc += '1'
        clinic.append([clinic_name, clinic_desc])
        clinic_desc = ''
    #如果是最后一天并且当日不开诊
    elif x.text == u'' and i == 14:
        clinic_desc += '0'
        clinic.append([clinic_name, clinic_desc])
        clinic_desc = ''
    else:
        break

for x in clinic:
    print x[0], x[1]

conn = db.connect("clinic.db")
#更新前先删除旧数据
sql = "DELETE FROM %s" % "clinic_schedule_common"
c = conn.cursor()
c.execute(sql)
conn.commit()
#将数据写入数据库
for x in clinic:
    sql = "INSERT INTO %s VALUES('%s','%s')" % ("clinic_schedule_common", x[0], x[1])
    c = conn.cursor()
    c.execute(sql)
conn.commit()


#读取专病门诊
response = urllib2.urlopen("http://www.chhospital.com.cn/news_show/?cid=98&po_id=8")
html = response.read()
#开始读入BeautifulSoup
soup = BS(html)
#更新前先删除旧数据
sql = "DELETE FROM %s" % "clinic_schedule_special"
c = conn.cursor()
c.execute(sql)
conn.commit()
#开始读取专病门诊信息
for tr in soup('tr'):
    if tr('td'):
        #科室，专病名称、开诊日期
        print tr('td')[0].text, tr('td')[1].text, tr('td')[2].text
        #写入数据库
        sql = "INSERT INTO %s VALUES('%s','%s','%s')"% ("clinic_schedule_special",tr('td')[0].text,tr('td')[1].text,tr('td')[2].text)
        c = conn.cursor()
        c.execute(sql)
conn.commit()
conn.close()