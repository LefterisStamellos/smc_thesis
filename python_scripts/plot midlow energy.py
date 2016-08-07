
# coding: utf-8

# In[ ]:

import os

import numpy as np

# %matplotlib inline

import matplotlib.pyplot as plt

from essentia.standard import MonoLoader,EnergyBand,FrameGenerator,Spectrum,Windowing


# In[ ]:

pardir = '../database/real_drums_7classes_no_silence'
instrument = 'snare'
filename = '79735__sandyrb__bmc-snare-001-woh_no_silence.wav'


# In[ ]:

loader = MonoLoader(filename = os.path.join(pardir,instrument,filename))


# In[ ]:

audio = loader()


# In[ ]:

energy = EnergyBand(startCutoffFrequency = 150,stopCutoffFrequency = 800)


# In[ ]:

w = Windowing(type = 'hann')


# In[ ]:

spec = Spectrum()


# In[ ]:

midlow_energy = np.array([])
for frame in FrameGenerator(audio, frameSize = 1024, hopSize = 512):
    midlow_energy = np.append(midlow_energy,energy(frame))


# In[ ]:

midlow_energy.shape


# In[ ]:

258*512/44100.0


# In[ ]:

t_rightlim = round(audio.shape[0]/44100.0,2)


# In[ ]:

ax1 = plt.subplot(211)
ax1.get_xaxis().set_ticks([])
Pxx, freqs, bins, im = plt.specgram(audio, NFFT=1024, Fs=44100, noverlap=512)
plt.ylim(150,800)
# plt.xlim(0,t_rightlim)
plt.title(instrument,fontsize = '20')
plt.ylabel('frequency')
# ax1.set_xticklabels(np.arange(0, round(75/44100.0,4),round(5/44100.0,4)))

ax2 = plt.subplot(212)
plt.plot(midlow_energy,'ro')
plt.xlabel('time (s)')
ax2.set_xticklabels(np.arange(0, round(audio.shape[0]/44100.0,2),round((audio.shape[0]/44100.0)/6,2)))
plt.ylabel('energy')
# plt.ylim(0,20)
plt.show()


# In[ ]:

round(audio.shape[0]/44100.0,2)


# In[ ]:

round((audio.shape[0]/44100.0)/6,2)


# In[ ]:



