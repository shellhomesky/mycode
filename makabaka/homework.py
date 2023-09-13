# #将罗马数字转换为阿拉伯数字
# dict={'I':1,'V':5,'X':10,'L':50,'C':100,'D':500,'M':1000} #罗马单个字母的数字值
# dict2={'IV':4,'IX':9,'XL':40,'XC':90,'CD':400,'CM':900} #几个特殊情况
# dict3=('IV','IX','XL','XC','CD','CM')
# #现在要求输入罗马字母，输出对应的数字值
# n=input()
# p=0
# if n in dict3:
#     p=dict2[n]
#     for i in n:
#         for k,v in dict.items():
#             if i  == k:
#                 p+=v
# print(p)
#
#
#
#
#
# """
# 1.通过字典存储罗马字符和整型数字的对应关系
# 2.先求出字符串最后一个罗马字符对应的数字res
# 3.从后开始遍历，如果后一个罗马字符大于前一个，res减去前一个罗马字符对应的
# 数字；如果小于前一个罗马字符，则加上前一个
# """
# r = {
#     'I':             1,
#     'V':             5,
#     'X':             10,
#     'L':             50,
#     'C':             100,
#     'D':             500,
#     'M':             1000
# }
#
# s = input('请输入罗马字符：')
# a = [i for i in s]
# res = r[a[-1]]
# for i in a[::-1]:
#     if res < r[i]:
#         res = res + r[i]
#     elif res > r[i]:
#         res = res - r[i]
# print(res)

# for i in range(1, 101):
#     if (i % 5 and i % 7) == 0:
#         print(i)
value = []
value1 = []
value2 = []
value3 = []
# for i in range(len(num)):
#     for j in range(len(num[i])):
#         value.append(num[i][j])
# value1=value[::3]
# for a in range(len(value1)):
#     print(value1[a],end=' ')
# print('\n')
# value2=value[1::3]
# for b in range(len(value2)):
#     print(value2[b],end=' ')
# print('\n')
# value3=value[2::3]
# for c in range(len(value3)):
#     print(value3[c],end=' ')

# num = [[1, 2, 3], [2, 3, 4], [5, 6, 7], [6, 7, 8]]
# def listReverse_1(nums):
#     ans = []
#     for i in range(len(nums[0])):
#         num = []
#         for j in range(len(nums)):
#             num.append(nums[j][i])
#         ans.append(num)
#     return ans
# a=listReverse_1(num)
# print(a)
import re, os

print(os.getcwd())
f = open('words.txt', encoding='UTF-8')
strs = f.read()
list = re.split('[^a-zA-Z]', strs)
count = {}
for word in list:
    count[word] = count.get(word, 0) + 1
max_list = []
max_value = max(count.values())
for m, n in count.items():
    if n == max_value:
        max_list.append(m)
print(max_list)
