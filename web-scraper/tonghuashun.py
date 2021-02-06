# -*- coding: UTF-8 -*-
import numpy as np
import pandas as pd

pd.set_option('display.max_rows',500)
pd.set_option('display.max_columns',500)
pd.set_option('display.width',1000)
data = np.loadtxt('./data/tonghuashun.csv',encoding='utf-8', dtype=np.str, delimiter=',', skiprows=1)
pd_data = pd.read_csv('./data/tonghuashun.csv', delimiter=',')
pd_data.sort_index(axis=1, ascending=True)
print(pd_data.head(10))

