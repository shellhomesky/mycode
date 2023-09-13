# coding=utf-8
# -*- coding: utf-8 -*- 
'''
Top极宽量化(原zw量化)，Python量化第一品牌 
网站:www.TopQuant.vip   www.ziwang.com
QQ总群:124134140   千人大群 zwPython量化&大数据 
    
TopQuant.vip ToolBox 2016
Top极宽·量化开源工具箱 系列软件 
by Top极宽·量化开源团队 2016.12.25 首发
  
文件名:ztools_data.py
默认缩写：import ztools_datadown as zddown
简介：Top极宽常用数据现在工具函数集
'''

import os, sys, io, re
import random, arrow, bs4
import numpy as np
import numexpr as ne
import pandas as pd
import tushare as ts
import time

import requests
#
import cpuinfo as cpu
import psutil as psu
import inspect
#
import matplotlib as mpl
import matplotlib.colors
from matplotlib import cm

#
import zsys
import ztools as zt
import ztools_str as zstr
import ztools_web as zweb
import ztools_data as zdat

#
ts.set_token('e829ebd8351cf044f5b0950e4fe06568ee8f7cf350ef192c28b4d7f9')
pro = ts.pro_api()


# financial statement
def downFinancialStatement(dPeriod):
    rss = ".\\topdown\\tmp\\"
    ts.set_token('e829ebd8351cf044f5b0950e4fe06568ee8f7cf350ef192c28b4d7f9')
    pro = ts.pro_api()
    fss = rss + 'stk_base2019.csv'
    print(fss)
    stkPoolSave = pro.stock_basic(exchange='', list_status='L',
                                  fields='ts_code,symbol,name,area,industry,fullname,enname,market,exchange,curr_type,list_status,list_date,delist_date,is_hs')
    stkPoolSave.columns = ['TS代码', '股票代码', '股票名称', '所在地域', '所属行业', '股票全称', '英文全称',
                           '市场类型 （主板/中小板/创业板）', '交易所代码', '交易货币', '上市状态： L上市 D退市 P暂停上市',
                           '上市日期', '退市日期', '是否沪深港通标的，N否 H沪股通 S深股通']
    stkPoolSave.to_csv(fss, encoding='utf-8-sig', index=False, date_format='str')
    fssBalance = rss + 'balancesheet.csv'
    fssIncome = rss + 'incomesheet.csv'
    stkPool = pd.read_csv(fss, encoding='utf-8', usecols=[0], header=None, names=['ts_code'])
    stkPool = stkPool.drop([0])
    xnq = len(stkPool.ts_code)
    reDataBalance = pd.read_csv(fssBalance, encoding='utf-8', header=None)
    reDataBalance.columns = ['ts_code', 'ann_date', 'f_ann_date', 'end_date', 'period', 'report_type', 'comp_type',
                             'total_share', 'cap_rese', 'undistr_porfit', 'surplus_rese', 'special_rese', 'money_cap',
                             'trad_asset', 'notes_receiv', 'accounts_receiv', 'oth_receiv', 'prepayment', 'div_receiv',
                             'int_receiv', 'inventories', 'amor_exp', 'nca_within_1y', 'sett_rsrv',
                             'loanto_oth_bank_fi', 'premium_receiv', 'reinsur_receiv', 'reinsur_res_receiv',
                             'pur_resale_fa', 'oth_cur_assets', 'total_cur_assets', 'fa_avail_for_sale', 'htm_invest',
                             'lt_eqt_invest', 'invest_real_estate', 'time_deposits', 'oth_assets', 'lt_rec',
                             'fix_assets', 'cip', 'const_materials', 'fixed_assets_disp', 'produc_bio_assets',
                             'oil_and_gas_assets', 'intan_assets', 'r_and_d', 'goodwill', 'lt_amor_exp',
                             'defer_tax_assets', 'decr_in_disbur', 'oth_nca', 'total_nca', 'cash_reser_cb',
                             'depos_in_oth_bfi', 'prec_metals', 'deriv_assets', 'rr_reins_une_prem',
                             'rr_reins_outstd_cla', 'rr_reins_lins_liab', 'rr_reins_lthins_liab', 'refund_depos',
                             'ph_pledge_loans', 'refund_cap_depos', 'indep_acct_assets', 'client_depos', 'client_prov',
                             'transac_seat_fee', 'invest_as_receiv', 'total_assets', 'lt_borr', 'st_borr', 'cb_borr',
                             'depos_ib_deposits', 'loan_oth_bank', 'trading_fl', 'notes_payable', 'acct_payable',
                             'adv_receipts', 'sold_for_repur_fa', 'comm_payable', 'payroll_payable', 'taxes_payable',
                             'int_payable', 'div_payable', 'oth_payable', 'acc_exp', 'deferred_inc', 'st_bonds_payable',
                             'payable_to_reinsurer', 'rsrv_insur_cont', 'acting_trading_sec', 'acting_uw_sec',
                             'non_cur_liab_due_1y', 'oth_cur_liab', 'total_cur_liab', 'bond_payable', 'lt_payable',
                             'specific_payables', 'estimated_liab', 'defer_tax_liab', 'defer_inc_non_cur_liab',
                             'oth_ncl', 'total_ncl', 'depos_oth_bfi', 'deriv_liab', 'depos', 'agency_bus_liab',
                             'oth_liab', 'prem_receiv_adva', 'depos_received', 'ph_invest', 'reser_une_prem',
                             'reser_outstd_claims', 'reser_lins_liab', 'reser_lthins_liab', 'indept_acc_liab',
                             'pledge_borr', 'indem_payable', 'policy_div_payable', 'total_liab', 'treasury_share',
                             'ordin_risk_reser', 'forex_differ', 'invest_loss_unconf', 'minority_int',
                             'total_hldr_eqy_exc_min_int', 'total_hldr_eqy_inc_min_int', 'total_liab_hldr_eqy',
                             'lt_payroll_payable', 'oth_comp_income', 'oth_eqt_tools', 'oth_eqt_tools_p_shr',
                             'lending_funds', 'acc_receivable', 'st_fin_payable', 'payables', 'hfs_assets', 'hfs_sales']
    reDataBalance = reDataBalance.drop([0])
    reDataIncome = pd.read_csv(fssIncome, encoding='utf-8', header=None)
    reDataIncome.columns = ['ts_code', 'ann_date', 'f_ann_date', 'end_date', 'period', 'report_type', 'comp_type',
                            'basic_eps', 'diluted_eps', 'total_revenue', 'revenue', 'int_income', 'prem_earned',
                            'comm_income', 'n_commis_income', 'n_oth_income', 'n_oth_b_income', 'prem_income',
                            'out_prem', 'une_prem_reser', 'reins_income', 'n_sec_tb_income', 'n_sec_uw_income',
                            'n_asset_mg_income', 'oth_b_income', 'fv_value_chg_gain', 'invest_income',
                            'ass_invest_income', 'forex_gain', 'total_cogs', 'oper_cost', 'int_exp', 'comm_exp',
                            'biz_tax_surchg', 'sell_exp', 'admin_exp', 'fin_exp', 'assets_impair_loss', 'prem_refund',
                            'compens_payout', 'reser_insur_liab', 'div_payt', 'reins_exp', 'oper_exp',
                            'compens_payout_refu', 'insur_reser_refu', 'reins_cost_refund', 'other_bus_cost',
                            'operate_profit', 'non_oper_income', 'non_oper_exp', 'nca_disploss', 'total_profit',
                            'income_tax', 'n_income', 'n_income_attr_p', 'minority_gain', 'oth_compr_income',
                            't_compr_income', 'compr_inc_attr_p', 'compr_inc_attr_m_s', 'ebit', 'ebitda',
                            'insurance_exp', 'undist_profit', 'distable_profit']
    reDataIncome = reDataIncome.drop([0])
    stkPool = stkPool.append(pd.DataFrame({'ts_code': reDataBalance.loc[reDataBalance.period == dPeriod, 'ts_code']}))
    stkPool = stkPool.drop_duplicates(subset=['ts_code'], keep=False)
    xny = len(stkPool.ts_code)
    try:
        for i, iCode in enumerate(stkPool.ts_code):
            print("\n", i, "/", xny, "/", xnq, "股票代码,", iCode, "开始下载", dPeriod, "资产负债表:")
            datBalance = pro.balancesheet(ts_code=iCode, period=dPeriod)
            lsColumnName = datBalance.columns.tolist()
            lsColumnName.insert(lsColumnName.index('report_type'), 'period')
            datBalance = datBalance.reindex(columns=lsColumnName, fill_value=dPeriod)
            print("\n", i, "/", xny, "/", xnq, "股票代码,", iCode, "开始下载", dPeriod, '利润表:')
            datIncome = pro.income(ts_code=iCode, period=dPeriod)
            lsColumnName = datIncome.columns.tolist()
            lsColumnName.insert(lsColumnName.index('report_type'), 'period')
            datIncome = datIncome.reindex(columns=lsColumnName, fill_value=dPeriod)
            reDataBalance = reDataBalance.append(datBalance)
            reDataIncome = reDataIncome.append(datIncome)
            time.sleep(2.5)
        # if i>3:
        #	break
        reDataBalance.columns = ['TS股票代码', '公告日期', '实际公告日期', '报告期', 'period',
                                 '报表类型：见下方详细说明', '公司类型：1一般工商业 2银行 3保险 4证券', '期末总股本',
                                 '资本公积金 (元，下同)', '未分配利润', '盈余公积金', '专项储备', '货币资金',
                                 '交易性金融资产', '应收票据', '应收账款', '其他应收款', '预付款项', '应收股利',
                                 '应收利息', '存货', '长期待摊费用', '一年内到期的非流动资产', '结算备付金', '拆出资金',
                                 '应收保费', '应收分保账款', '应收分保合同准备金', '买入返售金融资产', '其他流动资产',
                                 '流动资产合计', '可供出售金融资产', '持有至到期投资', '长期股权投资', '投资性房地产',
                                 '定期存款', '其他资产', '长期应收款', '固定资产', '在建工程', '工程物资',
                                 '固定资产清理', '生产性生物资产', '油气资产', '无形资产', '研发支出', '商誉',
                                 '长期待摊费用', '递延所得税资产', '发放贷款及垫款', '其他非流动资产', '非流动资产合计',
                                 '现金及存放中央银行款项', '存放同业和其它金融机构款项', '贵金属', '衍生金融资产',
                                 '应收分保未到期责任准备金', '应收分保未决赔款准备金', '应收分保寿险责任准备金',
                                 '应收分保长期健康险责任准备金', '存出保证金', '保户质押贷款', '存出资本保证金',
                                 '独立账户资产', '其中：客户资金存款', '其中：客户备付金', '其中:交易席位费',
                                 '应收款项类投资', '资产总计', '长期借款', '短期借款', '向中央银行借款',
                                 '吸收存款及同业存放', '拆入资金', '交易性金融负债', '应付票据', '应付账款', '预收款项',
                                 '卖出回购金融资产款', '应付手续费及佣金', '应付职工薪酬', '应交税费', '应付利息',
                                 '应付股利', '其他应付款', '预提费用', '递延收益', '应付短期债券', '应付分保账款',
                                 '保险合同准备金', '代理买卖证券款', '代理承销证券款', '一年内到期的非流动负债',
                                 '其他流动负债', '流动负债合计', '应付债券', '长期应付款', '专项应付款', '预计负债',
                                 '递延所得税负债', '递延收益-非流动负债', '其他非流动负债', '非流动负债合计',
                                 '同业和其它金融机构存放款项', '衍生金融负债', '吸收存款', '代理业务负债', '其他负债',
                                 '预收保费', '存入保证金', '保户储金及投资款', '未到期责任准备金', '未决赔款准备金',
                                 '寿险责任准备金', '长期健康险责任准备金', '独立账户负债', '其中:质押借款',
                                 '应付赔付款', '应付保单红利', '负债合计', '减:库存股', '一般风险准备',
                                 '外币报表折算差额', '未确认的投资损失', '少数股东权益',
                                 '股东权益合计(不含少数股东权益)', '股东权益合计(含少数股东权益)', '负债及股东权益总计',
                                 '长期应付职工薪酬', '其他综合收益', '其他权益工具', '其他权益工具(优先股)', '融出资金',
                                 '应收款项', '应付短期融资款', '应付款项', '持有待售的资产', '持有待售的负债']
        reDataBalance = reDataBalance.sort_values(by='TS股票代码')
        reDataBalance.to_csv(fssBalance, index=False, encoding='utf-8-sig')
        reDataIncome.columns = ['TS股票代码', '公告日期', '实际公告日期，即发生过数据变更的最终日期', '报告期', 'period',
                                '报告类型： 参考下表说明', '公司类型：1一般工商业 2银行 3保险 4证券', '基本每股收益',
                                '稀释每股收益', '营业总收入 (元，下同)', '营业收入', '利息收入', '已赚保费',
                                '手续费及佣金收入', '手续费及佣金净收入', '其他经营净收益', '加:其他业务净收益',
                                '保险业务收入', '减:分出保费', '提取未到期责任准备金', '其中:分保费收入',
                                '代理买卖证券业务净收入', '证券承销业务净收入', '受托客户资产管理业务净收入',
                                '其他业务收入', '加:公允价值变动净收益', '加:投资净收益',
                                '其中:对联营企业和合营企业的投资收益', '加:汇兑净收益', '营业总成本', '减:营业成本',
                                '减:利息支出', '减:手续费及佣金支出', '减:营业税金及附加', '减:销售费用', '减:管理费用',
                                '减:财务费用', '减:资产减值损失', '退保金', '赔付总支出', '提取保险责任准备金',
                                '保户红利支出', '分保费用', '营业支出', '减:摊回赔付支出', '减:摊回保险责任准备金',
                                '减:摊回分保费用', '其他业务成本', '营业利润', '加:营业外收入', '减:营业外支出',
                                '其中:减:非流动资产处置净损失', '利润总额', '所得税费用', '净利润(含少数股东损益)',
                                '净利润(不含少数股东损益)', '少数股东损益', '其他综合收益', '综合收益总额',
                                '归属于母公司(或股东)的综合收益总额', '归属于少数股东的综合收益总额', '息税前利润',
                                '息税折旧摊销前利润', '保险业务支出', '年初未分配利润', '可分配利润']
        reDataIncome = reDataIncome.sort_values(by='TS股票代码')
        reDataIncome.to_csv(fssIncome, index=False, encoding='utf-8-sig')
    except:
        reDataBalance.columns = ['TS股票代码', '公告日期', '实际公告日期', '报告期', 'period',
                                 '报表类型：见下方详细说明', '公司类型：1一般工商业 2银行 3保险 4证券', '期末总股本',
                                 '资本公积金 (元，下同)', '未分配利润', '盈余公积金', '专项储备', '货币资金',
                                 '交易性金融资产', '应收票据', '应收账款', '其他应收款', '预付款项', '应收股利',
                                 '应收利息', '存货', '长期待摊费用', '一年内到期的非流动资产', '结算备付金', '拆出资金',
                                 '应收保费', '应收分保账款', '应收分保合同准备金', '买入返售金融资产', '其他流动资产',
                                 '流动资产合计', '可供出售金融资产', '持有至到期投资', '长期股权投资', '投资性房地产',
                                 '定期存款', '其他资产', '长期应收款', '固定资产', '在建工程', '工程物资',
                                 '固定资产清理', '生产性生物资产', '油气资产', '无形资产', '研发支出', '商誉',
                                 '长期待摊费用', '递延所得税资产', '发放贷款及垫款', '其他非流动资产', '非流动资产合计',
                                 '现金及存放中央银行款项', '存放同业和其它金融机构款项', '贵金属', '衍生金融资产',
                                 '应收分保未到期责任准备金', '应收分保未决赔款准备金', '应收分保寿险责任准备金',
                                 '应收分保长期健康险责任准备金', '存出保证金', '保户质押贷款', '存出资本保证金',
                                 '独立账户资产', '其中：客户资金存款', '其中：客户备付金', '其中:交易席位费',
                                 '应收款项类投资', '资产总计', '长期借款', '短期借款', '向中央银行借款',
                                 '吸收存款及同业存放', '拆入资金', '交易性金融负债', '应付票据', '应付账款', '预收款项',
                                 '卖出回购金融资产款', '应付手续费及佣金', '应付职工薪酬', '应交税费', '应付利息',
                                 '应付股利', '其他应付款', '预提费用', '递延收益', '应付短期债券', '应付分保账款',
                                 '保险合同准备金', '代理买卖证券款', '代理承销证券款', '一年内到期的非流动负债',
                                 '其他流动负债', '流动负债合计', '应付债券', '长期应付款', '专项应付款', '预计负债',
                                 '递延所得税负债', '递延收益-非流动负债', '其他非流动负债', '非流动负债合计',
                                 '同业和其它金融机构存放款项', '衍生金融负债', '吸收存款', '代理业务负债', '其他负债',
                                 '预收保费', '存入保证金', '保户储金及投资款', '未到期责任准备金', '未决赔款准备金',
                                 '寿险责任准备金', '长期健康险责任准备金', '独立账户负债', '其中:质押借款',
                                 '应付赔付款', '应付保单红利', '负债合计', '减:库存股', '一般风险准备',
                                 '外币报表折算差额', '未确认的投资损失', '少数股东权益',
                                 '股东权益合计(不含少数股东权益)', '股东权益合计(含少数股东权益)', '负债及股东权益总计',
                                 '长期应付职工薪酬', '其他综合收益', '其他权益工具', '其他权益工具(优先股)', '融出资金',
                                 '应收款项', '应付短期融资款', '应付款项', '持有待售的资产', '持有待售的负债']
        reDataBalance = reDataBalance.sort_values(by='TS股票代码')
        reDataBalance.to_csv(fssBalance, index=False, encoding='utf-8-sig')
        reDataIncome.columns = ['TS股票代码', '公告日期', '实际公告日期，即发生过数据变更的最终日期', '报告期', 'period',
                                '报告类型： 参考下表说明', '公司类型：1一般工商业 2银行 3保险 4证券', '基本每股收益',
                                '稀释每股收益', '营业总收入 (元，下同)', '营业收入', '利息收入', '已赚保费',
                                '手续费及佣金收入', '手续费及佣金净收入', '其他经营净收益', '加:其他业务净收益',
                                '保险业务收入', '减:分出保费', '提取未到期责任准备金', '其中:分保费收入',
                                '代理买卖证券业务净收入', '证券承销业务净收入', '受托客户资产管理业务净收入',
                                '其他业务收入', '加:公允价值变动净收益', '加:投资净收益',
                                '其中:对联营企业和合营企业的投资收益', '加:汇兑净收益', '营业总成本', '减:营业成本',
                                '减:利息支出', '减:手续费及佣金支出', '减:营业税金及附加', '减:销售费用', '减:管理费用',
                                '减:财务费用', '减:资产减值损失', '退保金', '赔付总支出', '提取保险责任准备金',
                                '保户红利支出', '分保费用', '营业支出', '减:摊回赔付支出', '减:摊回保险责任准备金',
                                '减:摊回分保费用', '其他业务成本', '营业利润', '加:营业外收入', '减:营业外支出',
                                '其中:减:非流动资产处置净损失', '利润总额', '所得税费用', '净利润(含少数股东损益)',
                                '净利润(不含少数股东损益)', '少数股东损益', '其他综合收益', '综合收益总额',
                                '归属于母公司(或股东)的综合收益总额', '归属于少数股东的综合收益总额', '息税前利润',
                                '息税折旧摊销前利润', '保险业务支出', '年初未分配利润', '可分配利润']
        reDataIncome = reDataIncome.sort_values(by='TS股票代码')
        reDataIncome.to_csv(fssIncome, index=False, encoding='utf-8-sig')
        print("还有", "\n", xny - i, "个财务报表未下载", "当前完成股票代码是:", iCode)


# -------down_stk.xxx
# ---down_financial_data
def downFinancial():
    rss = ".\\topdown\\tmp\\"
    fss = rss + 'finacialdata.csv';
    print(fss);
    reData = pd.DataFrame(
        columns=['年度', '股票代码', '股票名称', '净资产收益率(%)', '净利率(%)', '毛利率(%)', '净利润(万元)',
                 '每股收益', '营业收入(百万元)', '每股主营业务收入(元)', '应收账款周转率(次)', '应收账款周转天数(天)',
                 '存货周转率(次)', '存货周转天数(天)', '流动资产周转率(次)', '流动资产周转天数(天)', '流动比率',
                 '速动比率', '现金比率', '利息支付倍数', '股东权益比率', '股东权益增长率'])
    for y in [1, 2, 3]:
        iYear = 2015 + y - 1
        dat = ts.get_profit_data(iYear, 4)
        dat.insert(0, '年度', iYear)
        dat1 = ts.get_operation_data(iYear, 4)
        dat = pd.merge(dat, dat1, how='outer', on=['code', 'name'])
        dat1 = ts.get_debtpaying_data(iYear, 4)
        dat = pd.merge(dat, dat1, how='outer', on=['code', 'name'])
        dat.columns = ['年度', '股票代码', '股票名称', '净资产收益率(%)', '净利率(%)', '毛利率(%)', '净利润(万元)',
                       '每股收益', '营业收入(百万元)', '每股主营业务收入(元)', '应收账款周转率(次)',
                       '应收账款周转天数(天)', '存货周转率(次)', '存货周转天数(天)', '流动资产周转率(次)',
                       '流动资产周转天数(天)', '流动比率', '速动比率', '现金比率', '利息支付倍数', '股东权益比率',
                       '股东权益增长率']
        reData = reData.append(dat)
    reData.to_csv(fss, index=True, encoding='gbk');


# -------down_stk.base
def down_stk_base():
    rss = ".\\topdown\\tmp\\"
    #
    fss = rss + 'stk_inx0.csv';
    print(fss);
    dat = ts.get_index()
    dat.to_csv(fss, index=False, encoding='gbk', date_format='str');

    # =========
    fss = rss + 'stk_base.csv';
    print(fss);
    dat = ts.get_stock_basics();
    dat.to_csv(fss, encoding='utf_8_sig', date_format='str');

    c20 = ['code', 'name', 'industry', 'area'];
    d20 = dat.loc[:, c20]
    d20['code'] = d20.index;

    fss = rss + 'stk_code.csv';
    print(fss);
    d20.to_csv(fss, index=False, encoding='gbk', date_format='str');
    #     现金流量
    #     fss=rss+'stk_cash.csv';print(fss);
    #     datcash = ts.get_cashflow_data(2017,3);
    #     dat=pd.merge(dat,datcash,how='left');
    #     datprofit=ts.get_profit_data(2017,3);
    #     dat=pd.merge(dat,datprofit,how='left');
    #     dattoday=ts.get_today_all();
    #     dat=pd.merge(dat,dattoday,how='left');
    #     dat.to_csv(fss,encoding='gbk',date_format='str');

    # sz50,上证50；hs300,沪深300；zz500，中证500
    fss = rss + 'stk_sz50.csv';
    print(fss);
    dat = ts.get_sz50s();
    if len(dat) > 3:
        dat.to_csv(fss, index=False, encoding='gbk', date_format='str');

    fss = rss + 'stk_hs300.csv';
    print(fss);
    dat = ts.get_hs300s();
    if len(dat) > 3:
        dat.to_csv(fss, index=False, encoding='gbk', date_format='str');

    fss = rss + 'stk_zz500.csv';
    print(fss);
    dat = ts.get_zz500s();
    if len(dat) > 3:
        dat.to_csv(fss, index=False, encoding='gbk', date_format='str');


# -------down_stk.inx.xxx


def down_stk_inx010(rdat, xcod, tim0):
    ''' 下载大盘指数数据,简版股票数据，可下载到1994年股市开市起
    【输入】
        xcod:指数代码
        rdat,数据文件目录
        tim0,数据起始时间
        

    '''
    xd = [];
    fss = rdat + xcod + '.csv';
    if tim0 == '': tim0 = '1994-01-01';
    # print('f,',fss)
    # -------------------
    xfg = os.path.exists(fss);
    xd0 = [];
    if xfg: xd0, tim0 = zdat.df_rdcsv_tim0(fss, 'date', tim0)

    #    
    print('\n', xfg, fss, ",", tim0);
    # -----------
    try:
        # xd=ts.get_h_data(xcod,start=tim0,index=True,end=None,retry_count=5,pause=1)     #Day9
        xdk = ts.get_k_data(xcod, index=True, start=tim0, end=None)
        xd = xdk
        # -------------
        if len(xd) > 0:
            if (len(xd0) > 0):
                xd = xdk[zsys.ohlcDVLst]
                xd = zdat.df_xappend(xd, xd0, 'date')
            # print('\nxd5\n',xd.head())
            xd = xd.sort_values(['date'], ascending=False);
            xd.to_csv(fss, index=False, encoding='gbk')
    except IOError:
        pass  # skip,error

    return xd


def down_stk_inx(rdat, finx):
    dinx = pd.read_csv(finx, encoding='gbk');
    print(finx);
    xn9 = len(dinx['code']);
    for i in range(xn9):
        # for xc,xtim0 in dinx['code'],dinx['tim0']:
        d5 = dinx.iloc[i]
        xc = d5['code'];
        xtim0 = d5['tim0']
        i += 1;
        code = "%06d" % xc
        print("\n", i, "/", xn9, "code,", code, xtim0)
        # ---
        down_stk_inx010(rdat, code, xtim0)


# -------down_stk.day.xxx


def down_stk010(rdat, xcod, xtyp):
    ''' 中国A股数据下载子程序
    【输入】
        xcod:股票代码
        rdat,数据文件目录
        xtyp (str)：k线数据模式，默认为D，日线
            D=日 W=周 M=月 ；5=5分钟 15=15分钟 ，30=30分钟 60=60分钟

    '''

    tim0, fss = '1994-01-01', rdat + xcod + '.csv'
    xfg = os.path.exists(fss);
    xd0 = [];
    xd = [];
    if xfg:
        xd0, tim0 = zdat.df_rdcsv_tim0(fss, 'date', tim0)

    print('\t', xfg, fss, ",", tim0)
    # -----------
    try:
        xdk = ts.get_k_data(xcod, index=False, start=tim0, end=None, ktype=xtyp);
        xd = xdk
        # -------------
        if len(xd) > 0:
            xd = xdk[zsys.ohlcDVLst]
            xd = zdat.df_xappend(xd, xd0, 'date')
            #
            xd = xd.sort_values(['date'], ascending=False);
            xd.to_csv(fss, index=False, encoding='utf-8-sig', date_format='string')
    except IOError:
        pass  # skip,error

    return xd, fss


def down_stk_all(rdat, finx, xtyp='D'):
    '''
    根据finx股票列表文件，下载所有，或追加日线数据
    自动去重，排序
    【输入】
        rdat,数据文件目录
        finx:股票代码文件
        xtyp (str)：k线数据模式，默认为D，日线
            D=日 W=周 M=月 ；5=5分钟 15=15分钟 ，30=30分钟 60=60分钟    
    
    '''
    stkPool = pd.read_csv(finx, encoding='gbk');
    print(finx);
    xn9 = len(stkPool['code']);
    for i, xc in enumerate(stkPool['code']):
        code = "%06d" % xc
        print("\n", i, "/", xn9, "code,", code)
        # ---
        down_stk010(rdat, code, xtyp);


# ------down__tick.xxx

def down_tick010(xcod, xtim, ftg):
    '''
    根据指定的日期，股票代码，数据文件名：ftg
    下载指定股票指定日期的ticks数据，并保存到ftg
    [输入]
        xcode，股票代码
        xtim，当前日期的字符串
        ftg，保存tick数据的文件名
    '''
    df, dn = [], 0
    try:
        df = ts.get_tick_data(xcod, date=xtim)  # print(df.head())
    except IOError:
        pass  # skip,error
    datFlag, dn = False, len(df);  # print('     n',dn,ftg) # 跳过无数据 日期
    # if zwt.xin(dn,0,9):print('n2',dn,ftg)
    if dn > 10:
        df['type'] = df['type'].str.replace(u'中性盘', 'norm');
        df['type'] = df['type'].str.replace(u'买盘', 'buy');
        df['type'] = df['type'].str.replace(u'卖盘', 'sell');
        df.to_csv(ftg, index=False, encoding='utf')
        datFlag = True
    #
    return datFlag, dn, df


def down_tickLib8tim(rs0, stkPool, xtim):
    '''
    下载指定日期，stkCodeLib包含的所有代码的tick历史分笔数据
    并转换成对应的分时数据：5/15/30/60 分钟
    数据文件保存在：对应的数据目录 \zwdat\tick\yyyy-mm\
        目录下，yyyy，是年份；mm，是月份
    运行时，会根据日期，股票代码，生成数据文件名：ftg
    [输入]
      rs0,保存tick数据的目录
      stkCodeLib，包含所有股票代码的pd数据表格
      xtim，当前日期，格式：yyyy-mm-dd
          '''
    # qx.xday0ChkFlag=False self.codeInx0k=-1
    # inx0,qx.codeNum=qx.codeInx,len(dinx['code']);
    s2 = xtim.split('-')
    mss = s2[0] + '-' + s2[1]
    rss = rs0 + mss + '/'
    xfg = os.path.exists(rss)
    if not xfg: os.mkdir(rss)
    #
    numNil, num_code = 0, len(stkPool)
    for i, xc in enumerate(stkPool['code']):
        code = "%06d" % xc;  # print("\n",i,"/",qx.codeNum,"code,",code)
        # code,qx.codeCnt=code,i
        # ---
        # ftg='%s%s_%s.csv'%(qx.rtickTimMon,code)
        ftg = '%s%s_%s.csv' % (rss, code, xtim);
        xfg = os.path.exists(ftg);
        if xfg:
            numNil = 0
        else:
            if numNil < 90:
                datFlag, dfNum, df = down_tick010(code, xtim, ftg)
                numNil = zt.iff2(datFlag, 0, numNil + 1)
                if dfNum == 3: numNil += 10;
            #
            print(xfg, datFlag, i, "/", num_code, ftg, numNil)
        #
        if numNil > 90: break
        # if i>3:break


def down_tickLib8tim_mul(rs0, stkPool, xtim0, xtim9):
    '''
    下载所有股票代码的所有tick历史分笔数据，按时间日期循环下载
    数据文件保存在：对应的数据目录 \zwdat\tick\yyyy-mm\
        目录下，yyyy，是年份；mm，是月份
    [输入]
      rs0,保存tick数据的目录
      stkCodeLib，包含所有股票代码的pd数据表格
      xtim0，起始日期，格式：yyyy-mm-dd
      xtim9，结束日期，格式：yyyy-mm-dd
      '''

    # xtick_down_init(qx,finx)
    # qx.xday0ChkFlag=False
    # print('r',qx.rdat,qx.rtickTim);
    #    self.rtickTimMon=self.rtickTim+'2010-01\\';  #   \zwDat\ticktim\  2012-01\
    nday = zt.timNDayStr(xtim9, xtim0) + 1
    tim0 = arrow.get(xtim0)
    print('t0,', tim0, nday)
    for tc in range(nday):
        # qx.DTxtim=qx.DTxtim0+dt.timedelta(days=tc)
        # qx.xdayInx,qx.xtimSgn=tc,qx.DTxtim.strftime('%Y-%m-%d');
        #
        #
        xtim = tim0.shift(days=tc)
        xtimSgn = xtim.format('YYYY-MM-DD')
        # print(tc,'#,xtim,',xtimSgn)
        print('\n', tc, '/', nday, xtimSgn)
        #
        # xtick_down8tim_codes(qx)
        down_tickLib8tim(rs0, stkPool, xtimSgn)


# ------------donw_min.real__

def down_min_real010(rdat, xcod, xtyp='5', fgIndex=False):
    ''' 下载大盘指数数据,简版股票数据，可下载到1994年股市开市起
    【输入】
        rdat,数据文件目录
        xcod:股票、指数代码
        finx:股票、指数代码文件
        xtyp (str)：k线数据模式，默认为D，日线
            D=日 W=周 M=月 ；5=5分钟 15=15分钟 ，30=30分钟 60=60分钟    
        fgIndex,指数下载模式；默认为 False，股票下载模式。
    
        

    '''
    xd = []
    xtim = arrow.now().format('YYYY-MM-DD')
    fss = rdat + xcod + '.csv';
    if fgIndex: fss = rdat + 'inx_' + xcod + '.csv';
    # print('f,',fss)
    print('\n', fss, ",", xtim);
    # -----------
    try:
        xd = ts.get_k_data(xcod, index=fgIndex, start=xtim, end=xtim, ktype=xtyp)
        # -------------
        if len(xd) > 0:
            xd = xd[zsys.ohlcDVLst]
            # print('\nxd5\n',xd.head())
            xd = xd.sort_values(['date'], ascending=True);
            xd = xd[xd.date > xtim]
            xd.to_csv(fss, index=False, encoding='gbk')
    except IOError:
        pass  # skip,error

    return xd


def down_min_all(rdat, finx, xtyp='5', fgIndex=False):
    '''
    根据finx列表文件，下载所有股票、指数实时数据
    【输入】
        rdat,数据文件目录
        finx:股票、指数代码文件
        xtyp (str)：k线数据模式，默认为D，日线
            D=日 W=周 M=月 ；5=5分钟 15=15分钟 ，30=30分钟 60=60分钟    
        fgIndex,指数下载模式；默认为 False，股票下载模式。
    
    
    '''
    stkPool = pd.read_csv(finx, encoding='gbk');
    print(finx);
    xn9 = len(stkPool['code']);
    for i, xc in enumerate(stkPool['code']):
        code = "%06d" % xc
        print("\n", i, "/", xn9, "code,", code)
        # ---
        down_min_real010(rdat, code, xtyp, fgIndex)
