from .model import Clock
from nonebot import on_command, on_regex, logger
from nonebot.typing import T_State
from nonebot.matcher import Matcher
from nonebot.params import CommandArg, Command
from nonebot.adapters.onebot.v11 import (Message, MessageEvent)

from .handle import job_handle
from .utils import (get_event_info, simple_time_to_cron, 
                    message_to_db)

check = on_regex("^(查看闹钟|提醒事项|闹钟|⏰)$" ,block=True) 
del_clock_qq = on_command('删除闹钟', block=True) 
add_clock_qq = on_command('添加闹钟',  aliases={"添加提醒", "添加临时闹钟", "添加临时提醒"}, block=True) 
enabled_clock_qq = on_command('开启闹钟', aliases={'开启提醒',}, block=True) 
disabled_clock_qq = on_command('关闭闹钟', aliases={'关闭提醒',}, block=True)


ADD_CLOCK_PROMPT = """ 示例>
1. 时间: /添加闹钟 21:00
2. 日期+时间: /添加闹钟 3.7 12:30
3. N小时、分钟后: /添加闹钟 +3h
4. cron表达式[5位]: /添加闹钟 30 8 * * *"""



@check.handle()
async def _(matcher: Matcher, event: MessageEvent):
    _, gid, uid = get_event_info(event)
    clocks = job_handle.list_clock(uid=uid, gid=gid)

    if not clocks:
        await matcher.finish("目前没有闹钟")

    clock_msg = []
    for i, clock in enumerate(clocks):
        info = await clock.get_info()
        clock_msg.append(f"{i+1}. {info}")

    await matcher.finish(Message("\n".join(clock_msg)))



@add_clock_qq.handle()
async def _(matcher: Matcher, event: MessageEvent, state: T_State, command: tuple = Command(), raw_msg: Message = CommandArg()):

    
    raw_msg = str(raw_msg)
    if not raw_msg:
        await matcher.finish("请附带时间" + ADD_CLOCK_PROMPT)
    
    try:
        cron_expr = simple_time_to_cron(raw_msg)
        typ, gid, uid = get_event_info(event)
        state['cron_expr'] = cron_expr
        state['type'] = typ
        state['gid'] = gid
        state['uid'] = uid
        state['is_one_time'] = True if '临时' in command[0] else False
    except ValueError:
        logger.exception("时间解析失败")
        await matcher.finish("时间解析失败" + ADD_CLOCK_PROMPT)


@add_clock_qq.got("content", prompt="请设置闹钟内容(可以发送图片)")
async def receive_content(matcher: Matcher, state):
    content = state.get("content")
    if not content:
        await matcher.finish("闹钟内容不能为空")

    payload = {
        "id": 0,
        "type": state['type'],
        "group_id": state['gid'],
        "user_id": state['uid'],
        "content": message_to_db(content),
        "cron_expression": state['cron_expr'],
        "is_one_time": state['is_one_time'],
    }

    job_handle.add_clock(Clock(payload))
    await matcher.finish("添加成功")





# 删除闹钟
@del_clock_qq.handle()
async def _(matcher: Matcher, event: MessageEvent, ids = CommandArg()):

    
    try:
        _, gid, uid = get_event_info(event)
        clock = job_handle.list_clock(uid=uid, gid=gid)[int(str(ids))-1]
        job_handle.delete_clock(clock)
        await matcher.send(message=f'操作完成')
    except Exception as e:
        logger.error(repr(e))
        await matcher.finish(message=f'出现了问题...')
    


@enabled_clock_qq.handle()
async def _(matcher: Matcher, event: MessageEvent, ids = CommandArg()):

   
    try:
        _, gid, uid = get_event_info(event)
        clock = job_handle.list_clock(uid=uid, gid=gid)[int(str(ids))-1]
        job_handle.enabled_clock(clock)
        await matcher.send(message=f'操作完成')
    except Exception as e:
        logger.error(repr(e))
        await matcher.finish(message=f'出现了问题...')
    


@disabled_clock_qq.handle()
async def _(matcher: Matcher, event: MessageEvent, ids = CommandArg()):

    try:
        _, gid, uid = get_event_info(event)
        clock = job_handle.list_clock(uid=uid, gid=gid)[int(str(ids))-1]
        job_handle.disable_clock(clock)
        await matcher.send(message=f'操作完成')
    except Exception as e:
        logger.error(repr(e))
        await matcher.finish(message=f'出现了问题...')