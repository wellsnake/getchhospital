#!/usr/bin/env python
# coding: utf-8
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
from google.appengine.ext import db
from bs4 import BeautifulSoup as BS
from string import strip
import urllib2


class clinic_schedule_common(db.Model):
    dept_name =db.StringProperty(required=True)
    schedule_desc = db.StringProperty(required=True)



class MainHandler(webapp2.RequestHandler):
    def get(self):
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
        db.delete(clinic_schedule_common.all())
        self.response.write("<table border=\"1\">")
        self.response.write("""
        <tr>
        <th rowspan = \"2\"><p>科室</p></th>
        <th colspan = \"2\"><p>星期一</p></th>
        <th colspan = \"2\"><p>星期二</p></th>
        <th colspan = \"2\"><p>星期三</p></th>
        <th colspan = \"2\"><p>星期四</p></th>
        <th colspan = \"2\"><p>星期五</p></th>
        <th colspan = \"2\"><p>星期六</p></th>
        <th colspan = \"2\"><p>星期日</p></th>
        </tr>
        """)
        self.response.write("""
        <tr>
        <th><p>上午</p></th>
        <th><p>下午</p></th>
        <th><p>上午</p></th>
        <th><p>下午</p></th>
        <th><p>上午</p></th>
        <th><p>下午</p></th>
        <th><p>上午</p></th>
        <th><p>下午</p></th>
        <th><p>上午</p></th>
        <th><p>下午</p></th>
        <th><p>上午</p></th>
        <th><p>下午</p></th>
        <th><p>上午</p></th>
        <th><p>下午</p></th>
        </tr>
        """)
        for x in clinic:
            weeks =[]
            for week in x[1].split(','):
                if week == '1':
                    weeks.append(u'★')
                else:
                    weeks.append(u"")
            e = clinic_schedule_common(dept_name = x[0],
                                       schedule_desc = x[1])
            e.put()
            self.response.write('<tr><td><p>%s</p></td>' % x[0])
            self.response.write('<td><p>%s</p></td>' % weeks[0])
            self.response.write('<td><p>%s</p></td>' % weeks[1])
            self.response.write('<td><p>%s</p></td>' % weeks[2])
            self.response.write('<td><p>%s</p></td>' % weeks[3])
            self.response.write('<td><p>%s</p></td>' % weeks[4])
            self.response.write('<td><p>%s</p></td>' % weeks[5])
            self.response.write('<td><p>%s</p></td>' % weeks[6])
            self.response.write('<td><p>%s</p></td>' % weeks[7])
            self.response.write('<td><p>%s</p></td>' % weeks[8])
            self.response.write('<td><p>%s</p></td>' % weeks[9])
            self.response.write('<td><p>%s</p></td>' % weeks[10])
            self.response.write('<td><p>%s</p></td>' % weeks[11])
            self.response.write('<td><p>%s</p></td>' % weeks[12])
            self.response.write('<td><p>%s</p></td></tr>' % weeks[13])
        self.response.write("</table>")
app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
