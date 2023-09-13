import os
import time
import math
import hashlib
import requests
import json
import re
from bs4 import BeautifulSoup
from html.parser import HTMLParser
import pandas as pd


def crawlDetail_Pages(source_Url):
    headerslist = {
        'authority': 'www.icourse163.org',
        'method': 'POST',
        'path': '/dwr/call/plaincall/MocQuizBean.getOpenQuizPaperDto.dwr',
        'scheme': 'https',
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-length': '286',
        'content-type': 'text/plain',
        'cookie': 'EDUWEBDEVICE=74b815e070e54ad08942a9fbfc490ada; __yadk_uid=dbQ8MRbbvJ9JCrJoGvdi2dU6gFBTDUlq; WM_TID=mm06%2BXde%2F%2BtBQAVQURI7stjTYy%2BLQb2W; P_INFO=18961157790|1639223660|1|imooc|00&99|CN&1639223545&edumooc_client#jis&320400#10#0#0|&0|null|18961157790; hasVolume=true; videoVolume=0.8; WM_NI=cHf5q9N7xMQV0VgyVDwDpPna%2BI%2BC86nHS3Q%2Bw4y6imfXbX9ZgqRY%2BoGaU20JMyriJ94vfmPuZRRGAr23KYj2W8Dp3kha2l%2BcxW8tgOK5VVLCMWDRIPZEmG5hwJYMbgg2R2Q%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eed1ea34879a89baee3b9aa88eb7c14e828f8fafae7a8798aba3bb798e9efca6e92af0fea7c3b92aa198aad6f4338ee9b8aed45ef48aa99ad550b59cc0b1ed6be997e5a4bb3eae989dd4d421b5ecb7d7ec67a688aeb9bc52a5af9ebaaa6585bf9bd3b3428fa7be8ac933f8aaaa8ed37f9a8e9ea8c47af2ed85bae93a95e88c91b261acbffe8daa69bc89f895e64589eb9ab7cf498f898cb3cc5c9a9ba3a8b864b59697aee16da5ee9ed3d437e2a3; hb_MA-A976-948FFA05E931_source=www.so.com; NTESSTUDYSI=484eaade2a724fd59b537faa402f0224; STUDY_INFO="yd.9740a9cb3ad4437ab@163.com|8|1478610057|1640925841908"; STUDY_SESS="DbwvmjZPx0m7GSxUtURduxZbEcZwhlAX4MeQyzix6I0M+06ByPnctsM+7ghAV9V3qanHmjvrgSyHNGqa4rLSnsui4TQ6JTnlni2/TcOlIEm0kM/dmJsnjywhpi7g8cZjEYAPfsIE38JGIldPdn3t7yYHOMXIz6dKkz9NREzeITELhur2Nm2wEb9HcEikV+3FTI8+lZKyHhiycNQo+g+/oA=="; STUDY_PERSIST="fXxSlUowk7IPIK88Oq3PaE447ex+KrsYkPxT3lkfmeACU5Aupk2FQohiARSTzplKzJ7lkhnGYWlGrAkQKv3MMQmniMWfmoCQ+Sz1sNv3n/QbHzQmzL19SoOToCb4AYfRxk6CT8VQliHJrfoEDX86ndWztfhhlCPC9bq7utxHXhIfLeBztrdxVdoO08D3EpJ5ZwY6Npl3BErjTDOw+/AboWZOBYEE1RkREbBVG3h8Yh3ZgpjCC7Iso4RP9U87vJE8LtaQzUT1ovP2MqtW5+L3Hw+PvH8+tZRDonbf7gEH7JU="; NETEASE_WDA_UID=1478610057#|#1628063366336; Hm_lvt_77dc9a9d49448cf5e629e5bebaa5500b=1640520466,1640863834,1640867922,1640925843; MOOC_PRIVACY_INFO_APPROVED=true; CLIENT_IP=117.63.9.249; Hm_lpvt_77dc9a9d49448cf5e629e5bebaa5500b=1640925893',
        'origin': 'https://www.icourse163.org',
        'eferer': 'https://www.icourse163.org/learn/NJUE-1458649164?tid=1465445504',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
    }
    data = {
        'callCount': '1',
        'scriptSessionId': '${scriptSessionId}190',
        'httpSessionId': '484eaade2a724fd59b537faa402f0224',
        'c0-scriptName': 'MocQuizBean',
        'c0-methodName': 'getOpenQuizPaperDto',
        'c0-id': '0',
        'c0-param0': 'string:1238157464',
        'c0-param1': 'number:2547483238',
        'c0-param2': 'boolean:false',
        'c0-param3': 'null:null',
        'batchId': '1640960535312'
    }
    url = 'https://www.icourse163.org/dwr/call/plaincall/MocQuizBean.getOpenQuizPaperDto.dwr' + source_Url
    responsews = requests.post(url, headers=headerslist, data=data)
    soup = BeautifulSoup(responsews.text, 'html5lib')
    pLists = soup.find_all('p')
    rLists = []
    for i in range(len(pLists)):
        x = pLists[i].get_text()
        # 去特殊字符
        a = re.compile(r'\u200a|\u200b|\u200c|\u200d|\u200e|\u200f|\u000d')
        x = re.sub(a, '', x)
        y = []
        y.append(i)
        y.append(x.encode('utf-8').decode('unicode_escape'))
        rLists.append(y)
    return pd.DataFrame(rLists)


if __name__ == '__main__':
    rss = ".\\data\\"
    fssjrtt = rss + 'jrtt2020.csv'
    user_ID = '6872288237'
    pdx = pd.DataFrame(columns=('索引', '内容'))
    x = crawlDetail_Pages('')
    pdx = pdx.append(x, ignore_index=True)
    fssjrtt = rss + 'mooc2021.csv'
    pdx.to_csv(fssjrtt, index=False, encoding='gbk')
