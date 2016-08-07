import os
import numpy as np
import pandas as pd
import pandas2arff

pardir = '../experiment_text_files/big_train_set_files/json_and_csv/7_classes'
filename = 'big_experiment_7classes_no_silence.csv'

df = pd.read_csv(os.path.join(pardir,filename))
df = df.iloc[:,1:]

instrument = 'kick'

inst = df[df['instrument'] == instrument]
not_inst_init = df[df['instrument'] != instrument]

instruments = np.unique(df[df['instrument']!= instrument]['instrument'])

not_inst = pd.DataFrame()
for i in instruments:
    #sample from each instrument as many samples as needed in order to accumulate a "not instrument" dataframe 
    #as big as the "instrument" dataframe
    tmp = df[df['instrument'] == i].sample(int(round(inst.shape[0]/6)))
    tmp_inst = np.chararray(tmp.shape[0],len('not '+instrument))
    tmp_inst[:] = 'not '+instrument
    tmp['instrument'] = tmp_inst
    not_inst = pd.concat([not_inst,tmp])

df = pd.DataFrame()
df = pd.concat([inst,not_inst])

df.to_csv('../experiment_text_files/big_train_set_files/json_and_csv/1classVSall/{instrument}_vs_all_nosil.csv'.format(instrument = instrument))
pandas2arff.pandas2arff(df,filename='../experiment_text_files/big_train_set_files/arff/1classVSall/{instrument}_vs_all_nosil.arff'.format(instrument = instrument),wekaname = 'instrument')

df = pd.read_csv('../experiment_text_files/big_train_set_files/json_and_csv/1classVSall/{instrument}_vs_all_nosil.csv'.format(instrument = instrument))