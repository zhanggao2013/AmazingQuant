# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2019/11/14
# @Author  : gao
# @File    : pytorch.py.py
# @Project : AmazingQuant
# ------------------------------

import torch
flag = torch.cuda.is_available()
print(flag)

ngpu= 1
# Decide which device we want to run on
device = torch.device("cuda:0" if (torch.cuda.is_available() and ngpu > 0) else "cpu")
print(device)
print(torch.cuda.get_device_name(0))
print(torch.rand(3,3).cuda())
