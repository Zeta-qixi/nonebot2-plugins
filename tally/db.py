import sqlite3
import os
import json
from functools import wraps
import time
PATH =os.path.dirname(__file__) + '/data'

DB_NAME = PATH + 'db.json'
DB = PATH + '/data.db'
TYPE = [

    '餐饮',
    '购物',
    '交通',
    '生活', # 水电 通讯
    '娱乐', 
    
]
with open(DB_NAME) as f:
    db_list = json.load(f)

def get_date():
    return time.strftime("%Y-%m-%d", time.localtime())

def get_time():
    return time.strftime("%H:%M:%S", time.localtime())

def exe_sql(sql: str):
    with sqlite3.connect(DB) as conn:
        c = conn.cursor()
        res = c.execute(sql)
    return res

def create_tabel(table_name: str):
    sql = f'''
    create table "{table_name}"(
    ID INTEGER PRIMARY KEY     AUTOINCREMENT ,
    AMOUNT         REAL    NOT NULL,
    DATE           TEXT    NOT NULL,
    TIME           TEXT    NOT NULL,
    TYPE           TEXT    NOT NULL,
    SUB_TYPE       TEXT    ,
    REMARK         TEXT    
    );
    '''
    return exe_sql(sql)


def insert_data(table: str, amount: int, date: str, time: str, type: str, sub_type: str ='null', remark: str='null'):
    sql = f"INSERT INTO {table} (AMOUNT, DATE, TIME, TYPE, SUB_TYPE, REMARK)\
        VALUES({amount}, '{date}', '{time}', '{type}', '{sub_type}', '{remark}');"
    return (exe_sql(sql))

