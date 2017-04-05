
# coding: utf-8

# Basically, this question is asking for: <br>
# The last table before doing a groupby'Job Family', it should only contain part of the employees who are :<br>
# In calendar year <br>
# Average overtime > average Salaries * 0.05 <br>
# <br>
# ### My steps are basically same as above thinking.<br>
# 1. take a look at the data, filter and narrow down and columns
# 2. find out the employees whos average overtime > average salaies * 0.5
# 3. create a new dataframe using above employees' identity id
# 4. merge with filtered table on employees' identity id
# 5. groupby Job Family and find mean values

# In[1]:

from pandas import Series, DataFrame
import pandas as pd
import os
import numpy as np


# In[2]:

df_origin = pd.read_csv(os.getcwd() + '/Data/employee_compensation.csv')
df_origin.ix[2]


# \>1

# In[3]:

df_1 = df_origin[df_origin['Year Type']=='Calendar']
df_1.head(4)


# In[4]:

df_1 = df_1[['Employee Identifier','Job Family','Salaries','Overtime','Total Benefits','Total Compensation']]
df_1.head(4)


# In[16]:

df_1['Employee Identifier'].unique().shape


# \>2

# In[7]:

df_2 = df_1.groupby('Employee Identifier').mean()
df_2.head(3)


# In[8]:

df_2 = df_2[df_2['Overtime'] > df_2['Salaries']*0.05]
df_2.head(3)


# In[9]:

df_2.index.get_values()


# \>3

# In[11]:

df_3 = pd.DataFrame(pd.Series(data=df_2.index.get_values(), name='Employee Identifier'))
df_3.head(3)


# In[12]:

df_3.shape


# \>4

# In[20]:

df_merged= pd.merge(df_1, df_3, on='Employee Identifier', how="right")
df_merged.head(3)


# In[21]:

df_merged['Employee Identifier'].unique().shape


# Number of unique employee identifiers is same as df_3

# \>5

# In[25]:

df_output = df_merged[['Job Family','Total Benefits','Total Compensation']].groupby('Job Family').mean().sort_values(by='Total Benefits')
df_output.head(5)


# In[27]:

df_output.to_csv(os.getcwd()+'/Q2_Part2_output.csv')


# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:



