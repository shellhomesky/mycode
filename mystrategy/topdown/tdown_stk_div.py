# -*- coding: utf-8 -*-


import os, sys, math, arrow
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#

#
import zsys
import ztools as zt
import ztools_str as zstr
import ztools_data as zdat
import ztools_draw as zdr
import ztools_tq as ztq
import zpd_talib as zta

#

# -------------------

# -------------------


# 1,set.env
print('\n#1,set Env')
pd.set_option('display.width', 450)
# pd.set_option('display.float_format', zt.xfloat3)
# tf.reset_default_graph()


# 1
finx = 'inx/stk_code.csv';
df = pd.read_csv(finx, index_col=False, dtype=str, encoding='gbk')
df = df.sort_values(['code'], ascending=True);
fss = 'tmp/stk_code.csv'
df.to_csv(fss, index=False, encoding='gbk')
print(df.tail())
xn9 = len(df.index)
xn = (xn9 // 200) + 1
for xc in range(xn):
    x1 = xc * 200
    x9 = x1 + 200
    df2 = df.iloc[x1:x9]
    nss = "%03d" % xc
    fss = 'tmp/stk_' + nss + '.csv'
    df2.to_csv(fss, index=False, encoding='gbk')

print('\nxn9,', xn9, xn)
x1, x9 = 0, 20
df2 = df.iloc[x1:x9]
print(df2)
