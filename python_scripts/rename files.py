import os
import numpy as np

pardir = '../database/real_drums_full_set'
folders = os.listdir(pardir)[1:]

for folder in folders:
    filenames = os.listdir(os.path.join(pardir,folder))[1:]
    for filename in filenames:
        os.rename(os.path.join(pardir,folder,filename),os.path.join(pardir,folder,filename.replace(' ','_')))