import akshare as ak
import  pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
if __name__ == '__main__':
    stock_financial_report_sina_df = ak.stock_financial_report_sina(stock="sh600519", symbol="资产负债表")
    stock_financial_report_sina_df.to_csv('sina.csv', index=False, encoding='utf_8_sig')
