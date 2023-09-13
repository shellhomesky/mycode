'''
本代码由邢不行提供。
对应视频：《大A万年不涨？量化指数增强策略，轻松多涨10倍！同样成分股稍作修改，收益却变天。【量化投资邢不行啊】》
视频地址：https://www.bilibili.com/video/BV1rT4y1Q7XP?spm_id_from=333.999.0.0
获取更多量化知识或有量化相关疑问，请联系邢不行个人微信：xbx719
'''

import pandas as pd

pd.set_option('display.max_rows', 1000)
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
# 设置命令行输出时的列对齐功能
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)

N = 100
df_list = []
df: pd.DataFrame = pd.read_pickle('./all_stock_data.pkl')
df = df[df['股票代码'].str.contains('sh60')]

for c, g in df.groupby('交易日期'):
    print(c)
    g['是否保留'] = True
    # 2020年7月22日上证指数发布新规
    if c < pd.to_datetime('2020-07-22'):
        g.loc[g['股票代码'].str.contains('sh68'), '是否保留'] = False
        g.loc[g['涨跌幅'] > 0.11, '是否保留'] = False
    elif c >= pd.to_datetime('2020-07-22'):
        g['市值排序'] = g['前60日均值'].rank(method='first', ascending=False)
        g.loc[g['股票名称'].str.contains('ST'), '是否保留'] = False
        g.loc[g['股票名称'].str.contains('退'), '是否保留'] = False
        g.loc[g['上市至今交易天数'] < 250, '是否保留'] = False
        cond = g['股票代码'].str.contains('sh68')
        g.loc[(g['涨跌幅'] > 0.21) & (~cond), '是否保留'] = False
        g.loc[(g['涨跌幅'] > 0.11) & (~cond), '是否保留'] = False

        g.loc[(g['上市至今交易天数'] == 60) & (g['市值排序'] <= 10), '是否保留'] = True
    g = g[g['是否保留'] == True]
    g['市值排名'] = g['总市值'].rank(ascending=False)
    g = g[g['市值排名'] >= 10]
    df_ = pd.DataFrame({'交易日期': [c], '涨跌幅': [g['涨跌幅'].mean()]})
    df_list.append(df_)

all_df = pd.concat(df_list, ignore_index=True)
print(all_df)
all_df.to_csv('./上证等权指数.csv', index=False, encoding='gbk')
