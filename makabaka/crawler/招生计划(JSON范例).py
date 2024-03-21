import json
import random
import time

import pandas as pd
import requests


# 定义爬取招生计划学校代码
def crawlList(page, year_Id):
    headersws = {
        'POST': '/home/data/spbone.html HTTP/1.1',
        'authority': 'gk.jseea.cn',
        'method': 'POST',
        'path': '/ksapi/zyservice/xk/queryUniversity?t=1615950189886',
        'scheme': 'https',
        'accept': 'application/json, text/plain, */*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-length': '158',
        'content-type': 'application/json;charset=UTF-8',
        'cookie': 'Hm_lvt_6f617ef469c36689efe6fc313f5a79ee=1605083834; __jsluid_s=c646ec422265968bbc6bf89adfd1718c; SESSION=ODU5NDA2ZDMtNTlhZC00YWY1LTg2MjktMTJjZDkxMTg5N2Y0; token=2674CF74022D50CF33ED7695DD15B6D679219639CE4C9FEF',
        'origin': 'https://gk.jseea.cn',
        'referer': 'https://gk.jseea.cn/volunteer-search',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJrcyIsImlhdCI6MTYxNTk0MTc4OSwiZXhwIjoxNjE1OTQ1Mzg5LCJpZCI6IjIxMDQwMTAzMDQ4OCJ9.bvmtjcy57xfvAKhZfoybQoixkUDBJH3y1b4AvJ2FiD8',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
    }
    payloadData = {"current": 1, "size": 10, "sxkm": "历史", "yxmc": "", "searchType": "1", "year": "2020", "kldm": "1",
                   "zdpmq": "", "zdpmz": "", "pxfs": "01", "tbpc": [{"pcdm": "2", "sfzq": "0"}]}
    payloadData['current'] = page
    payloadData['sxkm'] = "历史"
    payloadData['year'] = year_Id
    data = json.dumps(payloadData)
    url = 'https://gk.jseea.cn/ksapi/zyservice/xk/queryUniversity?t=1615950189886'
    params = {'t': '1615950189886'}
    responsews = requests.post(url, headers=headersws, data=data)
    jsonsplit = responsews.content.decode('utf-8')
    jsonsplit1 = '[' + jsonsplit.split('"records":[')[1].split('],"total"')[0] + ']'
    jsonsplit2 = json.loads(jsonsplit1)
    return pd.DataFrame(jsonsplit2)


# 查询学校id
def getschoolId(fss):
    return pd.read_csv(fss, encoding='gbk', usecols=[0])


# 定义爬取学校专业组招生计划
def crawlzyList(id, year_Id):
    headersws = {
        'authority': 'gk.jseea.cn',
        'method': 'POST',
        'path': '/ksapi/zyservice/queryMatchablePlanList?t=1624772668084&sfzq=0&zxkms=&yxdh=',
        'scheme': 'https',
        'accept': 'application/json, text/plain, */*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-length': '0',
        'Cookie': '__jsluid_s=79831a6375ff67face225e58235f9a05; TY_SESSION_ID=d2545159-d483-44b6-921d-564ee599aa4a; __jsluid_h=7fdc988c03703053a3aeadf728565aaa; SESSION=YjIxY2VhZDYtNjhiNS00MjAxLTkxMDEtZWEyMTFhOGZhNzNi; token=2674CF74022D50CF33ED7695DD15B6D679219639CE4C9FEF',
        'Origin': 'https://gk.jseea.cn',
        'Referer': 'https://gk.jseea.cn/university-detail?yxdh=',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJrcyIsImlhdCI6MTYyNDc3MjU4NSwiZXhwIjoxNjI0Nzc2MTg1LCJpZCI6IjIxMDQwMTAzMDQ4OCJ9.qY-vyUufmaduP9LIHP0U_i70viumZh0QK6PmDN2oV5c',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'x-tingyun-id': 'p35OnrDoP8k;r=772668085'
    }
    url = 'https://gk.jseea.cn/ksapi/zyservice/queryMatchablePlanList?t=1624774466303&sfzq=0&zxkms=&yxdh='
    headersws['path'] = headersws['path'] + str(id) + '&pcdms=2&zxkmyq=&sfzq=0&zydm='
    headersws['Referer'] = headersws['Referer'] + str(id) + '&pcdms=2&zxkmyq=&sfzq=0&zydm='
    url = url + str(id) + '&pcdms=2&zydm=&zyzdh='
    responsews = requests.post(url, headers=headersws)
    jsonsplit = responsews.content.decode('utf-8')
    jsonsplit1 = '[' + jsonsplit.split('"list":[')[1].split('}]}')[0] + '}]'
    jsonsplit2 = json.loads(jsonsplit1)
    pdzyz = pd.DataFrame(jsonsplit2)
    jsonsplit3 = []
    for listzyz in iter(jsonsplit2):
        for listzy in iter(listzyz['zyzDTO']):
            listzy['zyzdh'] = listzyz['zyzdh']
            jsonsplit3.append(listzy)
    pdzy = pd.DataFrame(jsonsplit3)
    return pd.DataFrame(pd.merge(pdzyz, pdzy, how='left', on=['zyzdh']))


if __name__ == '__main__':
    rss = ".\\CRAWL\\data\\"
    fss = rss + 'zsjh2021.csv'
    fsszyz = rss + 'zszyz2021.csv'
    year_Id = '2021'
    # pdx = pd.DataFrame(columns=("id","code","name","is985","is211","areaCode","areaName","type","typeName","ranking","phoneNo","officialWebsite","maleProportion","femaleProportion","descr","smallImgUrl","bigImgUrl","address","isAd","isTop","isGraduate","isCivilianrun","isIndependent","superior","superiorName","genre","genreName","summary","updateTime","status","isVip","zydm","zydh","zymc","zsjh","sxkm","zxkm","zxkmmc","zyzdh","zyzmc"))
    # for i in range(1,77,1):
    #	x = crawlList(i,year_Id)
    #	pdx = pdx.append(x,ignore_index=True)
    #	time.sleep(random.randint(1,3))
    # pdx.to_csv(fss,index=False,encoding='gbk')
    pdz = pd.DataFrame(columns=(
        "zyzsm", "zyzDTO", "sxkm", "zxkm", "zxkmyq", "sftj", "zssftj", "pcdm", "pcmc", "kldm", "kb", "yxdh",
        "yxlqfspmxx",
        "zydm", "zymc", "jhs", "zydh", "xn", "xf", "tishi"))
    pdx = getschoolId(fss)
    try:
        for i, iCode in enumerate(pdx.id):
            iCode = str(iCode).zfill(4)
            z = crawlzyList(iCode, year_Id)
            pdz = pdz.append(z, ignore_index=True)
            time.sleep(random.randint(1, 5))
            print(iCode)
    # data=data.set_index('trade_date').sort_index().loc[date:,]
    # data['trade_date'] =data.index
    # data.insert(0,'trade_date',data.index)
    # data.insert(0,'code',iCode)
    # reData=reData.append(data)
    except:
        pdz.to_csv(fsszyz, index=False, encoding='gbk')
        print("现在查到第", "\n", iCode)
    pdz.to_csv(fsszyz, index=False, encoding='gbk')
