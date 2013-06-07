#!/usr/bin/env python
# coding: utf-8
__author__ = 'well snake'

from bs4 import BeautifulSoup as BS
import urllib2
import sqlite3 as db

#获取特需门诊分页url信息
urls = []
for x in [1, 2, 3, 4, 5, 6, 7]:
    base_url = "http://www.chhospital.com.cn/news_show/index.php?cid=100&id=0&week=%s" % x
    response = urllib2.urlopen(base_url)
    html = response.read()
    soup = BS(html)
    op = soup.find('select', {"id": "pageselect"})
    if op:
        for o in op('option'):
            if o:
                urls.append(["%s&page=%s" % (base_url, o.text), x])
    else:
        urls.append([base_url, x])


#更新前先删除旧数据
conn = db.connect("clinic.db")
sql = "DELETE FROM %s" % "clinic_schedule_vip"
c = conn.cursor()
c.execute(sql)
conn.commit()
#开始逐条查询特需门诊信息
for url in urls:
    response = urllib2.urlopen(url[0])
    html = response.read()
    soup = BS(html)
    print url
    for tr in soup('table')[1]('tr'):
        if tr.td:
            print tr('p')[0].text, tr('p')[1].text, tr('p')[2].text, tr('p')[3].text, tr('p')[4].text, tr('p')[5].text
            sql = "INSERT INTO %s VALUES('%s','%s','%s','%s','%s','%s',%d)" % \
                  ("clinic_schedule_vip",tr('p')[0].text, tr('p')[1].text, tr('p')[2].text, tr('p')[3].text, tr('p')[4].text, tr('p')[5].text,url[1])
            c = conn.cursor()
            c.execute(sql)
conn.commit()
conn.close()
