from pixiv_api import Pixiv
import random
from PIL import Image
from io import BytesIO
import os, sys


PATH = os.path.dirname(__file__)
class SetuBot(Pixiv):
  def __init__(self):
    super(SetuBot, self).__init__()

  async def get_setu_info(self, num = 1, keyword = None):
    """

     return -> 状态码, path 列表
    """
    if keyword in self.rank_storage.keys() or not keyword:
      keyword = keyword or self.mode
      works = await self.illust_ranking(mode = keyword)
    else:
      works = await self.search_illust(word = keyword)

    if num > len(works):
      num = len(works)
    
    works = random.choices(works, k = num)
    picb64 = await self.get_pic(self.get_large_url(works))

    path_list = []
    for work, b64 in zip(works, picb64):
      img = Image.open(BytesIO(b64))
      path = PATH + f'/data/{work.id}.png'
      img.save(path)
      path_list.append(path)

    return (1000, path_list)