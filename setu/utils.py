from typing import List, Tuple
from nonebot.log import logger
import random
import time
import aiohttp
import asyncio

import json
import os

HEADERS = {'Referer': 'https://www.pixiv.net',}
PROXY = ""
TOKEN = ""
VIP = False

try:
    PATH = os.path.dirname(__file__) + "/data.json"
    with open(PATH) as f:
        data = json.load(f)
        PROXY = data['PROXY']
        TOKEN = data['TOKEN']
except:
    pass


def set_random_seed(id):
    seed = int(int(time.time())) ^ id
    random.seed((seed))


def get_original_url( works: List) -> Tuple[List[str], List[str]]:
    """
    input  -> 
        已重写的方法返回的result集合
        or 父类方法的result['illusts']

    return  -> 
        URL 集合
    """
    urls = []
    msgs = []
    for work in works:
        try:
            for w in work['meta_single_page'].values():
                urls.append(w)
                msgs.append({'id':work.id, 'artist':work.user.id})
            for i, w in enumerate(work['meta_pages']):
                urls.append(w['image_urls']['original'])
                msgs.append({'id':f"{work.id}_p{i}", 'artist':work.user.id})
                if i>3:
                    break
        except:
            ...
    return (urls, msgs)


async def get_pic_bytes( works: List[dict]) -> Tuple[List[bytes], List[str]]:
    
    urls, msgs = get_original_url(works)
    
    async def func(session, url):
        logger.info(f'downwork{url}')
        fin = bytes()
        
        async with session.get(url, verify_ssl=False, proxy=PROXY) as res:
            while True:
                data = await res.content.read(1048576)
                fin = fin + data
                if not data:
                    break
        return fin
    async with aiohttp.ClientSession(headers=HEADERS) as s:
        tasks = [asyncio.create_task(func(s, url)) for url in urls]
        picb64_list = await asyncio.gather(*tasks)
        return (picb64_list, msgs)