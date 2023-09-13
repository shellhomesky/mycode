import re
import os
import requests
import logging
import time
import csv

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')
RESPONSE_TIMEOUT = 5
P = 'C:'
DATABASE = '巨潮咨询股东大会'
# 判断文件夹是否存在，不存在，就创建
if os.path.exists(f'{P}\\{DATABASE}') == False:
    os.mkdir(f'{P}\\{DATABASE}')
"""
*****************
可改配置，酌情更改
*****************
"""
PLATE = 'sh;sz'
TRADE: str = '制造业'
STARTDAY = '2018-11-01'
ENDDAY = '2018-11-31'


# 定义爬取单页年报pdf——url的函数
def scrape_page_ajax_list(pageNum):
    url = 'http://www.cninfo.com.cn/new/hisAnnouncement/query'
    pageNum = int(pageNum)
    param = {
        'pageNum': pageNum,
        'pageSize': 30,
        'column': 'szse',
        'tabName': 'fulltext',
        'plate': PLATE,
        'stock': '',
        'searchkey': '',
        'secid': '',
        'category': 'category_gddh_szsh',
        'trade': TRADE,
        'seDate': STARTDAY + '~' + ENDDAY,
        'sortName': '',
        'sortType': '',
        'isHLtitle': 'true',
    }
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Length': '215',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': 'JSESSIONID=3D2C9AD1C9E6C884A48EE216FE50B480; insert_cookie=45380249; _sp_ses.2141=*; routeId=.uc2; SID=a4bfaf66-4071-4bec-bc8b-bdb7824d3871; _sp_id.2141=48258d87-38c7-4409-b999-e5ed41a663b2.1678705123.1.1678707048.1678705123.5fd0d0cb-b646-4508-8682-ff3c12815835',
        'Host': 'www.cninfo.com.cn',
        'Origin': 'http://www.cninfo.com.cn',
        'Referer': 'http://www.cninfo.com.cn/new/commonUrl/pageOfSearch?url=disclosure/list/search&checkedCategory=category_gddh_szsh',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
    logging.info('scraping page %s...', pageNum)
    try:
        r = requests.post(url, param, headers, timeout=RESPONSE_TIMEOUT)
        result = r.json().get('announcements')
        totalpages = r.json().get('totalpages')
        return result, totalpages
    except (requests.RequestException, TypeError):
        logging.error('error occurred while scraping page %s', pageNum, exc_info=True)


def get_and_download_pdf(result):
    ## 如果announcements不等于None,继续解析
    try:
        for item in result:
            ## 只获取带有《股东大会决议》的信息
            if re.search('股东大会决议公告', item.get('announcementTitle')):
                # pdfurl = item.get('adjunctUrl')
                full_pdf_url = 'http://static.cninfo.com.cn' + "/" + item.get('adjunctUrl')
                detail = {
                    'secCode': item.get('secCode'),
                    'secName': item.get('secName'),
                    'orgId': item.get('orgId'),
                    'announcementId': item.get('announcementId'),
                    'announcementTitle': item.get('announcementTitle'),
                    'adjunctUrl': full_pdf_url,
                    'announcementType': item.get('announcementType'),
                    'columnId': item.get('columnId'),
                    'orgId': item.get('orgId'),
                }
                secName = detail['secName'].replace('*', "")
                secCode = detail['secCode']
                title = detail['announcementTitle']
                # 构造文件名称
                filename = f'{secCode}-{secName}-{title}.pdf'
                # 构造文件路径
                filepath = f'{P}\\{DATABASE}\\{secName}\\{filename}'
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
                }
                logging.info('downloading file %s...', filename)
                # 判断文件夹是否存在，不存在就创建
                if os.path.exists(f'{P}\\{DATABASE}\\{secName}') == False:
                    os.mkdir(f'{P}\\{DATABASE}\\{secName}')
                # 判断文件是否存在，不存在就创建
                if os.path.exists(filepath) == False:
                    r = requests.get(full_pdf_url, headers=headers)
                    with open(filepath, 'wb') as f:
                        f.write(r.content)
                        f.close()
            time.sleep(2)
    except:
        logging.error('error occurred while downloading %s', filename, exc_info=True)
        pass


##设置循环下载每一页pdf
if __name__ == '__main__':
    r, totalpage = scrape_page_ajax_list(1)
    get_and_download_pdf(r)
    for page in range(2, totalpage + 1):
        res, _ = scrape_page_ajax_list(page)
        get_and_download_pdf(res)
