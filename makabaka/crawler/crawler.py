# import pybloom as bf
import re
import time

import json
import pandas as pd
import requests

rss = ".\\CRAWL\\data\\"
fssgdfx = rss + 'gdfx2020.csv'
fssggfx = rss + 'ggfx2020.csv'


# 判断是否可爬
# rp=ro.RobotFileParser()
# rp.set_url('http://eastmoney.com/robots.txt')
# rp.read()
# print(rp.can_fetch('*','http://data.eastmoney.com/notices'))
# print(rp.can_fetch('*','http://data.eastmoney.com/gdfx/HoldingAnalyse.aspx'))
# 字符串转字典
def str2obj(s, s1=';', s2='='):
    li = s.split(s1)
    res = {}
    for kv in li:
        li2 = kv.split(s2)
        if len(li2) > 1:
            res[li2[0]] = li2[1]
    return res


# class CrawlBSF:
#	downloaded_urls = []
#	dum_md5_file = '文件路径'
#	bloom_download_urls = bf.BloomFilter(1024*1024*16,0.01)
#	cur_queue = deque()
#	def __init__(self):
#		try:
#			self.dum_file = open(dum_md5_file,'r')
#			self.downloaded_urls = self.dun_file.readlines()
#			self.dum_file.close()
#			for urlmd5 in self.downloaded_urls:
#				bloom_download_urls.add(urlmd5[:-1])
#		except IOError:
#			print('file not found')
#		finally:
#			self.dum_file = open(dum_md5_file,'a')
# urlopen方式
# url='http://data.eastmoney.com/notices/getdata.ashx'
# headers='''
# GET /notices/getdata.ashx?StockCode=&FirstNodeType=0&CodeType=1&PageIndex=2&PageSize=50&jsObj=TdunRLyl&SecNodeType=0&Time=&rt=53175115 HTTP/1.1
# Host: data.eastmoney.com
# Connection: keep-alive
# User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36
# Accept: */*
# Referer: http://data.eastmoney.com/notices/
##Accept-Encoding: gzip, deflate
# Accept-Language: zh-CN,zh;q=0.9
# Cookie: qgqp_b_id=8991720f35873eedd43b19c0b5bf95ea; em_hq_fls=js; intellpositionL=946.556px; emshistory=%5B%22%E5%85%89%E6%B4%8B%E8%82%A1%E4%BB%BD%22%2C%22%E5%BC%BA%E5%8A%9B%E6%96%B0%E6%9D%90%22%2C%22%E7%BB%B4%E5%B0%94%E5%88%A9%22%2C%22%E9%9B%B7%E7%A7%91%E9%98%B2%E5%8A%A1%22%5D; HAList=a-sz-002708-%u5149%u6D0B%u80A1%u4EFD%2Ca-sz-300190-%u7EF4%u5C14%u5229%2Ca-sz-300429-%u5F3A%u529B%u65B0%u6750%2Ca-sz-300059-%u4E1C%u65B9%u8D22%u5BCC%2Ca-sz-002413-%u96F7%u79D1%u9632%u52A1%2Ca-sz-002074-%u56FD%u8F69%u9AD8%u79D1%2Ca-sz-002478-%u5E38%u5B9D%u80A1%u4EFD; waptgshowtime=2020720; st_si=07207023104500; cowCookie=true; dRecords=%u516C%u544A%u5927%u5168-%u96F7%u79D1%u9632%u52A1%7Chttp%3A//data.eastmoney.com/notices/stock/002413.html%2C*%u516C%u544A%u5927%u5168-%u7EF4%u5C14%u5229%7Chttp%3A//data.eastmoney.com/notices/stock/300190.html%2C*%u516C%u544A%u5927%u5168-%u5F3A%u529B%u65B0%u6750%7Chttp%3A//data.eastmoney.com/notices/stock/300429.html%2C*%u516C%u544A%u5927%u5168-%u5149%u6D0B%u80A1%u4EFD%7Chttp%3A//data.eastmoney.com/notices/stock/002708.html%2C*%u59D4%u6258%u7406%u8D22%7Chttp%3A//data.eastmoney.com/wtlc/%2C*%u59D4%u6258%u7406%u8D22-%u5E38%u5B9D%u80A1%u4EFD%7Chttp%3A//data.eastmoney.com/wtlc/detail/002478.html%2C*%u80A1%u4E1C%u5206%u6790%7Chttp%3A//data.eastmoney.com/gdfx/%2C*%u6CAA%u6DF1A%u80A1%u516C%u544A%7Chttp%3A//data.eastmoney.com/notices/; st_pvi=25324460572036; st_sp=2020-05-19%2010%3A48%3A04; st_inirUrl=https%3A%2F%2Fwww.so.com%2Flink; st_sn=5; st_psi=20200720215711515-113300301011-8855228064; st_asi=delete; intellpositionT=2315.8px
# '''
# headers=str2obj(headers,'\n',': ')
# params={
#	'StockCode':'',
#	'FirstNodeType':'0',
#	'CodeType': '1',
#	'PageIndex':'2',
#	'PageSize':'50',
#	'jsObj':'TdunRLyl',
#	'SecNodeType':'0',
#	'Time':'',
#	'rt':'53175115'
# }
# params=pa.urlencode(params)
# url=url+"?"+params
# requrl=req.Request(url,headers=headers)
# res=req.urlopen(requrl)
# ggweb=res.read().decode('gbk')
# print(ggweb)
# gdfxjson=json.loads(ggweb)
# row=pd.DataFrame(gdfxjson)
# print(response.status)
# print(response.getheaders())
# 查询上市公司股东变动分析
# url='http://data.eastmoney.com/DataCenter_V3/gdfx/data.ashx'
# headers='''
# GET /DataCenter_V3/gdfx/data.ashx?sty=analy&SortType=NDATE,SCODE,RANK&SortRule=1&PageIndex=2&PageSize=50&jsObj=VqojiBuY&type=NSHDDETAIL&date=&gdlx=0&cgbd=0&rt=53134086 HTTP/1.1
# Host: data.eastmoney.com
# Connection: keep-alive
# User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36
# Accept: */*
# Referer: http://data.eastmoney.com/gdfx/HoldingAnalyse.aspx
# Accept-Encoding: gzip, deflate
# Accept-Language: zh-CN,zh;q=0.9
# Cookie: qgqp_b_id=a5e6aeb93e1a469e5671edd8339874e0; em_hq_fls=js; intellpositionL=1079.19px; emshistory=%5B%22%E5%B8%B8%E5%AE%9D%E8%82%A1%E4%BB%BD%22%5D; ct=mGtiocHn5k79iqVP_ZotydTu6GcpSVkD-eFxmMu7dHV3qx9B5sTr4yEPU6qsj2PeMdoPAbiaiLcM3vA-LV4x6AelcUhOTm9ZDqA_TUroewSM_ozNtWq98Yf0cKUtkVQ7Fu84MQ8F5Wdg7UumfIhwvAHzXnhmWtDK880hzpmNSXw; ut=FobyicMgeV4NKY1cLeahQ1wbVHFP11odaQuPZoSnasCq_jOTs8w1K-X6NvUYKQMvf_EMRrjNL0SGAyKDVh3Ik4yT0uL-PsfPK2Iu_dCsfztJm5xdup6QqRVKyoXO_q5CGjlNmu_m0qWwQ3DJV-auRkMeBWGpqLAL9G6a82ywxBuHT2XoqFHSx-Az2tbmiZZppSqB-iwRm3EHQta8gXyCB-Mo_LSzQaVNxTpEsNya75Z2rxCLDqQ8bbr_AftnwFe92KmnMJo4rktAC5BtD10Jsif0LwoIl6Zz; pi=9191114038107504%3b%3b%e5%a4%9c%e8%89%b2%e6%97%8b%e5%be%8b%3bcpLX1VNFYZdcjqzxD2gWk4l8IpJuXHzvahY%2fjXRJ6cMP26BrACUbEFL5n1as0KTSmA9pc7vSwjCgJ2GAMsWTZvyxzpzGGiccNXIVVecYzbVevyabNNXYuHyu1koZtgzh9d0JXf7VPO9giIuO7U18cAvbPGKX%2fxbh9MFG%2bfZ6lnBgZuD8o3SfiEmVhsNuo0VU%2fuyCXcLA%3bhNq1rtZseNfocTATBjq2A1e%2b7HxpQ1yi3F4lU2WDdEEN2TVHw9KdnKhqhskvZ5bbrPME2CI9CjbscYidk9hF4xBgV2lDXEFU37pjXyGTdIwfcMJ7zE5AbATzLYzcaIJKLtOwnI9HeihXHVTeFuFQt4xa%2f3xZzA%3d%3d; uidal=9191114038107504%e5%a4%9c%e8%89%b2%e6%97%8b%e5%be%8b; sid=119055840; vtpst=|; dRecords=%u516C%u544A%u5927%u5168-%u767E%u5DDD%u80FD%u6E90%7Chttp%3A//data.eastmoney.com/notices/stock/600681.html%2C*%u516C%u544A%u5927%u5168-*ST%u767E%u82B1%7Chttp%3A//data.eastmoney.com/notices/stock/600721.html%2C*%u516C%u544A%u5927%u5168-%u5E38%u5B9D%u80A1%u4EFD%7Chttp%3A//data.eastmoney.com/notices/stock/002478.html%2C*%u80A1%u4E1C%u589E%u51CF%u6301%7Chttp%3A//data.eastmoney.com/executive/gdzjc.html%2C*%u5229%u6DA6%u8868%7Chttp%3A//data.eastmoney.com/bbsj/201912/lrb.html%2C*%u73B0%u91D1%u6D41%u91CF%u8868%7Chttp%3A//data.eastmoney.com/bbsj/201912/xjll.html%2C*%u6CAA%u6DF1A%u80A1%u516C%u544A%7Chttp%3A//data.eastmoney.com/notices/%2C*%u4E1A%u7EE9%u62A5%u8868%7Chttp%3A//data.eastmoney.com/bbsj/201912/yjbb.html%2C*%u8D44%u4EA7%u8D1F%u503A%u8868%7Chttp%3A//data.eastmoney.com/bbsj/zcfz.html%2C*%u80A1%u4E1C%u5206%u6790%7Chttp%3A//data.eastmoney.com/gdfx/; HAList=a-sz-300521-%u7231%u53F8%u51EF%2Ca-sz-300059-%u4E1C%u65B9%u8D22%u5BCC%2Ca-sh-688418-%u9707%u6709%u79D1%u6280%2Ca-sh-603197-%u4FDD%u9686%u79D1%u6280%2Ca-sz-300429-%u5F3A%u529B%u65B0%u6750%2Ca-sh-603188-ST%u4E9A%u90A6; cowCookie=true; st_si=66606257747131; st_asi=delete; st_pvi=38978053239260; st_sp=2019-03-06%2009%3A34%3A49; st_inirUrl=https%3A%2F%2Fhao.360.cn%2F; st_sn=3; st_psi=20200706160312482-0-2526275003; intellpositionT=2855px
# '''
# headers=str2obj(headers,'\n',': ')
# params={
#	'sty': 'analy',
#	'SortType':'NDATE,SCODE,RANK',
#	'SortRule':'1',
#	'PageIndex':'1',
#	'PageSize':'50',
#	'jsObj':'VqojiBuY',
#	'type':'NSHDDETAIL',
#	'date': '',
#	'gdlx':'0',
#	'cgbd':'0',
#	'rt':'53134086'
# }
# reData=pd.read_csv(fssgdfx,encoding='gbk')
# try:
#	for i in range(1,757):
#		params['PageIndex']=i
#		response = requests.get(url,params=params,headers=headers)
#		jsonsplit=response.content.decode('gbk').split('{pages:756,data:')[1].split('};')[0]
#		jsonlist = json.loads(jsonsplit)
#		gdfxpd=pd.DataFrame(jsonlist)
#		reData=reData.append(gdfxpd)
#		print(i)
#		time.sleep(2.5)
#	reData.to_csv(fssgdfx,index=False,encoding='gbk')
# except:
#	reData.to_csv(fssgdfx,index=False,encoding='gbk')
#	print(i)

# 查询上市公司公告
url = 'http://data.eastmoney.com/notices/getdata.ashx'
headers = '''
GET /notices/getdata.ashx?StockCode=&FirstNodeType=0&CodeType=1&PageIndex=2&PageSize=50&jsObj=TdunRLyl&SecNodeType=0&Time=&rt=53175115 HTTP/1.1
Host: data.eastmoney.com
Connection: keep-alive
User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36
Accept: */*
Referer: http://data.eastmoney.com/notices/
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Cookie: qgqp_b_id=8991720f35873eedd43b19c0b5bf95ea; em_hq_fls=js; intellpositionL=946.556px; emshistory=%5B%22%E5%85%89%E6%B4%8B%E8%82%A1%E4%BB%BD%22%2C%22%E5%BC%BA%E5%8A%9B%E6%96%B0%E6%9D%90%22%2C%22%E7%BB%B4%E5%B0%94%E5%88%A9%22%2C%22%E9%9B%B7%E7%A7%91%E9%98%B2%E5%8A%A1%22%5D; HAList=a-sz-002708-%u5149%u6D0B%u80A1%u4EFD%2Ca-sz-300190-%u7EF4%u5C14%u5229%2Ca-sz-300429-%u5F3A%u529B%u65B0%u6750%2Ca-sz-300059-%u4E1C%u65B9%u8D22%u5BCC%2Ca-sz-002413-%u96F7%u79D1%u9632%u52A1%2Ca-sz-002074-%u56FD%u8F69%u9AD8%u79D1%2Ca-sz-002478-%u5E38%u5B9D%u80A1%u4EFD; waptgshowtime=2020720; st_si=07207023104500; cowCookie=true; dRecords=%u516C%u544A%u5927%u5168-%u96F7%u79D1%u9632%u52A1%7Chttp%3A//data.eastmoney.com/notices/stock/002413.html%2C*%u516C%u544A%u5927%u5168-%u7EF4%u5C14%u5229%7Chttp%3A//data.eastmoney.com/notices/stock/300190.html%2C*%u516C%u544A%u5927%u5168-%u5F3A%u529B%u65B0%u6750%7Chttp%3A//data.eastmoney.com/notices/stock/300429.html%2C*%u516C%u544A%u5927%u5168-%u5149%u6D0B%u80A1%u4EFD%7Chttp%3A//data.eastmoney.com/notices/stock/002708.html%2C*%u59D4%u6258%u7406%u8D22%7Chttp%3A//data.eastmoney.com/wtlc/%2C*%u59D4%u6258%u7406%u8D22-%u5E38%u5B9D%u80A1%u4EFD%7Chttp%3A//data.eastmoney.com/wtlc/detail/002478.html%2C*%u80A1%u4E1C%u5206%u6790%7Chttp%3A//data.eastmoney.com/gdfx/%2C*%u6CAA%u6DF1A%u80A1%u516C%u544A%7Chttp%3A//data.eastmoney.com/notices/; st_pvi=25324460572036; st_sp=2020-05-19%2010%3A48%3A04; st_inirUrl=https%3A%2F%2Fwww.so.com%2Flink; st_sn=5; st_psi=20200720215711515-113300301011-8855228064; st_asi=delete; intellpositionT=2315.8px
'''
headers = str2obj(headers, '\n', ': ')
params = {
    'StockCode': '',
    'FirstNodeType': '0',
    'CodeType': '1',
    'PageIndex': '2',
    'PageSize': '50',
    'jsObj': 'TdunRLyl',
    'SecNodeType': '0',
    'Time': '',
    'rt': '53175115'
}
reData = pd.read_csv(fssggfx, encoding='gbk')
zz = '(?<="ENDDATE":").*?(?=T)'
rezz = re.compile(zz)
zz1 = '"ENDDATE":"(20[12][05678].*?)T.*?"Url":"(.*?)"'
try:
    for i in range(1, 3):
        params['PageIndex'] = i
        response = requests.request('GET', url, params=params, headers=headers)
        jsonsplit = response.content.decode('gbk')
        jsonsplit1 = jsonsplit.split('= {"data":')[1].split(',"TotalCount')[0]
        jsonlist2 = json.loads(jsonsplit1)
        talk_url = re.findall(r'(?<="ENDDATE":").*?(?=T)', jsonsplit2)
        ggfxpd = pd.DataFrame(jsonlist2)
        reData = reData.append(ggfxpd)
        print(i)
        time.sleep(2.5)
    reData.to_csv(fssggfx, index=False, encoding='gbk')
except:
    reData.to_csv(fssggfx, index=False, encoding='gbk')
    print(i)
# 解析url
# result = pa.urlparse(url)
# print(type(result),result)
