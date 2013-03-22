#!/usr/bin/env python
# coding: utf-8
__author__ = 'well snake'

from bs4 import BeautifulSoup as BS
import urllib2

#获取专家门诊分页url信息
urls = []
for x in [1, 2, 3, 4, 5, 6, 7]:
    base_url = "http://www.chhospital.com.cn/news_show/index.php?cid=99&id=0&week=%s" % x
    response = urllib2.urlopen(base_url)
    html = response.read()
    soup = BS(html)
    op = soup.find('select', {"id": "pageselect"})
    if op:
        for o in op('option'):
            if o:
                urls.append("%s&page=%s" % (base_url, o.text))
    else:
        urls.append(base_url)
for u in urls:
    print u