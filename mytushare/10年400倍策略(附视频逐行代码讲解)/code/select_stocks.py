"""
邢不行量化小讲堂系列文章配套代码
文章标题：10年400倍策略分享（附视频逐行代码讲解）
文章链接：https://mp.weixin.qq.com/s/yOuCVqeEPw11Y1xmqxKL0Q
作者：邢不行
微信号：xingbuxing0807
"""
# coding=utf-8
import os

import pandas as pd
from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt

pd.set_option('expand_frame_repr', False)

file_path = os.path.join(os.getcwd(), '10年400倍策略(附视频逐行代码讲解)\data')
# 导入数据
stock_data = pd.read_csv(f'{file_path}\\stock_data.csv', encoding='gbk')  # 此处填入数据在本地的路径
stock_data['交易日期'] = pd.to_datetime(stock_data['交易日期'])

# 排序
stock_data.sort_values(by=['交易日期', '股票代码'], inplace=True)

# 开始时间太早
stock_data = stock_data[stock_data['交易日期'] > pd.to_datetime('20060101')]

# 将月末停牌股票去除
# 万科在2015年12月18日停牌，2016年7月4日复牌。在12月31日那一天是不能买入这个股票的。
# 即最后一天不交易的股票，不能买入。
stock_data = stock_data[stock_data['是否交易'] != 0]
# 该月交易时间过短，去除
# 像万科在12月，停牌时间过长，这样的股票也不能买入。得知道这个股票在本月的交易天数
stock_data = stock_data[stock_data['交易天数'] >= 10]
# 在当天涨停的股票，也不能买入。这里使用0.097，是有问题的，没有考虑st股票
stock_data = stock_data[stock_data['最后一天涨跌幅'] <= 0.097]

# 计算所有股票在下个月的平均涨幅
output = pd.DataFrame()
output['所有股票下月涨幅'] = stock_data.groupby('交易日期')['下月涨幅'].mean()

# 计算每月市值排名
stock_data['市值_排名'] = stock_data.groupby('交易日期')['总市值'].rank()

# 选取排名前10的股票
stock_data = stock_data[stock_data['市值_排名'] <= 300]
stock_data.to_csv(f'{file_path}\\data.csv', encoding="utf_8_sig")
# 计算选中的股票在下月的涨幅
output['选中股票下月涨幅'] = stock_data.groupby('交易日期')['下月涨幅'].mean()

# 输出选择股票和资金曲线
stock_data['股票代码'] += ' '
output['股票代码'] = stock_data.groupby('交易日期')['股票代码'].sum()
output['line_benchmark'] = (output['所有股票下月涨幅'] + 1).cumprod()
output['line'] = (output['选中股票下月涨幅'] + 1).cumprod()
output.to_csv(f'{file_path}\\output.csv', encoding='gbk')  # 此处填入数据输出的路径
# 画图 
plt.plot(output['line'], color='r', label='女')
plt.plot(output['line_benchmark'], color='b', label='男')
plt.legend(loc='upper left')
plt.legend(prop={'family': 'SimHei', 'size': 15})
font_set = FontProperties(fname=r"c:\windows\fonts\simfang.ttf", size=15)
plt.title(u'10年400倍策略', FontProperties=font_set)
plt.show()
output.to_csv(f'{file_path}\\output.csv', encoding='gbk')  # 此处填入数据输出的路径
