
# coding: utf-8

# In[1]:

import os

import numpy as np

import pandas as pd

from sklearn.neighbors import KNeighborsClassifier

from sklearn.ensemble import RandomForestClassifier

from sklearn.preprocessing import MinMaxScaler

from sklearn.svm import SVC

from sklearn.cross_validation import cross_val_score

from sklearn.externals import joblib


# In[2]:

df = pd.DataFrame()
df = pd.read_csv('../experiment_text_files/big_train_set_files/json_and_csv/7_classes/big_experiment_7classes_no_silence.csv')


# In[3]:

y = df['instrument'].as_matrix()


# In[4]:

df_feat = pd.DataFrame()


# In[5]:

feats = ['zerocrossingrate_mean','spectral_entropy_mean','logattacktime_mean','spectral_energyband_middle_low_mean',
         'effective_duration_mean','spectral_skewness_mean','mfcc_mean_4','mfcc_mean_5','mfcc_mean_6','scvalleys_var_2',
         'pitch_instantaneous_confidence_mean','gfcc_mean_2','pitch_mean','spectral_kurtosis_mean']


# In[6]:

for feat in feats:
    df_feat[feat] = df[feat]


# In[7]:

df_feat.shape


# In[8]:

X = df_feat.as_matrix()


# In[9]:

min_max_scaler = MinMaxScaler()
X = min_max_scaler.fit_transform(X)
###### KNN manhattan ###############
model = KNeighborsClassifier(n_neighbors = 1,algorithm = 'brute',metric = 'manhattan',weights = 'uniform')
scores = cross_val_score(model,X,y, cv=10)


# In[10]:

# ###### SVM Poly, degree = 1, C=10 ###############
# model = SVC(C = 10.0,kernel = 'poly',degree = 1.0)
# scores = cross_val_score(model,X,y, cv=10)


# In[11]:

# ###### Random Forest, 100 Trees ###############
# model = RandomForestClassifier(n_estimators = 100)
# scores = cross_val_score(model,X,y, cv=10)


# In[12]:

np.mean(scores)


# In[13]:

model.fit(X,y)


# In[14]:

pardir = '../experiment_text_files/big_train_set_files/npy/7_classes'


# In[15]:

newdir = 'kNN_real_set_14FEATS_nosil'


# In[16]:

os.mkdir(os.path.join(pardir,newdir))


# In[17]:

joblib.dump(model, os.path.join(pardir,newdir,'kNN_real_set.pkl')) 


# In[ ]:




# In[ ]:



