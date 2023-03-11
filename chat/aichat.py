from nonebot.adapters.onebot.v11.bot import Bot
from nonebot import on_command, on_message
from nonebot.adapters.onebot.v11.message import MessageSegment
from nonebot.adapters.onebot.v11.event import GroupMessageEvent, Message
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.params import CommandArg
from .permission import CHAT_PERM

from .gpt import mode_list, user_list, get_chat



chat = on_message(rule=CHAT_PERM, priority=90, block=True)
@chat.handle()
async def _(bot: Bot, event: GroupMessageEvent):

    user = user_list.get_user(event.user_id)
    
    # if not user.check_times:
    #     await chat.finish(message='atri现在不想和你说话了')
        
    msg = str(event.get_message())
    user.add_message(msg)
    response_content = await get_chat(user)
    await chat.send(message = MessageSegment.at(event.user_id) + response_content.strip())



reset_chat = on_command('重置对话',aliases={'清空对话'},block=True)
@reset_chat.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    user_list.get_user(event.user_id).messages = []
    await reset_chat.finish(message='重置成功')



get_params = on_command('/chat', block=True)
@get_params.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State, msg: Message = CommandArg()):

    state['user'] = user_list.get_user(event.user_id)
    state['user'].last_time = 0
    if msg:
        state['ret'] = msg
    else:
        using = {state['user'].mode_type :'●'}
        await get_params.send(message = '\n'.join([f'{using.get(i, "○")}{i}.{c.mode_name}' for i, c in enumerate(mode_list)]))


@get_params.got('ret', prompt='选择更改的mode')
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
        
        index = int(str(state['ret']))
        assert index < len(mode_list)
        state['user'].mode_type = index
        await get_params.finish(message='ok~')
       