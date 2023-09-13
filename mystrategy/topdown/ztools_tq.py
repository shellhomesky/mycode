# -*- coding: utf-8 -*- 
'''
TopQuant-简称TQ极宽智能量化回溯分析系统，培训课件-配套教学python程序

Top极宽量化(原zw量化)，Python量化第一品牌 
by Top极宽·量化开源团队 2017.10.1 首发

网站： www.TopQuant.vip      www.ziwang.com
QQ群: Top极宽量化1群，124134140
      Top极宽量化2群，650924099


  
文件名:ztools_tq.py
默认缩写：import ztools_tq as ztq
简介：Top极宽量化·常用量化工具函数集
 

'''
#

import sys, os, re
import arrow, bs4, random
import numexpr as ne
import numpy as np
import pandas as pd
import tushare as ts
# import talib as ta

import pypinyin
#

import matplotlib as mpl
from matplotlib import pyplot as plt

from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
# import multiprocessing
#
import sklearn
from sklearn import metrics
#
import tflearn
import tensorflow as tf

#
import zsys
import ztools as zt
import ztools_str as zstr
import ztools_data as zdat

# -------------------
#
import zpd_talib as zta


#
# -------------------
def prVars(qx):
    print('\nzsys.xxx')
    print('    rdat0,', zsys.rdat0)
    print('    rdatCN,', zsys.rdatCN)
    print('    rdatCNX,', zsys.rdatCNX)
    print('    rdatInx,', zsys.rdatInx)
    print('    rdatMin0,', zsys.rdatMin0)
    print('    rdatTick,', zsys.rdatTick)

    #
    print('\nobj:qx')
    zt.xobjPr(qx)


# -------init.TQ.xxx

def tq_init(xcods, xinxs=['000001']):
    qx = zsys.TQ_bar()
    qx.CodPool = xcods
    # qx.codID,qx.codFN=xcod,zsys.rdatCN+xcod+'.csv'
    #
    #
    #
    print('tq_init code...')
    # f_stkCodNamTbl='stk_code.csv'
    fss = zsys.rdatInx + zsys.f_stkCodNamTbl  # ;print('f,',fss)
    zsys.stkCodNamTbl = pd.read_csv(fss, dtype={'code': str}, encoding='GBK')
    #
    for xcod in xcods:
        print('xcod:', xcod)
        xd = zsys.stkCodNamTbl[zsys.stkCodNamTbl['code'] == xcod]
        css = xd['name']
        ess = pypinyin.slug(css, style=pypinyin.FIRST_LETTER, separator='')
        xd['enam'] = ess
        zsys.stkLibCodX[xcod] = xd
        #
        fcod = zsys.rdatCN + xcod + '.csv'
        df = pd.read_csv(fcod, index_col=0)
        zsys.stkLib[xcod] = df.sort_index()
    #
    xcod = xcods[0]
    qx.wrkCod = xcod
    qx.wrkCodDat = zsys.stkLib[xcod]
    qx.wrkCodInfo = zsys.stkLibCodX[xcod]
    #
    print('tq_init inx...')
    # f_stkInxNamTbl='inx_code.csv'
    fss = zsys.rdatInx + zsys.f_stkInxNamTbl  # ;print('f,',fss)
    zsys.stkInxNamTbl = pd.read_csv(fss, dtype={'code': str}, encoding='GBK')

    for xinx in xinxs:
        print('xinx:', xinx)
        xd = zsys.stkInxNamTbl[zsys.stkInxNamTbl['code'] == xinx]
        css = xd['name']
        ess = pypinyin.slug(css, style=pypinyin.FIRST_LETTER, separator='')
        xd['enam'] = ess
        zsys.stkInxLibCodX[xinx] = xd
        #
        fcod = zsys.rdatCNX + xinx + '.csv'
        df = pd.read_csv(fcod, index_col=0)
        zsys.stkInxLib[xinx] = df.sort_index()
    #
    xinx = xinxs[0]
    qx.wrkInx = xinx
    qx.wrkInxDat = zsys.stkInxLib[xinx]
    qx.wrkInxInfo = zsys.stkInxLibCodX[xinx]
    #
    #
    # df=pd.read_csv(fdat)
    # df=df.sort_values('date')

    #
    return qx


# ---------------------------tick
def ai_acc_xed2x(y_true, y_pred, ky0=5, fgDebug=False):
    # 1
    df, dacc = pd.DataFrame(), -1
    # print('n,',len(y_true),len(y_pred))
    if (len(y_true) == 0) or (len(y_pred) == 0):
        # print('n,',len(y_true),len(y_pred))
        return dacc, df

    #
    y_num = len(y_true)
    # df['y_true'],df['y_pred']=zdat.ds4x(y_true,df.index),zdat.ds4x(y_pred,df.index)
    df['y_true'], df['y_pred'] = pd.Series(y_true), pd.Series(y_pred)
    df['y_diff'] = np.abs(df.y_true - df.y_pred)
    # 2
    df['y_true2'] = df['y_true']
    df.loc[df['y_true'] == 0, 'y_true2'] = 0.00001
    df['y_kdif'] = df.y_diff / df.y_true2 * 100
    # 3
    dfk = df[df.y_kdif < ky0]
    knum = len(dfk['y_pred'])
    dacc = knum / y_num * 100
    #
    # 5
    dacc = round(dacc, 3)
    return dacc, df


def ai_acc_xed2ext(y_true, y_pred, ky0=5, fgDebug=False):
    # 1
    df, dacc = pd.DataFrame(), -1
    if (len(y_true) == 0) or (len(y_pred) == 0):
        # print('n,',len(y_true),len(y_pred))
        return dacc, df

    #
    y_num = len(y_true)
    # df['y_true'],df['y_pred']=zdat.ds4x(y_true,df.index),zdat.ds4x(y_pred,df.index)
    df['y_true'], df['y_pred'] = y_true, y_pred
    df['y_diff'] = np.abs(df.y_true - df.y_pred)
    # 2
    df['y_true2'] = df['y_true']
    df.loc[df['y_true'] == 0, 'y_true2'] = 0.00001
    df['y_kdif'] = df.y_diff / df.y_true2 * 100
    # 3
    dfk = df[df.y_kdif < ky0]
    knum = len(dfk['y_pred'])
    dacc = knum / y_num * 100
    #
    # 4
    dmae = metrics.mean_absolute_error(y_true, y_pred)
    dmse = metrics.mean_squared_error(y_true, y_pred)
    drmse = np.sqrt(metrics.mean_squared_error(y_true, y_pred))
    dr2sc = metrics.r2_score(y_true, y_pred)
    #    
    # 5
    if fgDebug:
        # print('\nai_acc_xed')
        # print(df.head())
        # y_test,y_pred=df['y_test'],df['y_pred']
        print('n_df9,{0},n_dfk,{1}'.format(y_num, knum))
        print(
            'acc: {0:.2f}%;  MSE:{1:.2f}, MAE:{2:.2f},  RMSE:{3:.2f}, r2score:{4:.2f}, @ky0:{5:.2f}'.format(dacc, dmse,
                                                                                                            dmae, drmse,
                                                                                                            dr2sc, ky0))

    #
    # 6
    dacc = round(dacc, 3)
    return dacc, df, [dmae, dmse, drmse, dr2sc]


# ---------------------------stk

def stk2data_pre8FN(fss):
    if not os.path.exists(fss):
        return None
    #    
    df = pd.read_csv(fss, index_col=0)
    df['avg'] = df[zsys.ohlcLst].mean(axis=1)
    #
    df['avg'] = df[zsys.ohlcLst].mean(axis=1)
    df, avg_lst = zdat.df_xshift(df, ksgn='avg', num9=10)
    # print('avg_lst,',avg_lst)
    #
    mv_lst = [2, 3, 5, 10, 15, 20, 30, 50, 100, 150, 200]
    # ma_lst=[2,3,4,5,6,7,8,9,10,15,20,30,40,50,60,80,100,120,150,180,200,250,300]
    df = zta.mul_talib(zta.MA, df, ksgn='avg', vlst=mv_lst)
    ma_lst = zstr.sgn_4lst('ma', mv_lst)
    #
    df['xtim'] = df.index
    df['xyear'] = df['xtim'].apply(zstr.str_2xtim, ksgn='y')
    df['xmonth'] = df['xtim'].apply(zstr.str_2xtim, ksgn='m')
    df['xday'] = df['xtim'].apply(zstr.str_2xtim, ksgn='d')
    df['xweekday'] = df['xtim'].apply(zstr.str_2xtim, ksgn='w')
    tim_lst = ['xyear', 'xmonth', 'xday', 'xweekday']
    #
    df['price'] = df['avg']
    df['price_next'] = df[avg_lst].max(axis=1)
    # 涨跌幅,zsys.k_price_change=1000
    df['price_change'] = df['price_next'] / df['price'] * 100
    # df['ktype']=df['price_change'].apply(zt.iff2type,d0=100)
    # def dat2type(d,k9=2000,k0=0):
    # fd>120
    #
    df = df.dropna()
    # df['ktype']=round(df['price_change']).astype(int)
    # df['ktype']=df['kprice'].apply(zt.iff2type,d0=100)
    # df['ktype']=df['price_change'].apply(zt.iff3type,v0=95,v9=105,v3=3,v2=2,v1=1)
    #
    df = df.round(4)
    return df


def stk2data_pre8Flst(finx, rss):
    flst = pd.read_csv(finx, index_col=False, dtype='str', encoding='gbk')
    df9 = pd.DataFrame()
    xc = 0
    for xcod in flst['code']:
        # print(xcod)
        xc += 1
        fss = rss + xcod + '.csv';
        print(xc, '#', fss)
        df = stk2data_pre8FN(fss)
        df9 = df9.append(df)
    #
    return df9


# ---------------------------tick

def tick2x(df, ktim='1min'):
    '''
    ktim，是时间频率参数，请参看pandas的resample重新采样函数
        常见时间频率符号： 
            A， year 
            M， month 
            W， week 
            D， day 
            H， hour 
            T， minute 
            S，second
    '''
    #
    df['time'] = pd.to_datetime(df['time'])
    df = df.set_index('time')
    df = df.sort_index()
    #
    dfk = df['price'].resample(ktim).ohlc();
    dfk = dfk.dropna();
    vol2 = df['volume'].resample(ktim).sum();
    vol2 = vol2.dropna();
    df_vol2 = pd.DataFrame(vol2, columns=['volume'])
    amt2 = df['amount'].resample(ktim).sum();
    amt2 = amt2.dropna();
    df_amt2 = pd.DataFrame(amt2, columns=['amount'])
    #
    df2 = dfk.merge(df_vol2, left_index=True, right_index=True)
    df9 = df2.merge(df_amt2, left_index=True, right_index=True);
    #
    xtims = df9.index.format('%Y-%m-%d %H:%M:%S')
    del (xtims[0])
    df9['xtim'] = xtims  # df9.index.__str__();#  [str(df9.index)]
    #             
    return df9
