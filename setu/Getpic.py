from .pixiv_api import Pixiv, TOKEN
import random
from PIL import Image
from io import BytesIO
import os, sys


PATH = os.path.dirname(__file__)
class SetuBot(Pixiv):
  def __init__(self):
    super(SetuBot, self).__init__()

  async def login(self, token):

    if not token:
        token = random.choice(list(TOKEN.values())[:-1])
    return (await super().login(refresh_token=token))


  async def get_pic(self, works, num=1):
    '''
      input : 
        works: api返回的setu信息数组
        num: 随机的数量

      下载setu到本地

      return :
        setu绝对路径 List合集
    '''
    assert len(works) > 0
    if num < len(works):
      works = random.choices(works, k = num)
    
    res = await self.get_pic_bytes(works)

    path_list = []
    for b64, msg in zip(*res):
      img = Image.open(BytesIO(b64))
      path = PATH + f'/data/image/{msg["id"]}.png'
      img.save(path)
      msg = f'id:{msg["id"]}\n画师:{msg["artist"]}'
      path_list.append((msg, path))
    return path_list


  async def get_setu_base(self,keyword = None, num = 1, token=None):
    """
     return -> 状态码, (id, path_list)
    """
    if token:
      token = TOKEN[token]
    await self.login(token)

    if keyword in self.rank_storage.keys() or not keyword:
      keyword = keyword or self.mode
      works = await self.illust_ranking(mode = keyword)
    else:
      works = await self.search_illust(word = keyword)
    
    pic = await self.get_pic(works, num)
    return (1000, pic)

  async def get_setu_artist(self, name, num=1, token=None):
    """
     return -> 状态码, (id, path_list)
    """
    if token:
      token = TOKEN[token]
    await self.login(token)
    works = await self.user_illusts(name)
    return(1000, await self.get_pic(works, num))


  async def get_follow_setu(self, num=1, uid=None):
    if str(uid) not in TOKEN.keys():
      return (400, 0)
    await self.login(TOKEN[str(uid)])
    works = await self.illust_follow()
    if works:
      return(1000, await self.get_pic(works, num))

# ---- 重构 ⬆️ ---- #

# ---- 直接使用 ⬇️ ---- #
  async def get_setu_by_id(self,id , token=None):

      if token:
        token = TOKEN[token]
      await self.login(token)

      work = await self.illust_detail(id)
      work = work['illust']
      return(1000, await self.get_pic([work], 1))


  async def get_setu_recommend(self, id: int, num=1, token=None):
    if token:
      token = TOKEN[token]
    await self.login(token)

    works = await self.illust_related(id)
    if works:
      works = works['illusts']
      return(1000, await self.get_pic(works, num))