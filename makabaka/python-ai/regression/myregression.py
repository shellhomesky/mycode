import pandas as pd
import torch
from torch.utils.data import DataLoader
import torch.nn.functional as F
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from torch.autograd import Variable


def get_data():
    df = pd.read_csv('../data/shuju2.csv', header=0, index_col=None)
    # 提取特征和目标变量
    X = df.iloc[:, 5:-1]
    y = df.iloc[:, -1]
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
            torch.nn.Linear(in_features=51, out_features=64),
            torch.nn.ReLU(),
            torch.nn.Linear(in_features=64, out_features=32),
            torch.nn.ReLU(),
            torch.nn.Linear(in_features=32, out_features=2)
            # torch.nn.Softmax(dim=1)
        )

    def forward(self, x):
        return self.fc(x)


def train_loop(dataloader, model, lossfn, optimizer, epoch):
    global trainbst_acc
    size = len(dataloader.dataset)
    num_batches = len(dataloader)
    correct = 0
    trainbst_acc = 0
    train_loss = 0
    train_correct = 0
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
        if batch % 10 == 0:
            predicted = torch.max(pred.data, 1)[1]
            correct += (predicted == y_data).sum()
            current = (batch + 1) * len(X_data)
            losspic = loss.item()
            train_loss += losspic
            correctpic = (pred.argmax(dim=1) == y_data).sum().item()
            train_correct += correctpic
            print(f"Epoch:{epoch},batch:{batch},loss: {losspic:>8f}   [{current:>5d}/{size:>5d}],每批准确率:{correctpic/len(X_data)},累计准确率:{float(correct)}/{float(len(X_data) * (batch + 1))}={float(correct) / float(len(X_data) * (batch + 1))}")
    train_loss /= num_batches
    train_correct /= size
    # 保存最好的模型
    if train_correct > trainbst_acc:
        trainbst_acc = train_correct
    print(model.state_dict().keys())
    # 保存模型权重
    torch.save(model.state_dict(), 'model_parameter.pt')
    # 保存完整模型
    torch.save(model, 'best_model.pt')
    print(f"Train result: \n Accuracy: {(100 * train_correct):>0.4f}%, Avg loss: {train_loss:>8f} \n")


def test_loop(dataloader, model, lossfn):
    global testbst_acc
    global best_model
    size = len(dataloader.dataset)
    num_batches = len(dataloader)
    testbst_acc = 0
    test_loss = 0
    test_correct = 0
    model.eval()
    with torch.no_grad():
        for X_data, y in dataloader:
            X_data, y = Variable(X_data, volatile=True), Variable(y)
            pred = model.forward(X_data)
            test_loss += lossfn(pred, y).item()
            test_correct += (pred.argmax(1) == y).type(torch.float).sum().item()
    test_loss /= num_batches
    test_correct /= size
    # 保存最好的模型
    if test_correct > testbst_acc:
        testbst_acc = test_correct
        best_model = model
        print(model.state_dict().keys())
    print(f"Test result: \n Accuracy: {(100 * test_correct):>0.4f}%, Avg loss: {test_loss:>8f} \n")


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
            test_loss += lossfn(pred, target, size_average=False).item()
            pred = pred.data.max(1, keepdim=True)[1]
            correct += pred.eq(target.data.view_as(pred)).cpu().sum()
        test_loss /= len(test_dataloader.dataset)
        print('averageloss:{:.4f},Accuracy:{}/{}({:.0f}%)\n'.format(test_loss, correct,
                                                                    len(test_dataloader.dataset),
                                                                    100. * correct / len(test_dataloader.dataset)))


if __name__ == '__main__':
    i_batch_size = 64
    learning_rate = 1e-3
    epochs = 10
    X_train, y_train, X_test, y_test = get_data()
    train_dataset = Dataset(X_train, y_train)
    train_dataloader = DataLoader(dataset=train_dataset,
                                  batch_size=i_batch_size,
                                  shuffle=True,
                                  drop_last=True)
    # test_dataset = torch.utils.data.TensorDataset(X_test, y_test)
    test_dataset = Dataset(X_test, y_test)
    test_dataloader = DataLoader(dataset=test_dataset,
                                 batch_size=i_batch_size,
                                 shuffle=False,
                                 drop_last=True)
    model = Model()
    optimizer_fn = torch.optim.Adam(model.parameters(), lr=learning_rate)
    loss_fn = torch.nn.CrossEntropyLoss()
    for i_epoch in range(epochs):
        print(f"Epoch {i_epoch + 1}-------------------------------")
        train_loop(train_dataloader, model, loss_fn, optimizer_fn, i_epoch + 1)
        trainbst_acc = 0
        testbst_acc = 0
        best_model = Model()
        test_loop(test_dataloader, model, loss_fn)
    # 保存模型权重
    torch.save(model.state_dict(), 'model_parameter.pt')
    # 保存完整模型
    torch.save(model, 'best_model.pt')
    # torch.save(model, '../data/6.model')
    # model_test = torch.load('../data/6.model')
    # test_loop(test_dataloader, model_test, loss_fn)
