# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2023/11/28
# @Author  : gao
# @File    : factor_analysis_report.py 
# @Project : AmazingQuant 
# ------------------------------

from AmazingQuant.constant import LocalDataFolderName, RightsAdjustment
from AmazingQuant.config.local_data_path import LocalDataPath
from AmazingQuant.utils.get_data import get_local_data
from AmazingQuant.data_center.api_data.get_kline import GetKlineData

from AmazingQuant.strategy_model.multi_factor.single_factor_analysis.ic_analysis import IcAnalysis
from AmazingQuant.strategy_model.multi_factor.single_factor_analysis.regression_analysis import RegressionAnalysis
from AmazingQuant.strategy_model.multi_factor.single_factor_analysis.stratification_analysis import StratificationAnalysis


class FactorAnalysis(object):
    def __init__(self, factor, factor_name, benchmark_code='000300.SH'):
        self.factor = factor
        self.factor_name = factor_name
        self.benchmark_code = benchmark_code

        kline_object = GetKlineData()
        market_data = kline_object.cache_all_stock_data(dividend_type=RightsAdjustment.BACKWARD.value, field=['close'])
        self.market_close_data = kline_object.get_market_data(market_data, field=['close'])

        # 指数行情，沪深300代替
        all_index_data = kline_object.cache_all_index_data()
        self.benchmark_df = kline_object.get_market_data(all_index_data, stock_code=[self.benchmark_code],
                                                         field=['close']).to_frame(name='close')

    def ic_analysis(self, corr_method='spearmanr'):
        """
        corr_method = {‘pearsonr’,:皮尔逊相关系数，非排名类因子
                    ‘spearmanr’:斯皮尔曼相关系数，排名类因子}
        """
        ic_analysis_obj = IcAnalysis(self.factor, self.factor_name, self.market_close_data)
        ic_analysis_obj.cal_ic_df(method=corr_method)
        ic_analysis_obj.cal_ic_indicator()
        ic_analysis_obj.save_ic_analysis_result(path, factor_name)

    def regression_analysis(self, wls_weight_method='float_value_inverse', nlags=10):
        """
        以流通市值平方根或者流通市值的倒数为权重做WLS（加权最小二乘法估计）,
        wls_weight_method = {‘float_value_inverse’：流通市值的倒数,
                             ‘float_value_square_root’：流通市值的倒数}

        nlags: 因子收益率的自相关系数acf和偏自相关系数pacf，的阶数
        """
        regression_analysis_obj = RegressionAnalysis(self.factor, self.factor_name,
                                                     self.market_close_data, self.benchmark_df)
        regression_analysis_obj.cal_factor_return(method=wls_weight_method)
        regression_analysis_obj.cal_t_value_statistics()
        regression_analysis_obj.cal_net_analysis()
        regression_analysis_obj.cal_acf(nlags=nlags)

        regression_analysis_obj.save_regression_analysis_result(path, factor_name)

    def stratification_analysis(self, group_num=5):
        """
        group_num，分组组数
        """
        stratification_analysis_obj = StratificationAnalysis(self.factor, self.factor_name, group_num=group_num)
        stratification_analysis_obj.group_analysis()


if __name__ == '__main__':
    factor_name = 'factor_ma5'
    path = LocalDataPath.path + LocalDataFolderName.FACTOR.value + '/' + factor_name + '/'
    factor_ma5 = get_local_data(path, factor_name + '_pre' + '.h5')
    factor_ma5 = factor_ma5.iloc[:-50, :]

    factor_analysis_obj = FactorAnalysis(factor_ma5, factor_name)
    print('-'*20, 'ic_analysis',  '-'*20)
    factor_analysis_obj.ic_analysis()
    print('-'*20, 'regression_analysis',  '-'*20)
    factor_analysis_obj.regression_analysis()
    print('-'*20, 'stratification_analysis',  '-'*20)
    factor_analysis_obj.stratification_analysis()

