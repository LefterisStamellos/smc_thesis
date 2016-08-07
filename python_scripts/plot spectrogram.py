
# coding: utf-8

# In[1]:

import os

import numpy as np

get_ipython().magic(u'matplotlib inline')

import matplotlib.pyplot as plt

from essentia.standard import MonoLoader,RollOff,Centroid,ZeroCrossingRate,FrameGenerator,Windowing,Spectrum


# In[2]:

zcr = ZeroCrossingRate()


# In[3]:

w = Windowing(type = 'hann')


# In[4]:

pardir = '../database/real_drums_7classes_no_silence'
instrument = 'crash'
filename = 'crash1Choke_OH_F_1_no_silence.wav'


# In[5]:

loader = MonoLoader(filename = os.path.join(pardir,instrument,filename))


# In[6]:

audio = loader()


# In[7]:

spectrum = Spectrum()


# In[8]:

roll = RollOff()


# In[9]:

cntr = Centroid()


# In[10]:

t_rightlim = round(audio.shape[0]/44100.0,2)


# In[11]:

centroid = np.array([])


# In[12]:

rolloff = np.array([])


# In[13]:

zerocrossingrate = np.array([])


# In[23]:

ax = plt.subplot(111)
Pxx, freqs, bins, im = plt.specgram(audio, NFFT=1024, Fs=44100, noverlap=512)
plt.set_cmap('bone')
plt.ylim(0,22050)
plt.xlim(0,1.45)
plt.title(instrument,fontsize = '20')
plt.ylabel('frequency (Hz)')
plt.xlabel('time (s)')
for frame in FrameGenerator(audio, frameSize = 1024, hopSize = 512):
    zerocrossingrate = np.append(zerocrossingrate,zcr(w(frame)))
    centroid = np.append(centroid,cntr(spectrum(w(frame))))
    rolloff = np.append(rolloff,roll(spectrum(w(frame))))
plt.plot(centroid*22050,'g')
plt.plot(rolloff,'k')
plt.plot(zerocrossingrate*22050,'k')
plt.show()


# In[22]:

plt.plot(centroid*22050,'g')
plt.plot(rolloff,'bo')
plt.plot(zerocrossingrate*22050,'ko')
plt.xlim(0,60)


# In[ ]:



