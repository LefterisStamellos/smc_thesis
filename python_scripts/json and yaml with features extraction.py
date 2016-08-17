import os
import json
import yaml
import subprocess
import numpy as np

pardir = '../../../web_app/static/alt_sounds'
# folders = ['snare','hihat','rim']

# for folder in folders:
# folder = 'rim'
# tracks = [track for track in os.listdir(os.path.join(pardir,folder)) if (track[-3:] == 'wav' or track[-3:] == 'WAV')]
tracks = [track for track in os.listdir(pardir) if (track[-3:] == 'wav' or track[-3:] == 'WAV')]
for track in tracks[1000:]:
#     subprocess.Popen(['essentia_streaming_extractor_freesound',os.path.join(pardir,folder,track),os.path.join(pardir,folder,track[:-4] + '.json')])
    subprocess.Popen(['essentia_streaming_extractor_freesound',os.path.join(pardir,track),os.path.join(pardir,track[:-4] + '.json')])

