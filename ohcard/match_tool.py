import cv2
import os
import numpy
from PIL import Image

from aip import AipOcr

from nonebot import logger
from nonebot import get_driver

from .data_load import PATH
from .utils import aio_get_image

try:
    api_key = get_driver().config.ocr_key
    client = AipOcr(api_key['appId'], api_key['apiKey'], api_key['secretKey'])
except:
    ...

# 使用OCR API 
# def match(url :str):
#     res = client.basicGeneralUrl(url)
#     logger.info('识别完成')
#     if {'words': '配餐中'} in res['words_result'] and {'words': '待取餐'} in res['words_result']:
#         return True


templates_file = PATH+'templates/'
if not os.path.exists(templates_file):
    os.mkdir(templates_file)

async def match(url: str):
    
    target_img = await aio_get_image(url)
    target = cv2.cvtColor(numpy.asarray(target_img),cv2.COLOR_RGB2BGR)

    templates = os.listdir(templates_file)
    for flie in templates:
        template =  cv2.imread(templates_file + flie)
        t_height, t_width = template.shape[:2]
        result = cv2.matchTemplate(target, template, cv2.TM_SQDIFF_NORMED)
        
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        if min_val < 0.01:
            return(True)