import os
import json
import requests
from lxml import etree
from nonebot import on_command, on_regex
from nonebot.adapters.onebot.v11.bot import Bot
from nonebot.adapters.onebot.v11.event import Event
from nonebot.adapters.onebot.v11.message import Message

from nonebot.typing import T_State
from nonebot.params import CommandArg

PATH = os.path.dirname(__file__)

import requests
tq = {
    
    '晴': '☀️', 
    '阴':'☁️',
    '云':'☁️',
    '雪':'❄️',
    '雨':'🌧️', 
    }

class weather_data:
    def __init__(self, **params):
        self.temp = params['temp']
        self.location = params['location']
        self.feelsLike = params['feelsLike'] # 体感温度
        self.text = params['text'] # 气象
        self.obsTime = params['obsTime'] # 数据观测时间
        self.icon = '☁️'
        for i in tq:
            if i in self.text:
                self.icon = tq[i]
                break

    def __str__(self):
        return (f'{self.location}当前温度: {self.temp}˚C\n体感温度: {self.feelsLike}˚C\n天气「{self.text}」{self.icon}')
        

class heweather:
    def __init__(self):

        self.headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
        }
        self.params = {}
        self.load_file()

    def load_file(self):
        with open(f'{PATH}/asset/location.json', 'r') as f:
            self.location_id_dict = json.load(fp=f)
        with open(f'{PATH}/asset/data.json', 'r') as f:
            data = json.load(fp=f)
            self.params['key'] = data['key']
            self.city = data['city']

    def save_city_info(self):
        with open(f'{PATH}/asset/data.json', 'w') as f:
            data = {'key': self.params['key']}
            data['city'] = self.city
            json.dump(data, f)
    
    def save_location_id(self):
        with open(f'{PATH}/asset/location.json', 'w') as f:
            json.dump(self.location_id_dict, f)


    def get_weather(self, location):
        params=self.params
        localid = self.location_id_dict.get(location)
        if not localid:
            self.get_location_id(location)
            localid = self.location_id_dict.get(location)
        params['location'] = localid
        res = requests.get(url='https://devapi.qweather.com/v7/weather/now', headers=self.headers, params=self.params)
        assert res.status_code == 200
        data = res.json()['now']
        data['location'] = location
        return weather_data(**data)
        
    def get_location_id(self, city):
        params=self.params
        params['location'] = city
        res = requests.get(url='https://geoapi.qweather.com/v2/city/lookup', headers=self.headers, params=self.params)
        assert res.status_code == 200
        data = res.json()['location']
        
        for i in data:
            self.location_id_dict[i['name']] = i['id']
        self.save_location_id()






wbot = heweather()
setcity = on_command('设置天气城市', priority=10, block=True)
weather = on_regex('^(.*)天气|气温|多少度|几度', block=False, priority=11)


@weather.handle()
async def weather_handle(bot: Bot, event: Event, state: T_State):
    city = state['_matched_groups'][0]
    if city in ['', '今天', '今日']:
        city = wbot.city.get(str(event.user_id))

    msg = wbot.get_weather(city)
    await weather.finish(message = str(msg))


@setcity.handle()
async def weather_handle(bot: Bot, event: Event, state: T_State, city:Message = CommandArg()):
    city = str(city)
    wbot.city[str(event.user_id)] = city
    wbot.save_city_info()
    await setcity.finish(message=f"已设置当前城市为{city}")
