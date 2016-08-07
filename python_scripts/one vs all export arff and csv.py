
# coding: utf-8

# In[1]:

import os


# In[2]:

import numpy as np


# In[3]:

import pandas as pd


# In[4]:

import pandas2arff


# In[5]:

pardir = '../experiment_text_files/big_train_set_files/json_and_csv/7_classes'


# In[6]:

filename = 'big_experiment_7classes_no_silence.csv'


# In[7]:

df = pd.read_csv(os.path.join(pardir,filename))
df = df.iloc[:,1:]


# In[8]:

instrument = 'kick'


# In[9]:

inst = df[df['instrument'] == instrument]
not_inst_init = df[df['instrument'] != instrument]


# In[10]:

instruments = np.unique(df[df['instrument']!= instrument]['instrument'])


# In[11]:

not_inst = pd.DataFrame()
for i in instruments:
    #sample from each instrument as many samples as needed in order to accumulate a "not instrument" dataframe 
    #as big as the "instrument" dataframe
    tmp = df[df['instrument'] == i].sample(int(round(inst.shape[0]/6)))
    tmp_inst = np.chararray(tmp.shape[0],len('not '+instrument))
    tmp_inst[:] = 'not '+instrument
    tmp['instrument'] = tmp_inst
    not_inst = pd.concat([not_inst,tmp])


# In[12]:

df = pd.DataFrame()


# In[13]:

df = pd.concat([inst,not_inst])


# In[14]:

df.to_csv('../experiment_text_files/big_train_set_files/json_and_csv/1classVSall/{instrument}_vs_all_nosil.csv'.format(instrument = instrument))
pandas2arff.pandas2arff(df,filename='../experiment_text_files/big_train_set_files/arff/1classVSall/{instrument}_vs_all_nosil.arff'.format(instrument = instrument),wekaname = 'instrument')


# In[15]:

df = pd.read_csv('../experiment_text_files/big_train_set_files/json_and_csv/1classVSall/{instrument}_vs_all_nosil.csv'.format(instrument = instrument))


# In[16]:

df


# In[ ]:



