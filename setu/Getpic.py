import base64
from .pixiv_api import Pixiv
from .utils import get_pic_bytes, TOKEN
import random

from typing import  List, Tuple
import os
from typing import List, Tuple, Optional, Dict, Any
PATH = os.path.dirname(__file__) + '/data/image/'


async def get_pic(works, num=1) -> List[ Tuple[str, str] ]:
  '''
    input : 
      works: api返回的setu信息数组
      num: 出图数

    下载setu到本地

    return(List) :
      - 0: 图片信息(id, 画师id)
      - 1: 图片保存的path
  '''
  assert len(works) > 0
  if num < len(works):
    works = random.choices(works, k = num)
  
  res = await get_pic_bytes(works)
  path_list = []
  for b64, msg in zip(*res):

    msg = f'id:{msg["id"]}\n画师:{msg["artist"]}' # type: ignore
    path_list.append((msg, base64.b64encode(b64).decode()))
  return path_list


class SetuBot(Pixiv):

  def __init__(self):
    super(SetuBot, self).__init__()
    self.token: dict[str, str] = TOKEN
    self._private: bool  = False

  def is_private(self) -> bool:
      return self._private
  
  async def login(self) -> Any:
      return await super().login(refresh_token=self._token)
  
  async def set_token(self, uid: str, gid: str) -> None:

    self._private = False
    if str(uid) in self.token:
      self._token = self.token[str(uid)]
      self._private = True
    elif str(gid) in self.token:
     self. _token = self.token[str(gid)]
    else:
      self._token = random.choice(list(self.token.values()))
    
    await self.login()
    
    


  
  async def get_follow_setu(self, num=1):

    works = await self.illust_follow()
    if works:
      return await get_pic(works, num)


  async def get_setu_base(self,keyword = None, num = 1):
    """
     return -> 状态码, (id, path_list)
    """
    
    if keyword in self.rank_storage.keys() or not keyword:
      keyword = keyword or self.mode
      works = await self.illust_ranking(mode = keyword)
    else:
      works = await self.search_illust(word = keyword)
    return await get_pic(works, num)


  async def get_setu_artist(self, name, num=1):
    """
     return -> 状态码, (id, path_list)
    """
    
    works = await self.user_illusts(name)
    return await get_pic(works, num)

# ---- 重构 ⬆️ ---- #


# ---- 直接使用 ⬇️ ---- #
  async def get_setu_by_id(self, id):
      
      work = await self.illust_detail(id)
      work = work['illust'] # dict
      return await get_pic([work], 1)


  async def get_setu_recommend(self, id: int, num=1):
    
    works = await self.illust_related(id)
    if works:
      works = works['illusts']
      return await get_pic(works, num)
