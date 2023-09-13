import cv2
import os
import torch
import numpy as np
import pandas as pd


# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import StandardScaler
# from sklearn.preprocessing import LabelEncoder
# from torch.autograd import Variable
# from datasets import load_from_disk
# from torchvision import datasets
# import torch.nn.functional as F
def load_data(dir):
    xs = []
    ys = []
    for filename in os.listdir(dir):
        if not filename.endswith('.jpg'):
            continue
        x = cv2.imread(dir + '\\' + filename)
        x = x[:, :, ::-1]
        x = torch.FloatTensor(np.array(x)) / 255
        x = x.permute(2, 0, 1)
        y = int(filename[0])
        xs.append(x)
        ys.append(y)
    return xs, ys


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
        self.cnn1 = torch.nn.Conv2d(in_channels=3,
                                    out_channels=32,
                                    kernel_size=5,
                                    stride=1,
                                    padding=2)
        self.cnn2 = torch.nn.Conv2d(in_channels=32,
                                    out_channels=32,
                                    kernel_size=5,
                                    stride=1,
                                    padding=2)
        self.cnn3 = torch.nn.Conv2d(in_channels=32,
                                    out_channels=64,
                                    kernel_size=5,
                                    stride=1,
                                    padding=2)
        self.maxpool1 = torch.nn.MaxPool2d(kernel_size=2)
        self.maxpool2 = torch.nn.MaxPool2d(kernel_size=2)
        self.maxpool3 = torch.nn.MaxPool2d(kernel_size=2)
        self.flatten = torch.nn.Flatten()
        self.linear1 = torch.nn.Linear(in_features=1024, out_features=10)
        # self.linear2 = torch.nn.Linear(in_features=64, out_features=10)
        self.relu = torch.nn.ReLU()
        self.softmax = torch.nn.Softmax()

    def forward(self, x):
        x = self.cnn1(x)
        x = self.relu(x)
        x = self.maxpool1(x)
        x = self.cnn2(x)
        x = self.relu(x)
        x = self.maxpool2(x)
        x = self.cnn3(x)
        x = self.relu(x)
        x = self.maxpool3(x)
        x = self.flatten(x)
        x = self.linear1(x)
        # x = self.linear2(x)
        x = self.softmax(x)
        return x


def train(epoch, lr):
    global train_loss
    global test_loss
    global train_acc
    global test_acc
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    loss_fun = torch.nn.CrossEntropyLoss()
    model.train()
    for i, (x, y) in enumerate(train_loader):
        optimizer.zero_grad()
        out = model(x)
        loss = loss_fun(out, y)
        loss.backward()
        optimizer.step()
        _, lable = torch.max(out, 1)
        acca = torch.sum(lable == y).item()
        train_loss += loss.item()
        train_acc += acca
        if i % 200 == 0:
            acc = (out.argmax(dim=1) == y).sum().item() / len(y)
            print(epoch, i, loss.item(), train_loss, train_acc, acc)


if __name__ == '__main__':
    # dataset = load_from_disk('../data/Huggingface_Toturials-main/data/ChnSentiCorp')
    # train_dataset = datasets.CIFAR10('../dataset', train=True, download=True)
    i_batch_size = 64
    f_lr = 1e-3
    s_dir = r'C:\data\mypython\makabaka\python-ai\dataset\cifar-10-batches-py\train'
    train_loss = 0.0
    test_loss = 0.0
    train_acc = 0.0
    test_acc = 0.0
    ls_x, ls_y = load_data(s_dir)
    dataset = Dataset(ls_x, ls_y)
    train_loader = torch.utils.data.DataLoader(dataset=dataset,
                                               batch_size=i_batch_size,
                                               shuffle=True,
                                               drop_last=True)
    model = Model()
    for i_epoch in range(100):
        train(i_epoch, f_lr)
    torch.save(model, '../data/7.model')
    print('0')
