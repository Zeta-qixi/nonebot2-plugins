import aiohttp
import asyncio
from PIL import Image
from io import BytesIO
import base64
header = {
  'user-agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
  'Referer': 'https://www.pixiv.net',
  }


async def func(session, url):
  async with session.get(url, verify_ssl=False) as res:
    assert res.status == 200
    return (await res.read())
  
async def get_pic(url_list):
  async with aiohttp.ClientSession(headers=header) as s:
    tasks = [asyncio.create_task(func(s, url)) for url in url_list]
    done, _ = await asyncio.wait(tasks)

    pic_list = []
    for i in done:
      pic = base64.b64encode(i.result()).decode()
      pic_list.append(pic)
    return pic_list
    
    