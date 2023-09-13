# region 循环罗列33选6组合
# 循环罗列33选6组合
from itertools import combinations

import pandas as pd

fss = './data/DoubleBall.csv'
nCnt = 0
nNumList = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
            30, 31, 32, 33]
pdz = pd.DataFrame(columns=(0, 1, 2, 3, 4, 5))
nLast = len(nNumList)
for x in combinations(nNumList, 6):
    pdz = pd.concat([pdz, pd.DataFrame([x])], ignore_index=True)
    nCnt += 1
    print(nCnt)
pdz.to_csv(fss, index=False, encoding='gbk')
for i1 in range(0, (nLast - 5)):
    for i2 in range(0, (nLast - 4)):
        if (i2 == i1):
            continue
        for i3 in range(0, (nLast - 3)):
            if (i3 == i2 or i3 == i1):
                continue
            for i4 in range(0, (nLast - 2)):
                if (i4 == i3 or i4 == i2 or i4 == i1):
                    continue
                for i5 in range(0, (nLast - 1)):
                    if (i5 == i4 or i5 == i3 or i5 == i2 or i5 == i1):
                        continue
                    for i6 in range(0, nLast):
                        if (i6 == i5 or i6 == i4 or i6 == i3 or i6 == i2 or i6 == i1):
                            continue
                        if (nNumList[i1] > nNumList[i2] and nNumList[i2] > nNumList[i3] and nNumList[i3] > nNumList[
                            i4] and nNumList[i4] > nNumList[i5] and nNumList[i5] > nNumList[i6]):
                            continue
                        zh = [str(nNumList[i1]), str(nNumList[i2]), str(nNumList[i3]), str(nNumList[i4]),
                              str(nNumList[i5]), str(nNumList[i6])]
                        pdz = pd.concat([pdz, pd.DataFrame([zh])], ignore_index=True)
                        pdz.to_csv(fss, index=False, encoding='gbk')
                        nCnt += 1
pdz.to_csv(fss, index=False, encoding='gbk')
