import asyncio
import hashlib
import json
import re

import redis
from playwright.async_api import async_playwright

from config import Config


def get_md5(val):
    """把目标数据进行哈希，用哈希值去重更快"""
    md5 = hashlib.md5()
    md5.update(val.encode('utf-8'))
    return md5.hexdigest()


def add_url(url):
    res = red.sadd('shell-urlset', get_md5(url))  # 注意是 保存set的方式
    if res == 0:  # 若返回0,说明插入不成功，表示有重复
        return False
    else:
        return True



# Function to get page HTML
async def get_page_html(page, selector):
    # await page.wait_for_selector(selector)
    elements = await page.query_selector_all(selector)
    # return await element.inner_text() if element else ""


# Crawl function
async def crawl(config):
    results = []
    queue = [config.url]

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        if config.cookie:
            await page.context.add_cookies([{
                "name": config.cookie['name'],
                "value": config.cookie['value'], "url": config.url}])

        try:
            while queue and len(results) < config.max_pages_to_crawl:
                url = queue.pop(-1)
                print(f"Crawler: Crawling {url}")
                await page.goto(url)
                if re.search(config.htmlmatch, url):
                    html = await get_page_html(page, config.selector)
                    results.append({'url': url, 'html': html})
                    with open(config.output_file_name, 'w') as f:
                        json.dump(results, f, indent=2)

                # Extract and enqueue links
                links = await page.query_selector_all("a")
                for link in links:
                    href = await link.get_attribute("href")
                    if not re.search(config.Homematch, href):
                        href = config.Url + href
                    if href and re.match(config.urlmatch, href) and add_url(href):
                        queue.append(href)

                # Implement on_visit_page logic if needed
        finally:
            await browser.close()

    return results


# Main function
async def main(config):
    results = await crawl(config)
    with open(config.output_file_name, 'w') as f:
        json.dump(results, f, indent=2)


# Running the main function
if __name__ == "__main__":
    config = Config(
        Url="https://www.chinaacc.com",
        url="https://www.chinaacc.com/zyssfg/",
        Homematch="((http|https|ftp):)|(w{3})",
        urlmatch="https://www.chinaacc.com/zyssfg/|https://www.chinaacc.com/zcms/|https://www.chinaacc.com/new/|https://www.chinaacc.com/faguiku",
        htmlmatch="[^index](.*).shtml|[^index](.*).htm|[^index](.*).html",
        selector=".news.clearfix",
        max_pages_to_crawl=10,
        output_file_name="output.json"
    )
    red = redis.Redis(host='127.0.0.1', port=6379, db=0)
    red.delete('shell-urlset')
    asyncio.run(main(config))
