import requests
import time
import datetime
import re
import random
import json
class setubot:
    def __init__(self):
        #self.T = str((datetime.datetime.now()+datetime.timedelta(days=-2)).strftime("%Y-%m-%d")) #time 或许要用 前天
        self.R18 = 0
        self.key = '335515915f9b5c853e4e90'
        self.mode = ['day', 'week', 'month', 'day_male', 'day_female', 'week_rookie', 'week_original']
        self.mode_ = 3
        self.pic_id = []


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
    def setu_info(self, num=1, tag=''):
        url = 'https://api.lolicon.app/setu/v2/?' #v2的图太大
        params = {
        'apikey' : self.key,
        'num' : num,
        'tag' : f'{tag}',
        'r18' : self.R18, #  0 false 1 true
                          #  'size1200' : 'true'
        }
        r = requests.get(url, params=params)
        try:
            data = json.loads(r.text)['data']
            pic_url = []
            for item in data:
                pic_url.append(item['urls']['original'])

            return pic_url
        except:
            print(r)
            return []



#https://i.pixiv.cat/img-master/img/2021/01/13/23/48/44/87033047_p0_master1200.jpg

#https://i.pixiv.cat/img-original/img/2020/07/31/15/06/48/81664783_p0.png