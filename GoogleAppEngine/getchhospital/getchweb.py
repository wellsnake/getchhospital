#!/usr/bin/env python
# coding: utf-8
__author__ = 'Snake'
from BeautifulSoup import BeautifulSoup as BS
from string import strip
import urllib2


class getchweb(object):
    def __init__(self, url):
        self.url = url

    def getsoup(self,clinic):
        response = urllib2.urlopen(clinic)
        html = response.read()
        soup = BS(html)
        return soup

    def get_common(self):
        #获得普通门诊号表
        soup = self.getsoup(self.url['common'])
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
        return clinic

    def get_special(self):
        #获取专病门诊信息
        soup = self.getsoup(self.url['special'])
        clinic = []
        for tr in soup('tr'):
            if tr('td'):
                #科室，专病名称、开诊日期
                clinic.append([tr('td')[0].text, tr('td')[1].text, tr('td')[2].text])
        return clinic

    def get_expert_or_vip_url(self, clinic_type_url):
        #获取专家门诊分页url信息
        urls = []
        for x in [1, 2, 3, 4, 5, 6, 7]:
            base_url = clinic_type_url % x
            soup = self.getsoup(base_url)
            op = soup.find('select', {"id": "pageselect"})
            if op:
                for o in op('option'):
                    if o:
                        urls.append(["%s&page=%s" % (base_url, o.text), x])
            else:
                urls.append([base_url, x])
        return urls

    def get_expert_or_vip(self, clinic_type):
        urls = self.get_expert_or_vip_url(clinic_type)
        clinic = []
        for url in urls:
            soup = self.getsoup(url[0])
            for tr in soup('table')[1]('tr'):
                if tr.td:
                    #科室 姓名 职称 特长 出诊时间 挂号数 星期
                    clinic.append([tr('p')[0].text, tr('p')[1].text, tr('p')[2].text,
                                   tr('p')[3].text, tr('p')[4].text, tr('p')[5].text, url[1]])
        return clinic

    def get_expert(self):
        return self.get_expert_or_vip(self.url['expert'])

    def get_vip(self):
        return self.get_expert_or_vip(self.url['vip'])
