from nonebot import on_request, get_driver
from nonebot.adapters.onebot.v11.bot import Bot
from nonebot.adapters.onebot.v11.event import  GroupRequestEvent, FriendRequestEvent
from nonebot.adapters.onebot.v11.message import Message

try:
    master = get_driver().config.master
except:
    master = []

    
add_req = on_request()
@add_req.handle()
async def group_add(bot: Bot, event: GroupRequestEvent):
    '''
    入群申请
    '''
    if (event.sub_type) == "add":
        if str(event.comment) == 'ATRI -My Dear Moments-':
            await bot.set_group_add_request(flag=event.flag, sub_type='add', approve=True)
    elif (event.sub_type) == "invite":
        if event.user_id in master:
            await bot.set_group_add_request(flag=event.flag, sub_type='invite', approve=True)
    else :
        await bot.set_group_add_request(flag=event.flag, sub_type='invite', approve=False)


add_friend_req = on_request()
@add_friend_req.handle()

async def friend_add(bot: Bot, event: FriendRequestEvent):
    '''
    好友添加请求
    '''
    pass