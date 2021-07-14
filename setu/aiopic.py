import aiohttp
import asyncio
from PIL import Image
from io import BytesIO

header = {
  'Referer': 'https://www.pixiv.net',
  }


async def func(session, url):
  async with session.get(url, verify_ssl=False) as res: 
    return (await res.read())
  
async def get_pic(url_list):
  async with aiohttp.ClientSession() as s:
    tasks = [asyncio.create_task(func(s, url)) for url in url_list]
    done, _ = await asyncio.wait(tasks)


    pic_list = []
    for i in done:
      pic = Image.open(BytesIO(i.result()))
      pic_list.append(pic)
    return pic_list
    
