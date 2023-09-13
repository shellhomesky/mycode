# -*- coding:utf-8 -*-
'''
Created on 2016年2月16日

@author: shellcom
'''


def hello(name):
    '''
    :param name:
    '''
    return "hello," + name + "!"


def story(**kwds):
    return "once upon a time, there was a " \
           "%(job)s called %(name)s" % kwds


def power(x, y, *others):
    if others:
        print("received redundant parameters:", others)
    return pow(x, y)


def interval(start, stop=None, step=1):
    "imitates range() for step>0"
    if stop is None:
        start, stop = 0, start
    result = []
    i = start
    while i < stop:
        result.append(i + 1)
        i += step
    return result


def factory(n):
    if n == 1:
        return 1
    else:
        return n * factory(n - 1)


def search(l, key, lo=0, hi=None):
    if hi is None:
        hi = len(l) - 1
    if lo == hi:
        return hi
    else:
        mid = (lo + hi) // 2
        if key > l[mid]:
            return search(l, key, mid + 1, hi)
        else:
            return search(l, key, lo, mid)


def func(a, b, c=0, *tup, **dic):
    print("a=", a, "b=", b, "c=", c, "tup=", tup, "dic=", dic)


args = (1, 2, 3, 4, 5)
print(args)
kw = {"x": 100, "y": 200, "z": 101, "xx": 201}
print(kw)
func(1, 2, **kw)
seq = [56, 78, 12, 52, 31, 56, 46, 1, 13]
print(seq)
seq.sort()
print(seq)
print(search(seq, 12))


class sec:
    def __inai(self):
        print("you can't see me")

    def ai(self):
        print("message is")
        self.__inai()


s = sec()
s.ai()
s._sec__inai()


class fil:
    def init(self):
        self.blk = []

    def filter(self, seque):
        return [x for x in seque if x not in self.blk]


class samfil(fil):
    def init(self):
        self.blk = ["spam"]


f = fil()
f.init()
print(f.filter([1, 2, 3, 45, 56]))
s = samfil()
s.init()
print(s.filter(["spam", "spam", "sfsf", "123", "4646"]))

from numpy import matrix

ss = matrix([[1, 2, 3], [4, 5, 6]])
print(ss)

import seaborn as sns

tips = sns.load_dataset("tips")
sns.jointplot("total_bill", "tip", tips, kind='reg')

import matplotlib.pyplot as plt1
from mpl_toolkits.mplot3d import axes3d
from matplotlib import cm

fig = plt1.figure()
ax = fig.gca(projection='3d')
X, Y, Z = axes3d.get_test_data(0.05)
ax.plot_surface(X, Y, Z, rstride=8, cstride=8, alpha=0.3)
cset = ax.contour(X, Y, Z, zdir='z', offset=-100, cmap=cm.coolwarm)
cset = ax.contour(X, Y, Z, zdir='x', offset=-40, cmap=cm.coolwarm)
cset = ax.contour(X, Y, Z, zdir='y', offset=40, cmap=cm.coolwarm)

ax.set_xlabel('X')
ax.set_xlim(-40, 40)
ax.set_ylabel('Y')
ax.set_ylim(-40, 40)
ax.set_zlabel('Z')
ax.set_zlim(-100, 100)

plt1.show()

import numpy as np
import matplotlib.pyplot as plt2
import matplotlib.animation as animation


def data_gen(t=0):
    cnt = 0
    while cnt < 1000:
        cnt += 1
        t += 0.1
        yield t, np.sin(2 * np.pi * t) * np.exp(-t / 10.)


def init():
    ax.set_ylim(-1.1, 1.1)
    ax.set_xlim(0, 10)
    del xdata[:]
    del ydata[:]
    line.set_data(xdata, ydata)
    return line,


fig, ax = plt2.subplots()
line, = ax.plot([], [], lw=2)
ax.grid()
xdata, ydata = [], []


def run(data):
    # update the data
    t, y = data
    xdata.append(t)
    ydata.append(y)
    xmin, xmax = ax.get_xlim()

    if t >= xmax:
        ax.set_xlim(xmin, 2 * xmax)
        ax.figure.canvas.draw()
    line.set_data(xdata, ydata)

    return line,


ani = animation.FuncAnimation(fig, run, data_gen, blit=False, interval=10,
                              repeat=False, init_func=init)
plt2.show()
