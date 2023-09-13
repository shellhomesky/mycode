# -*- coding: utf-8 -*-
'''
TopQuant-简称TQ极宽智能量化回溯分析系统，培训课件-配套教学python课件程序

Top极宽量化(原zw量化)，Python量化第一品牌 
by Top极宽·量化开源团队 2017.10.1 首发

网站： www.TopQuant.vip      www.ziwang.com
QQ群: Top极宽量化1群，124134140
      Top极宽量化2群，650924099
  
'''

import os, sys
import numpy as np
import pandas as pd
import tushare as ts

#  TopQuant
import zsys
import ztools_datadown as zddown

# ----------

# 下载股票日线数据文件，
print('rs0:', zsys.rdatCN)
rss = zsys.rdatCN
# qx=zsys.TQ_dat(zsys.rdatCN);#qx.prDat();
vlst = sys.argv
print('vn', vlst)

'''
vn=len(vlst)
print('vn',vn)

for vc in range(1,vn):
    xv=sys.argv[vc]
    print(vc,'#',xv)
'''

v1 = vlst[1]
d1 = int(v1)
nss = "%03d" % d1
finx = 'inx/inxdiv/stk_' + nss + '.csv'
print('finx,', finx)

# stk_005.csv
#
# 自动下载，追加数据
# 股票代码文件
# finx='inx\\stk_code.csv';
zddown.down_stk_all(rss, finx, 'D')

# 下载单一股票数据
# code='603315'
# zddown.down_stk_day010(code,rss,'D')
