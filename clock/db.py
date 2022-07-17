
import os
import sqlite3
from .Clock import Clock
path =os.path.dirname(__file__)
db = path + '/data.sqlite'

TABLE = "CLOCKS"

def execute(sql:str):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    res = c.execute(sql)
    res = list(res)
    conn.commit()
    conn.close()
    return res

def add_clock_db(clock: Clock):
    sql = f'''INSERT INTO {TABLE} (type, user, content, month, day, week, c_time, ones)
    values ("{clock.type}", {clock.user}, "{clock.content}","{clock.month}","{clock.day}","{clock.week}","{clock.time}",{clock.ones});'''
    execute(sql)

def del_clock_db(id):
    execute(f"DELETE from {TABLE} where id = {id}")

def select_all():
    '''
    (id, type, user, content, c_time, ones) 
    '''
    #DataFrame(data = data, columns=['id', 'type', 'uid', 'note', 'time', 'omes'])
    return execute(f"SELECT * FROM {TABLE};")

    
def new_id():
    res = execute(f"SELECT max(id) FROM {TABLE};")
    return res[0][0] + 1 if res[0][0] else 0

try:
    execute(f'''CREATE TABLE {TABLE}(  
        id INTEGER NOT NULL primary key autoincrement,
        type CHAR(10),
        user INTEGER NOT NULL,
        content VARCHAR(20),
        month INTEGER,
        day INTEGER,
        week VARCHAR(7),
        c_time TIME,
        ones INTEGER NOT NULL);
    ''')
except:
    pass
