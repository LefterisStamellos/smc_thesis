
from essentia.standard import MonoLoader,GFCC,Windowing,Spectrum,FrameGenerator,Envelope,ERBBands,MFCC
import numpy as np
import os
import matplotlib.pyplot as plt
from pylab import imshow
from scipy.interpolate import interp1d

pardir = '../database/real_set_7_classes_unbalanced_wavs/hihat/'

# filenames = ['alpha_10_mini_x-hats_closed.wav','rim/03SS.SNR1C [s]-R.wav',
# 'snare/84065__sandyrb__kbsd-re20-velocity9.wav','crash/2002_20_rock_crash_edge.wav',
#              'ride/2002_20_heavy_ride_body.wav','kick/F023.wav','tom/06  .TOM3M   [s].wav']

# titles = ['closed hihat','rim','snare drum','crash','ride','kick','tom']

filenames = ['alpha_10_mini_x-hats_closed.wav','101_brass_14_hi-hat_open.wav',
'2002_14_heavy_hi-hat_chick.wav','116975__cbeeching__hat-open.wav']

titles = ['closed hihat','choke hihat','chick hihat','open hihat']
x = zip(filenames,titles)

w = Windowing(type = 'hann')
gfcc = GFCC()
mfcc = MFCC()
spectrum = Spectrum()
fig = plt.figure()
i=0

fig, axs = plt.subplots(2,2)
fig.subplots_adjust(hspace = 0.3)
axs = axs.ravel()

for filename,title in x:
    loader = MonoLoader(filename = os.path.join(pardir,filename))
    audio = loader()
    gfccs = []

    for frame in FrameGenerator(audio, frameSize = 1024, hopSize = 512):
        gfcc_bands, gfcc_coeffs = gfcc(spectrum(w(frame)))
        gfccs.append(gfcc_coeffs)

    # transpose to have it in a better shape
    # we need to convert the list to an essentia.array first (== numpy.array of floats)
    gfccs = np.array(gfccs).T

    axs[i].imshow(gfccs[1:,:], aspect = 'auto', interpolation = 'nearest')

#     axs[i].imshow(gfccs[2:3,:], aspect = 'auto',interpolation = 'nearest')
#     axs[i].plot(gfccs[2:3,:].T,'darksalmon')

    axs[i].set_title(title,fontsize = 16)
    axs[i].get_xaxis().set_ticks([])
    axs[i].get_yaxis().set_ticks(np.arange(0,12))

    i +=1

plt.show()

# for filename,title in x:
#     loader = MonoLoader(filename = os.path.join(pardir,filename))
#     audio = loader()
#     mfccs = []

#     for frame in FrameGenerator(audio, frameSize = 1024, hopSize = 512):
#         mfcc_bands, mfcc_coeffs = mfcc(spectrum(w(frame)))
#         mfccs.append(mfcc_coeffs)

#     # transpose to have it in a better shape
#     # we need to convert the list to an essentia.array first (== numpy.array of floats)
#     mfccs = np.array(mfccs).T

#     axs[i].imshow(mfccs[1:,:], aspect = 'auto',interpolation = 'nearest')

# #     axs[i].imshow(gfccs[2:3,:], aspect = 'auto',interpolation = 'nearest')
# #     axs[i].plot(gfccs[2:3,:].T,'darksalmon')

#     axs[i].set_title(title,fontsize = 16)
#     axs[i].get_xaxis().set_ticks([])


#     i +=1