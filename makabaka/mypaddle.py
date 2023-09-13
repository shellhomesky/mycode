import os
import paddle as pa
import numpy as np

# 定义训练和测试数据
x_data = np.array([[1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                   [2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                   [3.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                   [4.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                   [5.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]).astype('float32')
y_data = np.array([[3.0], [5.0], [7.0], [9.0], [11.0]]).astype('float32')
test_data = np.array([[6.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]).astype('float32')
# 定义一个简单的线性网络
net = pa.nn.Sequential(
    pa.nn.Linear(13, 100),
    pa.nn.ReLU(),
    pa.nn.Linear(100, 1)
)
# 定义优化方法
optimizer = pa.optimizer.SGD(learning_rate=0.01, parameters=net.parameters())
## 将numpy类型数据转换成tensor之后才能用于模型训练
inputs = pa.to_tensor(x_data)
labels = pa.to_tensor(y_data)
# 开始训练100个pass
for pass_id in range(10):
    out = net(inputs)
    loss = pa.mean(pa.nn.functional.square_error_cost(out, labels))
    loss.backward()
    optimizer.step()
    optimizer.clear_grad()
    print("Pass:%d, Cost:%0.5f" % (pass_id, loss))
# 开始预测
predict_inputs = pa.to_tensor(test_data)
result = net(predict_inputs)
print("当x为6.0时，y为：%0.5f" % result)
# 快来上手第一个Demo吧！——用PaddlePaddle做房价预测
# Step1：准备数据(1)数据集加载
BATCH_SIZE = 20
train_dataset = pa.text.datasets.UCIHousing(mode='train')
valid_dataset = pa.text.datasets.UCIHousing(mode='test')
# 用于训练的数据加载器，每次随机读取批次大小的数据，剩余不满足批大小的数据丢弃
train_loader = pa.io.DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True, drop_last=True)
# 用于测试的数据加载器，每次随机读取批次大小的数据
valid_loader = pa.io.DataLoader(valid_dataset, batch_size=BATCH_SIZE, shuffle=True)
# 用于打印，查看uci_housing数据
print(train_dataset[0])
# Step2:网络配置(1)网络搭建：对于线性回归来讲，它就是一个从输入到输出的简单的全连接层。
# 输入数据形状为[13]，输出形状[1]
net = pa.nn.Linear(13, 1)
# Step2:网络配置(2)定义损失函数
# 此处使用均方差损失函数。
# square_error_cost(input,lable):接受输入预测值和目标值，并返回方差估计,即为（y-y_predict）的平方
# Step2:网络配置(3)定义优化函数
optimizer = pa.optimizer.SGD(learning_rate=0.001, parameters=net.parameters())
# Step3.模型训练 and Step4.模型评估(1)定义绘制训练过程的损失值变化趋势的方法draw_train_process
import matplotlib.pyplot as plt

iter = 0
iters = []
train_costs = []


def draw_train_process(iters, train_costs):
    title = "training cost"
    plt.title(title, fontsize=24)
    plt.xlabel("iter", fontsize=14)
    plt.ylabel("cost", fontsize=14)
    plt.plot(iters, train_costs, color='red', label='training cost')
    plt.grid()
    plt.show()


# Step3.模型训练 and Step4.模型评估(2)训练并保存模型
EPOCH_NUM = 50
# 训练EPOCH_NUM轮
for pass_id in range(EPOCH_NUM):
    # 开始训练并输出最后一个batch的损失值
    train_cost = 0
    # 遍历train_reader迭代器
    for batch_id, data in enumerate(train_loader()):
        inputs = pa.to_tensor(data[0])
        labels = pa.to_tensor(data[1])
        out = net(inputs)
        train_loss = pa.mean(pa.nn.functional.square_error_cost(out, labels))
        train_loss.backward()
        optimizer.step()
        optimizer.clear_grad()
        # 每运行40步，输出一次信息,
        # 注意batch_id=0时也输出, 即 0, 40, 80, ...
        if batch_id % 40 == 0:
            print("Pass:%d, Cost:%0.5f" % (pass_id, train_loss))
        iter = iter + BATCH_SIZE
        iters.append(iter)
        train_costs.append(train_loss.numpy()[0])
    # 开始测试并输出最后一个batch的损失值
    test_loss = 0
    # 遍历test_reader迭代器
    for batch_id, data in enumerate(valid_loader()):
        inputs = pa.to_tensor(data[0])
        labels = pa.to_tensor(data[1])
        out = net(inputs)
        test_loss = pa.mean(pa.nn.functional.square_error_cost(out, labels))
    # 打印最后一个batch的损失值
    print('Test:%d, Cost:%0.5f' % (pass_id, test_loss))
# 保存模型
pa.save(net.state_dict(), 'fit_a_line.pdparams')
draw_train_process(iters, train_costs)
# Step5.模型预测(1)可视化真实值与预测值方法定义
infer_results = []
groud_truths = []


# 绘制真实值和预测值对比图
def draw_infer_result(groud_truths, infer_results):
    title = 'Boston'
    plt.title(title, fontsize=24)
    x = np.arange(1, 20)
    y = x
    plt.plot(x, y)
    plt.xlabel('ground truth', fontsize=14)
    plt.ylabel('infer result', fontsize=14)
    plt.scatter(groud_truths, infer_results, color='green', label='training cost')
    plt.grid()
    plt.show()


# Step5.模型预测((2)开始预测
valid_dataset = pa.text.UCIHousing(mode='test')
infer_loader = pa.io.DataLoader(valid_dataset, batch_size=200)
infer_net = pa.nn.Linear(13, 1)
param = pa.load('fit_a_line.pdparams')
infer_net.set_dict(param)
data = next(infer_loader())
inputs = pa.to_tensor(data[0])
results = infer_net(inputs)
for idx, item in enumerate(zip(results, data[1])):
    print("Index:%d, Infer Result: %.2f, Ground Truth: %.2f" % (idx, item[0], item[1]))
    infer_results.append(item[0].numpy()[0])
    groud_truths.append(item[1].numpy()[0])
draw_infer_result(groud_truths, infer_results)
