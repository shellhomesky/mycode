'''
本代码由邢不行提供。
对应视频：《基金反买,别墅靠海?每年买倒数前十基金,能赚这么多？Python量化分析告诉你答案【量化投资邢不行】》
视频地址：https://www.bilibili.com/video/BV1Tm4y1S7ws?spm_id_from=333.999.0.0
获取更多量化知识或有量化相关疑问，请联系邢不行个人微信：xbx971
'''

import pandas as pd
from matplotlib import pyplot as plt

pd.set_option('display.max_rows', 10000)
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行

# 设置命令行输出时的列对齐功能
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)

# 读取基金数据文件
df = pd.read_csv('2008-2021基金收益率数据.csv', encoding='utf-8', skiprows=1)
df1 = df.copy().rank(ascending=True)
df1.to_csv('排名数据.csv', encoding='gbk')

# 读取指数涨跌幅数据并处理
exponent_df = pd.read_csv('指数涨跌幅.csv', encoding='gbk')
exponent_df['年份'] = pd.to_datetime(exponent_df['candle_end_time']).dt.year
exponent_df['年份'] = exponent_df['年份'].apply(str)
df.set_index('基金代码', inplace=True)
# print(df)
# exit()
d = list(df.columns)


# 定义绘图函数
def draw_equity_curve(df, time, data_dict, pic_size=[22, 9], dpi=72, font_size=25):
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.figure(figsize=(pic_size[0], pic_size[1]), dpi=dpi)
    plt.xticks(fontsize=font_size)
    plt.yticks(fontsize=font_size)
    for key in data_dict:
        plt.plot(df[time], df[data_dict[key]], label=key)
    plt.legend(fontsize=font_size)
    plt.show()


# 次年表现统计
all_df = pd.DataFrame()
for i in range(df.shape[1] - 1):
    # 排序并选择后十基金
    df_ = df.copy().rank(ascending=True)
    df_ = df_[df_[d[i + 1]].notna()]
    df_now = df_.sort_values(d[i])
    now_ = list(df_now.head(10).index)
    print((df_[d[i + 1]].dropna().shape[0]) - df_.loc[now_][d[i + 1]])

    # 次年排名、收益率、相对收益率计算
    all_df.loc[f'{d[i]}年前十基金次年', '年份'] = d[i + 1]
    all_df.loc[f'{d[i]}年前十基金次年', '排名均数'] = (df_[d[i + 1]].dropna().shape[0] - df_.loc[now_][
        d[i + 1]].mean() + 1) / df_[d[i + 1]].dropna().shape[0]
    all_df.loc[f'{d[i]}年前十基金次年', '平均收益率'] = df.loc[now_][d[i + 1]].mean()
    # print(all_df)
    # exit()
    all_df.loc[f'{d[i]}年前十基金次年', '相对收益率'] = (
            df.loc[now_][d[i + 1]] - exponent_df[exponent_df['年份'] == d[i + 1]]['涨跌幅'].values[0]).mean()

# 将次年表现数据整理后输出
all_df.reset_index(inplace=True)
all_df = pd.merge(left=all_df, right=exponent_df[['涨跌幅', '年份']], how='left', on='年份')
all_df.rename(columns={'涨跌幅': '指数涨跌幅'}, inplace=True)
all_df.set_index('index', inplace=True)
print(all_df)

# 为画图表现准备，计算净值
all_df['基金净值计算'] = all_df['平均收益率'] + 1
all_df['指数净值计算'] = all_df['指数涨跌幅'] + 1
all_df['年份'] = all_df['年份'].astype('int')
all_df['年份'] = all_df['年份'] + 1
all_df['年份'] = all_df['年份'].apply(lambda x: str(x).split('.')[0])
all_df['基金净值'] = all_df['基金净值计算'].cumprod()
all_df['指数净值'] = all_df['指数净值计算'].cumprod()

# 展示数据结束时间
all_df.loc['2020年前十基金次年', '年份'] = '20210930'
all_df.set_index('年份', inplace=True)

# 默认开始的时候为1元
all_df.loc['2009', '基金净值'] = 1
all_df.loc['2009', '指数净值'] = 1
all_df.sort_values('年份', inplace=True)
all_df.reset_index(inplace=True)
print(all_df[['基金净值']])

# 画出净值图
draw_equity_curve(all_df, '年份', {'基金净值': '基金净值', '指数净值': '指数净值'})
