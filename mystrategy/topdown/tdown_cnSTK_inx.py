# -*- coding: utf-8 -*-
'''
TopQuant-简称TQ极宽智能量化回溯分析系统，培训课件-配套教学python课件程序

Top极宽量化(原zw量化)，Python量化第一品牌 
by Top极宽·量化开源团队 2017.10.1 首发

网站： www.TopQuant.vip      www.ziwang.com
QQ群: Top极宽量化1群，124134140
      Top极宽量化2群，650924099
  
'''

import os
import numpy as np
import pandas as pd
import tushare as ts

#  TopQuant
import zsys
import ztools_datadown as zddown

# ----------

# 指数数据文件保存目录
rss = zsys.rdatCNX
print('rs0:', rss)

# 指数索引文件
finx = 'inx\\inx_code.csv';
# 下载大盘指数文件，
zddown.down_stk_inx(rss, finx);

# 下载单一指数日线数据
# xcod='399003'
# zddown.down_stk_inx010(rss,xcod,'')
