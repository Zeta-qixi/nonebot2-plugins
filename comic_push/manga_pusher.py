import requests
import aiohttp
from .data_loader import DataLoader
from lxml import etree

helper = DataLoader('data/manga.json')

headers={
    'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) \
    AppleWebKit/605.1.15 (KHTML, like Gecko) \
    Version/14.0.2 Safari/605.1.15',
}
host_url = 'http://www.mangabz.com'

def crawler(id):

    res = requests.get(host_url + id, headers=headers)
    html = etree.HTML(res.content.decode('utf8'))
    target_list = html.xpath('//*[@id="chapterlistload"]/a')

    target = target_list[0]
    latest = target[0].xpath('./text()')[0].strip()
    
    url_ = host_url + id
    title = html.xpath('/html/body/div[3]/div/div/p[1]/text()')[0].strip()
    
    return (len(target_list), title, latest, url_)



async def aio_spider(id):
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(host_url + id) as resp:
            res = await resp.read()

            html = etree.HTML(res.decode('utf8'))

            target_list = html.xpath('//*[@id="chapterlistload"]/a')

            target = target_list[0]
            latest = target[0].xpath('./text()')[0].strip()
            
            url_ = host_url + id
            title = html.xpath('/html/body/div[3]/div/div/p[1]/text()')[0].strip()
            
            return (len(target_list), title, latest, url_)



async def get_response( bot ):
    for uid in helper.data:
        for cid in helper.data[uid]:

            try:
                total, title, _, url = await aio_spider(cid)
                if total > int(helper.data[uid][cid]):
                    helper.data[uid][cid] = total
                    msg = f"漫画{title}更新了\n:{url}"
                    await bot.send_msg(message_type='private', user_id=int(uid), message=msg)
                    helper.save()
            finally:
                ...
    