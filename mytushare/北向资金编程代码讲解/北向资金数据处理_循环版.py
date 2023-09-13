"""
邢不行-北向资金编程代码
作者：邢不行
作者微信：xbx297
讲解视频：https://www.bilibili.com/video/BV1c64y147Qz
"""
import pandas as pd

pd.set_option('display.max_rows', 5000)  # 最多显示数据的行数
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行

# ===读取沪深300历史数据
hs300 = pd.read_csv('sh000300.csv', encoding='gbk', parse_dates=['candle_end_time'], index_col='candle_end_time')
# 筛选数据
hs300 = hs300[hs300.index >= pd.to_datetime('2014-11-17')]

# ===读取北向资金数据
hgt = pd.read_csv('hgt_hist_data.csv', skiprows=1, encoding='gbk', parse_dates=['日期'], index_col='日期')
sgt = pd.read_csv('sgt_hist_data.csv', skiprows=1, encoding='gbk', parse_dates=['日期'], index_col='日期')

# ===从沪深300历史数据、北向资金数据中选取需要的列
df = hs300[['close']]
df['当日成交净买额h'] = hgt['当日成交净买额']
df['当日成交净买额s'] = sgt['当日成交净买额']
df['净流入'] = df[['当日成交净买额h', '当日成交净买额s']].sum(axis=1)
df['净流入'] = df['净流入'] / 100
del df['当日成交净买额h'], df['当日成交净买额s']

# ===计算未来N天涨跌幅
for i in [1, 3, 5]:
    df['未来%d日涨跌幅' % i] = df['close'].shift(-i) / df['close'] - 1
df = df[df.index <= pd.to_datetime('2021-05-31')]

# ===计算最终表格
result = pd.DataFrame()  # 创建一个空的表格
for flow in [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]:
    # 筛选出净买入大于flow的情况
    t_df = df[df['净流入'] > flow]
    # 计算出现次数
    result.loc[flow, '出现次数'] = t_df.shape[0]
    # 计算未来N天数据
    for i in [1, 3, 5]:
        result.loc[flow, '未来%d日上涨次数' % i] = t_df[t_df['未来%d日涨跌幅' % i] > 0].shape[0]
        result.loc[flow, '未来%d日上涨平均涨幅' % i] = t_df['未来%d日涨跌幅' % i].mean()

for i in [1, 3, 5]:
    result['未来%d日上涨概率' % i] = result['未来%d日上涨次数' % i] / result['出现次数']

result.to_csv('result.csv', encoding='gbk')
