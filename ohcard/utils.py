from io import BytesIO
import os
import aiohttp

from PIL import Image
from .data_load import PATH




def is_exists(id):
    if os.path.exists(PATH + str(id) + ".png"):
        return True

async def save_pic(url :str, name: str):
    img = await aio_get_image(url)
    img.save(PATH + name + ".png")
    

async def aio_get_image(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            bovw_res =  await resp.read()
            img = (Image.open(BytesIO(bovw_res)))
            return img