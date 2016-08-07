#http://pandas.pydata.org/
import pandas as pd
#https://github.com/saurabhnagrecha/Pandas-to-ARFF
import pandas2arff
import numpy as np
import os
import json
import yaml
import subprocess

feat_df = pd.DataFrame()

pardir = '../../../web_app/static/alt_sounds'
names = np.array([])

# for folder in folders:
# tracks = [track for track in os.listdir(os.path.join(pardir,folder)) if (track[-3:] == 'wav' or track[-3:] == 'WAV')]
tracks = [track for track in os.listdir(pardir) if (track[-3:] == 'wav' or track[-3:] == 'WAV')]

for track in tracks:
    if os.path.isfile(os.path.join(pardir,track[:-4] + '.json_statistics.yaml')):
#     if os.path.isfile(os.path.join(pardir,folder,track[:-4] + '.json_statistics.yaml')):
        names = np.append(names,track)

        df = pd.DataFrame()
        f = open(os.path.join(pardir,track[:-4] + '.json_statistics.yaml'))
#         f = open(os.path.join(pardir,folder,track[:-4] + '.json_statistics.yaml'))

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

        for family in feat_dict.keys():
            for desc in feat_dict[family]:
                if type(feat_dict[family][desc]) == dict:
                    feat_dict[family][desc].pop('dmean')
                    feat_dict[family][desc].pop('dmean2')
                    feat_dict[family][desc].pop('dvar')
                    feat_dict[family][desc].pop('dvar2')
                    feat_dict[family][desc].pop('max')
                    feat_dict[family][desc].pop('median')
                    feat_dict[family][desc].pop('min')                    

                    if type(feat_dict[family][desc]['mean']) != list:                
                        df[desc + '_' + 'mean'] = [feat_dict[family][desc]['mean']]
                    else:
                        for i in range(len(feat_dict[family][desc]['mean'])):
                            df[desc + '_' + 'mean' + '_' + str(i)] = feat_dict[family][desc]['mean'][i]
                            df[desc + '_' + 'var' + '_' + str(i)] = feat_dict[family][desc]['var'][i]            
                else:
                    df[desc] = feat_dict[family][desc]

#         df['instrument'] = folder

        feat_df = pd.concat([feat_df,df],ignore_index=True)


df_names = pd.DataFrame()
df_names['names'] = names
df_names.to_csv('alt_test_names_with_unspecified.csv')

feat_df.to_csv('alt_test_with_unspecified_all_feats.csv')

