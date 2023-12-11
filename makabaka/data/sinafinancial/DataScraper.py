import akshare as ak
import  pandas as pd
if __name__ == '__main__':
    # stock_info_a_code_name_df = ak.stock_info_a_code_name()
    # stock_info_a_code_name_df=stock_info_a_code_name_df.astype(str)
    # stock_financial_report_zcfz_sina_df = ak.stock_financial_report_sina(stock="sh600519", symbol="资产负债表")
    # zcfz= stock_financial_report_zcfz_sina_df[ stock_financial_report_zcfz_sina_df['报告日'].str.contains('.*1231')]
    # stock_financial_report_lrb_sina_df = ak.stock_financial_report_sina(stock="sh600519", symbol="利润表")
    # lrb = stock_financial_report_zcfz_sina_df[stock_financial_report_zcfz_sina_df['报告日'].str.contains('.*1231')]
    # financial_data = pd.concat([zcfz,lrb], axis=1)
    # stock_info_a_code_name_df.to_csv('stock.csv', index=False, encoding='utf_8_sig')
    # financial_data .to_csv('sina.csv', index=False, encoding='utf_8_sig')
    df=pd.read_csv('stock.csv',encoding='utf_8_sig')
    df['code']=df['code'].apply(lambda x:'{:0>6d}'.format(x))
    print(1)