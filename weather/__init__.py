from nonebot import on_command, on_regex
from nonebot import get_driver
from nonebot.typing import T_State
from nonebot.params import CommandArg
from nonebot.matcher import Matcher
from nonebot.adapters.onebot.v11.bot import Bot
from nonebot.adapters.onebot.v11.event import Event

from nonebot.adapters.onebot.v11.message import Message, MessageSegment
from .model import generator
from .llm import llm_respone
from .weather import Qeweather

config = get_driver().config
wbot = Qeweather(getattr(config, 'qweather_apikey'))

setcity = on_command('设置天气城市', priority=10, block=True)
ask_weather = on_regex('^(.*)天气|气温|多少度|几度', block=False, priority=11)


@ask_weather.handle()
async def weather_handle(matcher: Matcher, bot: Bot, event: Event, state: T_State):

    city = state['_matched'].groups()[0]
    if city in ['', '今天', '今日']:
        city = wbot.city.get(str(event.user_id))
    weather = wbot.get_weather(city)
    img_base64 = generator.generate_card(weather, return_bytes=True)
    await matcher.send(message = MessageSegment.image(f'base64://{img_base64}'))
    respone = await llm_respone(weather)
    await matcher.finish(message = respone)


@setcity.handle()
async def weather_handle(matcher: Matcher, event: Event, state: T_State, city:Message = CommandArg()):
    city = str(city)
    wbot.city[str(event.user_id)] = city
    wbot.save_city_info()
    await matcher.finish(message=f"已设置当前城市为{city}")