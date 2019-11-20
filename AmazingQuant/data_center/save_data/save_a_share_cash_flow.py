# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2019/11/18
# @Author  : gao
# @File    : save_a_share_cash_flow.py
# @Project : AmazingQuant 
# ------------------------------

from datetime import datetime
import pandas as pd
import numpy as np

from mongoengine import Document
from mongoengine.fields import StringField, FloatField, IntField, DateTimeField
from AmazingQuant.data_center.mongo_connection import MongoConnect
from AmazingQuant.utils.transfer_field import get_field_str_list


class AShareCashFlow(Document):
    """
    A股现金流量表
    """
    update_date = DateTimeField(default=datetime.utcnow())
    # 证券代码
    security_code = StringField(required=True, null=True)
    # 公告日期
    ann_dt = IntField(required=True, null=True)
    # 报告期
    report_period = IntField(required=True, null=True)
    # 报表类型
    statement_type = IntField(required=True, null=True)
    # 货币代码
    crncy_code = StringField(required=True, null=True)
    # 销售商品、提供劳务收到的现金
    cash_recp_sg_and_rs = FloatField(required=True, null=True)
    # 收到的税费返还
    recp_tax_rends = FloatField(required=True, null=True)
    # 客户存款和同业存放款项净增加额
    net_incr_dep_cob = FloatField(required=True, null=True)
    # 向中央银行借款净增加额
    net_incr_loans_central_bank = FloatField(required=True, null=True)
    # 向其他金融机构拆入资金净增加额
    net_incr_fund_borr_ofi = FloatField(required=True, null=True)
    # 收到原保险合同保费取得的现金
    cash_recp_prem_orig_inco = FloatField(required=True, null=True)
    # 保户储金净增加额
    net_incr_insured_dep = FloatField(required=True, null=True)
    # 收到再保业务现金净额
    net_cash_received_reinsu_bus = FloatField(required=True, null=True)
    # 处置交易性金融资产净增加额
    net_incr_disp_tfa = FloatField(required=True, null=True)
    # 收取利息和手续费净增加额
    net_incr_int_handling_chrg = FloatField(required=True, null=True)
    # 处置可供出售金融资产净增加额
    net_incr_disp_faas = FloatField(required=True, null=True)
    # 拆入资金净增加额
    net_incr_loans_other_bank = FloatField(required=True, null=True)
    # 回购业务资金净增加额
    net_incr_repurch_bus_fund = FloatField(required=True, null=True)
    # 收到其他与经营活动有关的现金
    other_cash_recp_ral_oper_act = FloatField(required=True, null=True)
    # 经营活动现金流入小计
    stot_cash_inflows_oper_act = FloatField(required=True, null=True)
    # 购买商品、接受劳务支付的现金
    cash_pay_goods_purch_serv_rec = FloatField(required=True, null=True)
    # 支付给职工以及为职工支付的现金
    cash_pay_beh_empl = FloatField(required=True, null=True)
    # 支付的各项税费
    pay_all_typ_tax = FloatField(required=True, null=True)
    # 客户贷款及垫款净增加额
    net_incr_clients_loan_adv = FloatField(required=True, null=True)
    # 存放央行和同业款项净增加额
    net_incr_dep_cbob = FloatField(required=True, null=True)
    # 支付原保险合同赔付款项的现金
    cash_pay_claims_orig_inco = FloatField(required=True, null=True)
    # 支付手续费的现金
    handling_chrg_paid = FloatField(required=True, null=True)
    # 支付保单红利的现金
    comm_insur_plcy_paid = FloatField(required=True, null=True)
    # 支付其他与经营活动有关的现金
    other_cash_pay_ral_oper_act = FloatField(required=True, null=True)
    # 经营活动现金流出小计
    stot_cash_outflows_oper_act = FloatField(required=True, null=True)
    # 经营活动产生的现金流量净额
    net_cash_flows_oper_act = FloatField(required=True, null=True)
    # 收回投资收到的现金
    cash_recp_disp_withdrwl_invest = FloatField(required=True, null=True)
    # 取得投资收益收到的现金
    cash_recp_return_invest = FloatField(required=True, null=True)
    # 处置固定资产、无形资产和其他长期资产收回的现金净额
    net_cash_recp_disp_fiolta = FloatField(required=True, null=True)
    # 处置子公司及其他营业单位收到的现金净额
    net_cash_recp_disp_sobu = FloatField(required=True, null=True)
    # 收到其他与投资活动有关的现金
    other_cash_recp_ral_inv_act = FloatField(required=True, null=True)
    # 投资活动现金流入小计
    stot_cash_inflows_inv_act = FloatField(required=True, null=True)
    # 购建固定资产、无形资产和其他长期资产支付的现金
    cash_pay_acq_const_fiolta = FloatField(required=True, null=True)
    # 投资支付的现金
    cash_paid_invest = FloatField(required=True, null=True)
    # 取得子公司及其他营业单位支付的现金净额
    net_cash_pay_aquis_sobu = FloatField(required=True, null=True)
    # 支付其他与投资活动有关的现金
    other_cash_pay_ral_inv_act = FloatField(required=True, null=True)
    # 质押贷款净增加额
    net_incr_pledge_loan = FloatField(required=True, null=True)
    # 投资活动现金流出小计
    stot_cash_outflows_inv_act = FloatField(required=True, null=True)
    # 投资活动产生的现金流量净额
    net_cash_flows_inv_act = FloatField(required=True, null=True)
    # 吸收投资收到的现金
    cash_recp_cap_contrib = FloatField(required=True, null=True)
    # 其中:子公司吸收少数股东投资收到的现金
    incl_cash_rec_saims = FloatField(required=True, null=True)
    # 取得借款收到的现金
    cash_recp_borrow = FloatField(required=True, null=True)
    # 发行债券收到的现金
    proc_issue_bonds = FloatField(required=True, null=True)
    # 收到其他与筹资活动有关的现金
    other_cash_recp_ral_fnc_act = FloatField(required=True, null=True)
    # 筹资活动现金流入小计
    stot_cash_inflows_fnc_act = FloatField(required=True, null=True)
    # 偿还债务支付的现金
    cash_prepay_amt_borr = FloatField(required=True, null=True)
    # 分配股利、利润或偿付利息支付的现金
    cash_pay_dist_dpcp_int_exp = FloatField(required=True, null=True)
    # 其中:子公司支付给少数股东的股利、利润
    incl_dvd_profit_paid_sc_ms = FloatField(required=True, null=True)
    # 支付其他与筹资活动有关的现金
    other_cash_pay_ral_fnc_act = FloatField(required=True, null=True)
    # 筹资活动现金流出小计
    stot_cash_outflows_fnc_act = FloatField(required=True, null=True)
    # 筹资活动产生的现金流量净额
    net_cash_flows_fnc_act = FloatField(required=True, null=True)
    # 汇率变动对现金的影响
    eff_fx_flu_cash = FloatField(required=True, null=True)
    # 现金及现金等价物净增加额
    net_incr_cash_cash_equ = FloatField(required=True, null=True)
    # 期初现金及现金等价物余额
    cash_cash_equ_beg_period = FloatField(required=True, null=True)
    # 期末现金及现金等价物余额
    cash_cash_equ_end_period = FloatField(required=True, null=True)
    # 净利润
    net_profit = FloatField(required=True, null=True)
    # 未确认投资损失
    unconfirmed_invest_loss = FloatField(required=True, null=True)
    # 加:资产减值准备
    plus_prov_depr_assets = FloatField(required=True, null=True)
    # 固定资产折旧、油气资产折耗、生产性生物资产折旧
    depr_fa_coga_dpba = FloatField(required=True, null=True)
    # 无形资产摊销
    amort_intang_assets = FloatField(required=True, null=True)
    # 长期待摊费用摊销
    amort_lt_deferred_exp = FloatField(required=True, null=True)
    # 待摊费用减少
    decr_deferred_exp = FloatField(required=True, null=True)
    # 预提费用增加
    incr_acc_exp = FloatField(required=True, null=True)
    # 处置固定、无形资产和其他长期资产的损失
    loss_disp_fiolta = FloatField(required=True, null=True)
    # 固定资产报废损失
    loss_scr_fa = FloatField(required=True, null=True)
    # 公允价值变动损失
    loss_fv_chg = FloatField(required=True, null=True)
    # 财务费用
    fin_exp = FloatField(required=True, null=True)
    # 投资损失
    invest_loss = FloatField(required=True, null=True)
    # 递延所得税资产减少
    decr_deferred_inc_tax_assets = FloatField(required=True, null=True)
    # 递延所得税负债增加
    incr_deferred_inc_tax_liab = FloatField(required=True, null=True)
    # 存货的减少
    decr_inventories = FloatField(required=True, null=True)
    # 经营性应收项目的减少
    decr_oper_payable = FloatField(required=True, null=True)
    # 经营性应付项目的增加
    incr_oper_payable = FloatField(required=True, null=True)
    # 其他
    others = FloatField(required=True, null=True)
    # 间接法-经营活动产生的现金流量净额
    im_net_cash_flows_oper_act = FloatField(required=True, null=True)
    # 债务转为资本
    conv_debt_into_cap = FloatField(required=True, null=True)
    # 一年内到期的可转换公司债券
    conv_corp_bonds_due_within_1y = FloatField(required=True, null=True)
    # 融资租入固定资产
    fa_fnc_leases = FloatField(required=True, null=True)
    # 现金的期末余额
    end_bal_cash = FloatField(required=True, null=True)
    # 减:现金的期初余额
    less_beg_bal_cash = FloatField(required=True, null=True)
    # 加:现金等价物的期末余额
    plus_end_bal_cash_equ = FloatField(required=True, null=True)
    # 减:现金等价物的期初余额
    less_beg_bal_cash_equ = FloatField(required=True, null=True)
    # 间接法-现金及现金等价物净增加额
    im_net_incr_cash_cash_equ = FloatField(required=True, null=True)
    # 企业自由现金流量(fcff)
    free_cash_flow = FloatField(required=True, null=True)
    # 公司类型代码
    comp_type_code = StringField(required=True, null=True)
    # 实际公告日期
    actual_ann_dt = IntField(required=True, null=True)
    # 经营活动现金流入差额(特殊报表科目)
    spe_bal_cash_inflows_oper = FloatField(required=True, null=True)
    # 经营活动现金流入差额(合计平衡项目)
    tot_bal_cash_inflows_oper = FloatField(required=True, null=True)
    # 经营活动现金流出差额(特殊报表科目)
    spe_bal_cash_outflows_oper = FloatField(required=True, null=True)
    # 经营活动现金流出差额(合计平衡项目)
    tot_bal_cash_outflows_oper = FloatField(required=True, null=True)
    # 经营活动产生的现金流量净额差额(合计平衡项目)
    tot_bal_netcash_outflows_oper = FloatField(required=True, null=True)
    # 投资活动现金流入差额(特殊报表科目)
    spe_bal_cash_inflows_inv = FloatField(required=True, null=True)
    # 投资活动现金流入差额(合计平衡项目)
    tot_bal_cash_inflows_inv = FloatField(required=True, null=True)
    # 投资活动现金流出差额(特殊报表科目)
    spe_bal_cash_outflows_inv = FloatField(required=True, null=True)
    # 投资活动现金流出差额(合计平衡项目)
    tot_bal_cash_outflows_inv = FloatField(required=True, null=True)
    # 投资活动产生的现金流量净额差额(合计平衡项目)
    tot_bal_netcash_outflows_inv = FloatField(required=True, null=True)
    # 筹资活动现金流入差额(特殊报表科目)
    spe_bal_cash_inflows_fnc = FloatField(required=True, null=True)
    # 筹资活动现金流入差额(合计平衡项目)
    tot_bal_cash_inflows_fnc = FloatField(required=True, null=True)
    # 筹资活动现金流出差额(特殊报表科目)
    spe_bal_cash_outflows_fnc = FloatField(required=True, null=True)
    # 筹资活动现金流出差额(合计平衡项目)
    tot_bal_cash_outflows_fnc = FloatField(required=True, null=True)
    # 筹资活动产生的现金流量净额差额(合计平衡项目)
    tot_bal_netcash_outflows_fnc = FloatField(required=True, null=True)
    # 现金净增加额差额(特殊报表科目)
    spe_bal_netcash_inc = FloatField(required=True, null=True)
    # 现金净增加额差额(合计平衡项目)
    tot_bal_netcash_inc = FloatField(required=True, null=True)
    # 间接法-经营活动现金流量净额差额(特殊报表科目)
    spe_bal_netcash_equ_undir = FloatField(required=True, null=True)
    # 间接法-经营活动现金流量净额差额(合计平衡项目)
    tot_bal_netcash_equ_undir = FloatField(required=True, null=True)
    # 间接法-现金净增加额差额(特殊报表科目)
    spe_bal_netcash_inc_undir = FloatField(required=True, null=True)
    # 间接法-现金净增加额差额(合计平衡项目)
    tot_bal_netcash_inc_undir = FloatField(required=True, null=True)
    # 公司id
    s_info_compcode = StringField(required=True, null=True)
    # 拆出资金净增加额
    s_dismantle_capital_add_net = FloatField(required=True, null=True)
    # 是否计算报表
    is_calculation = FloatField(required=True, null=True)

    meta = {'indexes': ['security_code', 'ann_dt', 'report_period', 'statement_type']}


class SaveCashFlow(object):
    def __init__(self, data_path, field_path):
        self.data_df = pd.read_csv(data_path, low_memory=False)
        self.field_is_str_list = get_field_str_list(field_path)

    def save_a_share_cash_flow(self):
        database = 'stock_base_data'
        with MongoConnect(database):
            doc_list = []
            for index, row in self.data_df.iterrows():
                row_dict = dict(row)
                row_dict['security_code'] = row_dict['WIND_CODE']
                row_dict.pop('S_INFO_WINDCODE')
                row_dict.pop('OBJECT_ID')
                row_dict.pop('WIND_CODE')

                doc = AShareCashFlow()
                for key, value in row_dict.items():
                    if key.lower() in self.field_is_str_list:
                        if key.lower() in ['ann_dt', 'report_period', 'statement_type', 'actual_ann_dt']:
                            if np.isnan(value):
                                setattr(doc, key.lower(), -1)
                            else:
                                setattr(doc, key.lower(), int(value))
                        else:
                            setattr(doc, key.lower(), str(value))
                    else:
                        setattr(doc, key.lower(), value)
                doc_list.append(doc)
                if len(doc_list) > 999:
                    AShareCashFlow.objects.insert(doc_list)
                    doc_list = []
            else:
                AShareCashFlow.objects.insert(doc_list)


if __name__ == '__main__':
    data_path = '../../../../data/finance/AShareCashFlow.csv'
    field_path = '../../config/field_a_share_cash_flow.txt'
    save_cash_flow_obj = SaveCashFlow(data_path, field_path)
    save_cash_flow_obj.save_a_share_cash_flow()
