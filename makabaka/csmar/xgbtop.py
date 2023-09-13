import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from xgboost import XGBClassifier
from xgboost import plot_importance
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.feature_selection import SelectFromModel

# 读取赛题训练集
# data = pd.read_csv('http://fdp.csmar.com:7092/group1/M00/15/8C/wKhlJmNfc2aAPCoZABLiIV8SXRM751.csv', header=0,
#                    index_col=None)
data = pd.read_csv('./data/训练集.csv', header=0, index_col=None)
# print(data.head())
# print(data.describe(include="all"))
# print(data.info())
# df2 = pd.read_csv('测试集答案.csv',header=0,index_col=None)
# print(df2.head(5))
# 选择你的特征和目标变量。 这取决于你的数据集和你想要预测的具体内容。
# 例如，如你想要预测的目标变量是在“target”列中,也可能是别的列名。
target = '评分等级'
# 选择所有数值型的特征
num_cols0 = data.select_dtypes(include=["int64", "float64"]).columns
# 排除目标变量target "评分等级"
num_cols = num_cols0.drop(target)
num_cols = num_cols.drop('ID号')
# 提取特征和目标变量
X = data[num_cols]
y = data[target]
# 填充缺失值
# X.mode().to_csv('./data/mode.csv')
# 使用每列的众数填充该列的缺失值
for column in X.columns:
    X[column].fillna(X[column].mode()[0], inplace=True)
# X = X.fillna(0)
# 将数据分为训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=1)
# 对特征进行规范化或标准化。 这在数据具有不同范围时非常有用。
scaler = StandardScaler()
scaler.fit(X_train)
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)
y_train = y_train - 1
y_test = y_test - 1
# 创建你的模型。如随机森林分类器 如XGBoost
# 随机森林
# clf = RandomForestClassifier(n_estimators=10)
# clf.fit(X_train, y_train)
# XGBoost
m = XGBClassifier()
m.fit(X_train, y_train)
# 选择重性特征
msf = SelectFromModel(m, threshold=0, max_features=9)
msf.fit(X_train, y_train)
X_train_select = msf.transform(X_train)
X_test_select = msf.transform(X_test)
# 再建一个原始分类函数
parameters = {

    'max_depth': [7],
    'min_child_weight': [3],
    'gamma': [0.4],
    'subsample': [1],
    'colsample_bytree': [1],
    # 'num_boost_round':[100],
    'eta': [0.03]
}
ms = XGBClassifier(param=parameters)
ms.fit(X_train_select, y_train)
# 使用测试集进行预测，并计算准确率
# 随机森林预测
# y_pred = clf.predict(X_test)

# XGBoost预测
y_pred = ms.predict(X_test_select)

# 准确率查看
accuracy = accuracy_score(y_test, y_pred)
print("Model Accuracy: ", accuracy)

# 查看重要性数据
m_fea = m.feature_importances_
msf_fea_name = num_cols[msf.get_support()]
print(m_fea)
print(msf_fea_name)
m = 0
# 画图
# 解决中文和负号显示问题
# plt.rcParams['font.sans-serif'] = ['SimHei']
# plt.rcParams['axes.unicode_minus'] = False
# 使显示图标自适应
# plt.rcParams['figure.autolayout'] = True
# plot_importance(m, title='特征重要性排序', xlabel='得分', ylabel='特征', importance_type='gain')
# plt.show()

# 对于赛题测试集也是数据预处理方式后，再传入到训练好的模型中
# 读取赛题测试集数据
df1 = pd.read_csv('./data/测试集.csv', header=0, index_col=None)
df1 = df1.dropna(subset=['ID号'])
print(df1.head(5))
# 提取特征
X0 = df1[num_cols]

# 填充缺失值
# 使用每列的众数填充该列的缺失值
for column in X0.columns:
    X0[column].fillna(X0[column].mode()[0], inplace=True)
X0.to_csv('./data/mode.csv', encoding='utf_8_sig')
# 对特征进行规范化或标准化。
X0 = scaler.transform(X0)

# 预测结果
# y_output = clf.predict(X0)
# 重要性特征选择数据
X0 = msf.transform(X0)
# 重要性特征训练好的模型
y_output = ms.predict(X0)
# print(y_output)
y_output = y_output + 1
# 数据输出
df1[target] = y_output
df1[["ID号", target]].to_csv('pred.csv', index=False)
# 参数调优对于模型的性能往往是非常重要的。对于XGBoost模型，我们可以调整的参数有很多，包括：`max_depth`（树的最大深度）、`min_child_weight`（子节点所需的最小权重）、`gamma`（控制是否后剪枝的参数）、`subsample`（样本采样比例）、`colsample_bytree`（列采样比例）等。

# 一种常用的参数调优方法是网格搜索（Grid Search），它会系统地遍历所有的参数组合。

# 参数调优

from sklearn.model_selection import GridSearchCV

# 设置参数范围
parameters = {

    'max_depth': [7],
    'min_child_weight': [3],
    'gamma': [0.4],
    'subsample': [1],
    'colsample_bytree': [1],
    'num_boost_round': [100],
    'eta': [0.03]
}

# 创建模型

# 创建网格搜索对象
grid_search = GridSearchCV(ms, parameters, cv=3, scoring='accuracy', verbose=1, n_jobs=3)

# 进行网格搜索
grid_search.fit(X_train_select, y_train)

# 打印最佳参数
print("Best Parameters: ", grid_search.best_params_)

# 使用最佳参数创建模型
best_model = grid_search.best_estimator_

# 使用最佳模型进行预测
y_pred = best_model.predict(X_test_select)

# 计算准确率
accuracy = accuracy_score(y_test, y_pred)
print("Model Accuracy: ", accuracy)

# 对测试集进行预测
y_output = best_model.predict(X0)
y_output = y_output + 1
print(y_output)
df1[target] = y_output
df1[["ID号", target]].to_csv('pred.csv', index=False)
