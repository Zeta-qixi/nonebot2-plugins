import os
import json
import requests
from lxml import etree
from nonebot import on_command, on_regex
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp.event import Event
from nonebot.typing import T_State

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
        with open(f'{PATH}/asset/data.txt', 'r') as f:
            key = f.readline().split()[0]
            self.params['key'] = key

    def save_(self):
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

        self.save_()

wbot = heweather()
weather = on_regex('(.*)天气|气温|多少度|几度', block=False)
@weather.handle()
async def weather_handle(bot: Bot, event: Event, state: T_State):
    city = state['_matched_groups'][0]
    msg = wbot.get_weather(city)
    await bot.send(event, message = str(msg))

