
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

feat_df = pd.read_csv(os.path.join(pardir,filename))


# In[8]:

feat_df = feat_df.iloc[:,1:]


# In[9]:

inst1 = 'ride'


# In[10]:

inst2 = 'rim'


# In[11]:

inst1_df = feat_df[feat_df['instrument'] == inst1]

inst2_df = feat_df[feat_df['instrument'] == inst2]

final_df = pd.concat([inst1_df,inst2_df],ignore_index=True)


# In[12]:

# apandas2arff.pandas2arff(final_df,filename='../experiment_text_files/big_train_set_files/arff/1classVS1class/{instrument1}_vs_{instrument2}_nosil.arff'.format(instrument1 = inst1,instrument2 = inst2),wekaname = 'instrument')


# In[13]:

dstdir = '../experiment_text_files/big_train_set_files/json_and_csv/1classVS1class'


# In[14]:

final_df.to_csv(os.path.join(dstdir,'{inst1}_vs_{inst2}_nosil.csv'.format(inst1 = inst1,inst2 = inst2)))


# In[ ]:



