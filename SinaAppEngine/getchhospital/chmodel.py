#!/usr/bin/env python
# coding: utf-8
__author__ = 'well snake'

import MySQLdb
import sae

sql_comm = "select * from clinic_schedule_common"
sql_special = "select * from clinic_schedule_special"
sql_expert = "select * from clinic_schedule_expert"
sql_vip = "select * from clinic_schedule_vip"
sql_comm_del = "delete from clinic_schedule_common"
sql_special_del = "delete from clinic_schedule_special"
sql_expert_del = "delete  from clinic_schedule_expert"
sql_vip_del = "delete from clinic_schedule_vip"
sql_vip_insert = """insert into clinic_schedule_vip
(dept_name,doctor_name,doctor_level,doctor_skill,clinic_desc,clinic_num,week)
values(%s,%s,%s,%s,%s,%s,%s)"""
sql_comm_insert = """insert into clinic_schedule_common
(dept_name,schedule_desc)
values(%s,%s)"""
sql_special_insert = """insert into clinic_schedule_special
(dept_name,clinic_name,schedule_desc)
values(%s,%s,%s)"""
sql_expert_insert = """insert into clinic_schedule_expert
(dept_name,doctor_name,doctor_level,doctor_skill,clinic_desc,clinic_num,week)
values(%s,%s,%s,%s,%s,%s,%s)"""

def conn_db_with_sql(sql_str):
    """查询数据"""
    conn=MySQLdb.connect(host=sae.const.MYSQL_HOST,
                                 user=sae.const.MYSQL_USER,
                                 passwd=sae.const.MYSQL_PASS,
                                 port=int(sae.const.MYSQL_PORT),
                                 charset='utf8')
    conn.select_db(sae.const.MYSQL_DB)
    cur=conn.cursor()
    cur.execute(sql_str)
    results=cur.fetchall()
    cur.close()
    conn.close()
    return results

def insert_db_with_sql(sql_str, param):
    """插入数据"""
    conn=MySQLdb.connect(host=sae.const.MYSQL_HOST,
                                 user=sae.const.MYSQL_USER,
                                 passwd=sae.const.MYSQL_PASS,
                                 port=int(sae.const.MYSQL_PORT),
                                 charset='utf8')
    conn.select_db(sae.const.MYSQL_DB)
    cur=conn.cursor()
    cur.execute(sql_str,param)
    cur.close()
    conn.close()

def del_db_with_sql(sql_str):
    """删除表数据"""
    conn=MySQLdb.connect(host=sae.const.MYSQL_HOST,
                                 user=sae.const.MYSQL_USER,
                                 passwd=sae.const.MYSQL_PASS,
                                 port=int(sae.const.MYSQL_PORT),
                                 charset='utf8')
    conn.select_db(sae.const.MYSQL_DB)
    cur=conn.cursor()
    cur.execute(sql_str)
    cur.close()
    conn.close()

def get_vip():
    vip = []
    results = conn_db_with_sql(sql_vip)
    for r in results:
        vip.append([r[0], r[1], r[2], r[3], r[4], r[5], r[6]])
    return vip

def insert_vip(param):
    insert_db_with_sql(sql_vip_insert, param)


def get_expert():
    expert = []
    results = conn_db_with_sql(sql_expert)
    for r in results:
        expert.append([r[0], r[1], r[2], r[3], r[4], r[5], r[6]])
    return expert


def insert_expert(param):
    insert_db_with_sql(sql_expert_insert, param)


def get_comm():
    comm = []
    results = conn_db_with_sql(sql_comm)
    for r in results:
        comm.append([r[0], r[1]])
    return comm


def insert_comm(param):
    insert_db_with_sql(sql_comm_insert, param)


def get_special():
    special = []
    results = conn_db_with_sql(sql_special)
    for r in results:
        special.append([r[0], r[1], r[2]])
    return special


def insert_special(param):
    insert_db_with_sql(sql_special_insert, param)

def del_comm():
    del_db_with_sql(sql_comm_del)

def del_special():
    del_db_with_sql(sql_special_del)

def del_vip():
    del_db_with_sql(sql_vip_del)

def del_expert():
    del_db_with_sql(sql_expert_del)