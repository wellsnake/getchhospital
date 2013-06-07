#!/usr/bin/env python
# coding: utf-8
__author__ = 'well snake'
import web
import chmodel as db
import task
import json

urls = (
    '/', 'index',
    '/getcommon', 'getcommon',
    '/getspecial', 'getspecial',
    '/getexpert', 'getexpert',
    '/getvip', 'getvip',
    '/insertvip', 'insertvip',
    '/insertcomm','insertcomm',
    '/insertspecial','insertspecial',
    '/insertexpert','insertexpert',
)
web.config.debug = True
render = web.template.render('templates/')


class index:
    """显示主页信息"""
    def GET(self):
        return render.index()


class insertvip:
    def GET(self):
        task.get_vip()
        raise web.seeother('/')


class insertcomm:
    def GET(self):
        task.get_comm()
        raise web.seeother('/')

class insertspecial:
    def GET(self):
        task.get_special()
        raise web.seeother('/')

class insertexpert:
    def GET(self):
        task.get_expert()
        raise web.seeother('/')


class getcommon:
    def GET(self):
        """获取普通号并且讲结果输出成json格式"""
        q = db.get_comm()
        a = []
        for r in q:
            a.append({'dept_name': r[0],
                      'schedule_desc': r[1]})
        x = {'count': len(q), 'desc': a}
        web.header('Content-Type', 'application/json; charset=utf-8')
        return json.dumps(x)


class getspecial:
    def GET(self):
        """获取专病号并且讲结果输出成json格式"""
        q = db.get_special()
        a = []
        for r in q:
            a.append({'dept_name': r[0],
                      'clinic_name': r[1],
                      'schedule_desc': r[2]})
        x = {'count': len(q), 'desc': a}
        web.header('Content-Type', 'application/json; charset=utf-8')
        return json.dumps(x)

class getexpert:
    def GET(self):
        """获取专家号并且讲结果输出成json格式"""
        q = db.get_expert()
        a = []
        for r in q:
            a.append({'dept_name': r[0],
                      'doctor_name': r[1],
                      'doctor_level': r[2],
                      'doctor_skill': r[3],
                      'clinic_desc': r[4],
                      'clinic_num': r[5],
                      'week': r[6]})
        x = {'count': len(q), 'desc': a}
        web.header('Content-Type', 'application/json; charset=utf-8')
        return json.dumps(x)


class getvip:
    def GET(self):
        """获取特需号并且讲结果输出成json格式"""
        q = db.get_vip()
        a = []
        for r in q:
            a.append({'dept_name': r[0],
                      'doctor_name': r[1],
                      'doctor_level': r[2],
                      'doctor_skill': r[3],
                      'clinic_desc': r[4],
                      'clinic_num': r[5],
                      'week': r[6]})
        x = {'count': len(q), 'desc': a}
        web.header('Content-Type', 'application/json; charset=utf-8')
        return json.dumps(x)


app = web.application(urls, globals())
