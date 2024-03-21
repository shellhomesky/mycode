import hashlib
import json
import re

import redis
from playwright.sync_api import sync_playwright

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
def get_page_html(page, selector):
    elements_text = page.locator(selector).all_inner_texts()
    text = ''
    for element_text in elements_text:
        text = text + element_text
    return text


# Crawl function
def crawl(config):
    results = []
    queue = [config.url]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        if config.cookie:
            page.context.add_cookies([{
                "name": config.cookie['name'],
                "value": config.cookie['value'], "url": config.url}])

        try:
            while queue and len(results) < config.max_pages_to_crawl:
                url = queue.pop(0)
                print(f"Crawler: Crawling {url}")
                page.goto(url)
                if re.search(config.htmlmatch, url):
                    html = get_page_html(page, config.selector)
                    results.append({'url': url, 'html': html})
                    with open(config.output_file_name, 'w', encoding="utf-8") as f:
                        json.dump(results, f, ensure_ascii=False)

                # Extract and enqueue links
                links = page.query_selector_all("a")
                for link in links:
                    href = link.get_attribute("href")
                    if not href:
                        href = ""
                    if not re.search(config.Homematch, href):
                        href = config.Url + href
                    if href and re.match(config.urlmatch, href) and add_url(href):
                        queue.append(href)

                # Implement on_visit_page logic if needed
        finally:
            browser.close()

    return results


# Main function
def main(config):
    results = crawl(config)
    with open(config.output_file_name, 'w', encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)


# Running the main function
if __name__ == "__main__":
    config = Config(
        Url="https://cmis.cicpa.org.cn",
        url="https://cmis.cicpa.org.cn/#/login-comprehensiveEvaluation?id=7dba3d77-2519-4222-a900-8d3ab3f64767",
        Homematch="((http|https|ftp):)|(w{3})",
        urlmatch="login-comprehensiveEvaluation",
        htmlmatch="login-comprehensiveEvaluation",
        selector="//html/body/div[1]/div/div[2]/div/div[1]/div[1]/table/tr",
        max_pages_to_crawl=10,
        output_file_name="output.json"
    )
    red = redis.Redis(host='127.0.0.1', port=6379, db=0)
    red.delete('shell-urlset')
    main(config)
# ^(tou)((?!zj).)*(?<!jw)$ 包括tou,不包括，不包括jw
# ^(tou)((?!zj).)*(jw)$ 包括tou,不包括，包括jw
