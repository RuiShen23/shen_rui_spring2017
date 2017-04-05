
# coding: utf-8

# step 1 <br>
#     1. Take a look at my dataset and only keep useful columns
#     2. Remove NaN rows in BOROUGH column
#     3. Select year>=2015 //performed a simply check and nothing need to be done
# step2 <br>
#     4. For each row，check vehicle type, cars_involved = max_vehicle_type - 1
#     5. Add a column "NUMBER_OF_VECHICLES_INVOLVED"
# step3 <br>
#     6. Base on the number of "NUMBER_OF_VECHICLES_INVOLVED", create following new columns:<br>
#     ("ONE_VEHICLE_INVOLVED","TWO_VEHICLES_INVOLVED","THREE_VEHICLES_INVOLVED","MORE_VEHICLES_INVOLVED")
#     7. Groupby"BOROUGH" and find the sum

# In[1]:

from pandas import Series, DataFrame
import pandas as pd
import os
import numpy as np


# In[2]:

df_origin = pd.read_csv(os.getcwd() + '/Data/vehicle_collisions.csv')
df_origin.head(5)


# In[3]:

df_origin.ix[477691]


# In[4]:

df_filter = df_origin[df_origin['BOROUGH'].notnull()]
df_filter.head(3)


# In[5]:

df_filter1 = df_filter[['DATE','BOROUGH','VEHICLE 1 TYPE','VEHICLE 2 TYPE','VEHICLE 3 TYPE','VEHICLE 4 TYPE','VEHICLE 5 TYPE']]
df_filter1.head(5)


# In[6]:

pd.to_datetime(df_filter1['DATE']).dt.year.unique()


# In[7]:

del df_filter1['DATE']
df_filter1.head(5)


# In[8]:

series_count = df_filter1.T.notnull().sum() -1


# In[9]:

series_count.head(5)


# In[10]:

df_filter1.T.notnull().sum().head(5)


# In[11]:

df_step2 = df_filter1.drop(df_filter1.columns[[1,2,3,4,5]], axis=1)


# In[12]:

df_step2['NUMBER_OF_VECHICLES_INVOLVED'] = series_count
df_step2.head(5)


# In[13]:

df_step3 = df_step2.copy()


# In[14]:

df_step3['ONE_VEHICLE_INVOLVED'] = df_step3['NUMBER_OF_VECHICLES_INVOLVED']==1
df_step3.head(5)


# In[15]:

df_step3['TWO_VEHICLES_INVOLVED'] = df_step3['NUMBER_OF_VECHICLES_INVOLVED']==2
df_step3.head(5)


# In[16]:

df_step3['THREE_VEHICLES_INVOLVED'] = df_step3['NUMBER_OF_VECHICLES_INVOLVED']==3
df_step3.head(5)


# In[17]:

df_step3['MORE_VEHICLES_INVOLVED'] = df_step3['NUMBER_OF_VECHICLES_INVOLVED'] > 3
df_step3.head(5)


# In[18]:

df_step3['ZERO_VEHICLE_INVOLVED'] = df_step3['NUMBER_OF_VECHICLES_INVOLVED'] == 0
df_step3.head(5)


# In[19]:

df_output = df_step3.groupby('BOROUGH')
df_output.sum()


# In[20]:

df_output.to_csv(os.getcwd()+'/Q1_Part2_output.csv')

