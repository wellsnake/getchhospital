#!/usr/bin/env python
# coding: utf-8
__author__ = 'Snake'
from google.appengine.ext import db


#存储普通号
class clinic_schedule_common(db.Model):
    dept_name = db.StringProperty(required=True)
    schedule_desc = db.StringProperty(required=True)


#存储专病号
class clinic_schedule_special(db.Model):
    dept_name = db.StringProperty(required=True)
    clinic_name = db.StringProperty(required=True)
    schedule_desc = db.StringProperty(required=True)


#存储专家号
class clinic_schedule_expert(db.Model):
    dept_name = db.StringProperty(required=True)
    doctor_name = db.StringProperty(required=True)
    doctor_level = db.StringProperty(required=True)
    doctor_skill = db.TextProperty()
    clinic_desc = db.StringProperty(required=True)
    clinic_num = db.StringProperty()
    week = db.IntegerProperty(required=True)


#存储特需号
class clinic_schedule_vip(db.Model):
    dept_name = db.StringProperty(required=True)
    doctor_name = db.StringProperty(required=True)
    doctor_level = db.StringProperty(required=True)
    doctor_skill = db.TextProperty()
    clinic_desc = db.StringProperty(required=True)
    clinic_num = db.StringProperty()
    week = db.IntegerProperty(required=True)
