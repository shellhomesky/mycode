# -*- coding: utf-8 -*- 
'''
TopQuant-简称TQ极宽智能量化回溯分析系统，培训课件-配套教学python程序

Top极宽量化(原zw量化)，Python量化第一品牌 
by Top极宽·量化开源团队 2017.10.1 首发

网站： www.TopQuant.vip      www.ziwang.com
QQ群: Top极宽量化1群，124134140
      Top极宽量化2群，650924099


  
文件名:zai_tf.py
默认缩写：import zai_tf as ztf
简介：Top极宽量化·TF神经网络、深度学习工具箱
 

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
import tflearn as tn
import tensorflow as tf
import tensorlayer as tl

#
import zsys
import ztools as zt
import zpd_talib as zta

# -------------------
#
import zsys
import ztools_tq as ztq
import zai_tools as zat


#
# -------------------

# ------misc

# ------model
# ---MLP
def mlp01(x, num_out):
    # v10=zt.nparr2tfvar(x)

    #
    with tf.variable_scope("MLP"):  # , reuse=False
        network = tl.layers.InputLayer(x, name='input_layer')
        #
        # network = tl.layers.DropoutLayer(network, keep=0.8, name='drop1')
        # network = tl.layers.DenseLayer(network, n_units=800,act = tf.nn.relu, name='relu1')
        #
        # network = tl.layers.DropoutLayer(network, keep=0.5, name='drop2')
        # network = tl.layers.DenseLayer(network, n_units=400,act = tf.nn.relu, name='relu2')
        #
        #
        # network = tl.layers.DropoutLayer(network, keep=0.5, name='drop9')
        network = tl.layers.DenseLayer(network, n_units=num_out, act=tf.identity, name='output_layer')

    #
    return network, network.outputs


def mlp03(x, num_out):
    v10 = zt.nparr2tfvar(x)

    #
    with tf.variable_scope("MLP"):  # , reuse=False
        network = tl.layers.InputLayer(x, name='input_layer')
        #
        network = tl.layers.DropoutLayer(network, keep=0.8, name='drop0')
        # network = tl.layers.DenseLayer(network, n_units=v10[0],act = tf.nn.relu, name='relu0')
        network = tl.layers.DenseLayer(network, n_units=100, act=tf.nn.relu, name='relu0')
        #
        # network = tl.layers.DropoutLayer(network, keep=0.8, name='drop1')
        # network = tl.layers.DenseLayer(network, n_units=v10[0],act = tf.nn.relu, name='relu1')
        #
        #
        network = tl.layers.DropoutLayer(network, keep=0.5, name='drop9')
        # network = tl.layers.DenseLayer(network, n_units=num_out,act = tf.identity,name='output_layer')
        network = tl.layers.DenseLayer(network, n_units=num_out, act=tf.identity, name='output_layer')

    #
    return network, network.outputs


def mlp05(x, num_out):
    v10 = zt.nparr2tfvar(x)

    #
    with tf.variable_scope("MLP"):  # , reuse=False
        network = tl.layers.InputLayer(x, name='input_layer')
        #
        network = tl.layers.DropoutLayer(network, keep=0.8, name='drop0')
        network = tl.layers.DenseLayer(network, n_units=v10[0], act=tf.nn.relu, name='relu0')
        #
        network = tl.layers.DropoutLayer(network, keep=0.5, name='drop1')
        network = tl.layers.DenseLayer(network, n_units=v10[1], act=tf.nn.relu, name='relu1')
        #
        #
        network = tl.layers.DropoutLayer(network, keep=0.5, name='drop9')
        network = tl.layers.DenseLayer(network, n_units=num_out, act=tf.identity, name='output_layer')

    #
    return network, network.outputs


def mlp09(x, num_out):
    v10 = zt.nparr2tfvar(x)

    #
    with tf.variable_scope("MLP"):  # , reuse=False
        network = tl.layers.InputLayer(x, name='input_layer')
        #
        network = tl.layers.DropoutLayer(network, keep=0.8, name='drop0')
        network = tl.layers.DenseLayer(network, n_units=v10[0], act=tf.nn.relu, name='relu0')
        #
        network = tl.layers.DropoutLayer(network, keep=0.5, name='drop1')
        network = tl.layers.DenseLayer(network, n_units=v10[1], act=tf.nn.relu, name='relu1')
        #
        network = tl.layers.DropoutLayer(network, keep=0.5, name='drop2')
        network = tl.layers.DenseLayer(network, n_units=v10[1], act=tf.nn.relu, name='relu2')
        #
        network = tl.layers.DropoutLayer(network, keep=0.5, name='drop3')
        network = tl.layers.DenseLayer(network, n_units=v10[1], act=tf.nn.relu, name='relu3')
        #
        network = tl.layers.DropoutLayer(network, keep=0.5, name='drop4')
        network = tl.layers.DenseLayer(network, n_units=v10[1], act=tf.nn.relu, name='relu4')
        #
        network = tl.layers.DropoutLayer(network, keep=0.5, name='drop5')
        network = tl.layers.DenseLayer(network, n_units=v10[1], act=tf.nn.relu, name='relu5')
        #
        #
        network = tl.layers.DropoutLayer(network, keep=0.5, name='drop9')
        network = tl.layers.DenseLayer(network, n_units=num_out, act=tf.identity, name='output_layer')

    #
    return network, network.outputs
