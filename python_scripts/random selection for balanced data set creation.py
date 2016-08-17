import os
import numpy as np
import pandas as pd

pardir = '../experiment_text_files/alt_test_set_text_files/json_and_csv/without_unspecified/unbalanced_set'

df = pd.read_csv(os.path.join(pardir,'alt_test_without_unspecified.csv'))
df_names = pd.read_csv(os.path.join(pardir,'alt_test_names_without_unspecified.csv'))
df_names = df_names.iloc[:,1:]
df = df.iloc[:,1:]
df['names'] = df_names

hh = ['hihat_chick','hihat_choke','hihat_closed','hihat_open']
crash = ['crash_edge','crash_choke']
ride = ['ride_bell','ride_bow']
rim = ['rim_hit','cross_stick']
snare = ['snare_on','rimshot']
tom = ['tom_high','tom_medium','tom_low','snare_off']

instruments = np.array([])

for inst in df['instrument']:
    if inst in hh:
        instruments = np.append(instruments,'hihat')
    elif inst in crash:
        instruments = np.append(instruments,'crash')
    elif inst in ride:
        instruments = np.append(instruments,'ride')
    elif inst in rim:
        instruments = np.append(instruments,'rim')
    elif inst in snare:
        instruments = np.append(instruments,'snare')
    elif inst in tom:
        instruments = np.append(instruments,'tom')
    else:
        instruments = np.append(instruments,'kick')

df['instrument'] = instruments
instruments = np.unique(instruments)

n_samples = min([len(df[df['instrument'] == inst]) for inst in instruments])

new_df = pd.DataFrame()
for inst in instruments:
    new_df = pd.concat([new_df,df[df['instrument'] == inst].sample(n_samples)],ignore_index=True)

names = new_df.iloc[:,-1:]
new_df = new_df.iloc[:,:-1]

import pandas2arff
pandas2arff.pandas2arff(new_df,filename='alt_experiment_7classes_balanced.arff',wekaname = 'instrument')

new_df.to_csv('alt_experiment_7classes_balanced.csv')
names.to_csv('alt_experiment_names_7classes_balanced.csv')