# coding=utf-8
from __future__ import print_function, absolute_import

from gm.api import *
from MyTT import *

"""
本策略采用布林线进行均值回归交易。当价格触及布林线上轨的时候进行卖出，当触及下轨的时候，进行买入。
使用600004在 2009-09-17 13:00:00 到 2020-03-21 15:00:00 进行了回测。
注意： 
1：实盘中，如果在收盘的那一根bar或tick触发交易信号，需要自行处理，实盘可能不会成交。
"""


# 策略中必须有init方法
def init(context):
    # 设置布林线的三个参数
    context.maPeriod = 20  # 计算BOLL布林线中轨的参数
    context.stdPeriod = 20  # 计算BOLL 标准差的参数
    context.stdRange = 1  # 计算BOLL 上下轨和中轨距离的参数

    # 设置要进行回测的合约
    context.symbol = 'SZSE.300798'  # 订阅&交易标的, 此处订阅的是600004
    context.period = max(context.maPeriod, context.stdPeriod, context.stdRange) + 1  # 订阅数据滑窗长度

    # 订阅行情
    subscribe(symbols=context.symbol, frequency='900s', count=context.period)


def on_bar(context, bars):
    # 获取数据滑窗，只要在init里面有订阅，在这里就可以取的到，返回值是pandas.DataFrame
    data = context.data(symbol=context.symbol, frequency='900s', count=context.period, fields='close')

    # 计算boll的上下界
    boll = data['close'].rolling(context.maPeriod).mean()
    bollUpper = boll + context.stdRange * data['close'].rolling(context.stdPeriod).std()
    bollBottom = boll - context.stdRange * data['close'].rolling(context.stdPeriod).std()
    C = data.close.values
    ZZ1 = (C > REF(C, 1)) & (C > REF(C, 2))
    ZZ2 = (REF(ZZ1, 1)) & (C <= REF(C, 1)) & (C >= REF(C, 2))
    ZZ3 = (REF(ZZ2, 1)) & (C >= REF(C, 1)) & (C <= REF(C, 2))
    ZZ4 = (REF(ZZ3, 1)) & (C <= REF(C, 1)) & (C >= REF(C, 2))
    ZZ5 = (REF(ZZ4, 1)) & (C >= REF(C, 1)) & (C <= REF(C, 2))
    ZZ6 = (REF(ZZ5, 1)) & (C <= REF(C, 1)) & (C >= REF(C, 2))
    ZZ7 = (REF(ZZ6, 1)) & (C >= REF(C, 1)) & (C <= REF(C, 2))
    ZZ8 = (REF(ZZ7, 1)) & (C <= REF(C, 1)) & (C >= REF(C, 2))
    ZZ9 = (REF(ZZ8, 1)) & (C >= REF(C, 1)) & (C <= REF(C, 2))
    ZZ10 = (REF(ZZ9, 1)) & (C <= REF(C, 1)) & (C >= REF(C, 2))
    ZZ11 = (REF(ZZ10, 1)) & (C >= REF(C, 1)) & (C <= REF(C, 2))
    ZZ12 = (REF(ZZ11, 1)) & (C <= REF(C, 1)) & (C >= REF(C, 2))

    DD1 = (C < REF(C, 1)) & (C < REF(C, 2))
    DD2 = (REF(DD1, 1)) & (C >= REF(C, 1)) & (C <= REF(C, 2))
    DD3 = (REF(DD2, 1)) & (C <= REF(C, 1)) & (C >= REF(C, 2))
    DD4 = (REF(DD3, 1)) & (C >= REF(C, 1)) & (C <= REF(C, 2))
    DD5 = (REF(DD4, 1)) & (C <= REF(C, 1)) & (C >= REF(C, 2))
    DD6 = (REF(DD5, 1)) & (C >= REF(C, 1)) & (C <= REF(C, 2))
    DD7 = (REF(DD6, 1)) & (C <= REF(C, 1)) & (C >= REF(C, 2))
    DD8 = (REF(DD7, 1)) & (C >= REF(C, 1)) & (C <= REF(C, 2))
    DD9 = (REF(DD8, 1)) & (C <= REF(C, 1)) & (C >= REF(C, 2))
    DD10 = (REF(DD9, 1)) & (C >= REF(C, 1)) & (C <= REF(C, 2))
    DD11 = (REF(DD10, 1)) & (C <= REF(C, 1)) & (C >= REF(C, 2))
    DD12 = (REF(DD11, 1)) & (C >= REF(C, 1)) & (C <= REF(C, 2))
    ZD = REF((ZZ1 | ZZ2 | ZZ3 | ZZ4 | ZZ5 | ZZ6 | ZZ7 | ZZ8 | ZZ9 | ZZ10 | ZZ11 | ZZ12), 1) & DD1
    XD = (DD1 | DD2 | DD3 | DD4 | DD5 | DD6 | DD7 | DD8 | DD9 | DD10 | DD11 | DD12)
    SZ = (ZZ1 | ZZ2 | ZZ3 | ZZ4 | ZZ5 | ZZ6 | ZZ7 | ZZ8 | ZZ9 | ZZ10 | ZZ11 | ZZ12)
    ZZ = REF((DD1 | DD2 | DD3 | DD4 | DD5 | DD6 | DD7 | DD8 | DD9 | DD10 | DD11 | DD12), 1) & ZZ1
    # 获取现有持仓
    pos = context.account().position(symbol=context.symbol, side=PositionSide_Long)
    cash = context.account().cash
    # 交易逻辑与下单
    # 当有持仓，且股价穿过BOLL上界的时候卖出股票。
    if ZD[-1] == True and pos and (
            data.close.values[-1] > bollUpper.values[-1] * 0.95 or abs(data.close.values[-1] - boll.values[-1]) <
            data.close.values[-1] * 0.03):
        vol = pos.volume - pos.volume_today
        sell_vol = int(vol)
        if sell_vol:  # 有持仓就市价卖出股票。
            order_volume(symbol=context.symbol, volume=sell_vol, side=OrderSide_Sell,
                         order_type=OrderType_Market, position_effect=PositionEffect_Close)
            print('以市价单卖出一手')

    # 当没有持仓，且股价穿过BOLL下界的时候买入股票。
    elif ZZ[-1] == True and cash and data.close.values[-1] < bollBottom.values[-1] / 0.9:
        if cash.available:  # 没有持仓就买入一百股。
            value = cash.available
            buy_value = value
            order_value(symbol=context.symbol, value=buy_value, side=OrderSide_Buy,
                        order_type=OrderType_Market, position_effect=PositionEffect_Open)
            print('以市价单买入一手')


if __name__ == '__main__':
    '''
        strategy_id策略ID,由系统生成
        filename文件名,请与本文件名保持一致
        mode实时模式:MODE_LIVE回测模式:MODE_BACKTEST
        token绑定计算机的ID,可在系统设置-密钥管理中生成
        backtest_start_time回测开始时间
        backtest_end_time回测结束时间
        backtest_adjust股票复权方式不复权:ADJUST_NONE前复权:ADJUST_PREV后复权:ADJUST_POST
        backtest_initial_cash回测初始资金
        backtest_commission_ratio回测佣金比例
        backtest_slippage_ratio回测滑点比例
        '''

    run(strategy_id='653232f3-c9a6-11ee-8b19-e02be93acce0',
        filename='main.py',
        mode=MODE_BACKTEST,
        token='65d90ee4bf6935b71d53a3912b016556327b3ffb',
        backtest_start_time='2024-02-04 14:40:00',
        backtest_end_time='2024-02-14 15:00:00',
        backtest_adjust=ADJUST_NONE,
        backtest_initial_cash=500000,
        backtest_commission_ratio=0.00025,
        backtest_slippage_ratio=0.0001)
