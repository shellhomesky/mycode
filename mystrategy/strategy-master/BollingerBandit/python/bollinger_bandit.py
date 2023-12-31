#!/usr/bin/env python
# encoding: utf-8

import sys
import logging
import logging.config
import configparser
import csv
import numpy as np
import datetime
import talib
import arrow
from gmsdk import *

EPS = 1e-6
INIT_CLOSE_PRICE = 0


class Bollinger_Bandit(StrategyBase):
    cls_config = None
    cls_user_name = None
    cls_password = None
    cls_mode = None
    cls_td_addr = None
    cls_strategy_id = None
    cls_subscribe_symbols = None
    cls_stock_pool = []

    cls_backtest_start = None
    cls_backtest_end = None
    cls_initial_cash = 1000000
    cls_transaction_ratio = 1
    cls_commission_ratio = 0.0
    cls_slippage_ratio = 0.0
    cls_price_type = 1
    cls_bench_symbol = None

    def __init__(self, *args, **kwargs):
        super(Bollinger_Bandit, self).__init__(*args, **kwargs)
        self.cur_date = None
        self.dict_close = {}
        self.dict_open_close_signal = {}
        self.dict_position_period = {}
        self.dict_entry_high_low = {}
        self.dict_last_factor = {}
        self.dict_open_cum_days = {}

    @classmethod
    def read_ini(cls, ini_name):
        """
        功能：读取策略配置文件
        """
        cls.cls_config = configparser.ConfigParser()
        cls.cls_config.read(ini_name)

    @classmethod
    def get_strategy_conf(cls):
        """
        功能：读取策略配置文件strategy段落的值
        """
        if cls.cls_config is None:
            return

        cls.cls_user_name = cls.cls_config.get('strategy', 'username')
        cls.cls_password = cls.cls_config.get('strategy', 'password')
        cls.cls_strategy_id = cls.cls_config.get('strategy', 'strategy_id')
        cls.cls_subscribe_symbols = cls.cls_config.get('strategy', 'subscribe_symbols')
        cls.cls_mode = cls.cls_config.getint('strategy', 'mode')
        cls.cls_td_addr = cls.cls_config.get('strategy', 'td_addr')
        if len(cls.cls_subscribe_symbols) <= 0:
            cls.get_subscribe_stock()
        else:
            subscribe_ls = cls.cls_subscribe_symbols.split(',')
            for data in subscribe_ls:
                index1 = data.find('.')
                index2 = data.find('.', index1 + 1, -1)
                cls.cls_stock_pool.append(data[:index2])

        return

    @classmethod
    def get_backtest_conf(cls):
        """
        功能：读取策略配置文件backtest段落的值
        """
        if cls.cls_config is None:
            return

        cls.cls_backtest_start = cls.cls_config.get('backtest', 'start_time')
        cls.cls_backtest_end = cls.cls_config.get('backtest', 'end_time')
        cls.cls_initial_cash = cls.cls_config.getfloat('backtest', 'initial_cash')
        cls.cls_transaction_ratio = cls.cls_config.getfloat('backtest', 'transaction_ratio')
        cls.cls_commission_ratio = cls.cls_config.getfloat('backtest', 'commission_ratio')
        cls.cls_slippage_ratio = cls.cls_config.getfloat('backtest', 'slippage_ratio')
        cls.cls_price_type = cls.cls_config.getint('backtest', 'price_type')
        cls.cls_bench_symbol = cls.cls_config.get('backtest', 'bench_symbol')

        return

    @classmethod
    def get_stock_pool(cls, csv_file):
        """
        功能：获取股票池中的代码
        """
        csvfile = open(csv_file, 'r')
        reader = csv.reader(csvfile)
        for line in reader:
            cls.cls_stock_pool.append(line[0])

        return

    @classmethod
    def get_subscribe_stock(cls):
        """
        功能：获取订阅代码
        """
        cls.get_stock_pool('stock_pool.csv')
        bar_type = cls.cls_config.getint('para', 'bar_type')
        if 86400 == bar_type:
            bar_type_str = '.bar.' + 'daily'
        else:
            bar_type_str = '.bar.' + '%d' % cls.cls_config.getint('para', 'bar_type')

        cls.cls_subscribe_symbols = ','.join(data + bar_type_str for data in cls.cls_stock_pool)
        return

    def utc_strtime(self, utc_time):
        """
        功能：utc转字符串时间
        """
        str_time = '%s' % arrow.get(utc_time).to('local')
        str_time.replace('T', ' ')
        str_time = str_time.replace('T', ' ')
        return str_time[:19]

    def get_para_conf(self):
        """
        功能：读取策略配置文件para(自定义参数)段落的值
        """
        if self.cls_config is None:
            return

        self.boll_bandit_period = self.cls_config.getint('para', 'boll_bandit_period')
        self.up_ratio = self.cls_config.getfloat('para', 'up_ratio')
        self.down_ratio = self.cls_config.getfloat('para', 'down_ratio')
        self.roc_period = self.cls_config.getint('para', 'roc_period')
        self.liq_days = self.cls_config.getint('para', 'liq_days')
        self.open_vol = self.cls_config.getint('para', 'open_vol')
        self.open_max_days = self.cls_config.getint('para', 'open_max_days')

        self.is_fixation_stop = self.cls_config.getint('para', 'is_fixation_stop')
        self.is_movement_stop = self.cls_config.getint('para', 'is_movement_stop')

        self.stop_fixation_profit = self.cls_config.getfloat('para', 'stop_fixation_profit')
        self.stop_fixation_loss = self.cls_config.getfloat('para', 'stop_fixation_loss')

        self.stop_movement_profit = self.cls_config.getfloat('para', 'stop_movement_profit')

        return

    def init_strategy(self):
        """
        功能：策略启动初始化操作
        """
        if self.cls_mode == gm.MD_MODE_PLAYBACK:
            self.cur_date = self.cls_backtest_start
            self.end_date = self.cls_backtest_end
        else:
            self.cur_date = datetime.date.today().strftime('%Y-%m-%d') + ' 08:00:00'
            self.end_date = datetime.date.today().strftime('%Y-%m-%d') + ' 16:00:00'

        self.dict_open_close_signal = {}
        self.dict_entry_high_low = {}
        self.get_last_factor()
        self.init_data()
        self.init_entry_high_low()
        return

    def init_data(self):
        """
        功能：获取订阅代码的初始化数据
        """
        for ticker in self.cls_stock_pool:
            # 初始化仓位操作信号字典
            self.dict_open_close_signal.setdefault(ticker, False)
            self.dict_position_period.setdefault(ticker, self.boll_bandit_period)

            daily_bars = self.get_last_n_dailybars(ticker, self.boll_bandit_period - 1, self.cur_date)
            if len(daily_bars) <= 0:
                continue

            end_daily_bars = self.get_last_n_dailybars(ticker, 1, self.end_date)
            if len(end_daily_bars) <= 0:
                continue

            if ticker not in self.dict_last_factor:
                continue

            end_adj_factor = self.dict_last_factor[ticker]
            cp_ls = [data.close * data.adj_factor / end_adj_factor for data in daily_bars]
            cp_ls.reverse()

            # 留出一个空位存储当天的一笔数据
            cp_ls.append(INIT_CLOSE_PRICE)
            close = np.asarray(cp_ls, dtype=np.float)

            # 存储历史的close
            self.dict_close.setdefault(ticker, close)

    def init_data_newday(self):
        """
        功能：新的一天初始化数据
        """
        # 新的一天，去掉第一笔数据,并留出一个空位存储当天的一笔数据
        for key in self.dict_close:
            if len(self.dict_close[key]) >= self.boll_bandit_period and abs(
                    self.dict_close[key][-1] - INIT_CLOSE_PRICE) > EPS:
                self.dict_close[key] = np.append(self.dict_close[key][1:], INIT_CLOSE_PRICE)
            elif len(self.dict_close[key]) < self.boll_bandit_period and abs(
                    self.dict_close[key][-1] - INIT_CLOSE_PRICE) > EPS:
                self.dict_close[key] = np.append(self.dict_close[key][:], INIT_CLOSE_PRICE)

        # 初始化仓位操作信号字典
        for key in self.dict_open_close_signal:
            self.dict_open_close_signal[key] = False

            # 持仓周期
        for key in self.dict_position_period:
            index = key.find('.')
            exchange = key[:index]
            sec_id = key[index:]
            pos = self.get_position(exchange, sec_id, OrderSide_Bid)

            if pos is not None and pos.volume > 0 and self.dict_position_period[key] > self.liq_days:
                self.dict_position_period[key] = self.dict_position_period[key] - 1
            else:
                self.dict_position_period[key] = self.boll_bandit_period

        # 开仓后到当前的交易日天数
        keys = list(self.dict_open_cum_days.keys())
        for key in keys:
            if self.dict_open_cum_days[key] >= self.open_max_days:
                del self.dict_open_cum_days[key]
            else:
                self.dict_open_cum_days[key] += 1

    def get_last_factor(self):
        """
        功能：获取指定日期最新的复权因子
        """
        for ticker in self.cls_stock_pool:
            daily_bars = self.get_last_n_dailybars(ticker, 1, self.end_date)
            if daily_bars is not None and len(daily_bars) > 0:
                self.dict_last_factor.setdefault(ticker, daily_bars[0].adj_factor)

    def init_entry_high_low(self):
        """
        功能：获取进场后的最高价和最低价,仿真或实盘交易启动时加载
        """
        pos_list = self.get_positions()
        high_list = []
        low_list = []
        for pos in pos_list:
            symbol = pos.exchange + '.' + pos.sec_id
            init_time = self.utc_strtime(pos.init_time)

            cur_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            daily_bars = self.get_dailybars(symbol, init_time, cur_time)

            high_list = [bar.high for bar in daily_bars]
            low_list = [bar.low for bar in daily_bars]

            if len(high_list) > 0:
                highest = np.max(high_list)
            else:
                highest = pos.vwap

            if len(low_list) > 0:
                lowest = np.min(low_list)
            else:
                lowest = pos.vwap

            self.dict_entry_high_low.setdefault(symbol, [highest, lowest])

    def on_bar(self, bar):
        if self.cls_mode == gm.MD_MODE_PLAYBACK:
            if bar.strtime[0:10] != self.cur_date[0:10]:
                self.cur_date = bar.strtime[0:10] + ' 08:00:00'
                # 新的交易日
                self.init_data_newday()

        symbol = bar.exchange + '.' + bar.sec_id

        self.movement_stop_profit_loss(bar)
        self.fixation_stop_profit_loss(bar)

        # 填充价格
        if symbol in self.dict_close:
            self.dict_close[symbol][-1] = bar.close

        pos = self.get_position(bar.exchange, bar.sec_id, OrderSide_Bid)

        if self.dict_open_close_signal[symbol] is False:
            # 代码持仓为空且当天未有对该代码开、平仓
            if symbol in self.dict_close and len(self.dict_close[symbol]) >= self.boll_bandit_period:
                average_close = np.average(self.dict_close[symbol])
                average_stddev = np.std(self.dict_close[symbol])
                upper_band = average_close + average_stddev * self.up_ratio
                down_band = average_close - average_stddev * self.down_ratio
                roc_calc = bar.close - self.dict_close[symbol][self.boll_bandit_period - self.roc_period]
                average_stop_loss = np.average(
                    self.dict_close[symbol][self.boll_bandit_period - self.dict_position_period[symbol]:])

                if pos is None and symbol not in self.dict_open_cum_days \
                        and ((roc_calc > EPS and bar.close > upper_band) \
                             or (average_close > upper_band and bar.close <= average_close)):

                    # 有开仓机会则设置已开仓的交易天数
                    self.dict_open_cum_days[symbol] = 0

                    cash = self.get_cash()
                    cur_open_vol = self.open_vol
                    if cash.available / bar.close > self.open_vol:
                        cur_open_vol = self.open_vol
                    else:
                        cur_open_vol = int(cash.available / bar.close / 100) * 100

                    if cur_open_vol == 0:
                        print('no available cash to buy, available cash: %.2f' % cash.available)
                    else:
                        # 当前价格大于roc周期的close，且上穿过了上轨
                        # 或者boll bandit周期的均价大于下轨且当前价格小于均价
                        self.open_long(bar.exchange, bar.sec_id, bar.close, cur_open_vol)
                        self.dict_open_close_signal[symbol] = True
                        logging.info('open long, symbol:%s, time:%s, price:%.2f' % (symbol, bar.strtime, bar.close))
                elif pos is not None:
                    if (roc_calc < EPS and bar.close < down_band) \
                            or (average_close < down_band and bar.close >= average_close):
                        # 当前价格低于roc周期的close，且低于了下轨
                        # 或者boll bandit周期的均价低于下轨且当前价格小于均价
                        vol = pos.volume - pos.volume_today
                        if vol > 0:
                            self.close_long(bar.exchange, bar.sec_id, bar.close, vol)
                            self.dict_open_close_signal[symbol] = True
                            logging.info('close long, symbol:%s, time:%s, price:%.2f, vwap: %.2f' % (symbol,
                                                                                                     bar.strtime,
                                                                                                     bar.close,
                                                                                                     pos.vwap))

                    elif bar.low < average_stop_loss:
                        # 止损
                        vol = pos.volume - pos.volume_today
                        if vol > 0:
                            stop_loss_price = average_stop_loss
                            if stop_loss_price > bar.open:
                                stop_loss_price = bar.open
                                self.close_long(bar.exchange, bar.sec_id, stop_loss_price, vol)
                                logging.info(
                                    'stop loss by lip days,close long, symbol:%s, time:%s, price:%.2f, vwap:%.2f' % (
                                        symbol,
                                        bar.strtime, stop_loss_price, pos.vwap))

    def on_order_filled(self, order):
        symbol = order.exchange + '.' + order.sec_id
        if order.position_effect == PositionEffect_CloseYesterday \
                and order.side == OrderSide_Bid:
            pos = self.get_position(order.exchange, order.sec_id, order.side)
            if pos is None and self.is_movement_stop == 1:
                self.dict_entry_high_low.pop(symbol)

    def fixation_stop_profit_loss(self, bar):
        """
        功能：固定止盈、止损,盈利或亏损超过了设置的比率则执行止盈、止损
        """
        if self.is_fixation_stop == 0:
            return

        symbol = bar.exchange + '.' + bar.sec_id
        pos = self.get_position(bar.exchange, bar.sec_id, OrderSide_Bid)
        if pos is not None:
            if pos.fpnl > 0 and pos.fpnl / pos.cost >= self.stop_fixation_profit:
                self.close_long(bar.exchange, bar.sec_id, 0, pos.volume - pos.volume_today)
                self.dict_open_close_signal[symbol] = True
                logging.info(
                    'fixnation stop profit: close long, symbol:%s, time:%s, price:%.2f, vwap: %s, volume:%s' % (symbol,
                                                                                                                bar.strtime,
                                                                                                                bar.close,
                                                                                                                pos.vwap,
                                                                                                                pos.volume))
            elif pos.fpnl < 0 and pos.fpnl / pos.cost <= -1 * self.stop_fixation_loss:
                self.close_long(bar.exchange, bar.sec_id, 0, pos.volume - pos.volume_today)
                self.dict_open_close_signal[symbol] = True
                logging.info(
                    'fixnation stop loss: close long, symbol:%s, time:%s, price:%.2f, vwap:%s, volume:%s' % (symbol,
                                                                                                             bar.strtime,
                                                                                                             bar.close,
                                                                                                             pos.vwap,
                                                                                                             pos.volume))

    def movement_stop_profit_loss(self, bar):
        """
        功能：移动止盈, 移动止盈止损按进场后的最高价乘以设置的比率与当前价格相比，
              并且盈利比率达到设定的盈亏比率时，执行止盈
        """
        if self.is_movement_stop == 0:
            return

        entry_high = None
        entry_low = None
        pos = self.get_position(bar.exchange, bar.sec_id, OrderSide_Bid)
        symbol = bar.exchange + '.' + bar.sec_id

        is_stop_profit = True

        if pos is not None and pos.volume > 0:
            if symbol in self.dict_entry_high_low:
                if self.dict_entry_high_low[symbol][0] < bar.close:
                    self.dict_entry_high_low[symbol][0] = bar.close
                    is_stop_profit = False
                if self.dict_entry_high_low[symbol][1] > bar.close:
                    self.dict_entry_high_low[symbol][1] = bar.close
                [entry_high, entry_low] = self.dict_entry_high_low[symbol]

            else:
                self.dict_entry_high_low.setdefault(symbol, [bar.close, bar.close])
                [entry_high, entry_low] = self.dict_entry_high_low[symbol]
                is_stop_profit = False

            if is_stop_profit:
                # 移动止盈
                if bar.close <= (
                        1 - self.stop_movement_profit) * entry_high and pos.fpnl / pos.cost >= self.stop_fixation_profit:
                    if pos.volume - pos.volume_today > 0:
                        self.close_long(bar.exchange, bar.sec_id, 0, pos.volume - pos.volume_today)
                        self.dict_open_close_signal[symbol] = True
                        logging.info(
                            'movement stop profit: close long, symbol:%s, time:%s, price:%.2f, vwap:%.2f, volume:%s' % (
                                symbol,
                                bar.strtime, bar.close, pos.vwap, pos.volume))

                        # 止损
            if pos.fpnl < 0 and pos.fpnl / pos.cost <= -1 * self.stop_fixation_loss:
                self.close_long(bar.exchange, bar.sec_id, 0, pos.volume - pos.volume_today)
                self.dict_open_close_signal[symbol] = True
                logging.info(
                    'movement stop loss: close long, symbol:%s, time:%s, price:%.2f, vwap:%.2f, volume:%s' % (symbol,
                                                                                                              bar.strtime,
                                                                                                              bar.close,
                                                                                                              pos.vwap,
                                                                                                              pos.volume))


if __name__ == '__main__':
    print(get_version())
    logging.config.fileConfig('bollinger_bandit.ini')
    Bollinger_Bandit.read_ini('bollinger_bandit.ini')
    Bollinger_Bandit.get_strategy_conf()

    bollinger_bandit = Bollinger_Bandit(username=Bollinger_Bandit.cls_user_name,
                                        password=Bollinger_Bandit.cls_password,
                                        strategy_id=Bollinger_Bandit.cls_strategy_id,
                                        subscribe_symbols=Bollinger_Bandit.cls_subscribe_symbols,
                                        mode=Bollinger_Bandit.cls_mode,
                                        td_addr=Bollinger_Bandit.cls_td_addr)

    if Bollinger_Bandit.cls_mode == gm.MD_MODE_PLAYBACK:
        Bollinger_Bandit.get_backtest_conf()
        ret = bollinger_bandit.backtest_config(start_time=Bollinger_Bandit.cls_backtest_start,
                                               end_time=Bollinger_Bandit.cls_backtest_end,
                                               initial_cash=Bollinger_Bandit.cls_initial_cash,
                                               transaction_ratio=Bollinger_Bandit.cls_transaction_ratio,
                                               commission_ratio=Bollinger_Bandit.cls_commission_ratio,
                                               slippage_ratio=Bollinger_Bandit.cls_slippage_ratio,
                                               price_type=Bollinger_Bandit.cls_price_type,
                                               bench_symbol=Bollinger_Bandit.cls_bench_symbol)

    bollinger_bandit.get_para_conf()
    bollinger_bandit.init_strategy()
    ret = bollinger_bandit.run()

print('run result %s' % ret)
