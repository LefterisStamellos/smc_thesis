
# coding: utf-8

# In[1]:

import os


# In[2]:

import numpy as np


# In[3]:

import pandas as pd


# In[4]:

pardir = '../experiment_text_files/alt_test_set_text_files/json_and_csv/without_unspecified/unbalanced_set'


# In[5]:

df = pd.read_csv(os.path.join(pardir,'alt_test_without_unspecified.csv'))


# In[6]:

df_names = pd.read_csv(os.path.join(pardir,'alt_test_names_without_unspecified.csv'))


# In[7]:

df_names = df_names.iloc[:,1:]


# In[8]:

df = df.iloc[:,1:]


# In[9]:

df['names'] = df_names


# In[10]:

hh = ['hihat_chick','hihat_choke','hihat_closed','hihat_open']


# In[11]:

crash = ['crash_edge','crash_choke']


# In[12]:

ride = ['ride_bell','ride_bow']


# In[13]:

rim = ['rim_hit','cross_stick']


# In[14]:

snare = ['snare_on','rimshot']


# In[15]:

tom = ['tom_high','tom_medium','tom_low','snare_off']


# In[16]:

instruments = np.array([])


# In[17]:

for inst in df['instrument']:
    if inst in hh:
        instruments = np.append(instruments,'hihat')
    elif inst in crash:
        instruments = np.append(instruments,'crash')
    elif inst in ride:
        instruments = np.append(instruments,'ride')
    elif inst in rim:
        instruments = np.append(instruments,'rim')
    elif inst in snare:
        instruments = np.append(instruments,'snare')
    elif inst in tom:
        instruments = np.append(instruments,'tom')
    else:
        instruments = np.append(instruments,'kick')


# In[18]:

df['instrument'] = instruments


# In[28]:

instruments = np.unique(instruments)


# In[29]:

n_samples = min([len(df[df['instrument'] == inst]) for inst in instruments])


# In[30]:

new_df = pd.DataFrame()


# In[31]:

for inst in instruments:
    new_df = pd.concat([new_df,df[df['instrument'] == inst].sample(n_samples)],ignore_index=True)


# In[32]:

new_df.shape


# In[35]:

names = new_df.iloc[:,-1:]


# In[37]:

new_df = new_df.iloc[:,:-1]


# In[39]:

cd 


# In[40]:

import pandas2arff


# In[41]:

pandas2arff.pandas2arff(new_df,filename='alt_experiment_7classes_balanced.arff',wekaname = 'instrument')


# In[42]:

new_df.to_csv('alt_experiment_7classes_balanced.csv')


# In[43]:

names.to_csv('alt_experiment_names_7classes_balanced.csv')


# In[ ]:



