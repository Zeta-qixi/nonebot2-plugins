'''
闹钟表
- ID (key)
- USER #id
- CONTENT #闹钟备注
- TYPE #private or group 
- C_TIME #默认 时/分
-ONES #一次性闹钟 #默认true
- 

CREATE TABLE clocks(  
    id INTEGER NOT NULL primary key autoincrement,
    type CHAR(10),
    user INTEGER NOT NULL,
    content VARCHAR(20),
    c_time TIME ,
    ones INTEGER NOT NULL
);
'''
import os
import sqlite3

path =os.path.dirname(__file__)
db = path+ '/data.db'

def execute(sql:str):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    res = c.execute(sql)
    res = list(res)
    conn.commit()
    conn.close()
    return res

def add_clock_db(user:int, content:str, time:str, ones = 1, type='private'):
   sql = f'''INSERT INTO CLOCKS (type, user, content, c_time, ones) 
   values ("{type}", {user}, "{content}", "{time}", {ones});'''
   execute(sql)

def del_clock_db(id):
    execute(f"DELETE from clocks where id = {id}")

def select_all():
    '''
    (id, type, user, content, c_time, ones) 
    '''
    #DataFrame(data = data, columns=['id', 'type', 'uid', 'note', 'time', 'omes'])
    return execute("SELECT * FROM clocks;")

    
def new_id():
    res = execute("SELECT max(id) FROM clocks;")
    return res[0][0]
