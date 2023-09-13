import torch
import torch.nn.functional as F
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder
from torch.autograd import Variable


def get_data():
    data = pd.read_csv('./data/训练集.csv', header=0, index_col=None)
    target = '评分等级'
    # 选择所有数值型的特征
    num_cols0 = data.select_dtypes(include=["int64", "float64"]).columns
    # 过滤异常数据
    data = data.loc[((data['年龄'] >= 18) & (data['年龄'] <= 70)), :]
    # 排除目标变量target "评分等级"
    num_cols = num_cols0.drop(target)
    num_cols = num_cols.drop('ID号')
    # 提取特征和目标变量
    X = data[num_cols]
    y = data[target]
    # 填充缺失值
    # 使用每列的众数填充该列的缺失值
    for column in X.columns:
        X[column].fillna(X[column].mode()[0], inplace=True)
    scaler = StandardScaler()
    scaler.fit(X)
    X = scaler.transform(X)
    encoder = LabelEncoder()
    encoder.fit(y)
    y = encoder.transform(y)
    # 将数据分为训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=7)
    # 对特征进行规范化或标准化。 这在数据具有不同范围时非常有用。
    X_train = torch.FloatTensor(X_train)
    y_train = torch.LongTensor(y_train)
    X_test = torch.FloatTensor(X_test)
    y_test = torch.LongTensor(y_test)
    return X_train, y_train, X_test, y_test


class Dataset(torch.utils.data.Dataset):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __len__(self):
        return len(self.x)

    def __getitem__(self, item):
        return self.x[item], self.y[item]


class Model(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.fc = torch.nn.Sequential(
            torch.nn.Linear(in_features=15, out_features=64),
            torch.nn.ReLU(),
            torch.nn.Linear(in_features=64, out_features=32),
            torch.nn.ReLU(),
            torch.nn.Linear(in_features=32, out_features=3)
            # torch.nn.Softmax(dim=1)
        )

    def forward(self, x):
        return self.fc(x)


def train(epoch, lr):
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    loss_fun = torch.nn.CrossEntropyLoss()
    model.train()
    for i, (x, y) in enumerate(train_loader):
        out = model(x)
        loss = loss_fun(out, y)
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()
    if epoch % 2 == 0:
        acc = (out.argmax(dim=1) == y).sum().item() / len(y)
        print(epoch, loss.item(), acc)


# @torch.no_grad()
def test():
    model.eval()
    test_loss = 0
    correct = 0
    for data, target in test_loader:
        data, target = Variable(data, volatile=True), Variable(target)
        out = model(data)
        test_loss += F.cross_entropy(out, target, size_average=False).item()
        pred = out.data.max(1, keepdim=True)[1]
        correct += pred.eq(target.data.view_as(pred)).cpu().sum()
    test_loss /= len(test_loader.dataset)
    print('averageloss:{:.4f},Accuracy:{}/{}({:.0f}%)\n'.format(test_loss, correct,
                                                                len(test_loader.dataset),
                                                                100. * correct / len(test_loader.dataset)))


if __name__ == '__main__':
    i_batch_size = 64
    f_lr = 1e-3
    X_train, y_train, X_test, y_test = get_data()
    dataset = Dataset(X_train, y_train)
    train_loader = torch.utils.data.DataLoader(dataset=dataset,
                                               batch_size=i_batch_size,
                                               shuffle=True,
                                               drop_last=True)
    test_dataset = torch.utils.data.TensorDataset(X_test, y_test)
    test_loader = torch.utils.data.DataLoader(dataset=test_dataset,
                                              batch_size=i_batch_size,
                                              shuffle=False,
                                              drop_last=True)
    model = Model()
    # for i_epoch in range(1000):
    #     train(i_epoch,f_lr)
    # torch.save(model, './data/5.model')
    model = torch.load('./data/5.model')
    test()
