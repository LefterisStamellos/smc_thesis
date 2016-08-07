
# coding: utf-8

# In[1]:

import os


# In[2]:

import numpy as np


# In[3]:

pardir = '../database/real_drums_full_set'


# In[4]:

folders = os.listdir(pardir)[1:]


# In[5]:

for folder in folders:
    filenames = os.listdir(os.path.join(pardir,folder))[1:]
    for filename in filenames:
        os.rename(os.path.join(pardir,folder,filename),os.path.join(pardir,folder,filename.replace(' ','_')))


# In[ ]:



