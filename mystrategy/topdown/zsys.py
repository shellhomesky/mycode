# -*- coding: utf-8 -*- 
'''
TopQuant-简称TQ极宽智能量化回溯分析系统，培训课件-配套教学python程序

Top极宽量化(原zw量化)，Python量化第一品牌 
by Top极宽·量化开源团队 2017.10.1 首发

网站： www.TopQuant.vip      www.ziwang.com
QQ群: Top极宽量化1群，124134140
      Top极宽量化2群，650924099
  
文件名:z_sys.py
默认缩写：import zsys as zsys
简介：Top极宽量化·常用量化系统参数模块
 

'''
#

import sys, os, re
import arrow, bs4, random
import numexpr as ne
#
import cpuinfo as cpu
import psutil as psu
from functools import wraps
#
import numpy as np
import pandas as pd
import tushare as ts
# import talib as ta

import matplotlib as mpl
import matplotlib.colors
from matplotlib import cm
from matplotlib import pyplot as plt

from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed

# import multiprocessing
#

#


#

# import zpd_talib as zta

# -------------------
# ----glbal var,const
__version__ = '2016.M10'

# ------sys.war
cpu_num_core = 8
cpu_num9 = 8
cpu_num = cpu_num9 - 1

tim0_sys = None
tim0_str = ''

fn_time_nloop = 5
fn_time_nloop5 = 500

# -----global.flag
web_get001txtFg = False  # @zt_web.web_get001txtFg

# -----bs4.findall
bs_get_ktag_kstr = ''

# --colors
# 10,prism,brg,dark2,hsv,jet
# 10,,hot,Vega10,Vega20
cors_brg = cm.brg(np.linspace(0, 1, 10))
cors_hot = cm.hot(np.linspace(0, 1, 10))
cors_hsv = cm.hsv(np.linspace(0, 1, 10))
cors_jet = cm.jet(np.linspace(0, 1, 10))
cors_prism = cm.prism(np.linspace(0, 1, 10))
cors_Dark2 = cm.Dark2(np.linspace(0, 1, 10))
cors_Vega10 = cm.tab10(np.linspace(0, 1, 10))
cors_Vega20 = cm.tab20(np.linspace(0, 1, 10))

# ------str.xxx
sgnSP4 = '    '
sgnSP8 = sgnSP4 + sgnSP4

# -----FN.xxx
logFN = ''

# --------------dir
#
rdat0 = 'D:/zdat/'
rdatCN = rdat0 + "cn/day/"
rdatCNX = rdat0 + "cn/xday/"
rdatInx = rdat0 + "inx/"
rdatMin0 = rdat0 + "min/"
rdatTick = rdat0 + "tick/"
rdatReal = rdat0 + "real/"
#
f_stkCodNamTbl = 'stk_code.csv'
f_stkInxNamTbl = 'inx_code.csv'
#
# ohlc=['open','high','low','close']
# ohlc_date=['date']+ohlc
#
# ---qxLib.xxxx
ohlcLst = ['open', 'high', 'low', 'close']
ohlcVLst = ohlcLst + ['volume']
ohlcALst = ohlcLst + ['amount']
#
ohlcDLst = ['date'] + ohlcLst
ohlcDVLst = ['date'] + ohlcLst + ['volume']
ohlcExtLst = ohlcDLst + ['volume', 'adj close']
#
xavg01Lst = ohlcLst + ['avg']
xavg10Lst = ['xavg', 'xavg_2', 'xavg_3', 'xavg_4', 'xavg_5', 'xavg_6', 'xavg_7', 'xavg_8', 'xavg_9']
avgXLst = ['open', 'high', 'close', 'low', 'volume', 'amount', 'avg']
# 
ma200Lst_var = [2, 3, 5, 10, 15, 20, 25, 30, 50, 100, 150, 200]
# ma200Lst=['ma_2', 'ma_3', 'ma_5', 'ma_10', 'ma_15', 'ma_20','ma_25', 'ma_30', 'ma_50', 'ma_100', 'ma_150', 'ma_200']
ma200Lst = ['ma_2', 'ma_3', 'ma_5', 'ma_10', 'ma_15', 'ma_20', 'ma_30', 'ma_50', 'ma_100', 'ma_150', 'ma_200']
#
ma030Lst_var = [2, 3, 5, 10, 15, 20, 25, 30]
ma030Lst = ['ma_2', 'ma_3', 'ma_5', 'ma_10', 'ma_15', 'ma_20', 'ma_25', 'ma_30']
xtimLst = ['xyear', 'xmonth', 'xday', 'xweekday']  # 'xtim',
priceLst = ['price', 'price_next', 'price_change']
#
#
# xtrdName=['date','ID','mode','code','dprice','num','kprice','sum','cash'];
# xtrdNil=['','','','',0,0,0,0,0];
# qxLibName=['date','stkVal','cash','dret','val','downLow','downHigh','downDay','downKMax'];
# qxLibNil=['',0,0,0,0,0,0,0,0];  #xBars:DF
#  
stkInxLib = {}  # 全局变量，大盘指数，内存股票数据库
stkInxLibCodX = {}  # 全局变量，大盘指数的交易代码等基本数据，内存股票数据库
stkInxNamTbl = None  # 全局变量，大盘指数的交易代码，名称对照表
#
stkLib = {}  # 全局变量，相关股票的交易数据，内存股票数据库
stkLibCodX = {}  # 全局变量，相关股票的交易代码等基本数据，内存股票数据库
stkCodNamTbl = None  # 全局变量，相关股票的交易代码，名称对照表

#
# rdatUS=_rdat0+"us\\"

# -----pre.init
# mpl.style.use('seaborn-whitegrid');
pd.set_option('display.width', 450)


# ----------class.def


class TQ_bar(object):
    ''' 
    设置TopQuant项目的各个全局参数
    尽量做到all in one

    '''

    def __init__(self):
        # ----rss.dir

        #
        # self.tim0,self.tim9,self.tim_now=None,None,None
        # self.tim0Str,self.tim9Str,self.timStr_now='','',''
        # self.tim0wrk=arrow.now()
        #
        # wrk:working
        self.wrkTim0, self.wrkTim9 = arrow.now(), None
        self.wrkTm0str, self.wrkTim9str = self.wrkTim0.format('YYYY-MM-DD HH:mm:ss '), ''
        # .format('YYYY-MM-DD HH:mm:ss ZZ')
        #
        self.wrkCod, self.wrkCodDat, self.wrkCodInfo = '', '', ''
        self.wrkInx, self.wrkInxDat, self.wrkInxInfo = '', '', ''
        # stk...，stk.Inx...
        self.stkPools = []
        self.stkInxPools = []
        #

        #
        # pre：dataPre,sta：strategy
        self.varPre, self.varSta = [], []

        '''
        self.tim0Str_gid='2010-01-01'
        self.tim0_gid=arrow.get(self.tim0Str_gid)
        
        #
        self.gid_tim0str,self.gid_tim9str='',''
        self.gid_nday,self.gid_nday_tim9=0,0
        #
        
        self.kgid=''
        self.kcid=''
        self.ktimStr=''
        #
        #----pool.1day
        self.poolInx=[]
        self.poolDay=pd.DataFrame(columns=poolSgn)
        #----pool.all
        self.poolTrd=pd.DataFrame(columns=poolSgn)
        self.poolRet=pd.DataFrame(columns=retSgn)
        self.poolTrdFN,self.poolRetFN='',''
        #
        self.bars=None
        self.gid10=None
        self.xdat10=None
        
        #
        #--backtest.var
        self.funPre,self.funSta=None,None
        self.preVars,self.staVars=[],[]
        #--backtest.ai.var
        #
        self.ai_mxFN0=''
        self.ai_mx_sgn_lst=[]
        self.ai_xlst=[]
        self.ai_ysgn=''
        self.ai_xdat,self.ai_xdat=None,None
        
        #
        #
        
        #
        #--ret.var
        self.ret_nday,self.ret_nWin=0,0
        self.ret_nplay,self.ret_nplayWin=0,0
        
        self.ret_msum=0
        
    '''

    # ----------


if __name__ == "__main__":
    dn = psu.cpu_count(logical=False)
    print('main', dn)

    # initSysVar(True)
