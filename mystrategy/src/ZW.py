# import seaborn as sns
# tips=sns.load_dataset("tips")
# sns.jointplot("total_bill", "tip",tips, kind='reg')
# sns.plt.show()

import pandas as pd
import numpy as np

dfa = pd.read_csv('Z:\mydbank\数据A.csv', encoding='gbk')
dfb = pd.read_csv('Z:\mydbank\数据B.csv', encoding='gbk')
s = dfa.ix[0, 0]
dfs = pd.DataFrame(list(s)).T
print(dfs)
print(dfb)


def _map(dataa, datab, exp):
    dfr = pd.DataFrame(list())
    for indexa, rowa in dataa.iterrows():
        for col_namea in dataa.columns:
            sa = rowa[col_namea]
            l = []
            for indexb, rowb in datab.iterrows():
                for col_nameb in datab.columns:
                    sb = rowb[col_nameb]
                    se = exp(sa, sb)
                    l.append(se)
            dfr = pd.concat([dfr, pd.DataFrame(l, columns=[col_namea])], axis=1)
    return dfr


temp = _map(dfs, dfb, lambda x, y: 1 if x in y else 0)
print(dfs.ix[0, 4] in dfb.ix[0, 0])
print(temp)
print(temp / list(temp.sum()))
