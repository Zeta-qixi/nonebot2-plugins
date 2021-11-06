from pixiv_api import Pixiv, TOKEN
import random
from PIL import Image
from io import BytesIO
import os, sys


PATH = os.path.dirname(__file__)
class SetuBot(Pixiv):
  def __init__(self):
    super(SetuBot, self).__init__()

  async def get_pic(self, works, num=1):
    '''
      input : 
        works: api返回的setu信息数组
        num: 随机的数量

      下载setu到本地

      return :
        setu绝对路径 List合集
    '''

    works = random.choices(works, k = num)
    picb64 = await self.get_pic_bytes(self.get_original_url(works))

    path_list = []
    for work, b64 in zip(works, picb64):
      img = Image.open(BytesIO(b64))
      path = PATH + f'/data/image/{work.id}.png'
      img.save(path)
      msg = f'id:{work.id}\n画师:{work.user.id}\n'
      path_list.append((msg, path))
    return path_list


  async def get_setu_base(self,keyword = None, num = 1):
    """
     return -> 状态码, (id, path_list)
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
     return -> 状态码, (id, path_list)
    """
    works = await self.user_illusts(name)
    return(1000, await self.get_pic(works, num))


  async def get_follow_setu(self, uid: str, num=1):
    if str(uid) not in TOKEN.keys():
      return (400, 0)
    works = await self.illust_follow(TOKEN[str(uid)])
    if works:
      return(1000, await self.get_pic(works, num))

# ---- 重构 ⬆️ ---- #

# ---- 直接使用 ⬇️ ---- #
  async def get_setu_by_id(self,id: int):
      await self.login()
      work = await self.illust_detail(id)
      work = work['illust']
      return(1000, await self.get_pic([work], 1))


  async def get_setu_recommend(self, id: int, num:int =1):
    await self.login()
    works = await self.illust_recommended(id)
    if works:
      works = works['illusts']
      return(1000, await self.get_pic(works, num))