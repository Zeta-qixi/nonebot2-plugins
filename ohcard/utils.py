from io import BytesIO

import requests
from aip import AipOcr
from nonebot import get_driver
from PIL import Image
from nonebot import logger
from .data_load import PATH


api_key = get_driver().config.ocr_key
client = AipOcr(api_key['appId'], api_key['apiKey'], api_key['secretKey'])


def save_pic(url :str, name: str):
    res = requests.get(url)
    img = Image.open(BytesIO(res.content))
    img.save(PATH + name + ".png")

def check_pic(url :str):
    res = client.basicGeneralUrl(url)
    logger.info('识别完成')
    if {'words': '配餐中'} in res['words_result'] and {'words': '待取餐'} in res['words_result']:
        return True
