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

# ---------------------------


# =====
# 下载tick数据


# -------设置参数
rs0 = zsys.rdatTick
# 股票代码文件
finx = 'inx/stk_code.csv';
stkPool = pd.read_csv(finx, encoding='gbk')
print(stkPool.tail())

# ==================


# 下载指定时间段，所以股票池的tick数据
xtim0, xtim9 = '2016-07-01', '2016-09-30'
zddown.down_tickLib8tim_mul(rs0, stkPool, xtim0, xtim9)
#


# -----------
# 下载指定日期，所以股票池的tick数据
# xtim='2016-07-01'
# zddown.down_tickLib8tim(rs0,stkPool,xtim)
