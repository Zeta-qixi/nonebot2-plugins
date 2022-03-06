from io import BytesIO

import cv2
import requests
from aip import AipOcr
from nonebot import get_driver
from PIL import Image

from .data_load import PATH

data = get_driver().config.oh_mai
'''
# .env.dev

OH_MAI = {"appId":"", "apiKey":"","secretKey": ""}

'''

client = AipOcr(data['appId'], data['apiKey'], data['secretKey'])



def save_pic(url :str, name: str):
    res = requests.get(url)
    img = Image.open(BytesIO(res.content))
    img.save(PATH + name + ".png")

def check_pic(url :str):
    res = client.basicGeneralUrl(url_)
    if {'words': 'OH麦卡OH麦卡月卡四件套25元起'} in res['words_result'] or {'words': 'OH麦卡四件套25元起'} in res['words_result']:
        return('25')

    elif {'words': 'OH麦卡早餐3件套6折'} in res['words_result']:
        return('breakfast')
