
# coding: utf-8

# In[1]:

import numpy as np

import pandas as pd

from sklearn.cluster import KMeans

import os


# In[2]:

df = pd.DataFrame()
df = pd.read_csv('../../../alt_test_set_text_files/json_and_csv/big_alt_test.csv')


# In[3]:

X = df.iloc[:,1:-1].as_matrix()
y = df.iloc[:,-1:].as_matrix()


# In[4]:

# # # ###### randomized principal component analysis for dimensionality reduction of alt set ########
# # # The purpose is to find a way to effectively label our data, since labeling based solely on 
# # # perceptual criteria (meaning, just listening to the sounds and judging to which instrument they should
# # # be assigned) does not work well enough.
# # from sklearn.decomposition import RandomizedPCA as RandPCA

# # pca = RandPCA(n_components = 30)

# # X = pca.fit_transform(X)
from sklearn.manifold import Isomap
isomap = Isomap(n_components=30)
X = isomap.fit_transform(X)


# In[5]:

############ cluster the alternative set into 17 clusters, using KMeans ##########
clstrer = KMeans(n_clusters = 17)
clstr = clstrer.fit_predict(X)


# In[6]:

########### names will be filled with the wav files' filenames ################
pardir = '../database/all_recorded_and_downloaded_alt_sounds_processed'
names = np.array([])
folders = os.listdir(pardir)[1:]
for folder in folders:
    tracks = os.listdir(os.path.join(pardir,folder))
    for track in tracks:
        if track[-3:] == 'wav' or track[-3:] == 'WAV':
            names = np.append(names,track)


# In[7]:

sorted_clstr = np.sort(clstr)
sorted_clstr_ind = np.argsort(clstr)

sorted_names = np.array([])
sorted_expexted_classes = np.array([])

for i in range(len(sorted_clstr_ind)):
    sorted_names = np.append(sorted_names,names[sorted_clstr_ind[i]])
    sorted_expexted_classes = np.append(sorted_expexted_classes,y[sorted_clstr_ind[i]])


# In[8]:

df_results = pd.DataFrame()

df_results['filename'] = sorted_names
df_results['expected_class'] = sorted_expexted_classes
df_results['cluster'] = sorted_clstr


# In[9]:

instruments = np.unique(y)


# In[10]:

pardir = '../database'


# In[11]:

from shutil import copyfile


# In[12]:

for i in range(len(instruments)):
    folder_name = 'cluster' + str(i)
    os.mkdir(os.path.join(pardir,folder_name))
    
    tmp = pd.DataFrame()
    tmp = df_results[df_results['cluster'] == i]
    
    filenames = np.array([])
    filenames = tmp['filename'].as_matrix()
    
    expected_classes = np.array([])
    expected_classes = tmp['expected_class'].as_matrix()
    
    clusters = np.array([])
    clusters = tmp['cluster'].as_matrix()
    
    for i in range(len(filenames)):
        src = os.path.join(pardir,'all_recorded_and_downloaded_alt_sounds_processed',expected_classes[i],filenames[i])
        dst = os.path.join(pardir,folder_name,filenames[i])
        copyfile(src,dst)


# In[14]:

df_results[df_results['cluster'] == 0].sort_values(by = 'expected_class')


# In[ ]:



