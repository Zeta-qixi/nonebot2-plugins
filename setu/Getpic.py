import requests
import time
import datetime
import re
import random
class setubot:
    def __init__(self):
        #self.T = str((datetime.datetime.now()+datetime.timedelta(days=-2)).strftime("%Y-%m-%d")) #time 或许要用 前天
        self.R18 = 0
        self.key = '335515915f9b5c853e4e90'
        self.mode = ['day', 'week', 'month', 'day_male', 'day_female', 'week_rookie', 'week_original']
        self.mode_ = 3
        self.pic_id = 0 


    def Cmode(self, num):
        self.mode_ = int(num)
        return self.mode[self.mode_]
    def tR18(self):
        if self.R18 ==0:
            self.R18 = 1
        else :
            self.R18 = 0
        return self.R18

    #检索
    def getpic(self, num=1, keyword=''):
        url = 'https://api.lolicon.app/setu/?'
        params = {
        'apikey' : self.key,
        'num' : num,
        'keyword' : f'{keyword}',
        'r18' : self.R18, #  0 false 1 true
        'size1200' : 'true'
        }
        r = requests.get(url,params=params)
        data = json.loads(r.text)['data']
        pic = []
        for item in data:
            pic.append(item['url'])
        return pic

