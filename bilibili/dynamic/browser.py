'''
> python -m playwright install
'''
import base64
import shutil
from pathlib import Path
from typing import Optional
import asyncio
from PIL import Image
from io import BytesIO
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
        card = await page.query_selector(".card")
        assert card is not None
        clip = await card.bounding_box()
        assert clip is not None

        # 获取动态文本
        text_content = await page.query_selector(".post-content")
        text = await text_content.text_content()
        try:
            img_content_ = await page.query_selector(".imagesbox")
            img_inner_html = await img_content_.inner_html()
            tree = etree.HTML(img_inner_html)
            url_list = []
            for i in tree.xpath('//div[@class="img-content"]'):
                img_url = "https:" + (re.search(r"//.*jpg",str(i.xpath('@style')))).group()
                url_list.append(img_url)
            res['img_url'] = url_list
        except Exception as e:
            logger.error(repr(e))

        if filter:
            if filter not in text:
                raise UserWarning('过滤动态')
            

        bar = await page.query_selector(".text-bar")
        assert bar is not None
        bar_bound = await bar.bounding_box()
        assert bar_bound is not None
        clip['height'] = bar_bound['y'] - clip['y']
        image = await page.screenshot(clip=clip)

        await page.close()
        pic_b64 = base64.b64encode(image).decode()
        res['dy'] = pic_b64
        return res

    except Exception:
        if page:
            await page.close()
        raise



def install():
    """自动安装、更新 Chromium"""
    import sys
    from playwright.__main__ import main
    sys.argv = ['', 'install', 'webkit']
    main()
#第一次
#install()