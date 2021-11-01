from datetime import datetime, timedelta
from pixivpy_async import AppPixivAPI, PixivAPI
from typing import List
import aiohttp
import asyncio
import random
import json
import os

HEADERS = {'Referer': 'https://www.pixiv.net',}

PROXY = ""
TOKEN = ""
try:
    path = os.path.dirname(__file__) + "/data.json"
    with open(path) as f:
        data = json.load(f)
        PROXY = data['PROXY']
        TOKEN = data['TOKEN'] 
except:
    pass



class Pixiv(AppPixivAPI):
    def __init__(self, **requests_kwargs):
        requests_kwargs['proxy'] = PROXY
        super(Pixiv, self).__init__(**requests_kwargs)

        self.date = ''
        self.myid = 'no_r18' # 对应json中没开启r18的账号
        self.mode = 'day_male'
        self.reset_storage()

    def reset_storage(self):
        self.rank_storage = {
        "day":[], "week":[], "month":[], 
        "day_male":[], "day_female":[], 
        "week_original":[], "week_rookie":[], 
        "day_r18":[], "day_male_r18":[], "day_female_r18":[], 
        "week_r18":[], "week_r18g":[],
        # "day_manga":[], 
        # "week_manga":[], "month_manga":[], "week_rookie_manga":[], 
        # "day_r18_manga":[], "week_r18_manga":[], "week_r18g_manga":[]
        }

    def filter_(self, res: List) -> List:
        return [work for work in res if work.type == 'illust']
        
    def set_user(self, id):
        self.user = str(id)

    async def login(self):
        token= random.choice(list(TOKEN.values()))
        return (await super().login(refresh_token=token))

    def update_date(self):
        yesterday = datetime.today() + timedelta(-2)
        yesterday_format = yesterday.strftime('%Y-%m-%d')
        if self.date != yesterday_format:
            self.date = yesterday_format
            self.reset_storage()
            return True
        return False

    def get_original_url(self, works: List) -> List[str]:
        """
        input: 已重写的方法返回的result集合
         或 父类方法的result['illusts']

        return: URL 集合
        """
        urls = []
        for work in works:
            try:
                for w in work['meta_single_page'].values():
                    urls.append(w)
                for w in work['meta_pages']:
                    urls.append(w['image_urls']['original'])
            except:
                pass
        return urls

    async def get_pic_bytes(self, urls: List[str]) -> List[bytes]:
        async def func(session, url):
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
            done, _ = await asyncio.wait(tasks)
            picb64_list = []
            for res_ in done:
                picb64_list.append(res_.result())
            return picb64_list
        
    async def get_more_illust(self, func, nums = 50, **kwargs):
        '''
        获取翻页内容
        '''
        await self.login()
        data = []
        results = await func(**kwargs)
        data = (self.filter_(results['illusts']))
        try:
            while (len(data)<nums):
                    next_kwargs = self.parse_qs(results.next_url)
                    results = await func(**next_kwargs)
                    data =+ (self.filter_(results['illusts']))
        except:
            pass
        return data

    async def search_illust(self, **kwargs) -> List:
        """
        word: tag
        search_target:
            'partial_match_for_tags',
            'exact_match_for_tags',
            'title_and_caption' - 标题说明文
        sort:
            'data_desc', 'data_asc', 'popular_desc'
        """
        tags = ['10000users入り', '5000users入り', '1000users入り']
        kwargs['word'] = kwargs['word'] + ' ' + random.choice(tags)
        return(await self.get_more_illust(super().search_illust, **kwargs))


    async def illust_ranking(self, **kwargs):
        kwargs.setdefault('mode', self.date)
        if self.update_date() or not self.rank_storage[kwargs['mode']]:    
            kwargs.setdefault('date', self.date)
            await self.login()
            results = await self.get_more_illust(super().illust_ranking, **kwargs)
            self.rank_storage[kwargs['mode']] = results

        return self.rank_storage[kwargs['mode']]

    async def user_illusts(self, name):
        '''
        画师id 或 名称
        '''
        await self.login()
        
        if isinstance(name, int):
            id = name
        else:
            info_ = await self.search_user(name)
            id = info_['user_previews'][0]['user']['id']
        return (await self.get_more_illust(super().user_illusts, user_id=id))


