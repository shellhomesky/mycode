import time
import akshare as ak
import pandas as pd

# code = lambda x: "sh" + x if x[0] == 6 else "sz" + x
# stock_zh_a_spot_df = ak.stock_zh_a_spot()
stock_dzjy_mrmx_df=pd.read_csv("11.csv")
stock_dzjy_mrmx_df["证券代码"]=stock_dzjy_mrmx_df["证券代码"].str[2:]
# stock_dzjy_mrmx_df = ak.stock_dzjy_mrmx(symbol='A股', start_date='20231101', end_date='20231102')
stock_dzjy_mrmx_df["成交量"]=stock_dzjy_mrmx_df.groupby("证券代码")["成交量"].transform('sum')
stock_dzjy_mrmx_df["成交额"]=stock_dzjy_mrmx_df.groupby("证券代码")["成交额"].transform('sum')
stock_dzjy_mrmx_df=stock_dzjy_mrmx_df.sort_values(by="交易日期",ascending=False).groupby("证券代码").apply(lambda x:x.head(1))
stock_dzjy_mrmx_df.reset_index(drop=True,inplace=True)
# stock_dzjy_mrmx_df.drop_duplicates('证券代码', inplace=True)
df=pd.DataFrame(columns=list(ak.stock_zh_a_hist (symbol="000001",start_date="20231102", end_date='20231108', adjust="qfq")))
df.insert(0, 'code','')
# dd.insert(0, "code", "000001")
# df = pd.DataFrame(columns=list(dd))
for item in stock_dzjy_mrmx_df.itertuples():
    # dm = code(item[3])
    # time.sleep(10)
    stock_zh_a_hist_df = ak.stock_zh_a_hist (symbol=item[3],start_date="20231102", end_date='20231108', adjust="qfq")
    stock_zh_a_hist_df.insert(0, "code", item[3])
    print(item[3])
    df = pd.concat([df, stock_zh_a_hist_df], ignore_index=True)
stock_zh_a_hist_df =pd.merge(stock_dzjy_mrmx_df,df,left_on="证券代码",right_on="code")
stock_zh_a_hist_df=stock_zh_a_hist_df.loc[pd.to_datetime(stock_zh_a_hist_df["日期"])<=ts.date()+pd.offsets.BDay(3)]
stock_zh_a_hist_df = stock_zh_a_hist_df .sort_values(by="收盘",ascending=False).groupby("证券代码").apply(lambda x:x.head(1))
stock_zh_a_hist_df["涨跌幅"]=(stock_zh_a_hist_df["收盘"]-stock_zh_a_hist_df["收盘价"])/stock_zh_a_hist_df["收盘价"]
print(0)
