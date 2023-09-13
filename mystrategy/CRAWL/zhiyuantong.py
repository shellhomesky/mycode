import os
import time
import requests
import json
import pandas as pd


# 定义爬取志愿通专业分数线列表函数
def crawlzyList(start, year_Id):
    headersws = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Length': '3454',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': 'PHPSESSID=5cdfcir9191ad64lp3428i8q96; Hm_lvt_4716722fb4ab5afbce610d397c76c3fd=1622261987; Hm_lpvt_4716722fb4ab5afbce610d397c76c3fd=1622261987; Hm_lvt_7fdc476582e50d70ca66420b1cda9f43=1622261988; Hm_lpvt_7fdc476582e50d70ca66420b1cda9f43=1622261988; sitemember=rn2l2ISodah_dHOqgHl5m7R81ZuU3qXbr66im8N6edzFgNzXkZagpox3eGONhX2cxozU3H_Of9yvnoyrrnd43LBssZeEuHVne52qqY1koNq-ap6Vk9KHzLFmnmiunXyZxLPT2YTOo5qWnYislImO1b5qq5SSu2_Yq56nrLCdgNuwoq2Rhqh1q4tih2iCdpfesnzImX_Oody7ZoRjsIqI2rB9z9iElompjJp4nYJ1fZzIstTcfrilzMR7eazFeqvYu2vQ1pi8dZqBY39pgIaFm66iqtx_p2rcr56Mp66HeJKto6nYgM6oq4GanWl8n6Dcvo-3z5TRjN3FrXxpxK2i269908ps1nuXaHmng2hnraeams6YZsabyJeWnHWWaIaTloWPyYDOqKuBmnetgpt-2L6Qs5STq2_Rw4ton8SgbNaqo9jbhs59Z3uedJ18nKjftKKumnrRos6rnqessJ2ImKqjtZWF3oFie5qmrYKcjZuupZbaitGi1ryHfGnEraLaro3TyoS4gWaAmnesgIaBmrSMps2Al2ag',
        'Host': 'www.zhiyuantong.com',
        'Origin': 'https://www.zhiyuantong.com',
        'Referer': 'https://www.zhiyuantong.com/Home/Data/cobone.html',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }
    data = {
        'draw': '',
        'columns[0][data]': 'cid',
        'columns[0][name]': '',
        'columns[0][searchable]': 'true',
        'columns[0][orderable]': 'true',
        'columns[0][search][value]': '',
        'columns[0][search][regex]': 'false',
        'columns[1][data]': 'specname',
        'columns[1][name]': '',
        'columns[1][searchable]': 'true',
        'columns[1][orderable]': 'true',
        'columns[1][search][value]': '',
        'columns[1][search][regex]': 'false',
        'columns[2][data]': 'cid',
        'columns[2][name]': '',
        'columns[2][searchable]': 'true',
        'columns[2][orderable]': 'false',
        'columns[2][search][value]': '',
        'columns[2][search][regex]': 'false',
        'columns[3][data]': 'province',
        'columns[3][name]': '',
        'columns[3][searchable]': 'true',
        'columns[3][orderable]': 'false',
        'columns[3][search][value]': '',
        'columns[3][search][regex]': 'false',
        'columns[4][data]': 'collegetype',
        'columns[4][name]': '',
        'columns[4][searchable]': 'true',
        'columns[4][orderable]': 'false',
        'columns[4][search][value]': '',
        'columns[4][search][regex]': 'false',
        'columns[5][data]': 'xdenji',
        'columns[5][name]': '',
        'columns[5][searchable]': 'true',
        'columns[5][orderable]': 'false',
        'columns[5][search][value]': '',
        'columns[5][search][regex]': 'false',
        'columns[6][data]': 'speccodenum',
        'columns[6][name]': '',
        'columns[6][searchable]': 'true',
        'columns[6][orderable]': 'true',
        'columns[6][search][value]': '',
        'columns[6][search][regex]': 'false',
        'columns[7][data]': 'yearno',
        'columns[7][name]': '',
        'columns[7][searchable]': 'true',
        'columns[7][orderable]': 'true',
        'columns[7][search][value]': '',
        'columns[7][search][regex]': 'false',
        'columns[8][data]': 'plannum',
        'columns[8][name]': '',
        'columns[8][searchable]': 'true',
        'columns[8][orderable]': 'true',
        'columns[8][search][value]': '',
        'columns[8][search][regex]': 'false',
        'columns[9][data]': 'lannum',
        'columns[9][name]': '',
        'columns[9][searchable]': 'true',
        'columns[9][orderable]': 'true',
        'columns[9][search][value]': '',
        'columns[9][search][regex]': 'false',
        'columns[10][data]': 'maxscore',
        'columns[10][name]': '',
        'columns[10][searchable]': 'true',
        'columns[10][orderable]': 'false',
        'columns[10][search][value]': '',
        'columns[10][search][regex]': 'false',
        'columns[11][data]': 'minscore',
        'columns[11][name]': '',
        'columns[11][searchable]': 'true',
        'columns[11][orderable]': 'false',
        'columns[11][search][value]': '',
        'columns[11][search][regex]': 'false',
        'columns[12][data]': 'minscoreminus',
        'columns[12][name]': '',
        'columns[12][searchable]': 'true',
        'columns[12][orderable]': 'true',
        'columns[12][search][value]': '',
        'columns[12][search][regex]': 'false',
        'columns[13][data]': 'segmentposition',
        'columns[13][name]': '',
        'columns[13][searchable]': 'true',
        'columns[13][orderable]': 'true',
        'columns[13][search][value]': '',
        'columns[13][search][regex]': 'false',
        'columns[14][data]': 'id',
        'columns[14][name]': '',
        'columns[14][searchable]': 'true',
        'columns[14][orderable]': 'false',
        'columns[14][search][value]': '',
        'columns[14][search][regex]': 'false',
        'order[0][column]': '0',
        'order[0][dir]': 'asc',
        'start': '',
        'length': '100',
        'search[value]': '',
        'search[regex]': 'false',
        'yearno': '',
        'tese': '0',
        'banxuetype': '',
        'province': '',
        'specialty': '',
        'fcstart': '',
        'fcend': '',
        'wcstart': '',
        'wcend': '',
        'coname': ''
    }
    url = 'https://www.zhiyuantong.com/home/data/spbone.html'
    data['draw'] = start / 100
    data['start'] = start
    data['yearno'] = year_Id
    responsews = requests.post(url, headers=headersws, data=data)
    jsonsplit = responsews.content.decode('gbk')
    jsonsplit1 = '[' + jsonsplit.split('"data":[')[1].split(']}')[0] + ']'
    jsonsplit2 = json.loads(jsonsplit1)
    return pd.DataFrame(jsonsplit2)


def crawlyxList(start, year_Id):
    headersws = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Length': '3454',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': 'PHPSESSID=5cdfcir9191ad64lp3428i8q96; Hm_lvt_4716722fb4ab5afbce610d397c76c3fd=1622261987; Hm_lpvt_4716722fb4ab5afbce610d397c76c3fd=1622261987; Hm_lvt_7fdc476582e50d70ca66420b1cda9f43=1622261988; Hm_lpvt_7fdc476582e50d70ca66420b1cda9f43=1622261988; sitemember=rn2l2ISodah_dHOqgHl5m7R81ZuU3qXbr66im8N6edzFgNzXkZagpox3eGONhX2cxozU3H_Of9yvnoyrrnd43LBssZeEuHVne52qqY1koNq-ap6Vk9KHzLFmnmiunXyZxLPT2YTOo5qWnYislImO1b5qq5SSu2_Yq56nrLCdgNuwoq2Rhqh1q4tih2iCdpfesnzImX_Oody7ZoRjsIqI2rB9z9iElompjJp4nYJ1fZzIstTcfrilzMR7eazFeqvYu2vQ1pi8dZqBY39pgIaFm66iqtx_p2rcr56Mp66HeJKto6nYgM6oq4GanWl8n6Dcvo-3z5TRjN3FrXxpxK2i269908ps1nuXaHmng2hnraeams6YZsabyJeWnHWWaIaTloWPyYDOqKuBmnetgpt-2L6Qs5STq2_Rw4ton8SgbNaqo9jbhs59Z3uedJ18nKjftKKumnrRos6rnqessJ2ImKqjtZWF3oFie5qmrYKcjZuupZbaitGi1ryHfGnEraLaro3TyoS4gWaAmnesgIaBmrSMps2Al2ag',
        'Host': 'www.zhiyuantong.com',
        'Origin': 'https://www.zhiyuantong.com',
        'Referer': 'https://www.zhiyuantong.com/Home/Data/cobone.html',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }
    data = {
        'columns[0][name]': '',
        'columns[0][searchable]': 'true',
        'columns[0][orderable]': 'true',
        'columns[0][search][value]': '',
        'columns[0][search][regex]': 'false',
        'columns[1][data]': 'specname',
        'columns[1][name]': '',
        'columns[1][searchable]': 'true',
        'columns[1][orderable]': 'true',
        'columns[1][search][value]': '',
        'columns[1][search][regex]': 'false',
        'columns[2][data]': 'cid',
        'columns[2][name]': '',
        'columns[2][searchable]': 'true',
        'columns[2][orderable]': 'false',
        'columns[2][search][value]': '',
        'columns[2][search][regex]': 'false',
        'columns[3][data]': 'province',
        'columns[3][name]': '',
        'columns[3][searchable]': 'true',
        'columns[3][orderable]': 'false',
        'columns[3][search][value]': '',
        'columns[3][search][regex]': 'false',
        'columns[4][data]': 'collegetype',
        'columns[4][name]': '',
        'columns[4][searchable]': 'true',
        'columns[4][orderable]': 'false',
        'columns[4][search][value]': '',
        'columns[4][search][regex]': 'false',
        'columns[5][data]': 'xdenji',
        'columns[5][name]': '',
        'columns[5][searchable]': 'true',
        'columns[5][orderable]': 'false',
        'columns[5][search][value]': '',
        'columns[5][search][regex]': 'false',
        'columns[6][data]': 'speccodenum',
        'columns[6][name]': '',
        'columns[6][searchable]': 'true',
        'columns[6][orderable]': 'true',
        'columns[6][search][value]': '',
        'columns[6][search][regex]': 'false',
        'columns[7][data]': 'yearno',
        'columns[7][name]': '',
        'columns[7][searchable]': 'true',
        'columns[7][orderable]': 'true',
        'columns[7][search][value]': '',
        'columns[7][search][regex]': 'false',
        'columns[8][data]': 'plannum',
        'columns[8][name]': '',
        'columns[8][searchable]': 'true',
        'columns[8][orderable]': 'true',
        'columns[8][search][value]': '',
        'columns[8][search][regex]': 'false',
        'columns[9][data]': 'lannum',
        'columns[9][name]': '',
        'columns[9][searchable]': 'true',
        'columns[9][orderable]': 'true',
        'columns[9][search][value]': '',
        'columns[9][search][regex]': 'false',
        'columns[10][data]': 'maxscore',
        'columns[10][name]': '',
        'columns[10][searchable]': 'true',
        'columns[10][orderable]': 'false',
        'columns[10][search][value]': '',
        'columns[10][search][regex]': 'false',
        'columns[11][data]': 'minscore',
        'columns[11][name]': '',
        'columns[11][searchable]': 'true',
        'columns[11][orderable]': 'false',
        'columns[11][search][value]': '',
        'columns[11][search][regex]': 'false',
        'columns[12][data]': 'minscoreminus',
        'columns[12][name]': '',
        'columns[12][searchable]': 'true',
        'columns[12][orderable]': 'true',
        'columns[12][search][value]': '',
        'columns[12][search][regex]': 'false',
        'columns[13][data]': 'segmentposition',
        'columns[13][name]': '',
        'columns[13][searchable]': 'true',
        'columns[13][orderable]': 'true',
        'columns[13][search][value]': '',
        'columns[13][search][regex]': 'false',
        'columns[14][data]': 'id',
        'columns[14][name]': '',
        'columns[14][searchable]': 'true',
        'columns[14][orderable]': 'false',
        'columns[14][search][value]': '',
        'columns[14][search][regex]': 'false',
        'order[0][column]': '0',
        'order[0][dir]': 'asc',
        'start': '',
        'length': '100',
        'search[value]': '',
        'search[regex]': 'false',
        'yearno': '',
        'tese': '0',
        'banxuetype': '',
        'province': '',
        'specialty': '',
        'fcstart': '',
        'fcend': '',
        'wcstart': '',
        'wcend': '',
        'coname': ''
    }
    url = 'https://www.zhiyuantong.com/Home/Data/cobone.html'
    data['draw'] = start / 100
    data['start'] = start
    data['yearno'] = year_Id
    responsews = requests.post(url, headers=headersws, data=data)
    jsonsplit = responsews.content.decode('gbk')
    jsonsplit1 = '[' + jsonsplit.split('"data":[')[1].split('}]}')[0] + '}]'
    jsonsplit2 = json.loads(jsonsplit1)
    return pd.DataFrame(jsonsplit2)


if __name__ == '__main__':
    rss = ".\\CRAWL\\data\\"
    fsszyt = rss + 'zyt2020.csv'
    fsszytyx = rss + 'zytyx2020.csv'
    start = 0
    year_Id = '2019'
    pdx = pd.DataFrame(columns=(
    'id', 'pcid', 'cid', 'zscode', 'zstype', 'coname', 'conamememo', 'bdenji', 'xdenji', 'xdenjinuma', 'xdenjinumb',
    'xdenjicanchange', 'diploma', 'yearno', 'ty', 'pici', 'source_pici', 'source_zscode', 'speccodenum', 'specname',
    'specflag_old', 'specflag', 'specnamememo_jiu', 'specnamememo', 'specnamememolq', 'specnamememoplan',
    'plannumupdown', 'xuezi', 'xuefei', 'xuancei', 'sid', 'speccode', 'scateid', 'stypebig', 'stypesmall', 'plannum',
    'lqnum', 'maxscore', 'minscore', 'minscoreminus', 'segmentposition', 'segmenttotalman', 'linescore', 'zypingxing',
    'zyzhengqiu', 'zyfucong', 'lastplannum', 'lastlqnum', 'lastmaxscore', 'lastminscore', 'lastminscoreminus',
    'lastsegmentposition', 'lastsegmenttotalman', 'lastlinescore', 'lastzypingxing', 'lastzyzhengqiu', 'lastzyfucong',
    'is985', 'is211', 'isyan', 'is11c', 'is11s', 'collegelevel', 'collegetype', 'province', 'banxuetype',
    'minscoreminus2019', 'segmentposition2019', 'minscoreminus2018', 'segmentposition2018', 'minscoreminus2017',
    'segmentposition2017', 'minscoreminus2016', 'segmentposition2016', 'minscoreminus2015', 'segmentposition2015',
    'isok'))
    for i in range(start, 1800, 100):
        x = crawlzyList(i, year_Id)
        pdx = pdx.append(x, ignore_index=True)
        time.sleep(5)
    pdx.to_csv(fsszyt, index=False, encoding='gbk')
# pdx = pd.DataFrame(columns=('id','pcid','cid','招生代码','zstype','coname','conamememo','bdenji','选测等级','xdenjinuma','xdenjinumb','xdenjicanchange','diploma','yearno','ty','pici','source_pici','source_zscode','招生专业代码','specname','specflag','specnamememo','specnamememolq','specnamememoplan','招生计划增减','xuezi','xuefei','xuancei','sid','speccode','scateid','stypebig','stypesmall','计划招生','录取人数','最高分','最低分','分差','位次','segmenttotalman','linescore','zypingxing','zyzhengqiu','zyfucong','lastplannum','lastlqnum','2018最高分','2018最低分','2018分差','2018位次','lastsegmenttotalman','lastlinescore','lastzypingxing','lastzyzhengqiu','lastzyfucong','is985','is211','isyan','is11c','is11s','collegelevel','collegetype','province','banxuetype','分差2019','位次2019','分差2018','位次2018','分差2017','位次2017','分差2016','位次2016','分差2015','位次2015','isok'))
# for i in range(start,247,100):
#	x = crawlyxList(i,year_Id)
#	pdx = pdx.append(x,ignore_index=True)
#	time.sleep(5)
# pdx.to_csv(fsszytyx,index=False,encoding='gbk')
