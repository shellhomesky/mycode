import datetime
import tushare as ts
import pandas as pd
import numpy as np
import time

if __name__ == '__main__':
    # 设置tushare pro的token并获取连接
    ts.set_token('e829ebd8351cf044f5b0950e4fe06568ee8f7cf350ef192c28b4d7f9')
    pro = ts.pro_api()
    # 设定获取日线行情的初始日期和终止日期，其中终止日期设定为昨天。
    start_dt = '20150101'
    time_temp = datetime.datetime.now() - datetime.timedelta(days=1)
    end_dt = time_temp.strftime('%Y%m%d')
    lsHead = ['ts_code', 'trade_date', 'open', 'high', 'low', 'close', 'pre_close', 'change', 'pct_chg', 'vol',
              'amount']
    ksgn = ['ts_code', 'trade_date']
    rss = ".\\dat\\"
    fssDat = rss + 'stk_dat.csv'
    fssCode = rss + 'stk_base2019.csv'
    reDat = pd.read_csv(fssDat, encoding='utf-8-sig')
    stkPoolSave = pro.stock_basic(exchange='', list_status='L',
                                  fields='ts_code,symbol,name,area,industry,fullname,enname,market,exchange,curr_type,list_status,list_date,delist_date,is_hs')
    stkPoolSave.columns = ['TS代码', '股票代码', '股票名称', '所在地域', '所属行业', '股票全称', '英文全称',
                           '市场类型 （主板/中小板/创业板）', '交易所代码', '交易货币', '上市状态： L上市 D退市 P暂停上市',
                           '上市日期', '退市日期', '是否沪深港通标的，N否 H沪股通 S深股通']
    stkPoolSave.to_csv(fssCode, encoding='utf-8-sig', index=False, date_format='str')
    stkPool = pd.read_csv(fssCode, encoding='utf-8', usecols=[0], header=0, names=['ts_code'])
    # stock_pool = ['603912.SH','300666.SZ','300618.SZ','002049.SZ','300672.SZ']
    total = len(stkPool)


    def reDatTimmax(reDat, ts_code, ksgn, tim0):
        xd0 = reDat.loc[reDat['ts_code'] == ts_code]
        if (len(xd0) > 0):
            xd0 = xd0.sort_values(ksgn, ascending=True)
            _xt = xd0.iloc[-1][ksgn[1]]
            s2 = str(_xt)
            if s2 != 'nan':
                tim0 = s2.split(" ")[0]
        return xd0, tim0


    def reDatAppend(df, df0, ksgn, num_round=3, vlst=lsHead):
        if (len(df0) > 0):
            df = df.append(df0)
            df = df.append(df0)
            df = df.sort_values(ksgn, ascending=True)
            df.drop_duplicates(subset=ksgn, keep=False, inplace=True)
            df = df.sort_values(ksgn, ascending=False)
        df = np.round(df, num_round)
        return df


    # 循环获取单个股票的日线行情1
    for i, iCode in enumerate(stkPool.ts_code):
        if i > 10:
            break
        try:
            reDati, startMax = reDatTimmax(reDat, iCode, ksgn, start_dt)
            df = pro.daily(ts_code=iCode, start_date=startMax, end_date=end_dt)
            time.sleep(0.2)
            if len(df) > 0:
                df.loc[:, 'trade_date'] = df.loc[:, 'trade_date'].astype('int64')
                df = reDatAppend(df, reDati, ksgn)
                reDat = reDat.append(df)
            # 打印进度
            print('Seq: ' + str(i + 1) + ' of ' + str(total) + '   Code: ' + str(iCode))
        except Exception as aa:
            print(aa)
            print('No DATA Code: ' + str(i))
            reDat = reDat.sort_values(by=['ts_code', 'trade_date'], ascending=(True, True))
            reDat.to_csv(fssDat, index=False, encoding='utf-8-sig', mode='w', header=True)
            continue
    reDat = reDat.sort_values(by=['ts_code', 'trade_date'], ascending=(True, True))
    reDat.to_csv(fssDat, index=False, encoding='utf-8-sig', mode='w', header=True)
    print('All Finished!')
