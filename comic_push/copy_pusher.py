
from .data_loader import DataLoader
from typing import Dict, List
import aiohttp
import asyncio
from lxml import etree

class Spider:

    def __init__(self) -> None:

        self.headers={'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) \
        AppleWebKit/605.1.15 (KHTML, like Gecko) \Version/14.0.2 Safari/605.1.15',}

        self.proxy = "http://127.0.0.1:1080"


    async def send_requests_use_async(self, url):

        async with aiohttp.ClientSession() as session:
            async with session.get(url=url, headers=self.headers,  proxy=self.proxy) as resp:
                    res = await resp.read()
                    return (res, resp.url)


    async def get_response_by_async(self, url_list):
        
        if isinstance(url_list, str):
            url_list = [url_list]
            
        tasks = [self.send_requests_use_async(url) for url in url_list]
        ret = await asyncio.gather(
            *tasks
            )
        return ret


class ComicSpider(Spider):

    def __init__(self):
        super().__init__()

    async def get_response(self, comic_list: list) -> Dict:
            
        urls = ['https://www.copymanga.site/comic/' + c for c in comic_list] 
        res = await self.get_response_by_async(urls)
        
        data = {'data':[]}
        for html, url in res:
            html = etree.HTML(html.decode('utf8'))
            name = html.xpath('//div[@class="col-9 comicParticulars-title-right"]/ul/li[1]/h6/@title')
            if name:
                name = name[0]
                box = html.xpath('//div[@class="col-9 comicParticulars-title-right"]/ul/li[5]/span[2]/text()')
                update_time = box[0] if box else '0'
                data['data'].append({
                    'name': name,
                    'url': str(url),
                    'update_time': update_time.strip()
                    })
            
        return data

helper = DataLoader('data/copy.json')

async def get_response( bot ):

    spider = ComicSpider()
    for uid in helper.data:

        comics = list(helper.data[uid].keys())
        response = await spider.get_response(comics)
        
        for data, comic in zip(response['data'], comics):
            
            if data['update_time'] != helper.data[uid][comic]:
                helper.data[uid][comic] = data['update_time']
                msg = f"{data['name']}  {data['update_time']}"
                await bot.send_msg(message_type='private', user_id=int(uid), message=msg)
                helper.save()


def copy_add(id, name):
    helper.data[id][name] = '0'
    helper.save()