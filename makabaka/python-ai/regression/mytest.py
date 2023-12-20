import torch
import torch.nn.functional as F
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder
from torch.autograd import Variable


def get_data():
    data = pd.read_csv('../data/训练集.csv', header=0, index_col=None)
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
    # 归一化
    scaler = StandardScaler()
    scaler.fit(X)
    X = scaler.transform(X)
    # 标签编码
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


def train_loop(dataloader, model, lossfn, optimizer, epoch):
    size = len(dataloader.dataset)
    model.train()
    for batch, (X_data, y_data) in enumerate(dataloader):
        # 前向传播
        pred = model(X_data)
        # 计算损失
        loss = lossfn(pred, y_data)
        # 反向传播
        loss.backward()
        # 更新参数
        optimizer.step()
        # 梯度置零
        optimizer.zero_grad()
        if batch % 10== 0:
            loss, current = loss.item(), (batch + 1) * len(X_data)
            acc = (pred.argmax(dim=1) == y_data).sum().item() / len(y_data)
            print(f"Epoch:{epoch},batch:{batch},loss: {loss:>7f}   [{current:>5d}/{size:>5d}],acc:{acc}")
        # print(epoch,loss,acc)


def test_loop(dataloader, model, lossfn):
    model.eval()
    size = len(dataloader.dataset)
    num_batches = len(dataloader)
    test_loss = 0
    correct = 0
    with torch.no_grad():
        for X_data, y in dataloader:
            X_data, y = Variable(X_data, volatile=True), Variable(y)
            pred = model(X_data)
            test_loss += loss_fn(pred, y).item()
            correct += (pred.argmax(1) == y).type(torch.float).sum().item()
        test_loss /= num_batches
        correct /= size
        print(f"Test Error: \n Accuracy: {(100 * correct):>0.1f}%, Avg loss: {test_loss:>8f} \n")


def myloop(dataloader, model, lossfn):
    model.eval()
    size = len(dataloader.dataset)
    num_batches = len(dataloader)
    test_loss = 0
    correct = 0
    with torch.no_grad():
        for X_data, target in dataloader:
            X_data, target = Variable(X_data, volatile=True), Variable(target)
            pred = model(X_data)
            test_loss += F.cross_entropy(pred, target, size_average=False).item()
            pred = pred.data.max(1, keepdim=True)[1]
            correct += pred.eq(target.data.view_as(pred)).cpu().sum()
        test_loss /= len(test_dataloader.dataset)
        print('averageloss:{:.4f},Accuracy:{}/{}({:.0f}%)\n'.format(test_loss, correct,
                                                                    len(test_dataloader.dataset),
                                                                    100. * correct / len(test_dataloader.dataset)))


if __name__ == '__main__':
    i_batch_size = 64
    learning_rate = 1e-3
    epochs = 1000
    X_train, y_train, X_test, y_test = get_data()
    dataset = Dataset(X_train, y_train)
    train_dataloader = torch.utils.data.DataLoader(dataset=dataset,
                                                   batch_size=i_batch_size,
                                                   shuffle=True,
                                                   drop_last=True)
    test_dataset = torch.utils.data.TensorDataset(X_test, y_test)
    test_dataloader = torch.utils.data.DataLoader(dataset=test_dataset,
                                                  batch_size=i_batch_size,
                                                  shuffle=False,
                                                  drop_last=True)
    model = Model()
    optimizer_fn = torch.optim.Adam(model.parameters(), lr=learning_rate)
    loss_fn = torch.nn.CrossEntropyLoss()
    for i_epoch in range(epochs):
        print(f"Epoch {i_epoch + 1}-------------------------------")
        train_loop(train_dataloader, model, loss_fn, optimizer_fn, i_epoch+1)
        # test_loop(test_dataloader, model, loss_fn)
    torch.save(model, '../data/5.model')
    # model = torch.load('./data/5.model')
    # myloop()
