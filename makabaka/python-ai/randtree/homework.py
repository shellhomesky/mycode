import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# 检测是不是非平衡数据
df = pd.read_csv('../data/shuju2.csv')
y = df.iloc[:, -1]
# 计算每个类别的样本数量
class_counts = y.value_counts()
# 计算最大和最小类别的样本数量比例
imbalance_ratio = class_counts.max() / class_counts.min()
print(f"类别不平衡比例: {imbalance_ratio}")

# 导入数据并划分训练集测试集
df = pd.read_csv('../data/shuju2.csv')
X = df.iloc[:, 5:-1]
y = df.iloc[:, -1]
# 使用每列的众数填充该列的缺失值
for column in X.columns:
    X[column].fillna(X[column].mode()[0], inplace=True)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.05, random_state=0)
# 平衡数据
from imblearn.over_sampling import SMOTE

smo = SMOTE(random_state=42)
X_train, y_train = smo.fit_resample(X_train, y_train)
# 计算每个类别的样本数量
class_counts = y_train.value_counts()
# 计算最大和最小类别的样本数量比例
imbalance_ratio = class_counts.max() / class_counts.min()
print(f"类别不平衡比例: {imbalance_ratio}")
# 建立神经网络
# clf=MLPClassifier(solver='adam',alpha=1e-5,hidden_layer_sizes=(5,5,2),random_state=1,max_iter=500)
# 建立随机森林
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)
# 测试神经网络
y_predict = clf.predict(X_test)
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# 计算准确率
accuracy = accuracy_score(y_test, y_predict)
print(f'准确率: {accuracy}')
# 计算精确率
precision = precision_score(y_test, y_predict)
print(f'精确率: {precision}')
# 计算召回率
recall = recall_score(y_test, y_predict)
print(f'召回率: {recall}')
# 计算F1分数
f1 = f1_score(y_test, y_predict)
print(f'F1分数: {f1}')

# # 袋装
# from sklearn.ensemble import BaggingClassifier
# from sklearn.tree import DecisionTreeClassifier
# # 创建基分类器
# base_classifier = DecisionTreeClassifier()
# # 创建袋装自主聚集分类器，设置基分类器数量为10
# bagging_classifier = BaggingClassifier(estimator=base_classifier, n_estimators=100, random_state=42)
# # 使用袋装自主聚集分类器进行训练
# bagging_classifier.fit(X_train, y_train)
# # 使用袋装自主聚集分类器进行预测
# y_pred = bagging_classifier.predict(X_test)
# # 计算准确率
# accuracy = accuracy_score(y_test, y_pred)
# print(f"准确率：{accuracy}")
# # 计算精确率
# precision = precision_score(y_test, y_predict)
# print(f'精确率: {precision}')
# # 计算召回率
# recall = recall_score(y_test, y_predict)
# print(f'召回率: {recall}')
# # 计算F1分数
# f1 = f1_score(y_test, y_predict)
# print(f'F1分数: {f1}')

# # 随机森林长期价值模型的特征重要性
# from sklearn.ensemble import RandomForestClassifier
# import pandas as pd
# import matplotlib.pyplot as plt
# # 获取特征重要性
# feature_importances = clf.feature_importances_
# # 将特征重要性与特征名称对应
# feature_importance_dict = dict(zip(X.columns, feature_importances))
# # 对特征重要性进行排序
# sorted_features = sorted(feature_importance_dict.items(), key=lambda x: x[1], reverse=True)
# # 转换为DataFrame以便于可视化
# feature_importance_df = pd.DataFrame(sorted_features, columns=['Feature', 'Importance'])
# # 绘制特征重要性表格
# print(feature_importance_df)
# # 绘制特征重要性图表
# plt.figure(figsize=(10, 6))
# plt.title("Feature Importances")
# plt.barh(feature_importance_df['Feature'], feature_importance_df['Importance'])
# plt.gca().invert_yaxis()  # 逆转y轴方向，使最重要的特征显示在顶部
# plt.xlabel('Relative Importance')
# plt.show()
