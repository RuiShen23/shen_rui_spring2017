
# coding: utf-8

# This question is so straightforward and self-explanatory... 

# In[1]:

from pandas import Series, DataFrame
import pandas as pd
import os
import numpy as np


# In[2]:

df_origin = pd.read_csv(os.getcwd() + '/Data/cricket_matches.csv')
df_origin.head(5)


# In[3]:

df_origin.ix[1]


# In[4]:

df_filter = df_origin[['home','winner','innings1','innings1_runs','innings2','innings2_runs']]


# In[5]:

df_step1 = df_filter[df_filter['home']==df_filter['winner']]
df_step1.head(5)


# why warning?????????

# In[6]:

df_step1['wins_1'] = df_step1['innings1']==df_step1['winner']
df_step1.head(5)


# In[7]:

df_step1['wins_2'] = df_step1['innings2']==df_step1['winner']
df_step1.head(5)


# In[8]:

df_step1[['home','innings1_runs','innings2_runs','wins_1','wins_2']].head(5)


# In[9]:

df_step1['score'] = df_step1['innings1_runs']*df_step1['wins_1'] + df_step1['innings2_runs']*df_step1['wins_2']


# In[10]:

df_output = df_step1[['home','score']].groupby('home').mean()
df_output.head(3)


# In[11]:

df_output.to_csv(os.getcwd()+'/Q3_Part1_output.csv')


# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:



