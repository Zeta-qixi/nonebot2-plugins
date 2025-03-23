import datetime
import aiosqlite
import sqlite3
from typing import List, Dict
from abc import ABC, abstractmethod
from collections import defaultdict
from typing import List, Dict
import os

os.makedirs('data/llm', exist_ok=True)
 
# 核心接口
class IHistoryManager(ABC):
    @abstractmethod
    async def save_message(self, session_id: str, role: str, content: str) -> None:
        pass

    @abstractmethod
    async def get_history(self, session_id: str, length: int = 10) -> List[Dict[str, str]]:
        pass
    
    @abstractmethod
    async def get_history_by_time(self, session_id: str, seconds: int = 1800) -> list:
        pass

    @abstractmethod
    async def clear_history(self, session_id: str) -> None:
        pass
    



# 内存实现（带Token计数）
class MemoryHistoryManager(IHistoryManager):
    def __init__(self):
        self.max_history_tokens = 2000
        self.histories = defaultdict(list)
        self.token_counts = defaultdict(int)

    async def save_message(self, session_id: str, role: str, content: str) -> None:
        new_tokens = self._count_tokens(content)
        current_time = datetime.now().isoformat()
        self.histories[session_id].append({
            "role": role,
            "content": content,
            "timestamp": current_time
        })
        self.token_counts[session_id] += new_tokens

        # 自动清理历史
        while self.token_counts[session_id] > self.max_history_tokens:
            if len(self.histories[session_id]) > 0:
                removed = self.histories[session_id].pop(0)
                self.token_counts[session_id] -= self._count_tokens(removed["content"])
            else:
                break

    async def get_history_by_time(self, session_id: str, seconds: int = 1800) -> List[Dict[str, str]]:
        if seconds <= 0:
            return []
        
        history = self.histories.get(session_id, [])
        result = []
        cutoff = datetime.now() - datetime.timedelta(seconds=seconds)
        
        for message in reversed(history):
            msg_time = datetime.fromisoformat(message["timestamp"])
            if msg_time >= cutoff:
                result.append({"role": message["role"], "content": message["content"]})
            else:
                break
        
        return result[::-1]  # 返回按时间顺序排列的结果
    async def get_history(self, session_id: str, length: int = 10) -> List[Dict[str, str]]:
        return self.histories[session_id].copy()[-length:]

    async def clear_history(self, session_id: str) -> None:
        self.histories[session_id].clear()
        self.token_counts[session_id] = 0

    def _count_tokens(self, text: str) -> int:
        # 简易token计算（实际应使用tiktoken库）
        return len(text) // 4




class SQLiteHistoryManager(IHistoryManager):
    def __init__(self, db_path: str = "data/llm/history.db"):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        with sqlite3.connect(self.db_path) as db:
            db.execute('''
                CREATE TABLE IF NOT EXISTS history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT,
                    role TEXT,
                    content TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            db.commit()

    async def save_message(self, session_id: str, role: str, content: str) -> None:
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "INSERT INTO history (session_id, role, content) VALUES (?, ?, ?)",
                (session_id, role, content)
            )
            await db.commit()

    async def get_history(self, session_id: str, length: int = 10) -> List[Dict[str, str]]:
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute("SELECT role, content FROM history WHERE session_id = ? ORDER BY timestamp DESC LIMIT ?", (session_id,length,))
            rows = await cursor.fetchall()
        return [{"role": row[0], "content": row[1]} for row in rows]
    
    
    async def get_history_by_time(self, session_id: str, seconds: int = 1800) -> List[Dict[str, str]]:
        if seconds <= 0:
            return []
        
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                "SELECT role, content FROM history "
                "WHERE session_id = ? AND timestamp >= datetime('now', ?) "
                "ORDER BY timestamp DESC",
                (session_id, f'-{seconds} seconds')
            )
            rows = await cursor.fetchall()
            return [{"role": row[0], "content": row[1]} for row in rows]


    async def clear_history(self, session_id: str) -> None:
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("DELETE FROM history WHERE session_id = ?", (session_id,))
            await db.commit()
