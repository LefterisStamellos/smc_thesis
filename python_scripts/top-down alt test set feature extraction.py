
# coding: utf-8

# In[8]:

#http://pandas.pydata.org/
import pandas as pd
import numpy as np
import os
import ipdb
import json
import subprocess
import yaml


# In[2]:

from sklearn.cluster import KMeans,k_means,Birch


# In[ ]:

from sklearn import cluster


# In[ ]:

path = '../database/recorded_and_downloaded_alt_sounds_processed'


# In[ ]:

folders = os.listdir(path)[1:]


# In[ ]:

for folder in folders:
    tracks = os.listdir(os.path.join(path,folder))
    for track in tracks:
        if (track[-3:] == 'wav' or track[-3:] == 'WAV'):        
            subprocess.Popen(['essentia_streaming_extractor_freesound',os.path.join(path,folder,track),os.path.join(path,folder,track[:-4] + '.json')])


# In[ ]:

feat_df = pd.DataFrame()
names = np.array([])


# In[ ]:

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


# In[9]:

feat_df.to_csv('alt_test_all.csv')


# In[13]:

feat_df = pd.read_csv('../../../alt_test_set_text_files/json_and_csv/alt_test_all.csv')


# In[ ]:

feats = ['spectral_contrast_mean_4','spectral_energyband_middle_low_mean','spectral_contrast_mean_5',
 'spectral_energyband_high_mean','spectral_contrast_var_0']


# In[ ]:

new_feat_df = pd.DataFrame()


# In[ ]:

for feat in feats:
    new_feat_df[feat] = feat_df[feat]


# In[ ]:

new_feat_df


# In[ ]:

feat_df.to_csv('alt_test_clustering1.csv')


# In[14]:

cd


# In[15]:

import pandas2arff


# In[16]:

pandas2arff.pandas2arff(feat_df,filename='alt_test_all.arff')


# In[ ]:

pandas2arff.pandas2arff(new_feat_df,filename='alt_test_clustering1.arff')


# In[6]:

fit_predict = model.fit_predict(X)


# # sorted_names = np.array([])

# In[ ]:

for i in np.argsort(fit_predict):
    sorted_names = np.append(sorted_names,names[i])


# In[ ]:

sorted_names


# In[ ]:

get_ipython().magic(u'pinfo Birch')


# In[ ]:



