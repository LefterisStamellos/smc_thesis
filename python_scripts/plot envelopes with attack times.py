# %matplotlib inline
import matplotlib.pyplot as plt
from essentia.standard import MonoLoader,Envelope
import os
import numpy as np

sizes = np.array([])
ride = '../database/real_set_7_classes_unbalanced_wavs/ride/2002_20_crush_ride_body.wav'
# crash = '../database/real_set_7_classes_unbalanced_wavs/crash/2002_16_power_crash_edge.wav'
# hihat = '../database/real_set_7_classes_unbalanced_wavs/hihat/02L3.UFHHM   [s].wav'
# kick = '../database/real_set_7_classes_unbalanced_wavs/kick/CLudwigKick-Dyn05.WAV'

loader = MonoLoader(filename = ride)
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
# plt.axvline(np.min(np.where(env>=0.9*np.max(env))))
# plt.axvline(np.sort(np.where(env<=0.2*np.max(env)))[:,1])
plt.axvline(np.abs(env-0.9*np.max(env)).argmin())
plt.axvline(np.abs(env-0.2*np.max(env)).argmin())
plt.xlabel('time (s)',fontsize = '12')
ax.set_xticklabels(np.arange(0, np.round(45000/44100.0,4),np.round(5000/44100.0,4)))
plt.title('ride',fontsize = '20')

ax.get_yaxis().set_ticks([])
plt.minorticks_on()

plt.show()