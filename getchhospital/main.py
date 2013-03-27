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
from chmodel import clinic_schedule_common as comm
from chmodel import clinic_schedule_special as sp
from chmodel import clinic_schedule_expert as ex
from chmodel import clinic_schedule_vip as vp
import json


class index(webapp2.RequestHandler):
    def get(self):
        self.response.out.write("<p><a href='/getcommon'>获得所有普通号</a></p>")
        self.response.out.write("<p><a href='/getspecial'>获得所有专病号</a></p>")
        self.response.out.write("<p><a href='/getexpert'>获得所有专家号</a></p>")
        self.response.out.write("<p><a href='/getvip'>获得所有特需号</a></p>")


class common(webapp2.RequestHandler):
    def get(self):
        q = comm.all()
        results = q.fetch(q.count())
        a = []
        for r in results:
            a.append({'dept_name': r.dept_name, 'schedule_desc': r.schedule_desc})
        x = {'count': q.count(), 'desc': a}
        self.response.headers["Content-Type"] = "application/json; charset=utf-8"
        self.response.out.write(json.dumps(x))

class special(webapp2.RequestHandler):
    def get(self):
        q = sp.all()
        results = q.fetch(q.count())
        a = []
        for r in results:
            a.append({'dept_name': r.dept_name, 'clinic_name': r.clinic_name, 'schedule_desc':r.schedule_desc})
        x = {'count': q.count(), 'desc': a}
        self.response.headers["Content-Type"] = "application/json; charset=utf-8"
        self.response.out.write(json.dumps(x))

class expert(webapp2.RequestHandler):
    def get(self):
        q = ex.all()
        results = q.fetch(q.count())
        a = []
        for r in results:
            a.append({'dept_name': r.dept_name,
                      'doctor_name': r.doctor_name,
                      'doctor_level': r.doctor_level,
                      'doctor_skill': r.doctor_skill,
                      'clinic_desc': r.clinic_desc,
                      'clinic_num': r.clinic_num,
                      'week': r.week})
        x = {'count': q.count(), 'desc': a}
        self.response.headers["Content-Type"] = "application/json; charset=utf-8"
        self.response.out.write(json.dumps(x))

class vip(webapp2.RequestHandler):
    def get(self):
        q = vp.all()
        results = q.fetch(q.count())
        a = []
        for r in results:
            a.append({'dept_name': r.dept_name,
                      'doctor_name': r.doctor_name,
                      'doctor_level': r.doctor_level,
                      'doctor_skill': r.doctor_skill,
                      'clinic_desc': r.clinic_desc,
                      'clinic_num': r.clinic_num,
                      'week': r.week})
        x = {'count': q.count(), 'desc': a}
        self.response.headers["Content-Type"] = "application/json; charset=utf-8"
        self.response.out.write(json.dumps(x))


app = webapp2.WSGIApplication([('/', index)], debug=False)
appcommon = webapp2.WSGIApplication([('/getcommon', common)], debug=False)
appspecial = webapp2.WSGIApplication([('/getspecial', special)], debug=False)
appexpert = webapp2.WSGIApplication([('/getexpert', expert)], debug=False)
appvip = webapp2.WSGIApplication([('/getvip', vip)], debug=False)

