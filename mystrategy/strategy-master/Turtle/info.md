海龟交易策略是个经典的策略

类型：日内趋势追踪+反转策略

周期：20天

交易规则：

根据配置文件csv中所列交易代码列表，先获取前一个周期的日线数据，获得该只股票代码的最高价和最低价

初始化时，同时订阅csv文件中所有代码的tick行情，当有数据来时，检查当前价格是否突破最高价或最低价。

如果向上突破这只代码过去20天的最高价，则按csv配置文件中的金额买入。
如果向下突破这只代码过去20天的最低价，并且有可卖仓位，则全部卖出。

csv 文件示例如下：

exchange, sec_id, buy_amount(¥)

SZSE,300275,200000

SHSE,600000,200000
 
