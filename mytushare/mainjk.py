# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import xcsc_tushare as xcts
import seaborn as sns
import matplotlib as mpl
import statsmodels.api as sm
import sqlite3 as sql

from pyecharts import options as opts
from pyecharts.charts import Radar
from os.path import exists
from tqdm import tqdm
from typing import List, Tuple, Dict
from pickle import dump
from gc import collect

sns.set()
# mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 指定默认字体：解决plot不能显示中文问题
mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题

token_xcts_prd = 'your token'
xcts.set_token(token_xcts_prd)
xpro = xcts.pro_api(env='')


def get_trading_dates(cur_conn: any, sdate: str, edate: str) -> pd.DataFrame:
    """取指定起止日期的交易日"""
    with cur_conn:
        cur_sql = 'select * from trade_date'
        cur = cur_conn.cursor()
        cur.execute(cur_sql)
        rs = cur.fetchall()

        print('读取交易日数据')
        col_name = [ii[0] for ii in cur.description]
        tdates = pd.DataFrame(rs, columns=col_name)


return tdates


def get_dates_week(tdates: any, is_end: bool = True, is_cut: bool = False) -> List:
    """
    从输入的日期序列中，按要求抽取指定频率的最后一天的日期出来，比如 'w' 是抽取每周最后一天
    参数说明：
    is_end: 取每个周期的第一天，还是最后一天
    is_cut: 如果时间序列不够整周期，是否要补充头尾日期。 is_cut = True 是补上
        比如取月频交易日的第一天的情况，如果时间序列的首个日期不是首个完整月的第一天，则补上
        或者取月频交易日最后一天的情况，如果时间序列的末个日期不是末个完整月的最后一天，则补上
    """
    if isinstance(tdates, List):
        tdates_df = pd.to_datetime([str(ii) for ii in tdates]).to_frame().reset_index(drop=True)
        tdates_df.columns = ['trade_date']
    elif isinstance(tdates, pd.Series):
        tdates_df = pd.to_datetime(tdates.astype(str)).to_frame()
        tdates_df.columns = ['trade_date']
    else:
        tdates_df = tdates['trade_date'].copy().to_frame()

        # 通过比较某一日及其前后日是周几，来判断该日是否周末
        # 只要发生后一天的 weekday 不大于前一天的，那前一天就一定是该周最后一天
        tdates_df['weekday'] = tdates_df['trade_date'].dt.weekday

        # 选出每周第一天，还是每周最后一天
        if is_end:
            weekend_index = tdates_df[tdates_df['weekday'] == 0].index - 1
        else:
            weekend_index = tdates_df[tdates_df['weekday'] == 0].index
        tdates2 = tdates_df.iloc[weekend_index]
    tdates_list = tdates2.iloc[:, 0].tolist()

    # 补充首末日期
    if not is_cut:
        if is_end:  # 取周期的末个日期，需要补上原日期序列的末位
            if tdates_list[-1] != tdates_df['trade_date'].iloc[-1]:
                tdates_list.append(tdates_df['trade_date'].iloc[-1])
        else:  # 取周期的首个日期，需要补上原日期序列的首位
            if tdates_list[0] != tdates_df['trade_date'].iloc[0]:
                tdates_list = [tdates_df['trade_date'].iloc[0]] + tdates_list

    return tdates_list


def calc_period_ret(raw_df: pd.DataFrame, cur_freq: str = 'w', is_end: bool = True,
                    is_cut: bool = False) -> pd.DataFrame:
    """
    将输入的 日收益率序列，计算指定频率的收益率
    不能直接用 .resample() 来改，因为它无法正确处理春节、五一、国庆等长假的情况
    """
    ddates = get_dates(raw_df.index.tolist(), cur_freq, is_end, is_cut)
    ddates_df = pd.DataFrame(ddates, index=ddates)
    raw_df2 = pd.merge(raw_df / 100 + 1, ddates_df, left_index=True, right_index=True, how='left')
    # if raw_df.index[0] != ddates[0]:
    #     raw_df2.iloc[0, -1] = raw_df.index[0]
    raw_df2 = raw_df2.fillna(method='bfill')
    raw_df2 = raw_df2.groupby(0).prod()

    return raw_df2 - 1


def calc_factors(raw_df: pd.DataFrame) -> Tuple[float, float]:
    """单个周期具体计算smb、hml因子值"""
    df_ = raw_df.copy()

    # 划分大小市值公司
    df_['sb'] = df_['float_a_shr'].apply(lambda x: 'b' if x >= df_['float_a_shr'].median() else 's')

    # 求账面市值比
    df_['bm'] = 1 / df_['pb_new']

    # 划分高、中、低账面市值比公司
    border_down, border_up = df_['bm'].quantile([0.3, 0.7])
    df_['hml'] = df_['bm'].apply(lambda x: 'h' if x >= border_up else 'm')
    df_['hml'] = df_.apply(lambda row: 'l' if row['bm'] <= border_down else row['hml'], axis=1)

    # 组合划分为6组
    df_sl = df_[(df_['sb'] == 's') & (df_['hml'] == 'l')]
    df_sm = df_[(df_['sb'] == 's') & (df_['hml'] == 'm')]
    df_sh = df_[(df_['sb'] == 's') & (df_['hml'] == 'h')]
    df_bl = df_[(df_['sb'] == 'b') & (df_['hml'] == 'l')]
    df_bm = df_[(df_['sb'] == 'b') & (df_['hml'] == 'm')]
    df_bh = df_[(df_['sb'] == 'b') & (df_['hml'] == 'h')]

    # 计算各组收益率
    ret_sl = (df_sl['pct_chg'] * df_sl['float_a_shr']).sum() / df_sl['float_a_shr'].sum()
    ret_sm = (df_sm['pct_chg'] * df_sm['float_a_shr']).sum() / df_sm['float_a_shr'].sum()
    ret_sh = (df_sh['pct_chg'] * df_sh['float_a_shr']).sum() / df_sh['float_a_shr'].sum()
    ret_bl = (df_bl['pct_chg'] * df_bl['float_a_shr']).sum() / df_bl['float_a_shr'].sum()
    ret_bm = (df_bm['pct_chg'] * df_bm['float_a_shr']).sum() / df_bm['float_a_shr'].sum()
    ret_bh = (df_bh['pct_chg'] * df_bh['float_a_shr']).sum() / df_bh['float_a_shr'].sum()

    # 计算smb, hml并返回
    cur_smb = (ret_sl + ret_sm + ret_sh - ret_bl - ret_bm - ret_bh) / 3
    cur_hml = (ret_sh + ret_bh - ret_sl - ret_bl) / 2
    return cur_smb, cur_hml


def get_factors_data(dpath: str, cur_conn: any, tdates: pd.Series, cur_freq: str = 'w') -> pd.DataFrame:
    """取相关数据，计算 smb、hml 因子"""

    # 按指定频率生成时间轴
    tdates_freq = get_dates_week(tdates=tdates, is_end=True, is_cut=False)

    # 计算指定时间轴上所有股票的收益率
    pct_chg_day = raw_data.pivot(index='trade_date', columns='ts_code', values='pct_chg').sort_index()
    pct_chg_freq = calc_period_ret(pct_chg_day, cur_freq, True, False)

    del pct_chg_day  # 变量用完之后值清除掉，释放内存
    collect()

    # 取指定频率日期的因子基础时点数据
    tdates_freq_str = [str(dt.year * 10000 + dt.month * 100 + dt.day) for dt in tdates_freq]
    raw_data_freq = raw_data[raw_data['trade_date'].isin(tdates_freq_str)].reset_index(drop=True)
    raw_data_freq.loc[:, 'trade_date'] = pd.to_datetime(raw_data_freq['trade_date'])

    del raw_data  # 变量用完之后值清除掉，释放内存
    collect()

    # 组合成包含指定频率的收益，和指定频率时点原始数据的 dataframe
    pct_chg_freq = pct_chg_freq.stack().to_frame()
    pct_chg_freq.columns = ['ret_w']
    pct_chg_freq = pct_chg_freq.reset_index()
    pct_chg_freq.columns = ['trade_date', 'ts_code', 'ret_w']

    raw_data_freq = pd.merge(raw_data_freq, pct_chg_freq, on=['trade_date', 'ts_code'], how='left')
    raw_data_freq = raw_data_freq.drop('pct_chg', axis=1)
    raw_data_freq.rename(columns={'ret_w': 'pct_chg'}, inplace=True)
    raw_data_freq['pct_chg'] -= 1

    res_ser = raw_data_freq.groupby('trade_date').apply(calc_factors)
    res_df = pd.DataFrame(list(res_ser), index=res.index, columns=['smb', 'hml'])
    res_df.to_pickle(dpath + f'\\three_factors_{cur_freq}_df.pkl')


return res_df


def get_ret_data(dpath: str, fdata: pd.DataFrame, stks_dict: Dict,
                 cur_idx: Dict, sdate: str, edate: str) -> pd.DataFrame:
    print('计算资产回报数据')
    # 取指定股票和基准指数的数据
    stks_data_list = []
    for kk, vv in stks_dict.items():
        cur_data = xpro.daily(ts_code=kk, start_date=sdate, end_date=edate)
        cur_data.index = pd.to_datetime(cur_data.trade_date)
        stks_data_list.append(cur_data.pct_chg / 100)

    # 补上指数的
    cur_data = xpro.index_daily(ts_code=cur_idx['code'], start_date=sdate, end_date=edate)
    cur_data.index = pd.to_datetime(cur_data.trade_date)
    stks_data_list.append(cur_data.pct_chg / 100)

    stock_df = pd.concat(stks_data_list, axis=1)
    stock_df.columns = list(stks_dict.values()) + [cur_idx['name']]
    stock_df = stock_df.sort_index(ascending=True)

    # 折算出指定频率的收益率
    stock_freq_ret_df = calc_period_ret(stock_df * 100, cur_freq, True, False)

    # 算出超额收益率
    rf = 1.032 ** (5 / 360) - 1
    stock_freq_ret_df -= rf

    stocks_ret = pd.merge(stock_freq_ret_df, fdata, left_index=True, right_index=True, how='inner')
    stocks_ret = stocks_ret.fillna(0)
    stocks_ret.to_pickle(dpath + r'\stocks_ret.pkl')


return stocks_ret


def plot_factors_radar(plt_data: pd.DataFrame, dpath: str) -> None:
    c_schema = [
        {"name": "alpha", "max": 0.01, "min": -0.01},
        {"name": "市场因子", "max": 2, "min": 0},
        {"name": "市值因子", "max": 1, "min": -1},
        {"name": "价值因子", "max": 1, "min": -1}]  # 以字典形式设置雷达图指标名称和范围

    cur_data = plt_data.values.T.tolist()  # 以字典形式设置雷达图指标名称和范围

    radar = Radar()  # 初始化对象,单独调用
    radar.add(series_name=plt_data.columns[0],
              data=[cur_data[0]],
              color="#f9713c",
              areastyle_opts=opts.AreaStyleOpts(opacity=0.1),
              linestyle_opts=opts.LineStyleOpts(width=3))  # 添加第一类数据并绘图
    radar.add(series_name=plt_data.columns[1],
              data=[cur_data[1]],
              color="#4169E1",
              areastyle_opts=opts.AreaStyleOpts(opacity=0.1),
              linestyle_opts=opts.LineStyleOpts(width=3))  # 添加第二类数据并绘图
    radar.add(series_name=plt_data.columns[2],
              data=[cur_data[2]],
              color="#00BFFF",
              areastyle_opts=opts.AreaStyleOpts(opacity=0.1),
              linestyle_opts=opts.LineStyleOpts(width=3))  # 添加第三类数据并绘图
    radar.add(series_name=plt_data.columns[3],
              data=[cur_data[3]],
              color="#3CB371",
              areastyle_opts=opts.AreaStyleOpts(opacity=0.1),
              linestyle_opts=opts.LineStyleOpts(width=3))  # 添加第四类数据并绘图
    radar.add_schema(schema=c_schema, shape="polygon")  # schema设置
    radar.set_series_opts(label_opts=opts.LabelOpts(is_show=False))  # 是否打标签
    radar.set_global_opts(title_opts=opts.TitleOpts(title="因子解释度"))  # 标题

    radar.render(dpath + r'\radar.html')  # 渲染成html格式


if __name__ == '__main__':
    # 参数
    start_date = '20170101'
    end_date = '20210118'
    data_path = r'e:\fama_french3\data'
    index_names = {
        'name': '中证800',
        'code': '000906.SH'
    }
    stock_names = {
        '000002.SZ': '万科A',
        '601318.SH': '中国平安',
        '600519.SH': '贵州茅台',
        '002415.SZ': '万华化学',
        '002230.SZ': '科大讯飞'
    }
    conn = sql.connect(data_path + r'\xctushare.db')
    freq = 'w'

    # 取交易日
    trading_dates = get_trading_dates(conn, start_date, end_date)

    # 取指数成分股的因子数据与收益率数据
    factors_data = get_factors_data(data_path, conn, trading_dates['trade_date'], freq)

    # 取指定资产的原始数据，与指数成分股分组收益率的时间周期对齐后合并
    ret_data = get_ret_data(data_path, factors_data, freq, stock_names, index_names, start_date, end_date)

    # 观察数据间的相关性热力图
    # sns.heatmap(ret_period.iloc[:, :5].corr(), cmap='bwr')

    # # 收益率时序图
    # plt.figure(figsize=(10, 5))
    # for col in ret_period.columns:
    #     plt.plot(ret_period[col], label=col)
    # plt.title('日收益率时序图', fontsize=20)
    # plt.legend()
    #
    # # 累计收益率时序图
    # plt.figure(figsize=(10, 5))
    # for col in ret_period.columns:
    #     plt.plot((ret_period[col]).cumprod()-1, label=col)
    # plt.title('累计收益率时序图', fontsize=20)
    # plt.legend()

    # 回归计算三因子载荷
    # res_model = {}
    ols_params = []
    for stock in stock_names.values():
        xx = sm.add_constant(ret_data[['中证800', 'smb', 'hml']].values)
        yy = ret_data[stock].values
        res = np.linalg.inv(xx.T.dot(xx)).dot(xx.T).dot(yy)
        ols_params.append(res)

        # result = sm.OLS(ret_data[stock], sm.add_constant(ret_data[['中证800', 'smb', 'hml']].values)).fit()
        # res_model[stock] = result
        # ols_params.append(result.params)
        # print(stock + '\n')
        # print(result.summary())
        # print('\n\n')

    # ols_params_df = pd.concat(ols_params, axis=1)
    ols_params_df = pd.DataFrame(ols_params).T
    ols_params_df.columns = stock_names.values()

    # 将以上股票的三因子载荷集中画在雷达图上，生成 .html 文档，需要手动打开
    plot_factors_radar(ols_params_df, data_path)
