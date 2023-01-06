from nonebot.permission import Permission
from nonebot.adapters.onebot.v11.event import MessageEvent
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11.permission import (
    GROUP_ADMIN,
    GROUP_OWNER
)

try:
    master = get_driver().config.master
except:
    master = []

async def _master(event: MessageEvent) -> bool:
    return event.user_id in master or event.group_id in [960349339, 960349339]

CHAT_PERM = Permission(_master) and to_me()