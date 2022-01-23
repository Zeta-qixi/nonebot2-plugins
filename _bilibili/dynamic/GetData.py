import requests
import json
import time


class Dynamic():
    def __init__(self, dynamic):
        self.id = dynamic['desc']['dynamic_id']
        self.dynamic = dynamic
        self.url = "https://t.bilibili.com/" + str(self.id)
        self.time = dynamic['desc']['timestamp']
        self.name = dynamic['desc']['user_profile']['info'].get('uname')

        self.type = dynamic['desc']['type']
        '''
        4/2: 新动态 图片/文字？",
        1: "转发",
        8: "新投稿",
        16: "短视频",
        64: "专栏",
        256: "音频"
        '''
    def get(self):
        return (self.name, self.type, self.url, self.time)

def get_dynamic(mid):
    url = f'https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history?'
    params = {
        'host_uid' : mid,
        'ffset_dynamic_id':0,
        'need_top=0':0
    }
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88\
    Safari/537.36 Edg/87.0.664.60',

        'Referer': 'https://www.bilibili.com/'
    }

    r = requests.get(url, params=params, headers = headers)
    r.encoding = 'utf-8'
    return json.loads(r.text)['data']