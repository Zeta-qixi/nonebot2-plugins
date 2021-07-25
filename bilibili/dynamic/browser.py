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
from playwright.async_api import Browser, async_playwright

_browser: Optional[Browser] = None


async def init(**kwargs) -> Browser:
    global _browser
    browser = await async_playwright().start()
    _browser = await browser.chromium.launch(**kwargs)
    return _browser


async def get_browser(**kwargs) -> Browser:
    return _browser or await init(**kwargs)

 
async def get_dynamic_screenshot(url, f=None):
    browser = await get_browser()
    page = None
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

        print(f)
        if f:
            if f not in text:
                print(text)
                raise UserWarning('过滤')
            

        bar = await page.query_selector(".text-bar")
        assert bar is not None
        bar_bound = await bar.bounding_box()
        assert bar_bound is not None
        clip['height'] = bar_bound['y'] - clip['y']
        image = await page.screenshot(clip=clip)

        await page.close()
        return base64.b64encode(image).decode()

    except Exception:
        if page:
            await page.close()
        raise



