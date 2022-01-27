
import os
import sqlite3
from clock import Clock
path =os.path.dirname(__file__)
db = path + '/data.db'



def execute(sql:str):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    res = c.execute(sql)
    res = list(res)
    conn.commit()
    conn.close()
    return res

def add_clock_db(clock: Clock):
    sql = f'''INSERT INTO CLOCKS_ (type, user, content, mouth, day, week, c_time, ones)
    values ("{clock.type}", {clock.user}, "{clock.content}","{clock.mouth}","{clock.day}","{clock.week}","{clock.time}",{clock.ones});'''
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

try:
    execute('''CREATE TABLE clocks_(  
        id INTEGER NOT NULL primary key autoincrement,
        type CHAR(10),
        user INTEGER NOT NULL,
        content VARCHAR(20),
        mouth INTEGER,
        day INTEGER,
        week VARCHAR(7),
        c_time TIME,
        ones INTEGER NOT NULL);
    ''')
except:
    pass