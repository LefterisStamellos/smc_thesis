
# coding: utf-8

# In[1]:

import os


# In[8]:

import numpy as np


# In[3]:

pardir = '../database/alt_set_wavs/'


# In[4]:

srcdir = 'with_unspecified'


# In[5]:

dstdir = 'with_unspecified_eq'


# In[6]:

tracks = np.array([track for track in os.listdir(os.path.join(pardir,srcdir)) if (track[-3:] == 'wav' or track[-3:] == 'WAV')])


# In[7]:

for track in tracks:
    os.system('sox {src} {dst} gain -n -3'.format(src = os.path.join(pardir,srcdir,track),dst = os.path.join(pardir,dstdir,track[:-4]+'_eq'+track[-4:])))


# In[ ]:



