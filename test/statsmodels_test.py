# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2020/4/19
# @Author  : gao
# @File    : statsmodels_test.py
# @Project : AmazingQuant
# ------------------------------
import numpy as np
import statsmodels.api as sm
num = 100
x = np.linspace(0, 50, num)
x1 = np.linspace(50, 100, num)
a = np.array([x, x1])
X = sm.add_constant(a)
y = np.linspace(50, 100, 2)
model = sm.OLS(X, y)
results = model.fit()

