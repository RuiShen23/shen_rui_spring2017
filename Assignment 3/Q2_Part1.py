
# coding: utf-8

# I guess the difficulties for this question is multi-index...？<br>
# The key point is do not do multi-index at the beginning, this will only return the corret layout, but won't be available for soring afterwards.<br>
# The correct way to do it is to: 
# 1. **group by Organization Group** first
# 2. **apply Total Compensation sum to Department**

# In[1]:

from pandas import Series, DataFrame
import pandas as pd
import os
import numpy as np


# In[2]:

df_origin = pd.read_csv(os.getcwd() + '/Data/employee_compensation.csv')
df_origin.head(5)


# In[3]:

df_filter = df_origin[['Organization Group','Department','Total Compensation']]
df_filter.head(5)


# In[4]:

df_step1 = df_filter.groupby('Organization Group')


# In[5]:

def sort_amount(group, key):
    totals = group.groupby(key)['Total Compensation'].mean()
    return totals.sort_values(ascending=False)


# In[6]:

Series_tc = df_step1.apply(sort_amount, 'Department')
Series_tc


# In[7]:

pd.DataFrame(Series_tc)


# In[11]:

pd.DataFrame(Series_tc).to_csv(os.getcwd()+'/Q2_Part1_output.csv')


# Alternative way **using lambda**:<br>
# For each organization group in groupby object, group by department again <br>
# Calculate the mean value of total compensation for each department and sort by value <br>

# In[8]:

df_filter.groupby('Organization Group').apply(lambda x: x.groupby('Department')['Total Compensation'].mean().sort_values(ascending=False))


# In[ ]:



