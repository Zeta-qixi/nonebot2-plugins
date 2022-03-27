from nonebot import on_command, logger
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11.bot import Bot
from nonebot.adapters.onebot.v11.event import GroupMessageEvent, Message


change = on_command('更改头衔',aliases={'申请头衔'}, block=True)
@change.handle()
async def special_title(bot: Bot, event: GroupMessageEvent, title: Message=CommandArg()):
    '''
    群头衔
    '''
    title = str(title)
    user_id = event.user_id
    group_id = event.group_id
    await bot.set_group_special_title(group_id=group_id, user_id=user_id, special_title=title,self_id=bot.self_id)



ban_to_sleep = on_command("精致睡眠", block=True)
@ban_to_sleep.handle()
async def ban_sleep(bot: Bot, event: GroupMessageEvent):
    id = event.user_id
    group = event.group_id
    await bot.set_group_ban(group_id=group, user_id=id, duration=60*60*8)
