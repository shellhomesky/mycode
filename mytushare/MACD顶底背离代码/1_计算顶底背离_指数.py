"""

作者：邢不行
微信号：xbx297
B站:量化投资邢不行啊
发送时间：2021/09/07
原始策略说明：用python找出12万次顶底背离，胜率究竟有多少？附代码【量化投资邢不行】
https://www.bilibili.com/video/BV1M64y1Y7Pt?from=search&seid=16855777977532986397&spm_id_from=333.337.0.0
完整数据下载地址：www.quantclass.cn/data/stock/stock-main-index-data，添加数据管家-耶伦微信获取。

"""

import pandas as pd

pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
pd.set_option('display.max_rows', 5000)  # 最多显示数据的行数


# 封装MACD计算函数，方便后续调用
def cal_macd(df_ma, short=12, long=26, dea=9, close='收盘价_复权'):
    df_ma['EMA_short'] = df_ma[close].ewm(span=short, adjust=False).mean()
    df_ma['EMA_long'] = df_ma[close].ewm(span=long, adjust=False).mean()
    df_ma['DIF'] = df_ma['EMA_short'] - df_ma['EMA_long']
    df_ma['DEA'] = df_ma['DIF'].ewm(span=dea, adjust=False).mean()
    df_ma['MACD'] = (df_ma['DIF'] - df_ma['DEA']) * 2
    del df_ma['EMA_short'], df_ma['EMA_long']
    return df_ma


# 将高点时间段定为30日，可自己修改参数把玩
days = 30  # 计算均线和斜率的时候需要的
# 后续计算N日后涨跌幅所需参数
day_list = [1, 5, 10, 20]
# 指数代码，可变更后把玩。
# 如需最新的常用指数数据，请至www.quantclass.cn/data/stock/stock-main-index-data，添加数据管家-耶伦微信获取。
symbol = '.\\MACD顶底背离代码\\sh000300'
# 测试时间段，可根据数据时间更改
start_time = '20070101'
end_time = '20210331'

# 读入数据
df = pd.read_csv('%s.csv' % symbol, encoding='gbk', parse_dates=['candle_end_time'])

# 0计算MACD指标
df = cal_macd(df, close='close')

# 计算开盘和收盘的最高价
df['max'] = df[['open', 'close']].max(axis=1)
# 计算开盘和收盘的最低价
df['min'] = df[['open', 'close']].min(axis=1)

# 峰值条件：max大于前后两天，且max大于最近30天的所有max
df.loc[(df['max'] > df['max'].shift(1)) & (df['max'] > df['max'].shift(-1)) & (
        df['max'] == df['max'].rolling(days).max()), 'price_new_high'] = 1
# 谷值条件：min小于前后两天，且小于最近30天所有的min
df.loc[(df['min'] < df['min'].shift(1)) & (df['min'] < df['min'].shift(-1)) & (
        df['min'] == df['min'].rolling(days).min()), 'price_new_low'] = 1

# 计算DIF高低点
df.loc[df['DIF'] == df['DIF'].rolling(days).max(), 'DIF_new_high'] = 1
df.loc[df['DIF'] == df['DIF'].rolling(days).min(), 'DIF_new_low'] = 1

# 记录前后的高低点价格
df.loc[df['price_new_high'] == 1, 'last_peak_price'] = df['close']
df.loc[df['price_new_high'] == 1, 'last_peak_dif'] = df['DIF']

df.loc[df['price_new_low'] == 1, 'last_valley_price'] = df['close']
df.loc[df['price_new_low'] == 1, 'last_valley_dif'] = df['DIF']

# 2.3、填充空值 & 取前值&高点低点价、dif下移一天
df['last_peak_price'].fillna(method='ffill', inplace=True)
df['last_peak_dif'].fillna(method='ffill', inplace=True)
df['last_peak_price'] = df['last_peak_price'].shift(1)
df['last_peak_dif'] = df['last_peak_dif'].shift(1)

df['last_valley_price'].fillna(method='ffill', inplace=True)
df['last_valley_dif'].fillna(method='ffill', inplace=True)
df['last_valley_price'] = df['last_valley_price'].shift(1)
df['last_valley_dif'] = df['last_valley_dif'].shift(1)
# 3、计算顶底背离
cond1 = df['price_new_high'] == 1  # 条件1：在拐点处判断
cond2 = df['price_new_low'] == 1  # 条件2：在拐点处判断
cond3 = df['close'] > df['last_peak_price']  # 条件3：当前收盘价比上一次拐点高（股价创新高）
cond4 = df['close'] < df['last_valley_price']  # 条件4：当前收盘价比上一次拐点低（股价创新低）
cond5 = df['DIF'] < df['last_peak_dif']  # 条件5：当前DIFF比上一次拐点低（DIF创新低）
cond6 = df['DIF'] > df['last_valley_dif']  # 条件6：当前DIFF比上一次拐点高（DIF创新高）

df.loc[cond1 & cond3 & cond5, 'state'] = '顶背离'
df.loc[cond2 & cond4 & cond6, 'state'] = '底背离'

df.loc[cond1 & cond3 & cond5, 'signal'] = 0  # 卖出信号（顶背离）
df.loc[cond2 & cond4 & cond6, 'signal'] = 1  # 买入信号（底背离）
# 框定时间范围
df = df[df['candle_end_time'] >= pd.to_datetime(start_time)]
df = df[df['candle_end_time'] <= pd.to_datetime(end_time)]

# 计算N日后涨跌幅，统计涨跌幅>0时间段
for day in day_list:
    df['%s日后涨跌幅' % day] = df['close'].shift(0 - day) / df['close'] - 1
    df['%s日后是否上涨' % day] = df['%s日后涨跌幅' % day] > 0
    df['%s日后是否上涨' % day].fillna(value=False, inplace=True)
df.to_csv('.\\MACD顶底背离代码\\data.csv', encoding="utf_8_sig")
# 计算N日后涨跌幅大于0的概率
for signal, group in df.groupby('signal'):
    print(signal)
    print(group[[str(i) + '日后涨跌幅' for i in day_list]].describe())
    for i in day_list:
        if signal == 1:
            print(str(i) + '天后涨跌幅大于0概率', '\t',
                  float(group[group[str(i) + '日后涨跌幅'] > 0].shape[0]) / group.shape[0])
        elif signal == 0:
            print(str(i) + '天后涨跌幅小于0概率', '\t',
                  float(group[group[str(i) + '日后涨跌幅'] < 0].shape[0]) / group.shape[0])

print(df.head(5))
