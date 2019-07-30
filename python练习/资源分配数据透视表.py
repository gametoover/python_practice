# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 14:40:54 2019

@author: xh-32
"""
import pandas as pd

df1 =  pd.read_excel(r"C:\Users\xh-32\Desktop\资源分配.xlsx",header=0,sheet_name='Sheet1')
df2 =  pd.read_excel(r"C:\Users\xh-32\Desktop\邀约试听.xlsx",header=0,sheet_name='Sheet1')
#将咨询组名称修改和部门一样
df1.replace({'学规1部':'学习规划1部','学规2部':'学习规划2部'},inplace=True)

#将源数据剔除未分配资源，分配资源量和邀约试听量先进行数据透视，后合并到一起
df11 = df1[df1.staff_name != '\\N'].pivot_table('std_count',index='staff_name',columns='live_source',aggfunc='sum',margins=True,fill_value=0)
df22 = df2[df2.staff_name != '\\N'].pivot_table('std_count',index='staff_name',columns='live_source',aggfunc='sum',margins=True,fill_value=0)
staff_data = pd.merge(df11,df22,on='staff_name',how='outer')
staff_data.fillna(0,inplace = True)
print(staff_data)

#将源数据剔除未分配资源，分配资源量和邀约试听量先进行数据透视，后合并到一起
df12 =  df1.pivot_table('std_count',index=['group_name','live_source'],columns='is_flag',margins=True,fill_value=0,aggfunc='sum')
df22 =  df2.pivot_table('std_count',index=['group_form','live_source'],margins=True,fill_value=0,aggfunc='sum')
df22.index.names = ['group_name','live_source']
form_data = pd.merge(df12,df22,how = 'outer',left_index = True,right_index = True)
form_data.fillna(0,inplace = True)
print(form_data)