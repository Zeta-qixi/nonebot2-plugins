from datetime import datetime, timedelta
from pixivpy_async import AppPixivAPI, PixivAPI

from typing import List, Any
from .utils import PROXY


class Pixiv(AppPixivAPI):
    def __init__(self, **requests_kwargs):
        requests_kwargs['proxy'] = PROXY
        super(Pixiv, self).__init__(**requests_kwargs)

        self.date = ''
        self.mode = 'day_male'
        self.reset_storage()
     
    def reset_storage(self):
        self.rank_storage = {
        "day":[], "week":[], "month":[], "day_male":[], "day_female":[], "week_original":[], "week_rookie":[], 
        "day_r18":[], "day_male_r18":[], "day_female_r18":[], "week_r18":[], "week_r18g":[],
        # "day_manga":[], 
        # "week_manga":[], "month_manga":[], "week_rookie_manga":[], 
        # "day_r18_manga":[], "week_r18_manga":[], "week_r18g_manga":[]
        }

    def get_rank_keys(self) -> List:
        return list(self.rank_storage.keys())
        
    def _filter(self, res: List) -> List:
        return [work for work in res if work.type == 'illust']
        

    def update_date(self):
        yesterday = datetime.today() + timedelta(-2)
        yesterday_format = yesterday.strftime('%Y-%m-%d')
        if self.date != yesterday_format:
            self.date = yesterday_format
            self.reset_storage()
            return True
        return False

        
    async def get_more_illust(self, func, nums = 50, **kwargs):
        '''
        获取翻页内容
        '''
        data = []
        results = await func(**kwargs)
        data = (self._filter(results['illusts']))
        try:
            while (len(data)<nums):
                    next_kwargs = self.parse_qs(results.next_url)
                    results = await func(**next_kwargs)
                    data += (self._filter(results['illusts']))
        except:
            pass
        return data

    async def search_illust(self, **kwargs) -> List[Any]:
        """
        word: tag
        search_target:
            'partial_match_for_tags',
            'exact_match_for_tags',
            'title_and_caption' - 标题说明文
        sort:
            'data_desc', 'data_asc', 'popular_desc'
        """ 
        res = []
        tags = ['50000', '10000', '5000', '3000', '1000']
        base_tag = kwargs['word']
        for tag in tags:
            kwargs['word'] = f'{base_tag} {tag}users入り'
            res += await self.get_more_illust(super().search_illust, 10 , **kwargs)
        return res


    async def illust_ranking(self, **kwargs):
        kwargs.setdefault('mode', self.mode)
        if self.update_date() or not self.rank_storage[kwargs['mode']]:    
            kwargs.setdefault('date', self.date)
            results = await self.get_more_illust(super().illust_ranking, **kwargs)
            self.rank_storage[kwargs['mode']] = results

        return self.rank_storage[kwargs['mode']]

    async def user_illusts(self, name):
        '''
        画师作品
        '''
        if name.isdigit():
            id = int(name)
        else:
            info_ = await self.search_user(name)
            id = info_['user_previews'][0]['user']['id']
            
        return (await self.get_more_illust(super().user_illusts, user_id=id))


    async def illust_follow(self):
        '''
        关注列表新作
        '''
        return (await self.get_more_illust(super().illust_follow, nums=30, req_auth=True))
