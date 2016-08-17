import os
import numpy as np
import pandas as pd
import pandas2arff

pardir = '../experiment_text_files/big_train_set_files/json_and_csv/7_classes'
filename = 'big_experiment_7classes_no_silence.csv'

feat_df = pd.read_csv(os.path.join(pardir,filename))
feat_df = feat_df.iloc[:,1:]

inst1 = 'ride'
inst2 = 'rim'

inst1_df = feat_df[feat_df['instrument'] == inst1]
inst2_df = feat_df[feat_df['instrument'] == inst2]

final_df = pd.concat([inst1_df,inst2_df],ignore_index=True)

# pandas2arff.pandas2arff(final_df,filename='../experiment_text_files/big_train_set_files/arff/1classVS1class/{instrument1}_vs_{instrument2}_nosil.arff'.format(instrument1 = inst1,instrument2 = inst2),wekaname = 'instrument')

dstdir = '../experiment_text_files/big_train_set_files/json_and_csv/1classVS1class'
final_df.to_csv(os.path.join(dstdir,'{inst1}_vs_{inst2}_nosil.csv'.format(inst1 = inst1,inst2 = inst2)))
