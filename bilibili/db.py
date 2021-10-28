import sqlite3
import os
import time
path =os.path.dirname(__file__)
db = path + '/data.db'

TABLE = 'bilibili'

def execute(sql:str):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    res = c.execute(sql)
    data = []
    if res:
        for i in res:
            data.append(i)

    conn.commit()
    conn.close()
    return data

'''
INSERT
'''
def add_focus(gid:int, mid:int,name:str, live=0, dynamic=0):

   sql = f'''INSERT INTO {TABLE} (gid, mid, name, live, is_live,dynamic, latest_dynamic) 
   values ("{gid}", {mid}, "{name}", "{live}", "0", "{dynamic}", {time.time()});'''
   execute(sql)



'''
SELECT
'''
BASE_SELECT_SQL = f"SELECT * FROM {TABLE}"

def select_all():
    return execute(BASE_SELECT_SQL)

def select_one(gid, mid):
    return execute(BASE_SELECT_SQL + f' where mid = {mid} and gid = {gid}')

def select_live():
    return execute(BASE_SELECT_SQL + " where live = 1")

def select_dynamic():
    return execute(BASE_SELECT_SQL + " where dynamic = 1")



def update(gid, mid ,field: str, value):
    execute(f'UPDATE {TABLE} set {field} = "{value}" WHERE mid = {mid} and gid = {gid}')


def delete_focus(gid, mid):
    execute(f'DELETE FROM {TABLE} WHERE mid = {mid} and gid = {gid}')