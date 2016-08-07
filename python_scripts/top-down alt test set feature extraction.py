import pandas as pd
import numpy as np
import os
import ipdb
import json
import subprocess
import yaml
from sklearn.cluster import KMeans,k_means,Birch
from sklearn import cluster

path = '../database/recorded_and_downloaded_alt_sounds_processed'
folders = os.listdir(path)[1:]

for folder in folders:
    tracks = os.listdir(os.path.join(path,folder))
    for track in tracks:
        if (track[-3:] == 'wav' or track[-3:] == 'WAV'):        
            subprocess.Popen(['essentia_streaming_extractor_freesound',os.path.join(path,folder,track),os.path.join(path,folder,track[:-4] + '.json')])

feat_df = pd.DataFrame()
names = np.array([])
for folder in folders:
    tracks = os.listdir(os.path.join(path,folder))
    for track in tracks:
        if (track[-3:] == 'wav' or track[-3:] == 'WAV'):
            
            names = np.append(names,track)
            
            df = pd.DataFrame()

            f = open(os.path.join(path,folder,track[:-4] + '.json_statistics.yaml'))
            feat_dict = yaml.safe_load(f)
            f.close()

            #first three are disacrded as irrelevant, fourth cause is full of nans and infs, the rest cause their
            #values are such that do not help in classification (almost always zero, always somewhere close)
            #]
            feat_dict.pop('tonal',None)
            feat_dict.pop('rhythm',None)
            feat_dict.pop('metadata',None)
            feat_dict['sfx'].pop('oddtoevenharmonicenergyratio',None)
            feat_dict['lowlevel'].pop('barkbands',None)
            feat_dict['lowlevel'].pop('erb_bands',None)
            feat_dict['lowlevel'].pop('spectral_decrease',None)
            feat_dict['lowlevel'].pop('spectral_rms',None)
            feat_dict['lowlevel'].pop('frequency_bands',None)
            feat_dict['lowlevel'].pop('spectral_energyband_low',None)

            for f in feat_dict.keys():
                for d in feat_dict[f]:
                    if type(feat_dict[f][d]) == dict:
                        feat_dict[f][d].pop('dmean')
                        feat_dict[f][d].pop('dmean2')
                        feat_dict[f][d].pop('dvar')
                        feat_dict[f][d].pop('dvar2')
                        feat_dict[f][d].pop('max')
                        feat_dict[f][d].pop('median')
                        feat_dict[f][d].pop('min')

            for family in feat_dict.keys():
                for desc in feat_dict[family]:
                    if type(feat_dict[family][desc]) == dict:
                        if type(feat_dict[family][desc]['mean']) != list:                
                            df[desc + '_' + 'mean'] = [feat_dict[family][desc]['mean']]
                        else:
                            for i in range(len(feat_dict[family][desc]['mean'])):
                                df[desc + '_' + 'mean' + '_' + str(i)] = feat_dict[family][desc]['mean'][i]
                                df[desc + '_' + 'var' + '_' + str(i)] = feat_dict[family][desc]['var'][i]            

            feat_df = pd.concat([feat_df,df],ignore_index=True)


feat_df.to_csv('alt_test_all.csv')
feat_df = pd.read_csv('../../../alt_test_set_text_files/json_and_csv/alt_test_all.csv')

feats = ['spectral_contrast_mean_4','spectral_energyband_middle_low_mean','spectral_contrast_mean_5',
 'spectral_energyband_high_mean','spectral_contrast_var_0']

new_feat_df = pd.DataFrame()

for feat in feats:
    new_feat_df[feat] = feat_df[feat]


new_feat_df

feat_df.to_csv('alt_test_clustering1.csv')

import pandas2arff

pandas2arff.pandas2arff(feat_df,filename='alt_test_all.arff')
pandas2arff.pandas2arff(new_feat_df,filename='alt_test_clustering1.arff')

fit_predict = model.fit_predict(X)

for i in np.argsort(fit_predict):
    sorted_names = np.append(sorted_names,names[i])

get_ipython().magic(u'pinfo Birch')