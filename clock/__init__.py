from nonebot import get_bot, on_command, on_regex, logger, require, on_message
from nonebot.typing import T_State
from nonebot.matcher import Matcher
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import (Message, GroupMessageEvent, MessageEvent, MessageSegment)
import random
from .model import Clock
from .database.database import db

from .handle.job import add_clock, del_clock, get_clock_by_owner, JobHandle, enabled_clock, disable_clock
from .uilts import (get_event_info, simple_time_to_cron, 
                    message_to_db, db_to_message, 
                    parse_natural_language)


scheduler = require('nonebot_plugin_apscheduler').scheduler
class Myhandle(JobHandle):
    def __init__(self, db, scheduler):
        super().__init__(db, scheduler)
    async def _job_function(self, clock: Clock):
        message = await db_to_message(clock.content)
        if clock.type == 'private':
            await get_bot().send_msg(message_type=clock.type, user_id=clock.user_id, message=message)
        elif clock.type == 'group':
            message = MessageSegment.at(clock.user_id) + message
            await get_bot().send_msg(message_type=clock.type, group_id=clock.group_id, message=message)
        if clock.is_one_time:
            del_clock(myhandle, clock)
myhandle = Myhandle(db, scheduler)



natural_language_add_clock = on_message(block=False)

check = on_regex("^(查看闹钟|提醒事项|闹钟|⏰)$" ,block=True)
del_clock_qq = on_command('删除闹钟', block=True)
add_clock_qq = on_command('添加闹钟', aliases={'设置闹钟',}, block=True)
enabled_clock_qq = on_command('打开闹钟', aliases={'开启闹钟',}, block=True)
disabled_clock_qq = on_command('关闭闹钟', block=True)

# 创建闹钟
@natural_language_add_clock.handle()
async def _(matcher: Matcher, event: MessageEvent, state: T_State): 

    content, cron_expression = parse_natural_language(event.get_plaintext())
    if content and cron_expression:
        
        data = {
            'id': 0,
            'is_one_time': True,
            'cron_expression': cron_expression,
            'content': message_to_db(Message(content))
        }
        data['type'], data['group_id'] ,data['user_id'] = get_event_info(event)
        add_clock(myhandle, **data)
        tmp_respone = ['嗯','好的','明白了，我会记住的。','知道啦']
        await matcher.finish(message=random.choice(tmp_respone))
    

# 创建闹钟
@add_clock_qq.handle()
async def _(matcher: Matcher, event: MessageEvent, state: T_State, messages: Message = CommandArg()): 
    try:
       state['cron_expression'] = simple_time_to_cron(str(messages[0]))
       state['type'], state['group_id'] ,state['user_id'] = get_event_info(event)
       if str(messages[0]).startswith('+'):
           state['is_one_time'] = True
    except Exception as e:
        logger.error(repr(e))
        await matcher.finish(message="""【时间格式错误】 示例>
（时间）添加闹钟 21:00
（日期&时间）添加闹钟 3.7 12:30
（n小时、分钟后）添加闹钟 +3h
cron表达式""")
        
    
@add_clock_qq.got('content', prompt="请设置闹钟内容(可以发送图片)")
async def _(matcher: Matcher, state: T_State):
    state['content'] = message_to_db(state['content'] )
    data = {
        'id': 0, # 临时, 入库后自动修改
        'type' : state['type'],
        'group_id' : state['group_id'],
        'user_id' : state['user_id'],
        'content' : state['content'],
        'cron_expression' : state['cron_expression'],
        'is_one_time': state.get('is_one_time', False),

    }
    add_clock(myhandle, **data)
    await matcher.finish(message=f"添加成功～")


@check.handle()
async def _(matcher: Matcher, event: MessageEvent):

    _, gid, uid = get_event_info(event)
    clock_msg = []
    for i, clock in enumerate(get_clock_by_owner(myhandle, uid=uid, gid=gid)):
        conent = await clock.get_info()
        clock_msg.append(f"{i+1}. {conent}")
    if clock_msg:
        await matcher.finish(message= Message('\n'.join(clock_msg)))
    else:
        await matcher.finish(message='目前没有闹钟')
    


# 删除闹钟
@del_clock_qq.handle()
async def _(matcher: Matcher, event: GroupMessageEvent, ids = CommandArg()):

    
    try:
        _, gid, uid = get_event_info(event)
        clock = get_clock_by_owner(myhandle, uid=uid, gid=gid)[int(str(ids))-1]
        del_clock(myhandle, clock)
        await matcher.finish(message=f'操作完成')
    except Exception as e:
        logger.error(repr(e))
        await matcher.finish(message=f'出现了问题...')
    


@enabled_clock_qq.handle()
async def _(matcher: Matcher, event: GroupMessageEvent, ids = CommandArg()):

   
    try:
        _, gid, uid = get_event_info(event)
        clock = get_clock_by_owner(myhandle, uid=uid, gid=gid)[int(str(ids))-1]
        if enabled_clock(myhandle, clock):
            await matcher.finish(message=f'操作完成')
    except Exception as e:
        logger.error(repr(e))
        await matcher.finish(message=f'出现了问题...')
    


@disabled_clock_qq.handle()
async def _(matcher: Matcher, event: GroupMessageEvent, ids = CommandArg()):

    
    try:
        _, gid, uid = get_event_info(event)
        clock = get_clock_by_owner(myhandle, uid=uid, gid=gid)[int(str(ids))-1]
        if disabled_clock(myhandle, clock):
            await matcher.finish(message=f'操作完成')
    except Exception as e:
        logger.error(repr(e))
        await matcher.finish(message=f'出现了问题...')