# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2019/11/21
# @Author  : gao
# @File    : field_finance_data.py
# @Project : AmazingQuant
# ------------------------------

from datetime import datetime

from mongoengine import Document
from mongoengine.fields import StringField, FloatField, IntField, DateTimeField


class AShareCashFlow(Document):
    """
    A股现金流量表
    """
    # 更新时间
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


class AShareIncome(Document):
    """
    A股利润表
    """
    # 更新时间
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


class AShareBalanceSheet(Document):
    """
    A股资产负债表
    """
    # 更新时间
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
    # 货币资金
    monetary_cap = FloatField(required=True, null=True)
    # 交易性金融资产
    tradable_fin_assets = FloatField(required=True, null=True)
    # 应收票据
    notes_rcv = FloatField(required=True, null=True)
    # 应收账款
    acct_rcv = FloatField(required=True, null=True)
    # 其他应收款
    oth_rcv = FloatField(required=True, null=True)
    # 预付款项
    prepay = FloatField(required=True, null=True)
    # 应收股利
    dvd_rcv = FloatField(required=True, null=True)
    # 应收利息
    int_rcv = FloatField(required=True, null=True)
    # 存货
    inventories = FloatField(required=True, null=True)
    # 消耗性生物资产
    consumptive_bio_assets = FloatField(required=True, null=True)
    # 待摊费用
    deferred_exp = FloatField(required=True, null=True)
    # 一年内到期的非流动资产
    non_cur_assets_due_within_1y = FloatField(required=True, null=True)
    # 结算备付金
    settle_rsrv = FloatField(required=True, null=True)
    # 拆出资金
    loans_to_oth_banks = FloatField(required=True, null=True)
    # 应收保费
    prem_rcv = FloatField(required=True, null=True)
    # 应收分保账款
    rcv_from_reinsurer = FloatField(required=True, null=True)
    # 应收分保合同准备金
    rcv_from_ceded_insur_cont_rsrv = FloatField(required=True, null=True)
    # 买入返售金融资产
    red_monetary_cap_for_sale = FloatField(required=True, null=True)
    # 其他流动资产
    oth_cur_assets = FloatField(required=True, null=True)
    # 流动资产合计
    tot_cur_assets = FloatField(required=True, null=True)
    # 可供出售金融资产
    fin_assets_avail_for_sale = FloatField(required=True, null=True)
    # 持有至到期投资
    held_to_mty_invest = FloatField(required=True, null=True)
    # 长期股权投资
    long_term_eqy_invest = FloatField(required=True, null=True)
    # 投资性房地产
    invest_real_estate = FloatField(required=True, null=True)
    # 定期存款
    time_deposits = FloatField(required=True, null=True)
    # 其他资产
    oth_assets = FloatField(required=True, null=True)
    # 长期应收款
    long_term_rec = FloatField(required=True, null=True)
    # 固定资产
    fix_assets = FloatField(required=True, null=True)
    # 在建工程
    const_in_prog = FloatField(required=True, null=True)
    # 工程物资
    proj_matl = FloatField(required=True, null=True)
    # 固定资产清理
    fix_assets_disp = FloatField(required=True, null=True)
    # 生产性生物资产
    productive_bio_assets = FloatField(required=True, null=True)
    # 油气资产
    oil_and_natural_gas_assets = FloatField(required=True, null=True)
    # 无形资产
    intang_assets = FloatField(required=True, null=True)
    # 开发支出
    r_and_d_costs = FloatField(required=True, null=True)
    # 商誉
    goodwill = FloatField(required=True, null=True)
    # 长期待摊费用
    long_term_deferred_exp = FloatField(required=True, null=True)
    # 递延所得税资产
    deferred_tax_assets = FloatField(required=True, null=True)
    # 发放贷款及垫款
    loans_and_adv_granted = FloatField(required=True, null=True)
    # 其他非流动资产
    oth_non_cur_assets = FloatField(required=True, null=True)
    # 非流动资产合计
    tot_non_cur_assets = FloatField(required=True, null=True)
    # 现金及存放中央银行款项
    cash_deposits_central_bank = FloatField(required=True, null=True)
    # 存放同业和其它金融机构款项
    asset_dep_oth_banks_fin_inst = FloatField(required=True, null=True)
    # 贵金属
    precious_metals = FloatField(required=True, null=True)
    # 衍生金融资产
    derivative_fin_assets = FloatField(required=True, null=True)
    # 代理业务资产
    agency_bus_assets = FloatField(required=True, null=True)
    # 应收代位追偿款
    subr_rec = FloatField(required=True, null=True)
    # 应收分保未到期责任准备金
    rcv_ceded_unearned_prem_rsrv = FloatField(required=True, null=True)
    # 应收分保未决赔款准备金
    rcv_ceded_claim_rsrv = FloatField(required=True, null=True)
    # 应收分保寿险责任准备金
    rcv_ceded_life_insur_rsrv = FloatField(required=True, null=True)
    # 应收分保长期健康险责任准备金
    rcv_ceded_lt_health_insur_rsrv = FloatField(required=True, null=True)
    # 存出保证金
    mrgn_paid = FloatField(required=True, null=True)
    # 保户质押贷款
    insured_pledge_loan = FloatField(required=True, null=True)
    # 存出资本保证金
    cap_mrgn_paid = FloatField(required=True, null=True)
    # 独立账户资产
    independent_acct_assets = FloatField(required=True, null=True)
    # 客户资金存款
    clients_cap_deposit = FloatField(required=True, null=True)
    # 客户备付金
    clients_rsrv_settle = FloatField(required=True, null=True)
    # 其中:交易席位费
    incl_seat_fees_exchange = FloatField(required=True, null=True)
    # 应收款项类投资
    rcv_invest = FloatField(required=True, null=True)
    # 资产总计
    tot_assets = FloatField(required=True, null=True)
    # 短期借款
    st_borrow = FloatField(required=True, null=True)
    # 向中央银行借款
    borrow_central_bank = FloatField(required=True, null=True)
    # 吸收存款及同业存放
    deposit_received_ib_deposits = FloatField(required=True, null=True)
    # 拆入资金
    loans_oth_banks = FloatField(required=True, null=True)
    # 交易性金融负债
    tradable_fin_liab = FloatField(required=True, null=True)
    # 应付票据
    notes_payable = FloatField(required=True, null=True)
    # 应付账款
    acct_payable = FloatField(required=True, null=True)
    # 预收款项
    adv_from_cust = FloatField(required=True, null=True)
    # 卖出回购金融资产款
    fund_sales_fin_assets_rp = FloatField(required=True, null=True)
    # 应付手续费及佣金
    handling_charges_comm_payable = FloatField(required=True, null=True)
    # 应付职工薪酬
    empl_ben_payable = FloatField(required=True, null=True)
    # 应交税费
    taxes_surcharges_payable = FloatField(required=True, null=True)
    # 应付利息
    int_payable = FloatField(required=True, null=True)
    # 应付股利
    dvd_payable = FloatField(required=True, null=True)
    # 其他应付款
    oth_payable = FloatField(required=True, null=True)
    # 预提费用
    acc_exp = FloatField(required=True, null=True)
    # 递延收益
    deferred_inc = FloatField(required=True, null=True)
    # 应付短期债券
    st_bonds_payable = FloatField(required=True, null=True)
    # 应付分保账款
    payable_to_reinsurer = FloatField(required=True, null=True)
    # 保险合同准备金
    rsrv_insur_cont = FloatField(required=True, null=True)
    # 代理买卖证券款
    acting_trading_sec = FloatField(required=True, null=True)
    # 代理承销证券款
    acting_uw_sec = FloatField(required=True, null=True)
    # 一年内到期的非流动负债
    non_cur_liab_due_within_1y = FloatField(required=True, null=True)
    # 其他流动负债
    oth_cur_liab = FloatField(required=True, null=True)
    # 流动负债合计
    tot_cur_liab = FloatField(required=True, null=True)
    # 长期借款
    lt_borrow = FloatField(required=True, null=True)
    # 应付债券
    bonds_payable = FloatField(required=True, null=True)
    # 长期应付款
    lt_payable = FloatField(required=True, null=True)
    # 专项应付款
    specific_item_payable = FloatField(required=True, null=True)
    # 预计负债
    provisions = FloatField(required=True, null=True)
    # 递延所得税负债
    deferred_tax_liab = FloatField(required=True, null=True)
    # 递延收益-非流动负债
    deferred_inc_non_cur_liab = FloatField(required=True, null=True)
    # 其他非流动负债
    oth_non_cur_liab = FloatField(required=True, null=True)
    # 非流动负债合计
    tot_non_cur_liab = FloatField(required=True, null=True)
    # 同业和其它金融机构存放款项
    liab_dep_oth_banks_fin_inst = FloatField(required=True, null=True)
    # 衍生金融负债
    derivative_fin_liab = FloatField(required=True, null=True)
    # 吸收存款
    cust_bank_dep = FloatField(required=True, null=True)
    # 代理业务负债
    agency_bus_liab = FloatField(required=True, null=True)
    # 其他负债
    oth_liab = FloatField(required=True, null=True)
    # 预收保费
    prem_received_adv = FloatField(required=True, null=True)
    # 存入保证金
    deposit_received = FloatField(required=True, null=True)
    # 保户储金及投资款
    insured_deposit_invest = FloatField(required=True, null=True)
    # 未到期责任准备金
    unearned_prem_rsrv = FloatField(required=True, null=True)
    # 未决赔款准备金
    out_loss_rsrv = FloatField(required=True, null=True)
    # 寿险责任准备金
    life_insur_rsrv = FloatField(required=True, null=True)
    # 长期健康险责任准备金
    lt_health_insur_v = FloatField(required=True, null=True)
    # 独立账户负债
    independent_acct_liab = FloatField(required=True, null=True)
    # 其中:质押借款
    incl_pledge_loan = FloatField(required=True, null=True)
    # 应付赔付款
    claims_payable = FloatField(required=True, null=True)
    # 应付保单红利
    dvd_payable_insured = FloatField(required=True, null=True)
    # 负债合计
    tot_liab = FloatField(required=True, null=True)
    # 股本
    cap_stk = FloatField(required=True, null=True)
    # 资本公积金
    cap_rsrv = FloatField(required=True, null=True)
    # 专项储备
    special_rsrv = FloatField(required=True, null=True)
    # 盈余公积金
    surplus_rsrv = FloatField(required=True, null=True)
    # 未分配利润
    undistributed_profit = FloatField(required=True, null=True)
    # 减:库存股
    less_tsy_stk = FloatField(required=True, null=True)
    # 一般风险准备
    prov_nom_risks = FloatField(required=True, null=True)
    # 外币报表折算差额
    cnvd_diff_foreign_curr_stat = FloatField(required=True, null=True)
    # 未确认的投资损失
    unconfirmed_invest_loss = FloatField(required=True, null=True)
    # 少数股东权益
    minority_int = FloatField(required=True, null=True)
    # 股东权益合计(不含少数股东权益)
    tot_shrhldr_eqy_excl_min_int = FloatField(required=True, null=True)
    # 股东权益合计(含少数股东权益)
    tot_shrhldr_eqy_incl_min_int = FloatField(required=True, null=True)
    # 负债及股东权益总计
    tot_liab_shrhldr_eqy = FloatField(required=True, null=True)
    # 公司类型代码
    comp_type_code = StringField(required=True, null=True)
    # 实际公告日期
    actual_ann_dt = IntField(required=True, null=True)
    # 流动资产差额(特殊报表科目)
    spe_cur_assets_diff = FloatField(required=True, null=True)
    # 流动资产差额(合计平衡项目)
    tot_cur_assets_diff = FloatField(required=True, null=True)
    # 非流动资产差额(特殊报表科目)
    spe_non_cur_assets_diff = FloatField(required=True, null=True)
    # 非流动资产差额(合计平衡项目)
    tot_non_cur_assets_diff = FloatField(required=True, null=True)
    # 资产差额(特殊报表科目)
    spe_bal_assets_diff = FloatField(required=True, null=True)
    # 资产差额(合计平衡项目)
    tot_bal_assets_diff = FloatField(required=True, null=True)
    # 流动负债差额(特殊报表科目)
    spe_cur_liab_diff = FloatField(required=True, null=True)
    # 流动负债差额(合计平衡项目)
    tot_cur_liab_diff = FloatField(required=True, null=True)
    # 非流动负债差额(特殊报表科目)
    spe_non_cur_liab_diff = FloatField(required=True, null=True)
    # 非流动负债差额(合计平衡项目)
    tot_non_cur_liab_diff = FloatField(required=True, null=True)
    # 负债差额(特殊报表科目)
    spe_bal_liab_diff = FloatField(required=True, null=True)
    # 负债差额(合计平衡项目)
    tot_bal_liab_diff = FloatField(required=True, null=True)
    # 股东权益差额(特殊报表科目)
    spe_bal_shrhldr_eqy_diff = FloatField(required=True, null=True)
    # 股东权益差额(合计平衡项目)
    tot_bal_shrhldr_eqy_diff = FloatField(required=True, null=True)
    # 负债及股东权益差额(特殊报表项目)
    spe_bal_liab_eqy_diff = FloatField(required=True, null=True)
    # 负债及股东权益差额(合计平衡项目)
    tot_bal_liab_eqy_diff = FloatField(required=True, null=True)
    # 长期应付职工薪酬
    lt_payroll_payable = FloatField(required=True, null=True)
    # 其他综合收益
    other_comp_income = FloatField(required=True, null=True)
    # 其他权益工具
    other_equity_tools = FloatField(required=True, null=True)
    # 其他权益工具:优先股
    other_equity_tools_p_shr = FloatField(required=True, null=True)
    # 融出资金
    lending_funds = FloatField(required=True, null=True)
    # 应收款项
    accounts_receivable = FloatField(required=True, null=True)
    # 应付短期融资款
    st_financing_payable = FloatField(required=True, null=True)
    # 应付款项
    payables = FloatField(required=True, null=True)
    # 公司ID
    s_info_compcode = StringField(required=True, null=True)
    # 期末总股本
    tot_shr = FloatField(required=True, null=True)
    # 持有待售的资产
    hfs_assets = FloatField(required=True, null=True)
    # 持有待售的负债
    hfs_sales = FloatField(required=True, null=True)
    # 以摊余成本计量的金融资产
    fin_assets_cost_sharing = FloatField(required=True, null=True)
    # 以公允价值计量且其变动计入其他综合收益的金融资产
    fin_assets_fair_value = FloatField(required=True, null=True)
    # 合同资产
    contractual_assets = FloatField(required=True, null=True)
    # 合同负债
    contract_liabilities = FloatField(required=True, null=True)
    # 应收票据及应收账款
    accounts_receivable_bill = FloatField(required=True, null=True)
    # 应付票据及应付账款
    accounts_payable = FloatField(required=True, null=True)
    # 其他应收款(合计)（元）
    oth_rcv_tot = FloatField(required=True, null=True)
    # 固定资产(合计)(元)
    stm_bs_tot = FloatField(required=True, null=True)
    # 在建工程(合计)(元)
    const_in_prog_tot = FloatField(required=True, null=True)
    # 其他应付款(合计)(元)
    oth_payable_tot = FloatField(required=True, null=True)
    # 长期应付款(合计)(元)
    lt_payable_tot = FloatField(required=True, null=True)
    # 债权投资(元)
    debt_investment = FloatField(required=True, null=True)
    # 其他债权投资(元)
    other_debt_investment = FloatField(required=True, null=True)
    # 其他权益工具投资(元)
    other_equity_investment = FloatField(required=True, null=True)
    # 其他非流动金融资产(元)
    other_illiquidfinancial_assets = FloatField(required=True, null=True)
    # 其他权益工具:永续债(元)
    other_sustainable_bond = FloatField(required=True, null=True)
    # 应收款项融资
    receivables_financing = FloatField(required=True, null=True)
    # 使用权资产
    right_use_assets = FloatField(required=True, null=True)
    # 租赁负债
    lease_liab = FloatField(required=True, null=True)




