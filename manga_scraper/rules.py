from lxml import etree
class Config:
    def __init__(self, func, fetch='aiohttp'): 
        self.rule = func
        self.fetch = fetch # ['playwright', 'aiohttp']
        

def rumanhua(tree: etree._Element):
    flag = tree.xpath("/html/body/div[2]/div[1]/div/div[2]/div/p[1]")
    flag = flag[0].text.split('：')[-1] if flag else None
    return  flag

def copymanga(tree: etree._Element):
    flag = tree.xpath("/html/body/main/div[1]/div/div[2]/ul/li[5]/span[2]")
    flag = flag[0].text if flag else None
    return  flag

def happymh(tree: etree._Element):
    flag = tree.xpath('//*[@id="testp"]/p[1]')
    flag = flag[0].text.strip() if flag else None
    return  flag

SITES = {
    'rumanhua': Config(rumanhua),
    'mangacopy': Config(rumanhua),
    'happymh': Config(happymh, 'playwright')
    }
