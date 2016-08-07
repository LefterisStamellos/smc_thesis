import numpy as np
import pandas as pd
import os
import random
import json
from sklearn.externals import joblib

class Loader:
    def __init__(self,dirs,filenames):
        self.dirs = dirs
        self.filenames = filenames

    def load_model(self):
        # Load the Classifier
        pardir = self.dirs['model_dir']
        filename = self.filenames['model_pkl']
        model = joblib.load(os.path.join(pardir,filename))

        return model

    def load_alt_sounds_feat_values(self):
        #alt test with unspecified
        filename = self.filenames['alt_feats']

        df = pd.DataFrame()
        df = pd.read_csv(filename)

        #with unspecified
        df = df.iloc[:,1:]

        # Turn stuff from DataFrames to matrices
        X = df.as_matrix()

        return X

    def load_alt_sounds_filenames(self):
        #Load the alt sounds' filenames (e.g. 123456.wav) for collection without unspecified
        # filename = 'alt_test_set_names_7classes_balanced.csv'

        #Load the alt sounds' filenames (e.g. 123456.wav) for collection with unspecified
        filename = self.filenames['alt_names']

        df_names = pd.DataFrame()
        df_names = pd.read_csv(filename)
        df_names = df_names.iloc[:,1:]

        alt_sounds_filenames = df_names.as_matrix()

        return alt_sounds_filenames


    def load_one_real_instruments_filemanes(self,instrument):
        pardir = os.path.join(self.dirs['real_dir'],instrument)
        one_real_instruments_filenames = os.listdir(pardir)

        return one_real_instruments_filenames

    def dump_answers_to_json(self,answers):
        if os.path.isfile('answers.json'):
            df = pd.read_json('answers.json')
        else:
            df = pd.DataFrame()
        df_tmp = pd.DataFrame()
        df_tmp = df_tmp.from_dict(answers)
        x = df_tmp.iloc[:,1:].dropna()
        y = np.array(df_tmp['step1'].dropna().tolist(),dtype = object)
        df_new_entry = pd.DataFrame()
        df_new_entry['step1'] = 's'
        df_new_entry.set_value(0,'step1',y)
        for i in range(2,22):
            ind = 'step'+str(i)
            df_new_entry[ind] = 's'
            df_new_entry.set_value(0,ind,(x[ind]['question1'],x[ind]['question2']))
        df = pd.concat([df,df_new_entry],ignore_index=True)
        # df.to_json('answers.json')

        return df







