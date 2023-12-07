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


class FactorAnalysis(object):
    def __init__(self, factor, factor_name):
        self.factor = factor
        self.factor_name = factor_name

    def ic_analysis(self):
        market_close_data = GetKlineData().cache_all_stock_data(dividend_type=RightsAdjustment.BACKWARD.value,
                                                                field=['close'])['close']
        ic_analysis_obj = IcAnalysis(self.factor, self.factor_name, market_close_data)
        ic_analysis_obj.cal_ic_df(method='spearmanr')
        ic_analysis_obj.cal_ic_indicator()
        ic_analysis_obj.save_ic_analysis_result(path, factor_name)


if __name__ == '__main__':
    factor_name = 'factor_ma5'
    path = LocalDataPath.path + LocalDataFolderName.FACTOR.value + '/' + factor_name + '/'
    factor_ma5 = get_local_data(path, factor_name + '_pre' + '.h5')
    factor_ma5 = factor_ma5.iloc[:-50, :]

    factor_analysis_obj = FactorAnalysis(factor_ma5, factor_name)
    factor_analysis_obj.ic_analysis()

