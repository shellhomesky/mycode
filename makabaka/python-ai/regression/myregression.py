import pandas as pd
import torch
from torch.utils.data import DataLoader
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler


def get_data():
    df = pd.read_csv('../data/shuju2.csv', header=0, index_col=None)
    # 提取特征和目标变量
    x = df.iloc[:, 5:-1]
    y = df.iloc[:, -1]
    # 填充缺失值
    # 使用每列的众数填充该列的缺失值
    for column in x.columns:
        x[column].fillna(x[column].mode()[0], inplace=True)
    # 归一化
    scaler = StandardScaler()
    scaler.fit(x)
    x = scaler.transform(x)
    # 标签编码
    encoder = LabelEncoder()
    encoder.fit(y)
    y = encoder.transform(y)
    # 将数据分为训练集和测试集
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=0)
    # 对特征进行规范化或标准化。 这在数据具有不同范围时非常有用。
    x_train = torch.FloatTensor(x_train)
    y_train = torch.LongTensor(y_train)
    x_test = torch.FloatTensor(x_test)
    y_test = torch.LongTensor(y_test)
    return x_train, y_train, x_test, y_test


class Dataset(torch.utils.data.Dataset):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __len__(self):
        return len(self.x)

    def __getitem__(self, item):
        return self.x[item], self.y[item]


class NeuralNetwork(torch.nn.Module):
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
    global trainbatchbst_acc
    global trainepochbst_acc
    epochssize = len(dataloader.dataset)
    batchessize = len(dataloader)
    trainepoch_correct = 0
    model.train()
    for ibatch, (X_data, y_data) in enumerate(dataloader):
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
        # 保存batch最好的模型
        trainbatchbst_acc = 0
        trainbatch_correct = (pred.argmax(dim=1) == y_data).sum().item()
        trainbatch_correct_acc = float((torch.max(pred.data, 1)[1] == y_data).sum()) / float(len(X_data))
        if trainbatch_correct_acc > trainbatchbst_acc:
            trainbatchbst_acc = trainbatch_correct_acc
            # print(model.state_dict().keys())
            # 保存模型权重
            # torch.save(model.state_dict(), 'batchbstmodel_parameter' + str(epoch) + '-' + str(ibatch + 1) + '.pt')
            # 保存完整模型
            # torch.save(model, 'batchbstmodel' + str(epoch) + '-' + str(ibatch + 1) + '.pt')
            print(f'Train Batch result-{str(epoch)}-{str(ibatch + 1)} Accuracy: {(100 * trainbatchbst_acc):>0.4f}%')
        # 保存epoch最好的模型
        trainepoch_correct += (torch.max(pred.data, 1)[1] == y_data).sum()
        trainepoch_correct_acc = float(trainepoch_correct) / float(epochssize)
        # 中途显示
        if ibatch % 10 == 0:
            current = (ibatch + 1) * len(X_data)
            trainbatch_loss = loss.item()
            print(
                f"Epoch:{epoch},batch:{ibatch},loss: {trainbatch_loss  :>8f}   [{current:>5d}/{epochssize:>5d}],每批准确率:{trainbatch_correct / len(X_data)},累计准确率:{float(trainepoch_correct)}/{float(len(X_data) * (ibatch + 1))}={float(trainepoch_correct) / float(len(X_data) * (ibatch + 1))}")
    if trainepoch_correct_acc > trainepochbst_acc:
        trainepochbst_acc = trainepoch_correct_acc
        # print(model.state_dict().keys())
        # 保存模型权重
        # torch.save(model.state_dict(), 'epochbstmodel_parameter' + str(epoch) + '-' + str(ibatch + 1) + '.pt')
        # 保存完整模型
        # torch.save(model, 'epochbstmodel' + str(epoch) + '-' + str(ibatch + 1) + '-' + str(trainepochbst_acc) + '.pt')
        print(f'Train Epoch result-{str(epoch)}-{str(ibatch + 1)} Accuracy: {(100 * trainepoch_correct_acc):>0.4f}%')


def test_loop(dataloader, model, lossfn, epoch):
    global testbst_acc
    global best_model
    epochssize = len(dataloader.dataset)
    batchessize = len(dataloader)
    test_loss = 0
    test_correct = 0
    model.eval()
    with torch.no_grad():
        for x_data, y in dataloader:
            pred = model(x_data)
            test_loss += lossfn(pred, y).item()
            test_correct += (pred.argmax(1) == y).type(torch.float).sum().item()
    test_loss /= batchessize
    test_correct /= epochssize
    # 保存最好的模型
    if test_correct > testbst_acc:
        testbst_acc = test_correct
        best_model = model
        # 保存模型权重
        # torch.save(best_model.state_dict(), 'testbstmodel_parameter' + str(epoch) + '.pt')
        # 保存完整模型
        # torch.save(best_model, 'testbstmodel' + str(epoch) + '-' + str(testbst_acc) + '.pt')
    print(
        f"Test result-{str(epoch)} Accuracy:{(100 * test_correct):>0.4f}%,Avg loss: {test_loss:>8f},Test Best result{str(epoch)} Accuracy: {(100 * testbst_acc):>0.4f}%")


if __name__ == '__main__':
    i_batch_size = 32
    learning_rate = 1e-3
    epochs = 50
    trainbatchbst_acc = 0
    trainepochbst_acc = 0
    testbst_acc = 0
    best_model = NeuralNetwork()
    Model = NeuralNetwork()
    optimizer_fn = torch.optim.Adam(Model.parameters(), lr=learning_rate)
    loss_fn = torch.nn.CrossEntropyLoss()
    for i_epoch in range(epochs):
        X_train, Y_train, X_test, Y_test = get_data()
        train_dataset = Dataset(X_train, Y_train)
        train_dataloader = DataLoader(dataset=train_dataset,
                                      batch_size=i_batch_size,
                                      shuffle=True,
                                      drop_last=True)
        # test_dataset = torch.utils.data.TensorDataset(X_test, y_test)
        test_dataset = Dataset(X_test, Y_test)
        test_dataloader = DataLoader(dataset=test_dataset,
                                     batch_size=i_batch_size,
                                     shuffle=False,
                                     drop_last=True)
        print(f"Epoch {i_epoch + 1}-------------------------------")
        train_loop(train_dataloader, Model, loss_fn, optimizer_fn, i_epoch + 1)
        test_loop(test_dataloader, Model, loss_fn, i_epoch + 1)
    # 保存模型权重
    # torch.save(model.state_dict(), 'model_parameter.pt')
    # # 保存完整模型
    # torch.save(model, 'best_model.pt')
    # # torch.save(model, '../data/6.model')
    # # model_test = torch.load('../data/6.model')
    # test_loop(test_dataloader, model_test, loss_fn)
