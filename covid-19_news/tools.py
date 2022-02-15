import requests
from typing import Dict, List
import json


POLICY_ID = {}
def set_pid():
    url_city_list = 'https://r.inews.qq.com/api/trackmap/citylist?'
    resp = requests.get(url_city_list)
    res = resp.json()

    for province in res['result']:
        if citys := province.get('list'):
            for city in citys:
                id = city['id']
                name = city['name']
                POLICY_ID[name] = id

try:
    set_pid()
except:
    pass


def citypolicy_info(id):
    url_get_policy = f"https://r.inews.qq.com/api/trackmap/citypolicy?&city_id={id}"
    resp = requests.get(url_get_policy)
    res_ = resp.json()
    assert res_['message'] == 'success'
    return (res_['result']['data'][0])

def get_policy(id):

    data = citypolicy_info(id)
    msg = f"出行({data['leave_policy_date']})\n{data['leave_policy']}\n\
------\n\
进入({data['back_policy_date']})\n{data['back_policy']}"
    return (msg)

def get_city_poi_list(id):

    data = citypolicy_info(id)['poi_list']
    t = {'0':'🟢','1':'🟡', '2':'🔴'}   
    list_ = [f"{t[i['type']]}{i['area'].split(i['city'])[-1]}" for i in data]
    return '\n\n'.join(list_) if data else "🟢全部低风险"



class Area():
    def __init__(self, data):
        self.name = data['name']
        self.today = data['today']
        self.total = data['total']
        self.grade = data['total'].get('grade', '风险未确认')
        self.children = data.get('children', None)

    @property
    def policy(self):
        return get_policy(POLICY_ID.get(self.name))

    @property
    def poi_list(self):
        return get_city_poi_list(POLICY_ID.get(self.name))

    @property
    def main_info(self):
        return (f"{self.name}({self.grade})\n今日新增: {self.today['confirm']}\n目前确诊: {self.total['nowConfirm']}")


class AreaList(Dict):
    def add(self, data):
        self[data.name] = data

    
class NewsData:
    def __init__(self):
        self.data = {}
        self.time = ''
        self.update_data()

    def update_data(self):
        url = "https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5"
        res = requests.get(url).json()

        assert res['ret'] == 0
        data = json.loads(res['data'])

        if data['lastUpdateTime'] != self.time:
            
            self.time = data['lastUpdateTime']
            self.data = AreaList()

            def get_Data(data):
                
                if isinstance(data, list):
                    for i in data:
                        get_Data(i)

                if isinstance(data, dict):
                    if area_:=data.get('children'):
                        get_Data(area_)

                    self.data.add(Area(data))

            get_Data(data['areaTree'][0])
            return True


