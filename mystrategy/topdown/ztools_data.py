# coding=utf-8
# -*- coding: utf-8 -*- 
'''
Top极宽量化(原zw量化)，Python量化第一品牌 
网站:www.TopQuant.vip   www.ziwang.com
QQ总群:124134140   千人大群 zwPython量化&大数据 
    
TopQuant.vip ToolBox 2016
Top极宽·量化开源工具箱 系列软件 
by Top极宽·量化开源团队 2016.12.25 首发
  
文件名:ztools_data.py
默认缩写：import ztools_data as zdat
简介：Top极宽常用数据工具函数集
'''

import os, sys, io, re
import random, arrow, bs4
import numpy as np
import numexpr as ne
import pandas as pd
import tushare as ts

import requests
#
import cpuinfo as cpu
import psutil as psu
import inspect
#
import matplotlib as mpl
import matplotlib.colors
from matplotlib import cm

#
import zsys
import ztools as zt
import ztools_str as zstr
import ztools_web as zweb

#

# -----------------------
'''

misc
#
df.xxx,pandas.xxx
    df.cov.
    df.get.
    df.cut.
#

'''


# -----------------------
# ----------data.misc


# -----Series
def ds4x(x, inx=None):
    ds = pd.Series(x)
    if len(inx) > 0: ds.index = inx

    return ds


# ----------df.misc
# df['ktype']=np.round(df['price_change'])

# df['ktype'][df.ktype<900]=900
# df['close'][df.close>1100]=1100

def df2type20(df, ksgn='ktype', n9=10):
    # dsk
    # df['price_change']=df['price_next']/df['price']*100
    #
    df[ksgn] = np.round(df[ksgn])
    d0, d9 = 100 - n9, 100 + n9
    # if df[ksgn]:
    df[ksgn][df[ksgn] < d0] = d0
    df[ksgn][df[ksgn] > d9] = d9
    df['ktype'] = df['ktype'].astype(int)
    #
    return df


def df_xshift(df, ksgn='avg', num9=10):
    xsgn = 'x' + ksgn
    alst = [xsgn]
    df[xsgn] = df[ksgn].shift(-1)
    for xc in range(2, num9):
        xss = xsgn + '_' + str(xc)
        df[xss] = df[ksgn].shift(-xc)
        alst.append(xss)
    #
    return df, alst


# ----------df2type
def df_type2float(df, xlst):
    for xsgn in xlst:
        df[xsgn] = df[xsgn].astype(float)


def df_type4mlst(df, nlst, flst):
    for xsgn in nlst:
        df[xsgn] = df[xsgn].astype(int)

    for xsgn in flst:
        df[xsgn] = df[xsgn].astype(float)


# ----------df.xxx,pandas.xxx

# ----------df.cov.xxx,pandas.xxx
def df_2ds8xlst(df, ds, xlst):
    for xss in xlst:
        ds[xss] = df[xss]
    #

    # df9.to_csv(ftg,index=False,encoding='gbk')
    return ds


# ----------df.get.xxx,pandas.xxx
def df_get8tim(df, ksgn, kpre, kn9, kpos):
    # @ zdr.dr_df_get8tim
    #
    xdf = pd.DataFrame(columns=['nam', 'dnum'])
    ds = pd.Series(['', 0], index=['nam', 'dnum'])
    for xc in range(1, kn9 + 1):
        xss, kss = '{0:02d}'.format(xc), '{0}{1:02d}'.format(kpre, xc)
        df2 = df[df[ksgn].str.find(kss) == kpos]
        ds['nam'], ds['dnum'] = xss, len(df2['gid'])
        xdf = xdf.append(ds.T, ignore_index=True)
        # print(xc,'#',xss,kss)
    #
    xdf.index = xdf['nam']
    return xdf


# ----------df.cut.xxx,pandas.xxx
def df_kcut8tim(df, ksgn, tim0str, tim9str):
    df2 = df[tim0str <= df[ksgn]]
    df3 = df2[df2[ksgn] <= tim9str]
    return df3


def df_kcut8yearlst(df, ksgn, ftg0, yearlst):
    for ystr in yearlst:
        tim0str, tim9str = ystr + '-01-01', ystr + '-12-31'
        df2 = df_kcut8tim(df, ksgn, tim0str, tim9str)
        ftg = ftg0 + ystr + '.dat';
        print(ftg)
        df2.to_csv(ftg, index=False, encoding='gb18030')


def df_kcut8myearlst(df, ksgn, tim0str, ftg0, yearlst):
    for ystr in yearlst:
        tim9str = ystr + '-12-31'
        df2 = df_kcut8tim(df, ksgn, tim0str, tim9str)
        ftg = ftg0 + ystr + '.dat';
        print(ftg)
        df2.to_csv(ftg, index=False, encoding='gb18030')


# ----------df.xed
def df_xappend(df, df0, ksgn, num_round=3, vlst=zsys.ohlcDVLst):
    if (len(df0) > 0):
        df2 = df0.append(df)
        df2 = df2.sort_values([ksgn], ascending=True);
        df2.drop_duplicates(subset=ksgn, keep='last', inplace=True);
        # xd2.index=pd.to_datetime(xd2.index);xd=xd2
        df = df2

    #
    df = df.sort_values([ksgn], ascending=False);
    df = np.round(df, num_round);
    df2 = df[vlst]
    #
    return df2


# ----------df.file
def df_rdcsv_tim0(fss, ksgn, tim0):
    xd0 = pd.read_csv(fss, index_col=False, encoding='utf-8-sig')
    # print('\nxd0\n',xd0.head())
    if (len(xd0) > 0):
        # xd0=xd0.sort_index(ascending=False);
        # xd0=xd0.sort_values(['date'],ascending=False);
        xd0 = xd0.sort_values([ksgn], ascending=True);
        # print('\nxd0\n',xd0)
        xc = xd0.index[-1];  ###
        _xt = xd0[ksgn][xc];  # xc=xd0.index[-1];###
        s2 = str(_xt);
        # print('\nxc,',xc,_xt,'s2,',s2)
        if s2 != 'nan':
            tim0 = s2.split(" ")[0]

            #
    return xd0, tim0
