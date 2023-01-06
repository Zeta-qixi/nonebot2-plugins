import aiohttp
from nonebot.log import logger
from nonebot.adapters.onebot.v11.message import MessageSegment
from nonebot import get_driver
from lxml import etree
from kth_timeoutdecorator import *

from typing import  List

SAUCENAO_KEY = get_driver().config.saucenao_key  # SauceNAO 的 API key
TIMELIMIT_IMAGE = 7 # 识图功能的时间限制

headers={
    'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) \
    AppleWebKit/605.1.15 (KHTML, like Gecko) \
    Version/14.0.2 Safari/605.1.15',
}

params = {
    'api_key' : SAUCENAO_KEY,
    'output_type' : 2
}

SIMILARITY = 50

class Ascii2dInfo:
    def __init__(self, box):
        self.image_url = "https://ascii2d.net" + box.xpath('.//img/@src')[0]

        self.info = ''
        detail = box.xpath('.//div[@class="detail-box gray-link"]/h6')
        if detail:
            detail = detail[0]
            urls = detail.xpath(".//a/@href")
            info = detail.xpath(".//a/text()")
            self.info = f"title:{info[0]}\nartist:{info[1]}\n{urls[0]}"

    @property
    def nonebot_msg(self):
        msg =  MessageSegment.image(self.image_url) + MessageSegment.text(self.info)
        return (msg)



class SaucenaoInfo:
    def __init__(self, data):

        self.similarity = data['header']['similarity']
        assert float(self.similarity) >= SIMILARITY, f"置信度小于{SIMILARITY}"
        self.thumbnail = data['header']['thumbnail']
        self.ext_urls = data['data'].get('ext_urls',[])
        self.source = data['data'].get('source','')
        self.title = data['data'].get('title',self.source)
        self.creator = data['data'].get('creator',None) if 'creator' in data['data'] else data['data'].get('member_name','')
        self.info = f"similarity:{self.similarity}\ntitle:{self.title}\ncreator:{self.creator}\n"

    @property
    def nonebot_msg(self):
        msg =  MessageSegment.image(self.thumbnail) + MessageSegment.text(self.info+'\n'.join(self.ext_urls))
        return (msg)

class PicInfoList(List):
    def __init__(self, results):
        
        for i in results:
            try:
                self.append(SaucenaoInfo(i))
            except Exception as e:
                ...

 
async def from_saucenao(session, url):
    params['url'] = url
    try:
        async with session.get('https://saucenao.com/search.php', params=params, headers = headers) as resp:
            data = await resp.json()
        res_ = PicInfoList(data['results'])
        return (['saucenao']+[i.nonebot_msg for i in res_])

    except Exception as e:
        logger.error(e)
        return(['saucenao搜不到啦'])


async def from_ascii2d(session, url):
    try: 
       
        async with session.get(f"https://ascii2d.net/search/url/{url}", headers = headers) as resp:
            clolr_res = await resp.text()

        html_index = etree.HTML(clolr_res)
        neet_div = html_index.xpath('//div[@class="detail-link pull-xs-right hidden-sm-down gray-link"]')
        url_bovw = "https://ascii2d.net" + neet_div[0].xpath('./span/a/@href')[1]

        async with aiohttp.ClientSession() as session:
            async with session.get(url_bovw, headers = headers) as resp:
                bovw_res = await resp.text()

        html_index2 = etree.HTML(bovw_res)

        res = []
        for html in [html_index, html_index2]:
            boxes = html.xpath('//div[@class="row item-box"]')
            for box in boxes[1:3]:
                res.append(Ascii2dInfo(box))
        return (["ascii2d"] + [i.nonebot_msg for i in res])

    except Exception as e:
        logger.error(e)
        return(['ascii2d搜不到啦'])




