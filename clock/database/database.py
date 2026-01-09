import os
import sqlite3
from contextlib import contextmanager
from typing import Dict, List
from ..model import Clock
from pathlib import Path


TABLE = "CLOCKS"
class ClockDB:
    def __init__(self, db_path, auto_commit=True):
        self.db_path = db_path
        self.auto_commit = auto_commit
        self.connection = None
        self._init_db()
        
    def connect(self):
        if not self.connection:
            self.connection = sqlite3.connect(self.db_path)
            
    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def commit(self):
        if self.connection:
            self.connection.commit()
    
    def rollback(self):
        if self.connection:
            self.connection.rollback()   

            
    @contextmanager
    def sql(self):
        try:
            self.connect()
            cursor = self.connection.cursor()
            yield cursor
            if self.auto_commit:
                self.commit()
        except sqlite3.Error as e:
            self.rollback()
            print(f"An error occurred: {e}")
            raise  # 重新抛出异常，允许用户处理
        finally:
            self.close()
            
    def execute(self, sql, params=()):
        with self.sql() as cursor:
            return cursor.execute(sql, params)
        
        
    def _init_db(self):
        """初始化数据库表"""
        with self.sql() as cursor:
            cursor.execute(f'''CREATE TABLE IF NOT EXISTS {TABLE}
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                             type TEXT,
                             group_id TEXT,
                             user_id TEXT,
                             content TEXT,
                             is_enabled BOOLEAN,
                             cron_expression TEXT,
                             is_one_time BOOLEAN,
                             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                             updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    
    def to_clock(self, row) -> Clock:
        return Clock({
                'id': row[0],
                'type': row[1],
                'group_id': row[2],
                'user_id': row[3],
                'content': row[4],
                'is_enabled': bool(row[5]),
                'cron_expression': row[6],
                'is_one_time': bool(row[7]),
                'created_at': row[8],
                'updated_at': row[9]
                })
        
        
    def select_all(self) -> List[Clock]:
        """获取所有提醒任务"""
        with self.sql() as cursor:
            cursor.execute(f'SELECT * FROM {TABLE}')
            rows = cursor.fetchall()
            data = []
            for row in rows:
                data.append(self.to_clock(row))
            return data
    
    def select_by_id(self, id: int | str) -> Clock:
        with self.sql() as cursor:
            cursor.execute(f'SELECT * FROM {TABLE} WHERE id =?', id)
            rows = cursor.fetchall()
        if rows:
            return self.to_clock(rows[0])
        
    def add(self, clock: Clock) -> int:
        """添加新的提醒任务"""
        data = clock.to_dict()
        with self.sql() as cursor:
      
            cursor.execute(f'''INSERT INTO {TABLE} 
                            (type, group_id, user_id, content, is_enabled, cron_expression, is_one_time)
                            VALUES (?, ?, ?, ?, ?, ?, ?)''',
                           (data['type'], data['group_id'], data['user_id'],
                            data['content'], data['is_enabled'], data['cron_expression'],
                            data['is_one_time']))
            return cursor.lastrowid
            
    
    def update(self, clock: Clock):
        """更新提醒任务"""
        data = clock.to_dict()
        with self.sql() as cursor:
            cursor.execute(f'''UPDATE {TABLE} SET
                            type=?, group_id=?, user_id=?, content=?,
                            is_enabled=?, cron_expression=?, is_one_time=?
                            WHERE id=?''',
                           (data['type'], data['group_id'], data['user_id'],
                            data['content'], data['is_enabled'], data['cron_expression'],
                            data['is_one_time'], data['id']))
    
    def delete(self, id: int):
        """删除提醒任务"""
        with self.sql() as cursor:
            cursor.execute(f'DELETE FROM {TABLE} WHERE id={id}')
            
    def select_by_owner(self, uid, gid) -> List[Clock]:
        with self.sql() as cursor:
            cursor.execute(f'SELECT * FROM {TABLE} WHERE user_id ={uid} AND group_id={gid} ORDER BY id;')
            rows = cursor.fetchall()
        data = []
        for row in rows:
            data.append(self.to_clock(row))
        return data
            
