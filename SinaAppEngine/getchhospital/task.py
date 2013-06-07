#!/usr/bin/env python
# coding: utf-8
__author__ = 'well snake'
import chmodel as db
from getchweb import getchweb as ch
from setting import chweburl as url

def get_vip():
    """"获得特需号信息"""
    chweb = ch(url)

    vip = chweb.get_vip()
    if vip:
        db.del_vip()
        for clinic in vip:
           param = (clinic[0], clinic[1], clinic[2], clinic[3], clinic[4], clinic[5], clinic[6])
           db.insert_vip(param)

def get_comm():
    """获取普通号信息"""
    chweb = ch(url)

    comm = chweb.get_common()
    if comm:
        db.del_comm()
        for clinic in comm:
           param = (clinic[0], clinic[1])
           db.insert_comm(param)

def get_special():
    """获取专病号信息"""
    chweb = ch(url)
    special = chweb.get_special()
    if special:
        db.del_special()
        for clinic in special:
           param = (clinic[0], clinic[1], clinic[2])
           db.insert_special(param)

def get_expert():
    """获取专家号信息"""
    db.del_expert()
    chweb = ch(url)
    for x in range(1,8):
        expert = chweb.get_expert(x)
        if expert:
            for clinic in expert:
                if clinic[1] != u'陶苏江':#目前有重复数据，暂时先这样解决，以后只能增加重复数据的校验
                   param = (clinic[0], clinic[1], clinic[2], clinic[3], clinic[4], clinic[5], clinic[6])
                   db.insert_expert(param)