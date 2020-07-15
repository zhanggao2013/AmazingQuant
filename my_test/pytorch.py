# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2019/11/14
# @Author  : gao
# @File    : pytorch.py.py
# @Project : AmazingQuant
# ------------------------------

import numpy as np
import torch
import time

flag = torch.cuda.is_available()
print(flag)

ngpu = 1
# Decide which device we want to run on
device = torch.device("cuda:0" if (torch.cuda.is_available() and ngpu > 0) else "cpu")
# print(device)
# print(torch.cuda.get_device_name(0))

aa = torch.rand(10000, 10000).cuda()
bb = torch.rand(10000, 10000).cuda()
a = np.random.rand(10000, 10000)
b = np.random.rand(10000, 10000)
time1 = time.time()
# cc = aa * bb
aa1 = torch.cuda.ones((10000, 10000)).cuda()
time2 = time.time()
print(time2 - time1)
b1 = np.ones((10000, 10000))
# c = a * b
time3 = time.time()
print(time3 - time2)
