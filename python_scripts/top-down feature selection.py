
# coding: utf-8

# In[1]:

import pandas as pd


# In[2]:

import numpy as np


# In[3]:

feat_df = pd.read_csv('../../../experiment_text_files/json_and_csv/big_experiment.csv')


# In[4]:

idiophones = ['crash_choke','crash_edge','hihat_chick','hihat_choke','hihat_closed','hihat_open','ride_bow','ride_bell',
              'cross_stick','rim_hit']


# In[5]:

category = np.array([])


# In[6]:

for inst in feat_df['instrument']:
    if inst in idiophones:
        category = np.append(category,'idiophone')
    else:
        category = np.append(category,'membranophone')


# In[7]:

instruments = np.unique(feat_df['instrument'])


# In[8]:

feat_df = feat_df.iloc[:,1:-1]


# In[9]:

feat_df['category'] = category


# In[17]:

cd


# In[18]:

import pandas2arff


# In[19]:

pandas2arff.pandas2arff(feat_df,filename='big_experiment_categories_1.arff',wekaname = 'category')


# In[ ]:



