# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2020/3/31
# @Author  : gao
# @File    : orthogonalization.py
# @Project : AmazingQuant
# ------------------------------
"""
因子正交化
(1)施密特正交
(2)规范正交
(3)对称正交
可仅仅实现对称正交
"""
from datetime import datetime

import numpy as np
import pandas as pd
from sympy.matrices import Matrix, GramSchmidt

from AmazingQuant.constant import LocalDataFolderName
from AmazingQuant.config.local_data_path import LocalDataPath
from AmazingQuant.data_center.api_data.get_data import get_local_data


class FactorOrthogonalization(object):
    def __init__(self, factor_data=None):
        """
        :param factor_data: Dataframe, multiindex: factor name--time_tag, columns: stock code
        """
        self.factor_data = pd.concat(factor_data, names=['factor_name'])
        self.time_tag_index = self.factor_data.index.levels[1].unique()
        self.factor_name = self.factor_data.index.levels[0].unique()
        # dict, key；factor name, value: factor_data_dataframe(因子原格式)
        self.factor_orthogonalization_data = {}

    def cal_orthogonalization(self, method='Symmetric'):
        """
        GramSchmidt，施密特正交
        Symmetric，对称正交
        Canonical，规范正交
        :param method:
        :return:
        """
        self.factor_orthogonalization_data = pd.DataFrame({})
        for time_tag in self.time_tag_index:
            time_tag_data = self.factor_data[self.factor_data.index.get_level_values(1) == time_tag]
            time_tag_data = time_tag_data.reset_index(level='time_tag', drop=True)

            if method == 'Symmetric':
                # 计算重叠矩阵
                overlapping_matrix = (time_tag_data.shape[1] - 1) * np.cov(time_tag_data.astype(float))
                # 计算特征值和特征向量
                eigenvalue, eigenvector = np.linalg.eig(overlapping_matrix)
                # 转换为np中的矩阵
                eigenvector = np.mat(eigenvector)

                # 对特征根元素开(-0.5)指数, 获取过渡矩阵transition_matrix
                transition_matrix = np.dot(np.dot(eigenvector, np.mat(np.diag(eigenvalue ** (-0.5)))), eigenvector.T)
                orthogonalization = np.dot(time_tag_data.T.values, transition_matrix)
                # 对因子数据赋值
                orthogonalization_df = pd.DataFrame(orthogonalization.T,
                                                    index=pd.MultiIndex.from_product([time_tag_data.index, [time_tag]]),
                                                    columns=time_tag_data.columns)
                self.factor_orthogonalization_data = self.factor_orthogonalization_data.append(orthogonalization_df)

            elif method == 'GramSchmidt':
                # 施密特正交化
                orthogonalization = GramSchmidt([Matrix(col) for col in time_tag_data.values])
                orthogonalization_df = pd.DataFrame(np.array(orthogonalization),
                                                    index=pd.MultiIndex.from_product([time_tag_data.index, [time_tag]]),
                                                    columns=time_tag_data.columns)
                self.factor_orthogonalization_data = self.factor_orthogonalization_data.append(orthogonalization_df)

            elif method == 'Canonical':
                # 计算重叠矩阵
                overlapping_matrix = (time_tag_data.shape[1] - 1) * np.cov(time_tag_data.astype(float))
                # 获取特征值和特征向量
                eigenvalue, eigenvector = np.linalg.eig(overlapping_matrix)
                # 转换为np中的矩阵
                eigenvector = np.mat(eigenvector)
                transition_matrix = np.dot(eigenvector, np.mat(np.diag(eigenvalue ** (-0.5))))
                orthogonalization = np.dot(time_tag_data.T.values, transition_matrix)
                orthogonalization_df = pd.DataFrame(orthogonalization.T,
                                                    index=pd.MultiIndex.from_product([time_tag_data.index, [time_tag]]),
                                                    columns=time_tag_data.columns)
                self.factor_orthogonalization_data = self.factor_orthogonalization_data.append(orthogonalization_df)
        self.factor_orthogonalization_data = {i: self.factor_orthogonalization_data.loc[(i, slice(None)), :]
                                              for i in self.factor_name}
        for i in self.factor_orthogonalization_data:
            self.factor_orthogonalization_data[i].index = self.factor_orthogonalization_data[i].index.droplevel(0)


if __name__ == '__main__':
    path = LocalDataPath.path + LocalDataFolderName.FACTOR.value + '/'
    factor_ma5 = get_local_data(path, 'factor_ma5.h5')
    # 指数数据不全，需要删一部分因子数据
    factor_ma5 = factor_ma5[factor_ma5.index < datetime(2020, 1, 1)]
    factor_ma10 = get_local_data(path, 'factor_ma10.h5')
    # 指数数据不全，需要删一部分因子数据
    factor_ma10 = factor_ma10[factor_ma10.index < datetime(2020, 1, 1)]
    factor_data = {'factor_ma5': factor_ma5, 'factor_ma10': factor_ma10}

    factor_orthogonalization_obj = FactorOrthogonalization(factor_data)
    factor_orthogonalization_obj.cal_orthogonalization()
