# -*- coding: utf-8 -*-
'''
TopQuant-简称TQ极宽智能量化回溯分析系统，培训课件-配套教学python课件程序

Top极宽量化(原zw量化)，Python量化第一品牌 
by Top极宽·量化开源团队 2017.10.1 首发

网站： www.TopQuant.vip      www.ziwang.com
QQ群: Top极宽量化1群，124134140
      Top极宽量化2群，650924099
  
'''

import sys, os
import tushare as ts
import pandas as pd
#  TopQuant 
from matplotlib import cm
import zsys
import ztools_datadown as zddown

# zddown.down_stk_base()
# zddown.downFinancial()
for s in ['2015', '2016', '2017']:
    dPeriod = s + '1231'
    zddown.downFinancialStatement(dPeriod)
