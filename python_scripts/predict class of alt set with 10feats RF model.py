
# coding: utf-8

# In[1]:

import numpy as np

import pandas as pd

import os

import random

from sklearn.externals import joblib

from essentia.standard import MonoLoader

import sounddevice

import IPython


# In[2]:

# Load the Classifier
pardir = '../experiment_text_files/big_train_set_files/npy/7_classes/RF100TreesModel_real_set_15featsNEW'
filename = 'RandomForestClassifier_real_set.pkl'
model = joblib.load(os.path.join(pardir,filename))


# In[3]:

# Load the alt sounds' feature values for the 32 "commonly selected" (best) features

#alt test without unspecified 
#pardir = '../experiment_text_files/alt_test_set_text_files/json_and_csv/without_unspecified/7_classes'
#filename = 'alt_test_set_7classes_balanced_32BESTfeats.csv'

#alt test with unspecified
pardir = '../experiment_text_files/alt_test_set_text_files/json_and_csv/with_unspecified'
filename = 'alt_test_with_unspecified_15featsNEW.csv'

df = pd.DataFrame()
df = pd.read_csv(os.path.join(pardir,filename))


# In[4]:

# without unspecified
# df = df.iloc[:,1:-1]

#with unspecified
df = df.iloc[:,1:]


# In[5]:

#Load the alt sounds' filenames (e.g. 123456.wav) for collection without unspecified
# filename = 'alt_test_set_names_7classes_balanced.csv'

#Load the alt sounds' filenames (e.g. 123456.wav) for collection with unspecified
filename = 'alt_test_names_with_unspecified.csv'

df_names = pd.read_csv(os.path.join(pardir,filename))
df_names = df_names.iloc[:,1:]


# In[6]:

# Turn stuff from DataFrames to matrices
X = df.as_matrix()
music_filenames = df_names.as_matrix()


# In[ ]:

########### We could have stored the predicted class of each sound in our collection. Then, when looking for ############
# an instrument, we would pick t random one of those predicted as said instrument. Instead, we pick sounds at random, 
# give it to our classifier and check if said sound is classified as one of the instruments we are interested in. This
#might be the slower choice, but it allows us to change the sound collection without changing our model.


# In[ ]:

# ####### drumloops #################

# drumloops_dict_with_inst = {'drumloop1':['kick','hihat','snare','crash','tom'],'drumloop2':['kick','ride','rim','hihat','tom'],
# 'drumloop3':['kick','hihat','snare','tom','tom','tom']}
# drumloops_dict_with_wav = {}

# #drumloop: drumloop+number
# #instruments: list of instruments in drumloop, e.g. ['kick','snare','hihat']
# #music_filename: e.g. 123456.wav

# for (drumloop,instruments) in drumloops_dict_with_inst.items():
#     result = []
#     while instruments:
#         #pick an instrument at random (more specfically, the row from X containing random instrument's feature values)
#         randind = random.randrange(0,len(X)-1)
#         randomX = X[randind].reshape(1,-1)
        
#         #predict random instrument's class
#         predicted_instrument = model.predict(randomX)[0]
        
#         #if (predicted) class is in instruments (e.g. random instrument's class == hihat and hihat in instruments)
#         #remove the instrument from instruments list (i.e. don't look for it again) and detect the sound's filename
#         if predicted_instrument in instruments:
#             index = instruments.index(predicted_instrument)        
#             instruments.remove(predicted_instrument)
#             music_filename = music_filenames[randind]
#             result.insert(index,(music_filename[0],predicted_instrument))
    
#     instruments = list(zip(*result)[1])
#     music_files = list(zip(*result)[0])
#     drumloops_dict_with_wav[drumloop] = (instruments,music_files)


# In[ ]:

# wavs = drumloops_dict_with_wav['drumloop3'][1]
# instruments = drumloops_dict_with_wav['drumloop3'][0]

#without unspecified
#pardir = '../database/alt_set_wavs/without_unspecified_unbalanced'

#with unspecified
# pardir = '../database/alt_set_wavs/with_unspecified'

# audios = []
# for wav in wavs:
#     audio = MonoLoader(filename = os.path.join(pardir,wav))()
#     audios.append(audio)

# print zip(instruments,wavs)
# for i in range(len(instruments)):
#     IPython.display.display(IPython.display.Audio(os.path.join(pardir,wavs[i])))


# In[ ]:

# # ############## ask for one instrument, get one real and one random alternative ##############

# #instrument we're looking for
# instrument = 'snare'

# pardir = os.path.join('../database/real_set_7_classes_unbalanced_wavs',instrument)
# real_instruments_wavs = os.listdir(pardir)

# predicted_instrument = ''

# while predicted_instrument!=instrument:
#     randind = random.randrange(0,len(X)-1)
#     randomX = X[randind].reshape(1,-1)

#     #predict random instrument's class
#     predicted_instrument = model.predict(randomX)[0]

# alt_instrument = music_filenames[randind]
# real_instrument = random.choice(real_instruments_wavs)


# In[ ]:

#without unspecified
# alt_pardir = '../database/alt_set_wavs/without_unspecified_unbalanced'

#with unspecified
# alt_pardir = '../database/alt_set_wavs/with_unspecified'

# real_pardir = os.path.join('../database/real_set_7_classes_unbalanced_wavs',instrument)

# print instrument+ '\n'
# print real_instrument
# IPython.display.display(IPython.display.Audio(os.path.join(real_pardir,real_instrument)))
# print alt_instrument
# IPython.display.display(IPython.display.Audio(os.path.join(alt_pardir,alt_instrument[0])))


# In[ ]:

# # ############## ask for one instrument, get 3 real and one random alternative ##############

# #instrument we're looking for
# instrument = 'rim'

# pardir = os.path.join('../database/real_set_7_classes_unbalanced_wavs',instrument)
# real_instruments_wavs = os.listdir(pardir)

# predicted_instrument = ''

# while predicted_instrument!=instrument:
#     randind = random.randrange(0,len(X)-1)
#     randomX = X[randind].reshape(1,-1)

#     #predict random instrument's class
#     predicted_instrument = model.predict(randomX)[0]

# alt_instrument = music_filenames[randind]
# real_instruments = []
# real_instruments = random.sample(real_instruments_wavs,3)


# In[ ]:

#without unspecified
# alt_pardir = '../database/alt_set_wavs/without_unspecified_unbalanced'

#with unspecified
# alt_pardir = '../database/alt_set_wavs/with_unspecified'

# real_pardir = os.path.join('../database/real_set_7_classes_unbalanced_wavs',instrument)

# print 'alternative '+instrument+ '\n'
# print alt_instrument
# IPython.display.display(IPython.display.Audio(os.path.join(alt_pardir,alt_instrument[0])))
# print 'real '+instrument+'s'+ '\n'
# for inst in real_instruments:
#     print inst
#     IPython.display.display(IPython.display.Audio(os.path.join(real_pardir,inst)))


# In[35]:

# ############## ask for one instrument, get 1 real and three random alternative ##############

#instrument we're looking for
instrument = 'ride'

pardir = os.path.join('../database/real_set_7_classes_unbalanced_wavs',instrument)
real_instruments_wavs = os.listdir(pardir)

alt_instruments = []

while (len(alt_instruments) < 3):
    randind = random.randrange(0,len(X)-1)
    randomX = X[randind].reshape(1,-1)

    #predict random instrument's class
    predicted_instrument = model.predict(randomX)[0]
    
    if predicted_instrument == instrument and predicted_instrument not in alt_instruments:
        music_filename = music_filenames[randind]
        alt_instruments.append(music_filename[0])

real_instrument = random.choice(real_instruments_wavs)


# In[36]:

#without unspecified
# alt_pardir = '../database/alt_set_wavs/without_unspecified_unbalanced'

#with unspecified
alt_pardir = '../database/alt_set_wavs/with_unspecified'

real_pardir = os.path.join('../database/real_set_7_classes_unbalanced_wavs',instrument)

print 'real '+instrument + '\n'
print real_instrument
IPython.display.display(IPython.display.Audio(os.path.join(real_pardir,real_instrument)))

print 'alternative '+instrument+'s'+ '\n'
for inst in alt_instruments:
    print inst
    IPython.display.display(IPython.display.Audio(os.path.join(alt_pardir,inst)))


# In[ ]:



