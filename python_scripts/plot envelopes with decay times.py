
# coding: utf-8

# In[1]:

get_ipython().magic(u'matplotlib inline')


# In[2]:

import matplotlib.pyplot as plt


# In[3]:

from essentia.standard import MonoLoader,Envelope


# In[4]:

import os


# In[5]:

import numpy as np


# In[6]:

sizes = np.array([])


# In[7]:

ride = '../database/real_set_7_classes_unbalanced_wavs/ride/2002_20_crush_ride_body.wav'


# In[8]:

crash = '../database/real_set_7_classes_unbalanced_wavs/crash/2002_16_power_crash_edge.wav'


# In[9]:

snare = '../database/real_set_7_classes_unbalanced_wavs/snare/91841__sandyrb__tac14x8-e22-velo7.wav'


# In[10]:

rim = '../database/real_set_7_classes_unbalanced_wavs/rim/CyCdh_K3SdSt-06.wav'


# In[11]:

loader = MonoLoader(filename = snare)


# In[12]:

audio = loader()


# In[13]:

# size = 44480.0


# In[14]:

envelope = Envelope()


# In[15]:

env = envelope(audio)


# In[16]:

# env = env[:int(size)]


# In[17]:

plt.plot(env)


# In[18]:

hline_end = np.empty(env.shape)
hline_end[:] = 0.9*np.max(env)


# In[19]:

hline_beg = np.empty(env.shape)
hline_beg[:] = 0.2*np.max(env)


# In[22]:

ax = plt.subplot(111)

plt.plot(env)
plt.plot(hline_beg)
plt.plot(hline_end)
beg = np.abs(env-0.9*np.max(env)).argmin()
plt.axvline(beg)
end = np.abs(env-0.2*np.max(env)).argmin()

if end>beg:
    xrightlim = end 
else:
    xrightlim = env.shape[0]

plt.xlim(0,xrightlim) 
plt.xlabel('time (s)',fontsize = '12')
ax.set_xticklabels(np.arange(0, np.round(45000/44100.0,4),np.round(5000/44100.0,4)))
plt.title('ride',fontsize = '20')
# ax.text(45000, 0.05, 'release slope = {}'.format(np.mean(np.diff(env[beg:xrightlim]))))
# ax.get_yaxis().set_ticks([])
plt.minorticks_on()


# In[21]:

plt.show()


# In[ ]:



