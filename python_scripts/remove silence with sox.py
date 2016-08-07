import os
import numpy as np

srcpardir = '../database/real_drums_full_set'
dstpardir = '../database/real_drums_full_set_no_silence'

folders = os.listdir(srcpardir)[1:]

for folder in folders:
    os.mkdir(os.path.join(dstpardir,folder))
    tracks = np.array([track for track in os.listdir(os.path.join(srcpardir,folder)) if (track[-3:] == 'wav' or track[-3:] == 'WAV')])
    #     tracks = np.random.choice(tracks,250,replace = False)
    for track in tracks:
        track.replace(' ','_')
        os.system('sox {src} {dst} silence 1 0.1 0.1% reverse silence 1 0.1 0.1% reverse'.format(src = os.path.join(srcpardir,folder,track),dst = os.path.join(dstpardir,folder,track[:-4]+'_no_silence'+track[-4:])))