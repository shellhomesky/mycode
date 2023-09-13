'''
本代码由邢不行提供。
对应视频：《大A万年不涨？量化指数增强策略，轻松多涨10倍！同样成分股稍作修改，收益却变天。【量化投资邢不行啊】》
视频地址：https://www.bilibili.com/video/BV1rT4y1Q7XP?spm_id_from=333.999.0.0
获取更多量化知识或有量化相关疑问，请联系邢不行个人微信：xbx719
'''

import pandas as pd
import matplotlib.pyplot as plt

pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
pd.set_option('display.max_rows', 5000)  # 最多显示数据的行数

# 选股参数
n = 10
# 读取文件
equity = pd.read_csv(r'小市值选股策略_全部A股_选%s只.csv' % n, encoding='gbk', parse_dates=['交易日期'])
equity.set_index(['交易日期'], inplace=True)

# print(equity) #可使用print功能观察数据

# 画图
equity[['策略净值', '沪深300指数']].plot(figsize=(16, 9), grid=False, fontsize=20)
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
plt.savefig(r'小市值选股策略净值.png')
plt.show()
