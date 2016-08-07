
# coding: utf-8

# In[1]:

import pandas as pd
import numpy as np
import os
from sklearn.cluster import Birch
from shutil import copyfile


# In[2]:

from sklearn import cluster


# In[3]:

path = '../database/recorded_and_downloaded_alt_sounds_processed'


# In[4]:

folders = os.listdir(path)[1:]


# In[5]:

filenames = np.array([])


# In[6]:

for folder in folders:
    tracks = os.listdir(os.path.join(path,folder))
    for track in tracks:
        if (track[-3:] == 'wav' or track[-3:] == 'WAV'):
            filenames = np.append(filenames,track)


# In[7]:

os.mkdir('../database/all_recorded_and_downloaded_alt_sounds_processed')


# In[8]:

for folder in folders:
    tracks = os.listdir(os.path.join(path,folder))
    for track in tracks:
        if (track[-3:] == 'wav' or track[-3:] == 'WAV'):
            copyfile(os.path.join(path,folder,track),os.path.join('../database/all_recorded_and_downloaded_alt_sounds_processed',track))


# In[9]:

new_feat_df = pd.read_csv('../../../alt_test_set_text_files/json_and_csv/alt_test_all.csv')


# In[10]:

X = new_feat_df.as_matrix()


# In[ ]:

cluster.Birch()


# In[11]:

model = cluster.Birch()


# In[12]:

fit_predict = model.fit_predict(X)


# In[13]:

fit_predict_sorted = np.argsort(fit_predict)


# In[14]:

sorted_filenames = np.array([])


# In[15]:

for i in fit_predict_sorted:
    sorted_filenames = np.append(sorted_filenames,filenames[i])


# In[16]:

cluster_labels = np.unique(fit_predict)


# In[17]:

cluster_folders = np.array([])


# In[18]:

for label in cluster_labels:
    new_folder = '../database/all_recorded_and_downloaded_alt_sounds_processed/LEVEL1_cluster_' + str(label)
    cluster_folders = np.append(cluster_folders,new_folder)
    os.mkdir(new_folder)


# In[19]:

for i in range(len(fit_predict)):
    copyfile('../database/all_recorded_and_downloaded_alt_sounds_processed/' + sorted_filenames[i],
            '../database/all_recorded_and_downloaded_alt_sounds_processed/LEVEL1_cluster_' + str(fit_predict[i]) + '/' + sorted_filenames[i])


# In[ ]:



