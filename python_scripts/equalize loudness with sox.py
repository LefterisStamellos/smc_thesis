import os
import numpy as np

pardir = '../database/alt_set_wavs/'
srcdir = 'with_unspecified'
dstdir = 'with_unspecified_eq'

tracks = np.array([track for track in os.listdir(os.path.join(pardir,srcdir)) if (track[-3:] == 'wav' or track[-3:] == 'WAV')])

for track in tracks:
    os.system('sox {src} {dst} gain -n -3'.format(src = os.path.join(pardir,srcdir,track),dst = os.path.join(pardir,dstdir,track[:-4]+'_eq'+track[-4:])))


