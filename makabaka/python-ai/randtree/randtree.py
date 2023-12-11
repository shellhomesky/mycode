from sklearn.neural_network import MLPClassifier
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
#导入数据并划分训练集测试集
df=pd.read_csv('data.csv')
X = df.iloc[:,5:-1]
y = df.iloc[:, -1]
# 使用每列的众数填充该列的缺失值
for column in X.columns:
    X[column].fillna(X[column].mode()[0], inplace=True)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=0)
# 建立神经网络
# clf=MLPClassifier(solver='adam',alpha=1e-5,hidden_layer_sizes=(5,5,2),random_state=1,max_iter=500)
#建立随机森林
clf = RandomForestClassifier(n_estimators=100, random_state=0)
clf.fit(X_train, y_train)
# 测试神经网络
y_predict= clf.predict(X_test)
# 计算准确率
accuracy = accuracy_score(y_test, y_predict)
print(f"测试集准确率: {accuracy}")
print("随机森林，测试样本总数：%d 错误样本数：%d"%(X_test.shape[0],(y_test!=y_predict).sum()))
