import requests
from lxml import etree
from kth_timeoutdecorator import *
import json

SAUCENAO_KEY = "22e3b750875fdd61ccd55426a1d7ee95bc8a4105" # SauceNAO 的 API key
TIMELIMIT_IMAGE = 7 # 识图功能的时间限制
params = {
    'api_key' : SAUCENAO_KEY,
    'output_type' : 2
}

def from_saucenao(url):
    params['url'] = url
    response = requests.get('https://saucenao.com/search.php', params=params)
    data = response.json()
    res_ = []
    for res in data['results']:

        similarity = res['header']['similarity']
        id = res['data'].get('pixiv_id')
        if id and float(similarity) > 80:
            title = res['data']['title']
            user_name  = res['data']['member_name']
            user_id = res['data']['member_id'] 
            res_.append((title, id, user_name, user_id))
    return res_

def from_ascii2d(url):
    clolr_res = requests.get(f"https://ascii2d.net/search/url/{url}")
    html_index = etree.HTML(clolr_res.text)

    neet_div = html_index.xpath('//div[@class="detail-link pull-xs-right hidden-sm-down gray-link"]')
    url_bovw = "https://ascii2d.net" + neet_div[0].xpath('./span/a/@href')[1]
    bovw_res = requests.get(url_bovw)
    html_index2 = etree.HTML(bovw_res.text)

    res_ = []
    for html in [html_index, html_index2]:
        all_data = html.xpath('//div[@class="detail-box gray-link"]/h6')
        for data in all_data[:3]:
            artworks_id, users_id = data.xpath(".//a/@href")
            artworks, users = data.xpath(".//a/text()")
            if ('pixiv' in artworks_id):
                artworks_id = artworks_id.split('/')[-1]
                users_id = users_id.split('/')[-1]
                res_.append((artworks,artworks_id,users,users_id))
    return res_

@timeout(TIMELIMIT_IMAGE)
async def get_view(sc, image_url: str) -> str:
    return sc(image_url)



async def get_image_data(image_url: str, api_key: str=SAUCENAO_KEY):

    putline = []
    repass = ''
    for sc in [from_saucenao, from_ascii2d]:
        try:
            putline += await get_view(sc, image_url)
        except :
            pass
    for (title, id, user_name, user_id) in list(set(putline)):
        msg = f'PixivID: {id}\n[作者]{user_name}: {user_id}'
        if repass:
            repass = repass + '\n----------\n' + msg
        else:
            repass += msg
    return repass