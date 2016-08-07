
# coding: utf-8

# In[1]:

import os


# In[2]:

import numpy as np


# In[3]:

srcpardir = '../database/real_drums_full_set'


# In[4]:

dstpardir = '../database/real_drums_full_set_no_silence'


# In[5]:

folders = os.listdir(srcpardir)[1:]


# In[6]:

for folder in folders:
    os.mkdir(os.path.join(dstpardir,folder))
    tracks = np.array([track for track in os.listdir(os.path.join(srcpardir,folder)) if (track[-3:] == 'wav' or track[-3:] == 'WAV')])
    #     tracks = np.random.choice(tracks,250,replace = False)
    for track in tracks:
        track.replace(' ','_')
        os.system('sox {src} {dst} silence 1 0.1 0.1% reverse silence 1 0.1 0.1% reverse'.format(src = os.path.join(srcpardir,folder,track),dst = os.path.join(dstpardir,folder,track[:-4]+'_no_silence'+track[-4:])))


# In[ ]:



