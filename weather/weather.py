import base64
import json
from pathlib import Path

import requests
from .model import Weather
PATH = Path("data/weather")





class Qeweather:
    def __init__(self, key):

        self.headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
        }
        self.params = {'key': key}
        self.init_from_file()

    def init_from_file(self):
        with open(f'{PATH}/weather/location.json', 'r') as f:
            self.location_id_dict = json.load(fp=f)
        with open(f'{PATH}/weather/data.json', 'r') as f:
            data = json.load(fp=f)
            self.city = data['city']

    def save_city_info(self):
        with open(f'{PATH}/weather/data.json', 'w') as f:
            data['city'] = self.city
            json.dump(data, f)
    
    def save_location_id(self):
        with open(f'{PATH}/weather/location.json', 'w') as f:
            json.dump(self.location_id_dict, f)


    def get_weather(self, location) -> Weather:

        localid = self.location_id_dict.get(location)
        if not localid:
            self.get_location_id(location)
            localid = self.location_id_dict.get(location)
        self.params['location'] = localid

        res = requests.get(url='https://devapi.qweather.com/v7/weather/now', headers=self.headers, params=self.params)
        assert res.status_code == 200
        data = res.json()['now']
        data['location'] = location
        return Weather(data)
        
    def get_location_id(self, city):
        params=self.params
        selfparams['location'] = city
        res = requests.get(url='https://geoapi.qweather.com/v2/city/lookup', headers=self.headers, params=self.params)
        assert res.status_code == 200
        data = res.json()['location']
        
        for i in data:
            self.location_id_dict[i['name']] = i['id']
        self.save_location_id()

