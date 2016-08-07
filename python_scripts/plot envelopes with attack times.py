
# coding: utf-8

# In[ ]:

# %matplotlib inline


# In[ ]:

import matplotlib.pyplot as plt


# In[ ]:

from essentia.standard import MonoLoader,Envelope


# In[ ]:

import os


# In[ ]:

import numpy as np


# In[ ]:

sizes = np.array([])


# In[ ]:

ride = '../database/real_set_7_classes_unbalanced_wavs/ride/2002_20_crush_ride_body.wav'


# In[ ]:

# crash = '../database/real_set_7_classes_unbalanced_wavs/crash/2002_16_power_crash_edge.wav'


# In[ ]:

# hihat = '../database/real_set_7_classes_unbalanced_wavs/hihat/02L3.UFHHM   [s].wav'


# In[ ]:

# kick = '../database/real_set_7_classes_unbalanced_wavs/kick/CLudwigKick-Dyn05.WAV'


# In[ ]:

loader = MonoLoader(filename = ride)


# In[ ]:

audio = loader()


# In[ ]:

# size = 44480.0


# In[ ]:

envelope = Envelope()


# In[ ]:

env = envelope(audio)


# In[ ]:

# env = env[:int(size)]


# In[ ]:

plt.plot(env)


# In[ ]:

hline_end = np.empty(env.shape)
hline_end[:] = 0.9*np.max(env)


# In[ ]:

hline_beg = np.empty(env.shape)
hline_beg[:] = 0.2*np.max(env)


# In[ ]:

ax = plt.subplot(111)

plt.plot(env)
plt.plot(hline_beg)
plt.plot(hline_end)
# plt.axvline(np.min(np.where(env>=0.9*np.max(env))))
# plt.axvline(np.sort(np.where(env<=0.2*np.max(env)))[:,1])
plt.axvline(np.abs(env-0.9*np.max(env)).argmin())
plt.axvline(np.abs(env-0.2*np.max(env)).argmin())
plt.xlabel('time (s)',fontsize = '12')
ax.set_xticklabels(np.arange(0, np.round(45000/44100.0,4),np.round(5000/44100.0,4)))
plt.title('ride',fontsize = '20')

ax.get_yaxis().set_ticks([])
plt.minorticks_on()


# In[ ]:

plt.show()


# In[ ]:



