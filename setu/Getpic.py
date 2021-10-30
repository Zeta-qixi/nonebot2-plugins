from pixiv_api import Pixiv
import random
from PIL import Image
from io import BytesIO
import os, sys


PATH = os.path.dirname(__file__)
class SetuBot(Pixiv):
  def __init__(self):
    super(SetuBot, self).__init__()

  async def get_pic(self, works, num=1):
    # 获取 or 下载图片
    works = random.choices(works, k = num)
    picb64 = await self.get_pic_bytes(self.get_original_url(works))

    path_list = []
    for work, b64 in zip(works, picb64):
      img = Image.open(BytesIO(b64))
      path = PATH + f'/data/image/{work.id}.png'
      img.save(path)
      path_list.append((work.id, path))
    return path_list


  async def get_setu_base(self,keyword = None, num = 1):
    """
    索引搜索和rank合并
     return -> 状态码, path_list
    """
    if keyword in self.rank_storage.keys() or not keyword:
      keyword = keyword or self.mode
      works = await self.illust_ranking(mode = keyword)
    else:
      works = await self.search_illust(word = keyword)

    if num > len(works):
      num = len(works)
    
    pic = await self.get_pic(works, num)
    return (1000, pic)

  async def get_setu_artist(self, name, num=1):
    """
    索引搜索和rank合并
     return -> 状态码, path_list
    """
    works = await self.user_illusts(name)
    pic = await self.get_pic(works, num)
    return (1000, pic)
