# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2023/10/25
# @Author  : gao
# @File    : plotly_test.py 
# @Project : AmazingQuant 
# ------------------------------
import plotly.graph_objs as go
import plotly.offline as offline
import numpy as np

# 示例数据
np.random.seed(42)
list1 = np.random.rand(50).tolist()
list2 = np.random.rand(50).tolist()
list3 = np.random.rand(50).tolist()

# 创建折线图
trace1 = go.Scatter(y=list1, mode='lines', name='List 1')
trace2 = go.Scatter(y=list2, mode='lines', name='List 2')
trace3 = go.Scatter(y=list3, mode='lines', name='List 3')

data = [trace1, trace2, trace3]

# 定义图表布局
layout = go.Layout(
    title='Interactive Line Plot of Float Lists',
    xaxis=dict(title='X-Axis'),
    yaxis=dict(title='Y-Axis')
)

# 创建图表对象
fig = go.Figure(data=data, layout=layout)

# 保存图表为HTML文件
offline.plot(fig, filename='interactive_line_plot.html', auto_open=False)