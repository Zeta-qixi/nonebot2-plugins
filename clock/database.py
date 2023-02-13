
import os
import sqlite3
from .Clock import Clock
path =os.path.dirname(__file__)

db_ = path + '/data.sqlite'
TABLE = "CLOCKS"


class DB:
    def __init__(self, db, table):
        self.db = db
        self.table =  table
        

    def execute(self, sql:str):
        conn = sqlite3.connect(self.db)
        c = conn.cursor()
        res = c.execute(sql)
        res = list(res)
        conn.commit()
        conn.close()
        return res

    def add_clock(self, clock: Clock):
        sql = f'''INSERT INTO {self.table} (type, user, content, month, day, week, c_time, ones)
        values ("{clock.type}", {clock.user}, "{clock.content}","{clock.month}","{clock.day}","{clock.week}","{clock.time}",{clock.ones});'''
        self.execute(sql)

    def del_clock(self, id):
        self.execute(f"DELETE from {self.table} where id = {id}")

    def select_all(self):
        '''
        (id, type, user, content, c_time, ones) 
        '''
        #DataFrame(data = data, columns=['id', 'type', 'uid', 'note', 'time', 'omes'])
        return self.execute(f"SELECT * FROM {self.table};")

        
    def new_id(self):
        res = self.execute(f"SELECT max(id) FROM {self.table};")
        return res[0][0] + 1 if res[0][0] else 0

    try:
        self.execute(f'''CREATE TABLE {self.table}(  
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

db = DB(db_, TABLE)