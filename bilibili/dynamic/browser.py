'''
> python -m playwright install
'''
import base64
from typing import Optional
from lxml import etree
from playwright.async_api import Browser, async_playwright
import re
from nonebot import logger
_browser: Optional[Browser] = None


async def init(**kwargs) -> Browser:
    global _browser
    browser = await async_playwright().start()
    _browser = await browser.chromium.launch(**kwargs)
    return _browser


async def get_browser(**kwargs) -> Browser:
    return _browser or await init(**kwargs)

 
async def get_dynamic_screenshot(url, filter=None):
    
    browser = await get_browser()
    page = None
    res = {}
    try:
        
        page = await browser.new_page()
        await page.goto(url, wait_until='networkidle', timeout=10000)
        await page.set_viewport_size({"width": 2560, "height": 1080})

        # 获取文本
        text_content = await page.query_selector(".bili-rich-text__content")  #text所在的class , page 定位到此 
        assert text_content is not None
        text = await text_content.text_content()     
        if filter and filter not in text:
            raise UserWarning('过滤动态')
        
        # 图片版本

        bar = await page.query_selector('.bili-dyn-item__main')  #卡片所在的class , page 定位到此 
        bar_bound = await bar.bounding_box()
        assert bar_bound is not None

        image = await page.screenshot(clip=bar_bound)
        pic_b64 = base64.b64encode(image).decode()
        res['dy'] = pic_b64
        
        # 获取动态图
        img_content_ = await page.query_selector(".bili-dyn-content__orig__major") #image-box所在的class , page 定位到此 
        
        img_inner_html = await img_content_.inner_html()
        tree = etree.HTML(img_inner_html)
        url_list = []

        for i in tree.xpath('//div[@class="bili-album__preview__picture__img bili-awesome-img"]'):  # image 的 class, 获取etree
            img_url = "https:" + (re.search('url\("(.*)"\)',str(i.xpath('@style')))).groups()[0]
            url_list.append(img_url)     
        res['img_url'] = url_list

        await page.close()
        return res

    except Exception as e:
        logger.error(repr(e))
        if page:
            await page.close()


def install():
    """自动安装、更新 Chromium"""
    import sys
    from playwright.__main__ import main
    sys.argv = ['', 'install', 'webkit']
    main()
    
#第一次
# install()