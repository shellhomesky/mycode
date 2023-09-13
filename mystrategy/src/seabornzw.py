import seaborn as sns

tips = sns.load_dataset("tips")
sns.jointplot("total_bill", "tip", tips, kind='reg')
sns.plt.show()
import pandas as pd

dfa = pd.read_csv('Z:\mydbank\数据A.csv', encoding='gbk')
dfb = pd.read_csv('Z:\mydbank\数据B.csv', encoding='gbk')
dfa
i = 0
s = dfa.iloc[i, 0]
print(s)
l = []
for i in s:
    print("1-", i)
    l.append(i)

# import matplotlib.pyplot as plt1
# from mpl_toolkits.mplot3d import axes3d 
# from matplotlib import cm
#   
# fig = plt1.figure()
# ax = fig.gca(projection='3d')
# X, Y, Z = axes3d.get_test_data(0.05)
# ax.plot_surface(X, Y, Z, rstride=8, cstride=8, alpha=0.3)
# cset = ax.contour(X, Y, Z, zdir='z', offset=-100, cmap=cm.coolwarm)
# cset = ax.contour(X, Y, Z, zdir='x', offset=-40, cmap=cm.coolwarm)
# cset = ax.contour(X, Y, Z, zdir='y', offset=40, cmap=cm.coolwarm)
#   
# ax.set_xlabel('X')
# ax.set_xlim(-40, 40)
# ax.set_ylabel('Y')
# ax.set_ylim(-40, 40)
# ax.set_zlabel('Z')
# ax.set_zlim(-100, 100)
#   
# plt1.show()
#   
#   
#   
# import numpy as np
# import matplotlib.pyplot as plt2
# import matplotlib.animation as animation
#   
#   
# def data_gen(t=0):
#     cnt = 0
#     while cnt < 1000:
#         cnt += 1
#         t += 0.1
#         yield t, np.sin(2 * np.pi * t) * np.exp(-t / 10.)
#   
#   
# def init():
#     ax.set_ylim(-1.1, 1.1)
#     ax.set_xlim(0, 10)
#     del xdata[:]
#     del ydata[:]
#     line.set_data(xdata, ydata)
#     return line,
#   
# fig, ax = plt2.subplots()
# line, = ax.plot([], [], lw=2)
# ax.grid()
# xdata, ydata = [], []
#   
#   
# def run(data):
#     # update the data
#     t, y = data
#     xdata.append(t)
#     ydata.append(y)
#     xmin, xmax = ax.get_xlim()
#   
#     if t >= xmax:
#         ax.set_xlim(xmin, 2 * xmax)
#         ax.figure.canvas.draw()
#     line.set_data(xdata, ydata)
#   
#     return line,
#   
# ani = animation.FuncAnimation(fig, run, data_gen, blit=False, interval=10,
#                               repeat=False, init_func=init)
# plt2.show()
