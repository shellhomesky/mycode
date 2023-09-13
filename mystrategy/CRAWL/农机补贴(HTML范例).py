import os
import time
import random
import requests
import json
from bs4 import BeautifulSoup
import pandas as pd


# 定义爬取农机补贴
def crawlListjs(Page, FactoryName, BusinessName, YearNum):
    headersws = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Length': '375',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': '__RequestVerificationToken_Lw__=8RqtxtsObjCOxHHBYWcm7PbCCopou8lJNV8RVPvuq7r9GsyHQKD8a0nNRI34yxhnGc7EiXt5kteDkQYlmDCO8UrcmzWBNFmd62CZ29vG1XTYB+FI9J475COP6Z13tn3PgNbm3va1/jfHsWxIw2xLGDr5PhG2LdQqV3JnvX0lCyI=',
        'Host': '202.102.17.134:85',
        'Origin': 'http://202.102.17.134:85',
        'Referer': 'http://202.102.17.134:85/pub/gongshi',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
    }
    data = {
        '__RequestVerificationToken': 'xonDc9JkZBTE8IBU/mYj/xCpbnIHjj94JJJpjS46gSeIJ5RcfrmMW9aR4hzB5rVXnn/tavoz1cuBPFdZ5YTbUfyBYGz2WzSAsRMhz/+2ppqtGzNvO2kZgnpq3DrK26aF8gyQZkR0yrTnkPZaolphvZHtOi+TwW5/XsWNJQBmlJ8=',
        'YearNum': '2020',
        'areaName': '',
        'AreaCode': '',
        'qy': '',
        'n': '',
        'JiJuLeiXing': '',
        'JiJuLeiXingCode': '',
        'FactoryName': '',
        'BusinessName': '',
        'ChuCBH': '',
        'StartGJRiQi': '',
        'EndGJRiQi': '',
        'StateValue': '',
        'StateName': ''
    }
    url = 'http://202.102.17.134:85/pub/GongShiSearch?pageIndex='
    data['FactoryName'] = FactoryName
    data['BusinessName'] = BusinessName
    data['YearNum'] = YearNum
    url = url + str(Page)
    data_list = []
    responsews = requests.post(url, headers=headersws, data=data)
    soup = BeautifulSoup(responsews.text, 'html5lib')
    trs = soup.find_all(bgcolor="#FFFFFF")
    for tr in trs:
        tds = tr.find_all('td')
        data_list.append({
            '序号': tds[0].contents[0].strip(),
            '县': tds[1].contents[0].strip(),
            '所在乡(镇)': tds[2].contents[0].strip(),
            '所在村组': tds[3].contents[0].strip(),
            '购机者姓名': tds[4].contents[0].strip(),
            '机具品目': tds[5].contents[0].strip(),
            '生产厂家': tds[6].contents[0].strip(),
            '产品名称': tds[7].contents[0].strip(),
            '购买机型': tds[8].contents[0].strip(),
            '购买数量(台)': tds[9].contents[0].strip(),
            '经销商': tds[10].contents[0].strip(),
            '购机日期': tds[11].contents[0].strip(),
            '单台销售价格(元)': tds[12].contents[0].strip(),
            '单台补贴额(元)': tds[13].contents[0].strip(),
            '总补贴额(元)': tds[14].contents[0].strip(),
            '出厂编号': tds[15].contents[0].strip(),
            '状态': tds[16].contents[0].strip(),
        })
    return pd.DataFrame(data_list)


def crawlListtj(Page, FactoryName, BusinessName, YearNum):
    headersws = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Length': '367',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': '__RequestVerificationToken_L0dvdVpCVF8yMDIxVG8yMw__=mhZHeW0LwVUDz+MKTzObGd+7YIDdqyeHgNy65f79Zxuu3HZTy5YVgi25mv1nYbdXhdjRvgUzBIQnSUWetlZpyChhqG6Blr/usIMPRyB9RJ5Ge0yC80FbKzmO59zWU18riq1amcfRHEqJqQXN1M5CLCipTnHAtkC0EebHYV3/pzg=; __RequestVerificationToken_L0dvdVpCVF8yMDE4VDIw=KFsTsGHWZXx+fUAlscUZhTudkuLU7H4W4FmGOgtUAJ4SZtrd1xeYGUS//kB+blJiFVCLjbxj113RkxXRR7eTlWX4Qek2+vXyVK0nmI7j7dmQU49jLISdBOIbEWZwEA59d1tY7y45ydHzyddjoDHlOFduWUt1CEXFOCbz17h3TnM=',
        'Host': '60.28.163.139:2018',
        'Origin': 'http://60.28.163.139:2018',
        'Referer': 'http://60.28.163.139:2018/GouZBT_2018T20/pub/GongShiSearch',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
    }
    data = {
        '__RequestVerificationToken': 'bhPfbCvh7yTjqVwvMYPvmRMNvL/JhJbG4flgw4VsO8n+a+WzMO853byd49XdMjBe1PlhiqZcVrDwRln7wMSc76PFC+wZfsiXIkNg/+iEId4HeZmRdmHDPssbp8dqaqcs6us6dVbvHUDTuUuc/CGUrwV560YMeLBgYhknnlaf7fc=',
        'YearNum': '2020',
        'areaName': '',
        'AreaCode': '',
        'qy': '',
        'n': '',
        'JiJuLeiXing': '',
        'JiJuLeiXingCode': '',
        'FactoryName': '',
        'BusinessName': '',
        'ChuCBH': '',
        'StartGJRiQi': '',
        'EndGJRiQi': '',
        'StateValue': '',
        'StateName': ''
    }
    url = 'http://60.28.163.139:2018/GouZBT_2018T20/pub/GongShiSearch?pageIndex='
    data['FactoryName'] = FactoryName
    data['BusinessName'] = BusinessName
    data['YearNum'] = YearNum
    url = url + str(Page)
    data_list = []
    responsews = requests.post(url, headers=headersws, data=data)
    soup = BeautifulSoup(responsews.text, 'html5lib')
    trs = soup.find_all(bgcolor="#FFFFFF")
    for tr in trs:
        tds = tr.find_all('td')
        data_list.append({
            '序号': tds[0].contents[0].strip(),
            '县': tds[1].contents[0].strip(),
            '所在乡(镇)': tds[2].contents[0].strip(),
            '所在村组': tds[3].contents[0].strip(),
            '购机者姓名': tds[4].contents[0].strip(),
            '机具品目': tds[5].contents[0].strip(),
            '生产厂家': tds[6].contents[0].strip(),
            '产品名称': tds[7].contents[0].strip(),
            '购买机型': tds[8].contents[0].strip(),
            '购买数量(台)': tds[9].contents[0].strip(),
            '经销商': tds[10].contents[0].strip(),
            '购机日期': tds[11].contents[0].strip(),
            '单台销售价格(元)': tds[12].contents[0].strip(),
            '单台补贴额(元)': tds[13].contents[0].strip(),
            '总补贴额(元)': tds[14].contents[0].strip(),
            '出厂编号': tds[15].contents[0].strip(),
            '状态': tds[16].contents[0].strip(),
        })
    return pd.DataFrame(data_list)


if __name__ == '__main__':
    rss = ".\\CRAWL\\data\\"
    fss = rss + '天津农机补贴2020.csv'
    sFactoryName = '江苏常发农业装备股份有限公司'
    sBusinessName = ''
    sYearNum = '2020'
    pdx = pd.DataFrame(columns=(
    "序号", "县", "所在乡(镇)", "所在村组", "购机者姓名", "机具品目", "生产厂家", "产品名称", "购买机型",
    "购买数量(台)", "经销商", "购机日期", "单台销售价格(元)", "单台补贴额(元)", "总补贴额(元)", "出厂编号", "状态"))
    try:
        for iPage in range(1, 5, 1):
            x = crawlListtj(iPage, sFactoryName, sBusinessName, sYearNum)
            pdx = pdx.append(x, ignore_index=True)
            time.sleep(random.randint(1, 6))
            print(iPage)
    except:
        pdx.to_csv(fss, index=False, encoding='gbk')
        print("现在查到第", "\n", iPage)
    pdx.to_csv(fss, index=False, encoding='gbk')
