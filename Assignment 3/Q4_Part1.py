
# coding: utf-8

# 1. The first step is always take a look at the data
# 2. Clean and reshape dataframe to the format that I can start working<br>
#     \* two marjor formats:<br>
#     \* Won/Nominated for xxx. Another x wins & y nominations <br>
#     \* x wins & y nominations
# 3. The 'Awards_won' and 'Awards_nomitated' column is a sum of both Won/Nominated for and another (...).

# ### Step 1

# In[1]:

from pandas import Series, DataFrame
import pandas as pd
import os
import numpy as np


# In[2]:

df_origin = pd.read_csv(os.getcwd() + '/Data/movies_awards.csv')
df_origin.head(1)


# In[3]:

df_origin.ix[:,'Awards'].dropna().head(50)


# In[4]:

df_origin.ix[1221,'Awards']


# ### Step 2

# Narrow columns

# In[5]:

df_filter = df_origin[['Title','Awards']].dropna()
df_filter.head(10)


# In[6]:

df_filter['Awards'].str.split('.').str.len().max()


# In[7]:

df_filter['Awards'].str.split('.').str.len().min()


# Conclusion: it's easier to check contents manually since the max layer is 3

# In[8]:

df_filter['1st step'] = df_filter['Awards'].str.split('.').str.get(0)


# In[9]:

df_filter['2nd step'] = df_filter['Awards'].str.split('.').str.get(1)


# In[10]:

df_filter['3rd step'] = df_filter['Awards'].str.split('.').str.get(2)


# Check content for '3rd step'

# In[11]:

df_filter['3rd step'][df_filter['3rd step'].notnull()].unique()


# Remove '3rd step' since it only contains ''

# In[12]:

del df_filter['3rd step']


# In[13]:

df_filter.head(8)


# My desired layout is:
# 
# Column1|Column2
# -------|-------
# Nominated for ...| Another ...
# Won ...| Another...
# (Blank/0)|x wins & y nominations
# (Blank/0)|x wins / y nominations
# 
# But this can't be done directly in dataframe (fillna function can only fill cell with a fix value), so I'm going to use append function in Series

# In[14]:

Series_3rd_step_1 = df_filter['1st step'][df_filter['2nd step']=='']


# In[15]:

Series_3rd_step_2 = df_filter['2nd step'][df_filter['2nd step']!='']


# In[16]:

Series_3rd_step_2.append(Series_3rd_step_1).size


# In[17]:

df_filter['3rd step'] = Series_3rd_step_2.append(Series_3rd_step_1)


# In[18]:

df_filter['4th step'] = df_filter['1st step'][df_filter['2nd step']!='']


# In[19]:

df_filter.head(8)


# In[20]:

df_filter.columns.tolist()


# In[21]:

df_step1 = df_filter[['Title','Awards','3rd step','4th step']]
df_step1.head(8)


# Now I can start getting data from this dataframe
# ### Step 3

# Work with '3rd step' first

# In[22]:

s_split = df_step1['3rd step'].str.split('&')


# In[23]:

s_split.head(3)


# In[24]:

s_split.str.len().unique()


# Create 'Awards_Won_Raw' column

# In[25]:

s_win = s_split.str[0].str.contains('win') #bool Series


# In[26]:

df_d = df_step1['3rd step'][s_win].str.split('(\d+)').str[1]


# In[27]:

df_step1['Awards_Won_Raw'] = df_d


# In[28]:

df_step1 = df_step1.fillna(0)
df_step1.head(8)


# Create 'Awards_Nominated_Raw' column

# In[29]:

s_nominate_1 = df_step1['3rd step'].str.split('&').str[0].str.contains('nomina')


# In[30]:

s_nominate_2 = df_step1['3rd step'].str.split('&').str[1].str.contains('nomina').fillna(False)


# In[31]:

s_nominate = s_nominate_1 | s_nominate_2


# In[32]:

df_step1['Awards_Nominated_Raw'] = df_step1['3rd step'][s_nominate].str.split('(\d+ nomination)').str[1].str.split('(\d+)').str[1]


# In[33]:

df_step1 = df_step1.fillna(0)
df_step1.head(5)


# Now work with '4th step' column <br>
#     \* do not assume nomination and win share the same name set

# Create '_nominated' columns

# In[34]:

pd_w_nomi = df_step1.copy()


# In[35]:

s_nomi = df_step1['4th step'][df_step1['4th step'].str.contains('Nomi').fillna(False)] # bool Series


# In[36]:

s_award_name = s_nomi.str.split('for').str[1].str.split('(\d+ )').str[2].unique()


# In[37]:

column_names = set([x[:-1] for x in [x.split()[0] for x in s_award_name] if x.endswith('s')] + [x for x in [x.split()[0] for x in s_award_name] if x[-1]!='s'])


# In[38]:

column_names


# Assign value to each column Series

# In[39]:

s_search = s_nomi.str.split('for').str[1].str.split('(\d+ )')


# In[40]:

s_nomi_prime = s_search.str[1][s_search.str[2].str.contains('Prime')]


# In[41]:

pd_w_nomi['Primetime_Awards_nominated'] = s_nomi_prime


# In[42]:

s_nomi_BAFTA = s_search.str[1][s_search.str[2].str.contains('BAFTA')]


# In[43]:

pd_w_nomi['BAFTA_Awards_nominated'] = s_nomi_BAFTA


# In[44]:

s_nomi_Oscar = s_search.str[1][s_search.str[2].str.contains('Oscar')]


# In[45]:

pd_w_nomi['Oscar_nominated'] = s_nomi_Oscar


# In[46]:

s_nomi_GG = s_search.str[1][s_search.str[2].str.contains('Golden')].str.strip()


# In[47]:

pd_w_nomi['Golden_Awards_nominated'] = s_nomi_GG


# In[48]:

pd_w_nomi = pd_w_nomi.fillna(0)
pd_w_nomi.ix[24]


# 告一段落，新建一个copy <br>
# 然后在这个copy上计算真正的Awards_Nominated value

# In[49]:

pd_w_nomi_copy = pd_w_nomi.copy()


# In[50]:

col_list = list(pd_w_nomi_copy)


# In[51]:

col_list[4]


# In[52]:

pd_w_nomi_copy.head(1)


# In[53]:

pd_w_nomi_copy =pd.concat([pd_w_nomi[col_list[:4]], pd_w_nomi[col_list[4:]].astype(int)], axis=1)


# In[54]:

pd_w_nomi_copy['Awards_nominated'] = pd_w_nomi_copy[col_list[5:]].sum(axis=1)


# In[55]:

pd_w_nomi_copy.ix[24]


# Create '_won' columns <br>
# 从这儿开始算won的数字

# In[56]:

pd_w_won = pd_w_nomi_copy.copy()


# In[57]:

s_won = pd_w_won['4th step'][pd_w_won['4th step'].str.contains('Won').fillna(False)]


# In[58]:

s_won.head(5)


# In[59]:

s_award_name = s_won.str.split('(\d+ )').str[2].unique()


# In[60]:

s_award_name


# In[61]:

column_names = set([x[:-1] for x in [x.split()[0] for x in s_award_name] if x.endswith('s')] + [x for x in [x.split()[0] for x in s_award_name] if x[-1]!='s'])


# In[62]:

column_names


# Assign values to columns

# In[63]:

s_search = s_won.str.split('(\d+)')


# In[64]:

s_won_prime = s_search.str[1][s_search.str[2].str.contains('Prime')]


# In[65]:

pd_w_won['Primetime_Awards_won'] = s_won_prime


# In[66]:

s_won_Oscar = s_search.str[1][s_search.str[2].str.contains('Oscar')]


# In[67]:

pd_w_won['Oscar_Awards_won'] = s_won_Oscar


# In[68]:

s_won_GG= s_search.str[1][s_search.str[2].str.contains('Golden')]


# In[69]:

pd_w_won['Golden_Awards_won'] = s_won_GG


# In[70]:

pd_w_won = pd_w_won.fillna(0)


# In[71]:

pd_w_won.head(3)


# In[72]:

pd_w_won_copy = pd_w_won.copy()


# In[73]:

col_list = list(pd_w_won_copy)


# In[74]:

col_list


# In[75]:

col_list = ['Title',
 'Awards',
 '3rd step',
 '4th step',
 'Awards_Nominated_Raw',
 'Primetime_Awards_nominated',
 'BAFTA_Awards_nominated',
 'Oscar_nominated',
 'Golden_Awards_nominated',
 'Awards_nominated',
 'Awards_Won_Raw',
 'Primetime_Awards_won',
 'Oscar_Awards_won',
 'Golden_Awards_won']


# In[76]:

pd_w_won_copy = pd_w_won_copy[col_list]


# In[ ]:




# In[77]:

pd_w_won_copy.head(1)


# In[78]:

pd_w_won_copy.ix[50]


# In[79]:

col_list[9:13]


# In[80]:

pd_w_won_copy =pd.concat([pd_w_won_copy[col_list[:4]], pd_w_won_copy[col_list[4:]].astype(int)], axis=1)


# In[81]:

pd_w_won_copy['Awards_won'] = pd_w_won_copy[col_list[10:]].sum(axis=1)


# In[82]:

pd_w_won_copy.ix[50]


# In[ ]:




# In[83]:

pd_w_won_copy2 = pd_w_won_copy


# In[84]:

pd_w_won_copy2.drop(['3rd step','4th step','Awards_Nominated_Raw','Awards_Won_Raw'], axis=1).head(20)


# In[ ]:




# Last step is to switch column orders and output to csv

# In[87]:

l_out = pd_w_won_copy2.columns.tolist()
l_out


# In[88]:

l_out = ['Title',
 'Awards',
 'Awards_won',
 'Awards_nominated',
 'Primetime_Awards_nominated',
 'BAFTA_Awards_nominated',
 'Oscar_nominated',
 'Golden_Awards_nominated',
 'Primetime_Awards_won',
 'Oscar_Awards_won',
 'Golden_Awards_won'
 ]


# In[90]:

df_output = pd_w_won_copy2[l_out]
df_output.head(25)


# In[92]:

df_output.to_csv(os.getcwd()+'/Q4_Part1_output.csv')


# In[ ]:



