
import os
import asyncio
import aiohttp
data_path = os.path.dirname(__file__) + "/starrail/strategy/role/"


roleAlias = {
  "阿兰": ['Alan', '阿郎', '阿蓝'],
  "艾丝妲": ['爱思达', '爱丝妲', '爱思妲', '爱丝达', '艾思达', '艾思妲', '艾丝达','富婆'],
  "白露": ['龙女', '小龙女', '白鹭', '白鹿', '白麓'],
  "布洛妮娅": ['布诺妮亚', '布洛妮亚', '布诺妮娅', '布洛尼亚', '鸭鸭', '大鸭鸭'],
  "丹恒": ['单恒', '单垣', '丹垣', '丹桁', '冷面小青龙'],
  "黑塔": ['人偶', '转圈圈'],
  "虎克": ['胡克'],
  "姬子": ['机子', '寄子'],
  "杰帕德": ['杰哥'],
  "景元": [],
  "开拓者·存护": ['火爷', '火主', '开拓者存护'],
  "开拓者·毁灭": ['物理爷', '物爷', '物理主', '物主', '开拓者毁灭'],
  "克拉拉": ['可拉拉', '史瓦罗'],
  "娜塔莎": ['那塔莎', '那塔沙', '娜塔沙'],
  "佩拉": ['配拉', '佩啦', '冰砂糖'],
  "青雀": ['青却', '卿雀'],
  "三月七": ['三月', '看板娘', '三七', '三祁'],
  "桑博": [],
  "素裳": ['李素裳'],
  "停云": ['停运', '听云'],
  "瓦尔特": ['杨叔', '老杨', '瓦尔特杨'],
  "希儿": ['希尔'],
  "希露瓦": ['希录瓦'],
  "彦卿": ['言情', '彦情', '彦青', '言卿', '燕青']
}

def get_role_from_file(name):

    for n, a in roleAlias.items():
        if n == name or name in a:
            return data_path + n + '.png'
            
    return None


async def fetch_post(session, id):
    url = f'https://bbs-api.mihoyo.com/post/wapi/getPostFullInCollection?&gids=6&order_type=2&collection_id={id}'
    async with session.get(url) as response:
        data = await response.json()
        return data['data']['posts']

async def download_image(session, url):
    async with session.get(url) as response:
        return await response.read()

async def get_role(name, ids):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_post(session, id) for id in ids]
        results = await asyncio.gather(*tasks)

        for data in results:
            for val in data:
                if name in str(val['post']['subject']):
                    sub = val['image_list']
                    heights = [i['height'] for i in sub]
                    index = heights.index(max(heights))
                    url = sub[index]['url']
                    byte = await download_image(session, url)
                    return byte