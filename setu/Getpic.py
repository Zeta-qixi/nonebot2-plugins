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
        msg = r.text
        row_list = msg.split('"url":"')
        row_list.pop(0)
        pic = []
        for i, row in enumerate(row_list):
            pic.append(row.split('","')[0].replace('\\',''))
        return pic

    ##画师
    def artist(self,num=1, artistID=''):
        
        url = f'https://api.imjad.cn/pixiv/v1/?type=member_illust&id={artistID}'
        r = requests.get(url)
        msg = r.text.replace('\\','')
        list1 = msg.split('img-master/img/')#split('img-master/img/')
        list1.pop(0)
        setu_list = []
        for i in list1:
            if 'master1200' in i:
                setu_list.append('https://i.pixiv.cat/img-master/img/'+i.split('"')[0])
        
        return setu_list[:num]
        
    
    ##rank榜
    def rank(self,**kwargs):

        modetype = self.mode_
        ttime = str((datetime.datetime.now()+datetime.timedelta(days=-1)).strftime("%Y-%m-%d"))
        if kwargs:
            modetype = kwargs['mode']
        early=int(time.strftime("%H", time.localtime()))
        if early < 12 :
            ttime = str((datetime.datetime.now()+datetime.timedelta(days=-2)).strftime("%Y-%m-%d"))
            

        
        url = f'https://api.imjad.cn/pixiv/v2/?type=rank&mode={self.mode[modetype]}&page=1&date={ttime}'
        r = requests.get(url)
        msg = r.text.replace('\\','')
        list = msg.split('img-original/img/')
        list.pop(0)
        res = []
        id_type = {}
        for i in  list:
            type = re.split(r'_p\d+',i)[1].split('"')[0]
            id = re.split(r'_p\d+',i)[0]
            id_type[id] = type
            res.append(id)
        from collections import Counter
        b = dict(Counter(res))
        pic = []
        for key,value in b.items() :
            if value == 1 :
                pic.append('https://i.pixiv.cat/img-original/img/' + key + '_p0' + id_type[key])   
        return pic
