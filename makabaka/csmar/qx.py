import pandas as pd

df = pd.read_excel('http://fdp.csmar.com:7092/group1/M00/15/89/wKhlJmNfcPiAa3VDAAXRcmIwJXY33.xlsx')

# print(df.columns)

df = df.dropna(subset=["姓名"], axis=0)

# 年龄
df.drop(df[(df["年龄"] > 80) | (df["年龄"] < 18)].index, inplace=True)

# 年收入计算月基本工资后填充
mon_salary = df["年收入"] / 12

df["月基本工资"].fillna(mon_salary, inplace=True)  # .round(2)

df["月基本工资"] = df["月基本工资"].round(2)

# 特殊字符处理
df.replace(r'!@9#%8', '', regex=True, inplace=True)

# 评分等级替换
df.loc[df["评分等级"] == 1, ["评分等级"]] = "Poor"
df.loc[df["评分等级"] == 2, ["评分等级"]] = "Standard"
df.loc[df["评分等级"] == 3, ["评分等级"]] = "Good"

# 特殊字符处理
df.replace(r'"', '', regex=True, inplace=True)
df["姓名"] = df["姓名"].replace(r'-', ' ', regex=True)
df["姓名"] = df["姓名"].replace(r',', '', regex=True)
# df["姓名"]=df["姓名"].replace(r'\.','',regex=True)
# print(df.info())
# print(df)

# 信用年份提取
df["信用年龄"] = df["信用年龄"].str[:2].fillna(0)

df["信用年龄"].replace(to_replace='0.0', value='0', inplace=True)
df["信用年龄"] = df["信用年龄"].astype('int')

# 异常值处理-3σ检测(银行账户数）
des = df.describe()
std = des["银行账户数"]['std']  # 获取指定列的标准差
mean = des["银行账户数"]['mean']  # 获取指定列的平均值
data = df["银行账户数"]  # 抽取frame中指定列列数据
# print(data[abs(data-mean)>3*std])      #用data中每个数据减均值mean，当差的绝对值abs大于3σ时，输出相应的data数据，即计算｜x-μ｜>3σ计算异常值
for i in data[abs(data - mean) > 3 * std]:
    df["银行账户数"].replace(i, '', inplace=True)
# 信用卡数
std2 = des["信用卡数"]['std']  # 获取指定列的标准差
mean2 = des["信用卡数"]['mean']  # 获取指定列的平均值
data2 = df["信用卡数"]
for a in data2[abs(data2 - mean2) > 3 * std2]:
    df["信用卡数"].replace(a, '', inplace=True)
print(df["银行账户数"], df["信用卡数"])

# 字段提取
frame = pd.DataFrame(df, columns=["姓名", "年龄", "月", "年收入", "月基本工资", "银行账户数", "信用卡数", "信用年龄",
                                  "评分等级"])

# 写入excel
frame.to_excel('数据清洗完成.xlsx', index=False)
# print(frame)
