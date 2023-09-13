# 导入API接口服务包
from OnePlusX.OnePlusXService import OnePlusXClass

# 初始化实例
oneplusx = OnePlusXClass()
import pandas as pd

query = oneplusx.query(
    tablename='stk_cash_flow a left join stk_level_of_risk b on a.code=b.code and a.FI_T6_Accper=b.FI_T7_Accper left join stk_management_ability c on a.code=c.code and a.FI_T6_Accper=c.FI_T4_Accper left join stk_profitability d on a.code=d.code and a.FI_T6_Accper=d.FI_T5_Accper',
    fields='a.code,a.short_name,a.FI_T6_Accper,a.FI_T6_F060101B,b.FI_T7_F070101B,b.FI_T7_F070201B,c.FI_T4_F040101B,d.FI_T5_F051501B,d.FI_T5_Indcd,d.FI_T5_F053202B',
    conditions="a.FI_T6_Accper='2021/12/31'")
# 从返回字典数据中提取data值，即带条件查询的数据
if query['state'] == 0:  # 如果返回状态码state为0，则查询成功，提取查询的数据
    querydata = query['data']
    for item in querydata:  # 打印查询的数据
        print(item)
# 自定义股票交易信息数组querydata
# print(querydata)

data = []
for re in querydata:
    code = re['code']
    short_name = re['short_name']
    FI_T6_Accper = re['FI_T6_Accper']
    FI_T6_F060101B = re['FI_T6_F060101B']
    FI_T7_F070101B = re['FI_T7_F070101B']
    FI_T7_F070201B = re['FI_T7_F070201B']
    FI_T4_F040101B = re['FI_T4_F040101B']
    FI_T5_F051501B = re['FI_T5_F051501B']
    FI_T5_Indcd = re['FI_T5_Indcd']
    FI_T5_F053202B = re['FI_T5_F053202B']

    data.append(
        [code, short_name, FI_T6_Accper, FI_T6_F060101B, FI_T7_F070101B, FI_T7_F070201B, FI_T4_F040101B, FI_T5_F051501B,
         FI_T5_Indcd, FI_T5_F053202B])
#    #querydata.append([code,short_name,FI_T6_Accper,FI_T6_F060101B,FI_T7_F070101B,FI_T7_F070201B])
#    #querydata.append([FI_T4_F040101B,FI_T5_F051501B,FI_T5_Indcd,FI_T5_F053202B])


for item in data:
    print(item)

df = pd.DataFrame(data, columns=['股票代码', '股票简称', '截止日期', '净利润现金净含量', '财务杠杆', '经营杠杆',
                                 '应收账款与收入比', '营业利润率', '行业代码', '投资收益率'])
print(df)
print('--------------' * 10)
print(df.info())
df.to_excel('大赛采集答案.xlsx', index=False)
