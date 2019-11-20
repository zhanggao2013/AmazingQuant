# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2019/11/20
# @Author  : gao
# @File    : save_a_share_income.py
# @Project : AmazingQuant 
# ------------------------------


from datetime import datetime
import pandas as pd
import numpy as np

from mongoengine import Document
from mongoengine.fields import StringField, FloatField, IntField, DateTimeField
from AmazingQuant.data_center.mongo_connection import MongoConnect
from AmazingQuant.utils.transfer_field import get_field_str_list


class AShareIncome(Document):
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
    # 营业总收入
    tot_oper_rev = FloatField(required=True, null=True)
    # 营业收入
    oper_rev = FloatField(required=True, null=True)
    # 利息收入
    int_inc = FloatField(required=True, null=True)
    # 利息净收入
    net_int_inc = FloatField(required=True, null=True)
    # 已赚保费
    insur_prem_unearned = FloatField(required=True, null=True)
    # 手续费及佣金收入
    handling_chrg_comm_inc = FloatField(required=True, null=True)
    # 手续费及佣金净收入
    net_handling_chrg_comm_inc = FloatField(required=True, null=True)
    # 其他经营净收益
    net_inc_other_ops = FloatField(required=True, null=True)
    # 加:其他业务净收益
    plus_net_inc_other_bus = FloatField(required=True, null=True)
    # 保费业务收入
    prem_inc = FloatField(required=True, null=True)
    # 减:分出保费
    less_ceded_out_prem = FloatField(required=True, null=True)
    # 提取未到期责任准备金
    chg_unearned_prem_res = FloatField(required=True, null=True)
    # 其中:分保费收入
    incl_reinsurance_prem_inc = FloatField(required=True, null=True)
    # 代理买卖证券业务净收入
    net_inc_sec_trading_brok_bus = FloatField(required=True, null=True)
    # 证券承销业务净收入
    net_inc_sec_uw_bus = FloatField(required=True, null=True)
    # 受托客户资产管理业务净收入
    net_inc_ec_asset_mgmt_bus = FloatField(required=True, null=True)
    # 其他业务收入
    other_bus_inc = FloatField(required=True, null=True)
    # 加:公允价值变动净收益
    plus_net_gain_chg_fv = FloatField(required=True, null=True)
    # 加:投资净收益
    plus_net_invest_inc = FloatField(required=True, null=True)
    # 其中:对联营企业和合营企业的投资收益
    incl_inc_invest_assoc_jv_entp = FloatField(required=True, null=True)
    # 加:汇兑净收益
    plus_net_gain_fx_trans = FloatField(required=True, null=True)
    # 营业总成本
    tot_oper_cost = FloatField(required=True, null=True)
    # 减:营业成本
    less_oper_cost = FloatField(required=True, null=True)
    # 减:利息支出
    less_int_exp = FloatField(required=True, null=True)
    # 减:手续费及佣金支出
    less_handling_chrg_comm_exp = FloatField(required=True, null=True)
    # 减:营业税金及附加
    less_taxes_surcharges_ops = FloatField(required=True, null=True)
    # 减:销售费用
    less_selling_dist_exp = FloatField(required=True, null=True)
    # 减:管理费用
    less_gerl_admin_exp = FloatField(required=True, null=True)
    # 减:财务费用
    less_fin_exp = FloatField(required=True, null=True)
    # 减:资产减值损失
    less_impair_loss_assets = FloatField(required=True, null=True)
    # 退保金
    prepay_surr = FloatField(required=True, null=True)
    # 赔付总支出
    tot_claim_exp = FloatField(required=True, null=True)
    # 提取保险责任准备金
    chg_insur_cont_rsrv = FloatField(required=True, null=True)
    # 保户红利支出
    dvd_exp_insured = FloatField(required=True, null=True)
    # 分保费用
    reinsurance_exp = FloatField(required=True, null=True)
    # 营业支出
    oper_exp = FloatField(required=True, null=True)
    # 减:摊回赔付支出
    less_claim_recb_reinsurer = FloatField(required=True, null=True)
    # 减:摊回保险责任准备金
    less_ins_rsrv_recb_reinsurer = FloatField(required=True, null=True)
    # 减:摊回分保费用
    less_exp_recb_reinsurer = FloatField(required=True, null=True)
    # 其他业务成本
    other_bus_cost = FloatField(required=True, null=True)
    # 营业利润
    oper_profit = FloatField(required=True, null=True)
    # 加:营业外收入
    plus_non_oper_rev = FloatField(required=True, null=True)
    # 减:营业外支出
    less_non_oper_exp = FloatField(required=True, null=True)
    # 其中:减:非流动资产处置净损失
    il_net_loss_disp_noncur_asset = FloatField(required=True, null=True)
    # 利润总额
    tot_profit = FloatField(required=True, null=True)
    # 所得税
    inc_tax = FloatField(required=True, null=True)
    # 未确认投资损失
    unconfirmed_invest_loss = FloatField(required=True, null=True)
    # 净利润(含少数股东损益)
    net_profit_incl_min_int_inc = FloatField(required=True, null=True)
    # 净利润(不含少数股东损益)
    net_profit_excl_min_int_inc = FloatField(required=True, null=True)
    # 少数股东损益
    minority_int_inc = FloatField(required=True, null=True)
    # 其他综合收益
    other_compreh_inc = FloatField(required=True, null=True)
    # 综合收益总额
    tot_compreh_inc = FloatField(required=True, null=True)
    # 综合收益总额(母公司)
    tot_compreh_inc_parent_comp = FloatField(required=True, null=True)
    # 综合收益总额(少数股东)
    tot_compreh_inc_min_shrhldr = FloatField(required=True, null=True)
    # 息税前利润
    ebit = FloatField(required=True, null=True)
    # 息税折旧摊销前利润
    ebitda = FloatField(required=True, null=True)
    # 扣除非经常性损益后净利润（扣除少数股东损益）
    net_profit_after_ded_nr_lp = FloatField(required=True, null=True)
    # 国际会计准则净利润
    net_profit_under_intl_acc_sta = FloatField(required=True, null=True)
    # 公司类型代码
    comp_type_code = StringField(required=True, null=True)
    # 基本每股收益
    s_fa_eps_basic = FloatField(required=True, null=True)
    # 稀释每股收益
    s_fa_eps_diluted = FloatField(required=True, null=True)
    # 实际公告日期
    actual_ann_dt = IntField(required=True, null=True)
    # 保险业务支出
    insurance_expense = FloatField(required=True, null=True)
    # 营业利润差额(特殊报表科目)
    spe_bal_oper_profit = FloatField(required=True, null=True)
    # 营业利润差额(合计平衡项目)
    tot_bal_oper_profit = FloatField(required=True, null=True)
    # 利润总额差额(特殊报表科目)
    spe_bal_tot_profit = FloatField(required=True, null=True)
    # 利润总额差额(合计平衡项目)
    tot_bal_tot_profit = FloatField(required=True, null=True)
    # 净利润差额(特殊报表科目)
    spe_bal_net_profit = FloatField(required=True, null=True)
    # 净利润差额(合计平衡项目)
    tot_bal_net_profit = FloatField(required=True, null=True)
    # 年初未分配利润
    undistributed_profit = FloatField(required=True, null=True)
    # 调整以前年度损益
    adjlossgain_prevyear = FloatField(required=True, null=True)
    # 盈余公积转入
    transfer_from_surplusreserve = FloatField(required=True, null=True)
    # 住房周转金转入
    transfer_from_housingimprest = FloatField(required=True, null=True)
    # 其他转入
    transfer_from_others = FloatField(required=True, null=True)
    # 可分配利润
    distributable_profit = FloatField(required=True, null=True)
    # 提取法定盈余公积
    withdr_legalsurplus = FloatField(required=True, null=True)
    # 提取法定公益金
    withdr_legalpubwelfunds = FloatField(required=True, null=True)
    # 职工奖金福利
    workers_welfare = FloatField(required=True, null=True)
    # 提取企业发展基金
    withdr_buzexpwelfare = FloatField(required=True, null=True)
    # 提取储备基金
    withdr_reservefund = FloatField(required=True, null=True)
    # 可供股东分配的利润
    distributable_profit_shrhder = FloatField(required=True, null=True)
    # 应付优先股股利
    prfshare_dvd_payable = FloatField(required=True, null=True)
    # 提取任意盈余公积金
    withdr_othersurpreserve = FloatField(required=True, null=True)
    # 应付普通股股利
    comshare_dvd_payable = FloatField(required=True, null=True)
    # 转作股本的普通股股利
    capitalized_comstock_div = FloatField(required=True, null=True)
    # 公司ID
    s_info_compcode = StringField(required=True, null=True)
    # 扣除非经常性损益后的净利润(财务重要指标(更正前))
    net_after_ded_nr_lp_correct = FloatField(required=True, null=True)
    # 其他收益
    other_income = FloatField(required=True, null=True)
    # 备注
    memo = StringField(required=True, null=True)
    # 资产处置收益
    asset_disposal_income = FloatField(required=True, null=True)
    # 持续经营净利润
    continued_net_profit = FloatField(required=True, null=True)
    # 终止经营净利润
    end_net_profit = FloatField(required=True, null=True)
    # 信用减值损失
    credit_impairment_loss = FloatField(required=True, null=True)
    # 净敞口套期收益
    net_exposure_hedging_benefits = FloatField(required=True, null=True)
    # 研发费用
    rd_expense = FloatField(required=True, null=True)
    # 财务费用:利息费用
    stmnote_finexp = FloatField(required=True, null=True)
    # 财务费用:利息收入
    fin_exp_int_inc = FloatField(required=True, null=True)
    # 是否计算报表
    is_calculation = FloatField(required=True, null=True)

    meta = {'indexes': ['security_code', 'ann_dt', 'report_period', 'statement_type']}


class SaveIncome(object):
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

                doc = AShareIncome()
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
    data_path = '../../../../data/finance/ASHAREINCOME.csv'
    field_path = '../../config/field_a_share_income.txt'
    save_cash_flow_obj = SaveIncome(data_path, field_path)
    save_cash_flow_obj.save_a_share_cash_flow()
