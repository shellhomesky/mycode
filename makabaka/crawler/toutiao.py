import hashlib
import json
import math
import os
import re
import time
from html.parser import HTMLParser

import pandas as pd
import requests
from bs4 import BeautifulSoup


def getHoney():
    i = math.floor(time.time())
    e = str('%X' % i)
    md5 = hashlib.md5()
    md5.update(str(i).encode('utf-8'))
    t = str(md5.hexdigest()).upper()
    if 8 != len(e):
        return {
            'as': "479BB4B7254C150",
            'cp': "7E0AC8874BB0985"
        }
    o = t[0:5]
    n = t[-5:]
    a = ''
    r = ''
    for i in range(5):
        a += o[i] + e[i]
        r += e[i + 3] + n[i]
    return {
        'as': "A1" + a + e[-3:],
        'cp': e[0:3] + r + "E1"
    }


def get_signature(url):
    sign = os.popen('node .\CRAWL\signature.js {url}'.format(url='"' + url + '"')).read()
    return "&_signature=" + sign


def get_signacookie(cookiex):
    sign = os.popen('node .\CRAWL\signacookie.js {x}'.format(x='"' + cookiex + '"')).read()
    return sign


# 定义爬取用户文章列表函数
def crawlList(user_Id):
    headersws = {
        'Referer': 'https://www.toutiao.com/',
        'authority': 'www.toutiao.com',
        'method': 'GET',
        'path': '',
        'scheme': 'https',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'max-age=0',
        'cookie': 'WEATHER_CITY=%E5%8C%97%E4%BA%AC; __tasessionId=mpmcsahg41598082395365; csrftoken=d88edde850d6e743da81c381ccf33b43; ttcid=8aea1c38d9a9488da519aca292ffef3020; MONITOR_WEB_ID=9683749b-f33d-4f0e-afef-c33581fc975a; tt_webid=6863713774852097544; s_v_web_id=verify_ke5db22i_L3Mw4ccA_QxUm_4RYw_8uKv_8UUmjp4T80cp; tt_webid=6863713774852097544; tt_scid=7nmY9ofjDc1oXK2HiQT.8nH1OpayLQsQIQc-ACWXm6hhQqzmVwJR-DbvPNAbTdJ-0fe4',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
    }
    headersts = {
        'authority': 'www.toutiao.com',
        'method': 'GET',
        'path': '',
        'scheme': 'https',
        'accept': 'application/json, text/javascript',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'content-type': 'application/x-www-form-urlencoded',
        'cookie': 'tt_webid=6863704123716912653; s_v_web_id=verify_ke5bywrf_T2ajwpWr_T6um_4fXS_AR3f_qnGXQ1mBHQlS; WEATHER_CITY=%E5%8C%97%E4%BA%AC; __tasessionId=j5zm6js4r1598080670602; tt_webid=6863704123716912653; csrftoken=7b4e053e84afcabc65c1e73581704fbf; ttcid=7fcc03c138ee4b339aecc9139094f0f440; MONITOR_WEB_ID=d559fff4-408e-4157-8756-fc6a8dce3448; tt_scid=xjRm2btSqoIz0iBALBchgrc39YsENJgJG63jQzZ9kj4voWOLpFg4MNRoM5CyPMzq12bb',
        'referer': 'https://www.toutiao.com/',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36 Edg/84.0.522.61',
        'x-requested-with': 'XMLHttpRequest'
    }
    base_url = 'https://www.toutiao.com/toutiao'
    param = '/c/user/article/?page_type=1&user_id=' + user_ID + '&max_behot_time=0&count=20&as={as}&cp={cp}'.format(
        **getHoney())
    base_url += param
    signature = get_signature(base_url).replace('\n', '')
    path = param + signature
    headersws['path'] = path
    url = base_url + signature
    print(url)
    urlts = 'https://www.toutiao.com/c/user/article/?page_type=1&user_id=6872288237&max_behot_time=0&count=20&as=A1A5EF44D02B220&cp=5F40FB12D230FE1&_signature=_02B4Z6wo00f01t8HtvwAAIBBxllQyU0K.0rfArJAAOiPqnAb7Rg536p1V5zRrpPCZGtLHx7MtPVc6IxJlEjQWNpYJXULwjHVYf8u.RHaqoZ2MOUrP20i.XRecxfTZ756ZAE-FafMgk7A7rFO85'
    responsews = requests.get(url, headers=headersws)
    responsets = requests.get(urlts, headers=headersts)
    jsonsplit = responsews.content.decode('gbk')
    jsonsplit1 = jsonsplit.split('"data": ')[1].split(', "is_self": false}')[0]
    jsonsplit2 = json.loads(jsonsplit1)
    print(jsonsplit2)
    return pd.DataFrame(jsonsplit2)


# 定义爬取详情页函数
def crawlDetail_Pages(source_Url):
    headerslist = {
        'Referer': 'https://www.toutiao.com/',
        'authority': 'www.toutiao.com',
        'method': 'GET',
        'path': '',
        'scheme': 'https',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'max-age=0',
        'cookie': 'WEATHER_CITY=%E5%8C%97%E4%BA%AC; __tasessionId=mpmcsahg41598082395365; csrftoken=d88edde850d6e743da81c381ccf33b43; ttcid=8aea1c38d9a9488da519aca292ffef3020; MONITOR_WEB_ID=9683749b-f33d-4f0e-afef-c33581fc975a; tt_webid=6863713774852097544; s_v_web_id=verify_ke5db22i_L3Mw4ccA_QxUm_4RYw_8uKv_8UUmjp4T80cp; tt_webid=6863713774852097544; tt_scid=7nmY9ofjDc1oXK2HiQT.8nH1OpayLQsQIQc-ACWXm6hhQqzmVwJR-DbvPNAbTdJ-0fe4',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
    }
    headerslist['path'] = source_Url
    urllist = 'https://www.toutiao.com' + source_Url
    responselist = requests.get(urllist, headers=headerslist)
    resp_cookie = responselist.cookies.get_dict()
    if resp_cookie:
        x = resp_cookie['__ac_nonce']
        __ac_signature = get_signacookie(x).replace('\n', '')
        cookie = '__ac_nonce=' + x + '; ' + '__ac_signature=' + __ac_signature
        print(cookie)
        headerslist.update({"cookie": cookie})
        responselist = requests.get(url=urllist, headers=headerslist)
    soup = BeautifulSoup(responselist.text, 'html5lib')
    x = soup.find_all('script')[7].get_text()
    x1 = x.split('content: \'&quot;')[1].split('&quot;\'.slice(6, -6),')[0]
    # 去转义符
    html_parser = HTMLParser()
    x2 = html_parser.unescape(x1)
    # 网上去\u方法,匹配到的第一组内\\u002F的,传给x，先编码，再解码去除
    # content = "\\u002F哈哈"
    # content = re.sub(r'(\\u[\s\S]{4})',lambda x:x.group(1).encode("utf-8").decode("unicode-escape"),content)
    # 去特殊字符
    # a = re.compile(r'\n|&nbsp|\xa0|\\xa0|\u3000|\\u3000|\\u0020|\u0020|\t|\r')
    a = re.compile(r'\u3000|\u0020|\n|&nbsp|\xa0')
    x2 = re.sub(a, '', x2)
    # json 格式，使用json.loads 解码
    x3 = json.loads('"%s"' % x2)
    x4 = BeautifulSoup(x3, 'html5lib')
    x5 = x4.find_all('p')
    x6 = []
    for s in x5:
        x6.append(s.text)
    x7 = ''.join(x6)
    x8 = {"索引": source_Url, "内容": x7}
    return pd.DataFrame(x8, index=[0])


if __name__ == '__main__':
    rss = ".\\CRAWL\\data\\"
    fssjrtt = rss + 'jrtt2020.csv'
    user_ID = '6872288237'
    jrttpd = crawlList(user_ID)
    jrttpd.to_csv(fssjrtt, index=False, encoding='gbk')
    fss = rss + 'jrtt2020.csv'
    print(fss)
    stkPool = pd.read_csv(fss, encoding='gbk', usecols=[2, 20], header=0, names=['标题', 'source_url'])
    xn = len(stkPool.标题)
    pdx = pd.DataFrame(columns=('索引', '内容'))
    for i in range(2, xn):
        s = stkPool.iloc[i, 1]
        source_Url = '/i' + s.split('/item/')[1]
        x = crawlDetail_Pages(source_Url)
        pdx = pdx.append(x, ignore_index=True)
    fssjrtt = rss + 'jrtt2023.csv'
    pdx.to_csv(fssjrtt, index=False, encoding='gbk')
