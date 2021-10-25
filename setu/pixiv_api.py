from datetime import datetime, timedelta
from pixivpy_async import AppPixivAPI, PixivAPI
from typing import List
import aiohttp
import asyncio
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
        self.mode = 'day_male'
        self.refresh_token = TOKEN
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
        
    def update_date(self):
        yesterday = datetime.today() + timedelta(-2)
        yesterday_format = yesterday.strftime('%Y-%m-%d')
        if self.date != yesterday_format:
            self.date = yesterday_format
            self.reset_storage()
            return True
        return False

    def get_large_url(self, works: List) -> List[str]:
        """
        input: 已重写的方法返回的result集合
         或 父类方法的result['illusts']

        return: URL 集合
        """
        urls = []
        for work in works:
            try:
                urls.append(work['image_urls']['large'])
            except:
                urls.append(work['image_urls']['medium'])
        return urls

    async def get_pic(self, urls: List[str]) -> List[bytes]:
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
        

    async def search_illust(self, **kwargs) -> List:
        """
        word: tag
        search_target:
            1:'partial_match_for_tags',
            2:'exact_match_for_tags',
            3:'title_and_caption'
        """
        await self.login()
        kwargs.setdefault('word', None)
        kwargs.setdefault('search_target', 'exact_match_for_tags')
        results = await super().search_illust(**kwargs)
        return self.filter_(results['illusts'])
        #await self.search_illust(tag, search_types[search_type])

    async def illust_ranking(self, **kwargs):
        kwargs.setdefault('mode', self.date)
        if self.update_date() or not self.rank_storage[kwargs['mode']]:    
            kwargs.setdefault('date', self.date)
            await self.login()
            results = await super().illust_ranking(**kwargs)
            self.rank_storage[kwargs['mode']] = (self.filter_(results['illusts']))
            try:
                while len(self.rank_storage[kwargs['mode']]) < 100:
                    next_kwargs = self.parse_qs(results.next_url)
                    results = await super().illust_ranking(**next_kwargs)
                    self.rank_storage[kwargs['mode']].extend(self.filter_(results['illusts']))
            except:
                pass
            
        return self.rank_storage[kwargs['mode']]