#!/usr/bin/env python
# coding: utf-8
__author__ = 'well snake'

from bs4 import BeautifulSoup as BS
from string import strip
import urllib2

#获得普通门诊号表
response=urllib2.urlopen('http://www.chhospital.com.cn/news_show/?cid=97')
html=response.read()
#开始读入BeautifulSoup
soup = BS(html)

#读取门诊号表内容，整理成形如：
#[["中医门诊",1,2,3,4,5,6,7,9],["儿科门诊",1,4,5]]
#其中1表示星期一上午，2表示星期一下午，以此类推
clinic = []
a = []
i = 1
for x in soup('td'):
    #写入科室
    if  x.text != u"★" and x.text != u'':
        a.append(x.text)
        i = 1
    #写入开诊日期
    elif x.text == u"★" and i != 14:
        a.append(i)
        i += 1
    #不开诊就跳过
    elif x.text == u'' and i != 14:
        i +=1
    #如果是最后一天就将结果写入clinic
    elif x.text == u"★" and i == 14:
        a.append(i)
        clinic.append(a)
        a = []
    elif x.text == u'' and i == 14:
        clinic.append(a)
        a = []
    else:
        break

#循环打印clinic
for x in clinic:
    print strip(x[0]),x[1:]

