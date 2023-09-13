# -*- coding: utf-8 -*- 
'''
TopQuant-简称TQ极宽智能量化回溯分析系统，培训课件-配套教学python程序

Top极宽量化(原zw量化)，Python量化第一品牌 
by Top极宽·量化开源团队 2017.10.1 首发

网站： www.TopQuant.vip      www.ziwang.com
QQ群: Top极宽量化1群，124134140
      Top极宽量化2群，650924099


  
文件名:zai_ks.py
默认缩写：import zai_keras as zks
简介：Top极宽量化·keras神经网络、深度学习工具箱
 

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
# import sklearn
# from sklearn import metrics

import keras as ks
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.optimizers import RMSprop, SGD
from keras.utils import plot_model
from keras import backend as kback
# from keras import layers
#
import tflearn as tn
import tensorflow as tf
import tensorlayer as tl

#
import zsys
import ztools as zt

# -------------------
#
import ztools_tq as ztq
import zpd_talib as zta
import zai_tools as zat


#
# -------------------

# ------misc

# ------model

# -------------MLP
def mlp(num_in, num_out, num_layer, vlst=[256, 128, 64, 32], kinit='uniform'):
    with tf.variable_scope("MLP"):  # , reuse=False
        # 选择序贯模型（Sequential）
        model = Sequential()
        #
        # 构建网络层 relu tanh
        # model.add(Dense(512, activation='relu', input_shape=(num_in,)))
        # kernel_initializer='uniform'
        model.add(Dense(vlst[0], activation='tanh', kernel_initializer=kinit, input_shape=(num_in,)))
        model.add(Dropout(0.5))  # 采用50%的dropout
        #
        for xc in range(1, num_layer):
            model.add(Dense(vlst[xc], activation='tanh', kernel_initializer=kinit))
            model.add(Dropout(0.5))  # 采用50%的dropout

        #
        model.add(Dense(num_out, activation='softmax'))  # 输出结果是10个类别，所以维度是10
        #
    #
    return model
# ---------------tst

# ---------------????
