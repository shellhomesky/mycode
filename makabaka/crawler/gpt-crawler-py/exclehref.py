import asyncio
import hashlib
import json
import re

import redis
import xlwings as xw
from playwright.async_api import async_playwright

from config import Config


def xlookup(lookup_value, lookup_array, return_array, if_not_found: str = ''):
    match_value = return_array.loc[lookup_array == lookup_value]
    if match_value.empty:
        return f'"{lookup_value}" 没有找到！' if if_not_found == '' else if_not_found
    else:
        return match_value.tolist()[0]


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
    await page.wait_for_selector(selector)
    elements_text = await page.locator(selector).all_inner_texts()
    text = []
    for element_text in elements_text:
        text = text + element_text.split("\t")
    return text


# Crawl function
async def crawl(config):
    results = []
    queue = ls_data

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        if config.cookie:
            await page.context.add_cookies([{
                "name": config.cookie['name'],
                "value": config.cookie['value'], "url": config.url}])

        try:
            while queue and len(results) < config.max_pages_to_crawl:
                url = queue.pop(0)
                print(f"Crawler: Crawling {url}")
                await page.goto(url)
                if re.search(config.htmlmatch, url):
                    html = await get_page_html(page, config.selector)
                    results.append(html)
        finally:
            await browser.close()
    return results


# Main function
async def main(config):
    results = await crawl(config)
    for j in range(len(results)):
        sh2(j + 1, 14).value = results[j][1]
        sh2(j + 1, 15).value = results[j][3]
        sh2(j + 1, 16).value = results[j][5]
        sh2(j + 1, 17).value = results[j][7]
        sh2(j + 1, 18).value = results[j][9]
        sh2(j + 1, 19).value = results[j][11]
        sh2(j + 1, 20).value = results[j][13]
    with open(config.output_file_name, 'w', encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)


# Running the main function
if __name__ == "__main__":
    config = Config(
        Url="https://cmis.cicpa.org.cn",
        url="https://www.chinaacc.com/zyssfg/",
        Homematch="((http|https|ftp):)|(w{3})",
        urlmatch="login-comprehensiveEvaluation",
        htmlmatch="login-comprehensiveEvaluation",
        selector="//html/body/div[1]/div/div[2]/div/div[1]/div[1]/table/tr",
        max_pages_to_crawl=10,
        output_file_name="output.json"
    )
    red = redis.Redis(host='127.0.0.1', port=6379, db=0)
    red.delete('shell-urlset')
    path = '../data/中注协2022.xlsx'
    app = xw.App(visible=True, add_book=False)
    wb = app.books.open(path)
    sh1 = wb.sheets['Table 1']
    sh2 = wb.sheets[1]
    rng = sh2.range('a1').expand('table')
    nrowsd = rng.rows.count
    ncolsd = rng.columns.count
    a = sh2[0, :ncolsd - 1].value
    sh2[0, :ncolsd - 1].value = a
    nrows = sh1.used_range.last_cell.row
    ncolumns = sh1.used_range.last_cell.column
    ls_data = []
    is_key = []
    for i in range(nrows - 1):
        ls_data.append(sh1[i + 1, 9].hyperlink.replace("%23", "#"))

    # app.kill()  # 终止进程，强制退出。
    # app.quit()  # 在不保存的情况下，退出excel程序。
    asyncio.run(main(config))
# ^(tou)((?!zj).)*(?<!jw)$ 包括tou,不包括，不包括jw
# ^(tou)((?!zj).)*(jw)$ 包括tou,不包括，包括jw
