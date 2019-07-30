to# -*- coding: utf-8 -*-
"""
Created on Fri Jan 18 19:08:59 2019
"""


import pandas as pd 
import numpy as np 
import pymysql 

#从mysql中将统计好的数据导入，后关闭
db = pymysql.connect(host = '10.10.8.1',port = 3906,user = 'pangbin',password = 'D0423jkds2#dsj22',db = 'bi_eduboss_xinghuo')
cursor = db.cursor()
sql = ' select * from tmp_pb_py_finance_monthly'
cursor.execute(sql)
data = cursor.fetchall()
field = cursor.description
db.close()

#将列名添加到DataFrame中，重新设置索引
columns_name = [field[i][0] for i in range(len(field))]
finance_df = pd.DataFrame(list(data),columns = columns_name )
finance_df = finance_df.sort_values(by=['branch','sum_year','sum_month'])
finance_df['sum_time'] = finance_df['sum_year'].map(str) + finance_df['sum_month'].map(lambda x : "0" + str(x) if len(str(x)) < 2 else x ).map(str)
finance_df['sum_time'] = finance_df.sum_time.astype(int)
finance_df['refund_rate'] = finance_df['refund_rate'].apply(lambda x :format(x,'.0%'))
finance_df['charge_rate'] = finance_df['charge_rate'].apply(lambda x:format(x,'.0%'))

this_month_finance_df = finance_df[(finance_df.sum_year == 2018) & (finance_df.sum_month == 12)]
#this_month_finance_df['refund_rate'] = this_month_finance_df['refund_rate'].apply(lambda x :format(x,'.0%'))
#this_month_finance_df['charge_rate'] = this_month_finance_df['charge_rate'].apply(lambda x :format(x,'.0%'))











