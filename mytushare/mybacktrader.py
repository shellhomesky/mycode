import datetime  # For datetime objectsimport os.path  # To manage pathsimport sys  # To find out the script name (in argv[0])import pandas as pdimport backtrader as btimport akshare as akimport tushare as tsfrom backtrader.feeds import PandasDatafrom backtrader.feeds import GenericCSVData# tushare pro需到官网注册并获取token才能用token = 'e829ebd8351cf044f5b0950e4fe06568ee8f7cf350ef192c28b4d7f9'pro = ts.pro_api(token)rss = ".\\dat\\"# 查询股票列表def getStockCodeName():    fss = rss + "stk_base2020.csv"    df = ak.stock_info_a_code_name()    df.to_csv(fss, encoding='UTF-8-sig', index=None)# 导入股票池def getStkPool():    fss = rss + "stk_base2020.csv"    return pd.read_csv(fss, encoding='utf-8', usecols=[0])# 查询全部股票def getMultipleData(date):    stkPool = getStkPool()    # n=len(stkPool.code)    fss = rss + "indicator2020.csv"    reData = pd.read_csv(fss, encoding='utf-8')    # reData.columns=['code','trade_date','pe','pe_ttm','pb','ps','ps_ttm','dv_ratio','dv_ttm','total_mv']    for i, iCode in enumerate(stkPool.code):        iCode = str(iCode).zfill(6)        data = ak.stock_a_lg_indicator(stock=iCode)        data = data.set_index('trade_date').sort_index().loc[date:, ]        # data['trade_date'] =data.index        data.insert(0, 'trade_date', data.index)        data.insert(0, 'code', iCode)        reData = reData.append(data)    reData.to_csv(fss, encoding='UTF-8-sig', index=None)# 单只直接读取网络数据def get_data(code, date='2016-01-01'):    data1 = ak.stock_zh_a_daily(symbol=code, adjust="qfq")    data1 = data1.loc[date:, ['open', 'high', 'low', 'close', 'volume', 'turnover']]    data2 = ak.stock_a_lg_indicator(stock=code[2:8])    data2.rename(columns={'trade_date': 'date'}, inplace=True)    data2 = data2.set_index('date').sort_index().loc[date:, ['pe', 'pb']]    data = pd.merge(data1, data2, on='date')    data['openinterest'] = 0    data['datetime'] = data.index    data = data[['datetime', 'open', 'high', 'low', 'close', 'volume', 'openinterest', 'turnover', 'pe', 'pb']]    data = data.fillna(0)    return data# pandas的数据格式class Addmoredata(PandasData):    lines = ('turnover', 'pe', 'pb',)    params = (('turnover', 7), ('pe', 8), ('pb', 9),)# 扩展GenericCSVData加载csv格式数据# 直接读取本地csv格式数据class AddCsvData(GenericCSVData):    lines = ('turnover', 'pe', 'pb',)    params = (('turnover', 7), ('pe', 8), ('pb', 9),)# 标准策略模板class StdStrategy(bt.Strategy):    def log(self, txt, dt=None):        ''' Logging function fot this strategy'''        dt = dt or self.datas[0].datetime.date(0)        print('%s, %s' % (dt.isoformat(), txt))    def __init__(self):        # Keep a reference to the "close" line in the data[0] dataseries        self.dataclose = self.datas[0].close        # To keep track of pending orders        self.order = None    def notify(self, order):        if order.status in [order.Submitted, order.Accepted]:            # Buy/Sell order submitted/accepted to/by broker - Nothing to do            return        # Check if an order has been completed        # Attention: broker could reject order if not enougth cash        if order.status in [order.Completed, order.Canceled, order.Margin]:            if order.isbuy():                self.log('BUY EXECUTED, %.2f' % order.executed.price)            elif order.issell():                self.log('SELL EXECUTED, %.2f' % order.executed.price)            self.bar_executed = len(self)        # Write down: no pending order        self.order = None    def next(self):        # Simply log the closing price of the series from the reference        self.log('Close, %.2f' % self.dataclose[0])        # Check if an order is pending ...  if yes, we cannot send a 2nd one        if self.order:            return        # Check if we are in the market        if not self.position:            # Not yet ...  we MIGHT BUY if ...            if self.dataclose[0] < self.dataclose[-1]:                # current close less than previous close                if self.dataclose[-1] < self.dataclose[-2]:                    # previous close less than the previous close                    # BUY, BUY, BUY!!!  (with default parameters)                    self.log('BUY CREATE, %.2f' % self.dataclose[0])                    # Keep track of the created order to avoid a 2nd order                    self.order = self.buy()        else:            # Already in the market ...  we might sell            if len(self) >= (self.bar_executed + 5):                # SELL, SELL, SELL!!!  (with all possible default parameters)                self.log('SELL CREATE, %.2f' % self.dataclose[0])                # Keep track of the created order to avoid a 2nd order                self.order = self.sell()# 单只股票策略class SingleStrategy(bt.Strategy):    def log(self, txt, dt=None):        dt = dt or self.datas[0].datetime.date(0)        print('%s, %s' % (dt.isoformat(), txt))    def next(self):        self.log(f"换手率:{self.datas[0].turnover[0]},\		  市净率:{self.datas[0].pb[0]},市盈率:{self.datas[0].pe[0]}")# 多只股票策略class MultipleStrategy(bt.Strategy):    def log(self, txt, dt=None):        dt = dt or self.datas[0].datetime.date(0)        print('%s, %s' % (dt.isoformat(), txt))    def next(self):        for data in self.datas:            print(data._name)            self.log(f"换手率:{data.turnover[0]},\			市净率:{data.pb[0]},市盈率:{data.pe[0]}")# 加载的换手率和市盈率数据构建多因子策略class MultifactorStrategy(bt.Strategy):    def next(self):        if not self.position:  # 没有持仓            if self.datas[0].turnover[0] < 3 and 0 < self.datas[0].pe[0] < 50:                # 得到当前的账户价值                total_value = self.broker.getvalue()                # 1手=100股，满仓买入                ss = int((total_value / 100) / self.datas[0].close[0]) * 100                self.order = self.buy(size=ss)        else:  # 持仓，满足条件全部卖出            if self.datas[0].turnover[0] > 10 or self.datas[0].pe[0] > 80:                self.close(self.datas[0])# 标准策略运行函数def StdCerebro():    # 标准模板    cerebro = bt.Cerebro()    # Add a strategy    cerebro.addstrategy(StdStrategy)    # Create a Data Feed    # 本地数据，笔者用Wind获取的东风汽车数据以csv形式存储在本地。    # parase_dates = True是为了读取csv为dataframe的时候能够自动识别datetime格式的字符串，big作为index    # 注意，这里最后的pandas要符合backtrader的要求的格式    dataframe = pd.read_csv('..\\mystrategy\\topdown\\data\\zdat\\cn\\day\\600663.csv', index_col=0, parse_dates=True)    dataframe['openinterest'] = 0    data = bt.feeds.PandasData(dataname=dataframe,                               fromdate=datetime.datetime(2015, 1, 1),                               todate=datetime.datetime(2016, 12, 31))    # Add the Data Feed to Cerebro    cerebro.adddata(data)    # Set our desired cash start    cerebro.broker.setcash(100000.0)    # 设置每笔交易交易的股票数量    cerebro.addsizer(bt.sizers.FixedSize, stake=1000)    # Set the commission    cerebro.broker.setcommission(commission=0.0)    # Print out the starting conditions    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())    # Run over everything    cerebro.run()    # Print out the final result    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())    # Plot the result    cerebro.plot()# 单只股票策略运行函数def SingleCerebro():    # 单只股票测试    cerebro = bt.Cerebro()    cerebro.addstrategy(SingleStrategy)    feed = Addmoredata(dataname=get_data('sz300002', '2019-01-01'))    # 如果是读取csv数据使用下式    # feed = AddCsvData(dataname = 'test.csv',dtformat=('%Y-%m-%d'))    cerebro.adddata(feed)    cerebro.run()    cerebro.plot()# 多只股票策略运行函数def MultipleCerebro():    cerebro = bt.Cerebro()    cerebro.addstrategy(MultipleStrategy)    codes = ['600862.SH', '300326.SZ', '300394.SZ']    # 加载最近两日交易数据    for code in codes:        feed = Addmoredata(dataname=get_data(code, '20200506'), name=code)        cerebro.adddata(feed)    cerebro.run()    cerebro.plot()# 多因子策略运行函数def MultifactorCerebro():    cerebro = bt.Cerebro()    cerebro.addstrategy(MyStrategy)    feed = Addmoredata(dataname=get_data('300002.SZ', '20050101'))    cerebro.adddata(feed)    startcash = 100000    cerebro.broker.setcash(startcash)    cerebro.broker.setcommission(commission=0.001)    cerebro.run()    portvalue = cerebro.broker.getvalue()    pnl = portvalue - startcash    # 打印结果    print(f'期初总资金: {round(startcash, 2)}')    print(f'期末总资金: {round(portvalue, 2)}')    print(f'净收益: {round(pnl, 2)}')    cerebro.plot()if __name__ == '__main__':    # SingleCerebro()    # getStockCodeName()    getMultipleData('2015-01-01')