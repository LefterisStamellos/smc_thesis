import os
import numpy as np
get_ipython().magic(u'matplotlib inline')
import matplotlib.pyplot as plt
from essentia.standard import MonoLoader,RollOff,Centroid,ZeroCrossingRate,FrameGenerator,Windowing,Spectrum

zcr = ZeroCrossingRate()

w = Windowing(type = 'hann')

pardir = '../database/real_drums_7classes_no_silence'
instrument = 'crash'
filename = 'crash1Choke_OH_F_1_no_silence.wav'

loader = MonoLoader(filename = os.path.join(pardir,instrument,filename))
audio = loader()

spectrum = Spectrum()
roll = RollOff()
cntr = Centroid()

t_rightlim = round(audio.shape[0]/44100.0,2)

centroid = np.array([])
rolloff = np.array([])
zerocrossingrate = np.array([])

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

plt.plot(centroid*22050,'g')
plt.plot(rolloff,'bo')
plt.plot(zerocrossingrate*22050,'ko')
plt.xlim(0,60)