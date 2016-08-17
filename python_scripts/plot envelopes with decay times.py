get_ipython().magic(u'matplotlib inline')
import matplotlib.pyplot as plt
from essentia.standard import MonoLoader,Envelope
import os
import numpy as np

sizes = np.array([])
ride = '../database/real_set_7_classes_unbalanced_wavs/ride/2002_20_crush_ride_body.wav'
crash = '../database/real_set_7_classes_unbalanced_wavs/crash/2002_16_power_crash_edge.wav'
snare = '../database/real_set_7_classes_unbalanced_wavs/snare/91841__sandyrb__tac14x8-e22-velo7.wav'
rim = '../database/real_set_7_classes_unbalanced_wavs/rim/CyCdh_K3SdSt-06.wav'

loader = MonoLoader(filename = snare)
audio = loader()
# size = 44480.0

envelope = Envelope()
env = envelope(audio)
# env = env[:int(size)]
plt.plot(env)

hline_end = np.empty(env.shape)
hline_end[:] = 0.9*np.max(env)

hline_beg = np.empty(env.shape)
hline_beg[:] = 0.2*np.max(env)

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

plt.show()