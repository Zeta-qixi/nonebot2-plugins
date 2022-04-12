from nonebot import on_command, get_driver
from nonebot.adapters.onebot.v11.bot import Bot
from nonebot.adapters.onebot.v11.event import GroupMessageEvent
from nonebot import logger
try:
    master =  get_driver().config.master
except:
    master = []

withdraw = on_command('撤回')
@withdraw.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    
    if event.reply:
        
        try:
            if event.reply.sender.user_id == int(bot.self_id) or event.reply.sender.user_id in master:
                await bot.delete_msg(message_id=event.reply.message_id)
                await bot.delete_msg(message_id=event.message_id)
            else:
                ...
                # await withdraw.finish(message="你没有权限哦～")
            
        except BaseException as e:
            await withdraw.finish(message="撤回不了哦～")