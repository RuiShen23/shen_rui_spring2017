
# coding: utf-8

# 1. **Filter columns**: only get the ones I need (keep NaN for now, they won't be counted anyway)
# 2. **Filter date** using *pd.to_datetime('Series').dt.[year/month]*: only keep the ones happened in 2016
# 3. **Add columns** 'MONTH', 'MANHATTAN' and rename column 'BOROUGH' to 'NYC'
# 4. **Group by 'MONTH'**, get the count Series for 'NYC', do sum to 'MANHATTAN' because it's a bool Series
# 5. **Put two Series** back in dataframe, add 'PERCENTAGE' column

# ### Step 1

# In[1]:

from pandas import Series, DataFrame
import pandas as pd
import os


# In[2]:

df_origin = pd.read_csv(os.getcwd() + '/Data/vehicle_collisions.csv')
df_origin.head(5)


# In[3]:

df_step1 = df_origin[['DATE','BOROUGH']]
df_step1.head(5)


# ### Step 2

# In[4]:

df_step2 = df_step1[pd.to_datetime(df_step1['DATE']).dt.year==2016]
df_step2.head(5)


# In[6]:

type(pd.to_datetime(df_step2['DATE']))


# ### Step 3
# I found this method Series.dt.strftime('%b'), this follows same rule as Datetime module

# In[7]:

df_step3 = df_step2.copy()


# In[11]:

df_step3.insert(loc=1, column='MONTH', value=pd.to_datetime(df_step3['DATE']).dt.strftime('%b'))


# In[12]:

df_step3.head(5)


# In[13]:

df_step3 = df_step3.drop('DATE', axis=1)
df_step3.head(5)


# In[14]:

df_step3['MANHATTAN'] = df_step3['BOROUGH'].values==['MANHATTAN']
df_step3.head(5)


# In[15]:

df_step3 = df_step3.rename(columns={'BOROUGH':'NYC'})
df_step3.head(5)


# In[16]:

df_step3['NYC'] = df_step3['NYC'].fillna(value="NOT IN RECORD")
df_step3.head(5)


# ### Step 4

# In[17]:

series_nyc = df_step3.groupby('MONTH')['NYC'].count()


# In[18]:

series_nyc.head(3)


# In[19]:

series_manhattan = df_step3.groupby('MONTH')['MANHATTAN'].sum()


# In[20]:

series_manhattan.head(3)


# ### Part 5

# In[21]:

df_output = DataFrame(series_manhattan, columns=['MANHATTAN'])
df_output['NYC'] = series_nyc
df_output['MANHATTAN'] = df_output['MANHATTAN'].astype(int)
df_output.head(5)


# In[22]:

df_output['PERCENTAGE'] = df_output['MANHATTAN']/df_output['NYC']


# In[23]:

df_output.head(5)


# In[24]:

df_output.to_csv(os.getcwd()+ '/Q1_Part1_output.csv')


# In[ ]:




# Since I've already finished, I don't want to go back fix the month order...the way to fix is DO NOT remove number month column....

# In[ ]:



