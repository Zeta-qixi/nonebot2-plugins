from typing import Dict, Union
from nonebot import  get_driver
from datetime import datetime
from copy import deepcopy
import time
import aiohttp
import json

openai_key = get_driver().config.openai_key
PROXY='http://localhost:1080'

model_type = ['gpt-3.5-turbo', 'text-davinci-003', 'code-davinci-002']
class Mode:
    def __init__(
        self,
        mode_name,
        model_index=0,
        **kwargs
    ):
        self.mode_name = mode_name
        self._data = kwargs
        self._data['model'] = model_type[model_index]
        self._data['messages'] = [{'role':'system', 'content': kwargs.get('messages')}] if 'messages' in kwargs else []


    @property
    def data(self):
            return deepcopy(self._data)






"""
        mode_name: str,
        max_tokens:int = 150,

        模型参数  参考 https://platform.openai.com/docs/guides/chat
        temperature:  [0, 2], 默认1 ; 设置越高,输出更随机; 设置越低,输出更精确; 不建议和top_p同时修改
        top_p:float: [0, 1], 默认1; 输出质量阈值, 设置0.1 表示只考虑最多10%可能的输出; 一般设置为 1
        frequency_penalty:  [-2, 2], 默认0; 重复惩罚项, 一般设置为[0,1]之间, 大于1可能会降低采样质量
        presence_penalty:  [-2, 2], 默认0;  创新（谈论新话题）惩罚项

        关于两个惩罚项
        mu[j] -> mu[j] - c[j] * alpha_frequency - float(c[j] > 0) * alpha_presence
"""
mode_list = [


Mode('ATRI', max_tokens = 300, temperature = 0.9, top_p = 1.0, frequency_penalty = 0.3, presence_penalty = 0.6, 
messages = "现在你叫ATRI，自称高性能机器人；之后的回答都要用atri代替“我”。"),
Mode('QA'),
Mode('chat',max_tokens = 80, temperature = 0.5, top_p=1.0, frequency_penalty=0.5),
Mode('SQL_request', max_tokens = 100, temperature = 0.3, top_p = 1.0),
Mode('story_creator', max_tokens = 60, temperature = 0.3, frequency_penalty = 1.0, presence_penalty = 0.5),
]


# User

class User:
    def __init__(self):
        
        self.last_time = 0
        self.mode_type = 0
        self.day = 0
        self.times = 5
        self.messages = []


    def add_message(self, msg: Union[Dict,str]):

        if type(msg) == str:
            self.check_time()
            msg = {"role":"user","content":msg}
        self.messages.append(msg)


    def check_time(self):
        # 根据上次回复时间差 新开会话
        if (t:=time.time()) - self.last_time > 300 and self.mode_type != 1: # QA下不知道清除历史对话
            self.messages = []
            self.last_time = t

    def check_times(self):
        # 次数限制
        if (d:=datetime.today().strftime('%d')) != self.day:
            self.day = d
            self.times = 5
        if self.times:
            return True
        return False



class User_list:
    def __init__(self):
        self.data = {}

    def get_user(self, id):
        if not self.data.get(id):
            self.data[id] = User()
        return self.data[id]
    
user_list = User_list()




url = 'https://api.openai.com/v1/chat/completions'
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + openai_key,
}


async def get_chat(user: User):

    data = mode_list[user.mode_type].data
    data['messages'] += user.messages

    print(data)

    async with aiohttp.ClientSession() as session:
        async with session.post(url=url, headers=headers, data=json.dumps(data), proxy=PROXY) as resp:
            response = await resp.json()
            
            if not response.get('choices'):
                print(response)
                return(f'请求出错\n{str(response)}')
            user.add_message(response['choices'][0]['message'])
            user.times -= 1
            return (response['choices'][0]['message']['content'])
