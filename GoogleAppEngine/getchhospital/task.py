#!/usr/bin/env python
# coding: utf-8
import webapp2
from chmodel import *
from getchweb import getchweb as ch
from setting import chweburl as url


class MainHandler(webapp2.RequestHandler):
    def get(self):
        get_chweb()
app = webapp2.WSGIApplication([('/task', MainHandler)], debug=True)


def get_chweb():
    chweb = ch(url)

    db.delete(clinic_schedule_common.all())
    common = chweb.get_common()
    for clinic in common:
        e = clinic_schedule_common(dept_name=clinic[0],
                                   schedule_desc=clinic[1])
        e.put()

    db.delete(clinic_schedule_special.all())
    special = chweb.get_special()
    for clinic in special:
        e = clinic_schedule_special(dept_name=clinic[0],
                                    clinic_name=clinic[1],
                                    schedule_desc=clinic[2])
        e.put()

    db.delete(clinic_schedule_expert.all())
    expert = chweb.get_expert()
    for clinic in expert:
        e = clinic_schedule_expert(dept_name=clinic[0],
                                   doctor_name=clinic[1],
                                   doctor_level=clinic[2],
                                   doctor_skill=clinic[3],
                                   clinic_desc=clinic[4],
                                   clinic_num=clinic[5],
                                   week=clinic[6])
        e.put()

    db.delete(clinic_schedule_vip.all())
    vip = chweb.get_vip()
    for clinic in vip:
        e = clinic_schedule_vip(dept_name=clinic[0],
                                doctor_name=clinic[1],
                                doctor_level=clinic[2],
                                doctor_skill=clinic[3],
                                clinic_desc=clinic[4],
                                clinic_num=clinic[5],
                                week=clinic[6])
        e.put()