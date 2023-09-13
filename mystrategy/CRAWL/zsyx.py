import os
import time
import random
import requests
import json
import pandas as pd


# 定义爬取招生计划学校代码
def crawlList(page, year_Id):
    headersws = {
        'authority': 'gk.jseea.cn',
        'method': 'POST',
        'path': '/ksapi/zyservice/xk/queryUniversity?t=1624768188618',
        'scheme': 'https',
        'accept': 'application/json, text/plain, */*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-length': '158',
        'content-type': 'application/json;charset=UTF-8',
        'cookie': '__jsluid_s=79831a6375ff67face225e58235f9a05; TY_SESSION_ID=d2545159-d483-44b6-921d-564ee599aa4a; __jsluid_h=7fdc988c03703053a3aeadf728565aaa; SESSION=YjIxY2VhZDYtNjhiNS00MjAxLTkxMDEtZWEyMTFhOGZhNzNi; token=2674CF74022D50CF33ED7695DD15B6D679219639CE4C9FEF',
        'origin': 'https://gk.jseea.cn',
        'referer': 'https://gk.jseea.cn/volunteer-search',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJrcyIsImlhdCI6MTYyNDc2ODEzOSwiZXhwIjoxNjI0NzcxNzM5LCJpZCI6IjIxMDQwMTAzMDQ4OCJ9.TbAQXmyrtWN5gVLvxGWSRZzhlJO6oo_LrjeNVCtXZ7c',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'x-tingyun-id': 'p35OnrDoP8k;r=768188620'
    }
    payloadData = {"current": 1, "size": 40, "sxkm": "历史", "yxmc": "", "searchType": "1", "year": "2020", "kldm": "1",
                   "zdpmq": "", "zdpmz": "", "pxfs": "01", "tbpc": [{"pcdm": "2", "sfzq": "0"}]}
    payloadData['current'] = page
    payloadData['sxkm'] = "历史"
    payloadData['year'] = year_Id
    data = json.dumps(payloadData)
    url = 'https://gk.jseea.cn/ksapi/zyservice/xk/queryUniversity?t=1624761455846'
    params = {'t': '1624761455846'}
    responsews = requests.post(url, headers=headersws, data=data)
    jsonsplit = responsews.content.decode('utf-8')
    jsonsplit1 = '[' + jsonsplit.split('"records":[')[1].split('],"total"')[0] + ']'
    jsonsplit2 = json.loads(jsonsplit1)
    return pd.DataFrame(jsonsplit2)


if __name__ == '__main__':
    rss = ".\\CRAWL\\data\\"
    fss = rss + 'zsjh202102.csv'
    year_Id = '2021'
    pdx = pd.DataFrame(columns=(
    "id", "code", "name", "is985", "is211", "areaCode", "areaName", "type", "typeName", "ranking", "phoneNo",
    "officialWebsite", "maleProportion", "femaleProportion", "descr", "smallImgUrl", "bigImgUrl", "address", "isAd",
    "isTop", "isGraduate", "isCivilianrun", "isIndependent", "superior", "superiorName", "genre", "genreName",
    "summary", "updateTime", "status", "isVip", "zydm", "zydh", "zymc", "zsjh", "sxkm", "zxkm", "zxkmmc", "zyzdh",
    "zyzmc"))
    try:
        for i in range(4, 22, 1):
            x = crawlList(i, year_Id)
            pdx = pdx.append(x, ignore_index=True)
            time.sleep(random.randint(1, 10))
            print(i)
    except:
        pdx.to_csv(fss, index=False, encoding='gbk')
        print("现在查到第", "\n", i)
    pdx.to_csv(fss, index=False, encoding='gbk')
