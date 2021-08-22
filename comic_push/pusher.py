import requests
from lxml import etree

headers={
    'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) \
    AppleWebKit/605.1.15 (KHTML, like Gecko) \
    Version/14.0.2 Safari/605.1.15',
}
host_url = 'http://www.mangabz.com'

def crawler(id):

    res = requests.get(host_url + id, headers=headers)
    html = etree.HTML(res.content.decode('utf8'))
    target = html.xpath('//*[@id="chapterlistload"]/a[1]')
    latest = target[0].xpath('./text()')[0].strip()
    
    url_ = host_url + target[0].xpath('./@href')[0]
    title = html.xpath('/html/body/div[3]/div/div/p[1]/text()')[0].strip()
    
    return (title, latest, url_)




