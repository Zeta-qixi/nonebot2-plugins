# File: manga_update_checker.py
import asyncio
from typing import Callable, Tuple
import aiohttp
import sqlite3
from lxml import etree
from playwright.async_api import async_playwright
from .database import database_file
from .rules import SITES


playwright_proxy = {"server": "socks5://127.0.0.1:1080"}


        

async def fetch_with_aiohttp(session, url: str, f) -> Tuple[str, etree._Element, Callable]:
    try:
        async with session.get(url) as response:
            assert response.status == 200, f"status: {response.status}"
            html = await response.text()
            return (url, etree.HTML(html), f)
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

async def fetch_with_playwright(url: str, f)-> Tuple[str, etree._Element, Callable]:
    try:
        async with async_playwright() as p:
            browser = await p.firefox.launch(headless=True, 
                    proxy=playwright_proxy) 
            
            page = await browser.new_page()
            await page.goto(url)
            html = await page.content()
            await browser.close()
            return (url, etree.HTML(html), f)
        
    except Exception as e:
        print(f"Error using Playwright on {url}: {e}")
        return None


def check_update(html, url, rule, db_conn):
  
    if html:
        flag = rule(html)
        if not flag:
            return
        
        cursor = db_conn.cursor()
        cursor.execute("SELECT last_update FROM manga WHERE url = ?", (url,))
        result = cursor.fetchone()
        if result and result[0] == flag:
            print(f"No updates for manga {url} ({flag})")
            return

        cursor.execute("""UPDATE manga SET last_update = ?, 
                       update_flag = ?WHERE url = ?""", (flag, 1, url))
        db_conn.commit()


async def update():

    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()
    cursor.execute("SELECT url, rule FROM manga")
    manga_records = cursor.fetchall()
    manga_sites = [(url,  SITES.get(site)) for url, site in manga_records]
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url, site in manga_sites:
            if not site: continue
            if site.fetch == 'aiohttp':
                tasks.append(fetch_with_aiohttp(session, url, site.rule))
            elif site.fetch == 'playwright':
                tasks.append(fetch_with_playwright(url, site.rule))
 
        res = await asyncio.gather(*tasks)
        
    for url, html, f in res:
        check_update(html, url, f, conn)
        
    conn.close()

    
    
    
if __name__ == "__main__":
    asyncio.run(update())
    