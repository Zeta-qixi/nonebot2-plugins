import re
import os
from pathlib import Path
from typing import Tuple
import requests
from datetime import datetime, timedelta
from nonebot.adapters.onebot.v11 import MessageEvent, GroupMessageEvent, Message, MessageSegment, PrivateMessageEvent
from nonebot.adapters.qq import GuildMessageEvent, DirectMessageCreateEvent
from .llm import decorate_content
import uuid
import re
from datetime import datetime
from .config import IMAGE_DIR, USE_LLM

if not os.path.exists(IMAGE_DIR):
    os.mkdir(IMAGE_DIR)


def message_to_db(message: Message):

    def download(url: str) -> Path:
        if not url.startswith('http'):
            url = 'https://' + url
        res = requests.get(url)
        path = IMAGE_DIR.joinpath(f'{uuid.uuid4()}.jpg')
        with open(path, 'wb') as f:
            f.write(res.content)
        return  path
    
    content = ''
    for msg in message:
        if msg.type == 'image':
            url = msg.data['url']
            content += f"<image:{download(url)}>"
        else:
            content += f"<text:{str(msg)}>"
    return content


async def db_to_message(content: str, only_show = False):

    message = Message()
    pattern = r"<(image|text):([^>]+)>"
    parts = re.split(pattern, content)
    for i in range(0,len(parts)-1,3):
        _, _type, data = parts[i:i+3]
        if _type == 'image':
            message += MessageSegment.image(Path(data)) # type: ignore
        elif _type == 'text':
            if not only_show and USE_LLM:
                data = await decorate_content(data) 
            message += Message(data)
    
    return message



def get_event_info( event: MessageEvent ) -> Tuple[str, str, str]:
        """
        Return (type gid uid)
        """
        if isinstance(event, DirectMessageCreateEvent): # 频道私聊
            return ('dms', event.guild_id, event.get_user_id()) 
        elif isinstance(event, GuildMessageEvent):
            return ('channel', event.channel_id, event.get_user_id()) 
        elif isinstance(event, GroupMessageEvent):
            return ('group', str(event.group_id), str(event.get_user_id()))
        elif isinstance(event, PrivateMessageEvent):
            return ('private', '0', event.get_user_id())
            

def simple_time_to_cron(time_str: str) -> str:
    """
    将简化的时间字符串转换为标准的Cron表达式(5位)。
    """
    time_str = time_str.strip()
    
    if len(time_str.split()) == 5:
        return time_str
    
    month, day, weekday = '*', '*', '*'
    if time_str.startswith('+'):
        h = re.search(r"(\d+)[hH时]",time_str)
        m = re.search(r"(\d+)[mM分]",time_str)
        h=int(h.groups()[0]) if h else 0
        m=int(m.groups()[0]) if m else 0
        target_time = datetime.now() + timedelta(hours=h, minutes=m)
        hour = target_time.hour
        minute = target_time.minute

    elif r:=re.match(r'(\d+)[.|-|/](\d+) (\d+)[:|：|.](\d+)',time_str):
        month, day, hour, minute = map(int, r.groups())
        assert 1 <= month <=12 and 1<= day <=31, "Invalid date"
    elif r:=re.match(r'(\d+)[:|\-|：|.](\d+)',time_str):
        hour, minute = map(int, r.groups())
    else:
        minute, hour, day, month, weekday = time_str.split()
    assert 0 <= hour <24 and 0<= minute <60, "Invalid time"
    return f"{minute} {hour} {day} {month} {weekday}"  


def cron_to_natural(cron_expr: str) -> str:
    """
    Cron表达式转为自然语言, 目前不支持 / - 等表示
    """
    fields = cron_expr.split()
    if len(fields) != 5:
        # "无效的 cron 表达式"
        return cron_expr
    minute, hour, day, month, weekday = fields
    # 处理星期
    weekdays = {
        "0": "周日", "1": "周一", "2": "周二", "3": "周三", "4": "周四",
        "5": "周五", "6": "周六","7": "周日"
    }

    time_str = f"{hour.zfill(2)}:{minute.zfill(2)}" if hour != "*" and minute != "*" else "任意时间"
    if month != "*" and day != "*":
        date_str = f"{month}月{day}日"
    elif month != "*":
        date_str = f"{month}月的每天"
    elif day != "*":
        date_str = f"每月{day}日"
    else:
        date_str = "每天"
    if weekday != "*":
        if day == "*":  # 如果没有指定具体日期
            date_str = f"每{weekdays.get(weekday, weekday)}"
        else:  # 既有日期又有星期
            date_str += f" 和 {weekdays.get(weekday, weekday)}"

    return f"{date_str} {time_str}"



def parse_natural_language(input_text: str):
    """
    从自然语言获取 内容 和 cron 表达式
    """
    time_patterns = [
        (r'(\d+)分钟后', lambda m: f'+{m.group(1)}m'),
        (r'(\d+)小时后', lambda m: f'+{m.group(1)}h'),
        (r'(\d+)天后', lambda m: f'+{m.group(1)}d'),
        (r'([零一二两三四五六七八九十百]+)分钟后', lambda m: f'+{convert_chinese_to_digit(m.group(1))}m'),
        (r'([一二两三四五六七八九十百]+)小时后', lambda m: f'+{convert_chinese_to_digit(m.group(1))}h'),
        (r'([一二两三四五六七八九十百]+)天后', lambda m: f'+{convert_chinese_to_digit(m.group(1))}d'),
        (r'(\d+):(\d+)', lambda m: f'{m.group(1)}:{m.group(2)}'),
        (r'([零一二两三四五六七八九十]+)点', lambda m: f'{convert_chinese_to_digit(m.group(1))}:00'),
    ]
    
    expression = None
    for pattern, formatter in time_patterns:
        match = re.search(pattern, input_text)
        if match:
            expression = formatter(match)
            break
    try:
        expression = simple_time_to_cron(expression)
        content = re.search(r'(提醒|叫)我(.*)', input_text).groups()[-1]
    except:
        content = None
    return (content, expression)

def convert_chinese_to_digit(chinese_num: str) -> int:
    mapping = {'零': 0, '一': 1, '二': 2, '两':2,'三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9, '十': 10, '百': 100}
    if chinese_num in mapping:
        return mapping[chinese_num]
    elif '百' in chinese_num:
        parts = chinese_num.split('百')
        return mapping[parts[0]] * 100 + (convert_chinese_to_digit(parts[1]) if parts[1] else 0)
    elif '十' in chinese_num:
        parts = chinese_num.split('十')
        if parts[0] == '':
            return 10 + mapping[parts[1]] if parts[1] else 10
        return mapping[parts[0]] * 10 + (mapping[parts[1]] if parts[1] else 0)
    return None