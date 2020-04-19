# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2020/4/19
# @Author  : gao
# @File    : statsmodels_test.py
# @Project : AmazingQuant
# ------------------------------
import numpy as np
import pandas as pd
import statsmodels.api as sm
num = 100
x1 = np.linspace(0, 50, num)
x2 = np.linspace(50, 100, num)
e = np.ones(100)
a = np.array([x1, x2])
X_CL = pd.DataFrame({'coe1': x1, 'coe2': x2})
X_CL = sm.add_constant(X_CL)
y = np.linspace(500, -500, num)
model = sm.OLS(y, X_CL)
results = model.fit()
resid = results.resid
