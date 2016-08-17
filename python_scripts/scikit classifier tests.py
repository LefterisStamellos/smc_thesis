import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cross_validation import cross_val_score
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import MinMaxScaler
import os

# df_train = pd.DataFrame()
# df_test = pd.DataFrame()

# df_train = pd.read_csv('../../../experiment_text_files/json_and_csv/big_experiment.csv')
# df_test = pd.read_csv('../../../alt_test_set_text_files/json_and_csv/big_alt_test.csv')

pardir = '../experiment_text_files/big_train_set_files/json_and_csv/7_classes'
filename = 'big_experiment_7classes_balanced.csv'

df = pd.DataFrame()
df = pd.read_csv(os.path.join(pardir,filename))
df = df.iloc[:,1:]


####################################################################

# # ######## features for percussive vs non-percussive classification #######################
# # # feats = ['temporal_centroid_mean','temporal_skewness_mean','effective_duration_mean','logattacktime_mean',
# # # 'temporal_kurtosis_mean','instrument']

# # ###### 30 features selected for 17 classes classifier (alternative data set) ######################
# # feats = ['spectral_rolloff_mean','zerocrossingrate_mean','mfcc_mean_2','pitch_instantaneous_confidence_mean',
# #          'spectral_centroid_mean','spectral_flatness_db_mean','spectral_contrast_var_4','gfcc_mean_1',
# #          'spectral_energyband_high_mean','spectral_energyband_middle_low_mean','spectral_entropy_mean',
# #          'barkbands_spread_mean','pitch_mean','spectral_contrast_var_3','spectral_contrast_mean_5','dissonance_mean',
# #          'mfcc_mean_3','spectral_skewness_mean','spectral_kurtosis_mean','spectral_strongpeak_mean',
# #          'scvalleys_mean_5','spectral_contrast_var_2','mfcc_mean_4','hfc_mean','scvalleys_mean_4','mfcc_var_0',
# #          'spectral_contrast_var_0','spectral_contrast_mean_4','mfcc_mean_1','spectral_complexity_mean']

# ####### 30 features selected for 17 classes classifier (real data set) ######################
# feats = ['der_av_after_max_mean','effective_duration_mean','gfcc_mean_2','logattacktime_mean','mfcc_mean_5',
#   'spectral_centroid_mean','gfcc_mean_1','spectral_kurtosis_mean','spectral_contrast_mean_4','pitch_mean',
#   'silence_rate_20dB_mean','spectral_rolloff_mean','mfcc_mean_2','mfcc_mean_4','spectral_contrast_var_5','mfcc_mean_3',
#   'mfcc_mean_6','spectral_entropy_mean','spectral_skewness_mean','spectral_contrast_var_0','temporal_centroid_mean',
#   'zerocrossingrate_mean','barkbands_skewness_mean','temporal_kurtosis_mean','spectral_flatness_db_mean','mfcc_var_1',
#   'mfcc_mean_1','spectral_contrast_var_4','gfcc_mean_3','spectral_energyband_high_mean']


####################################################################

# df_X = pd.DataFrame()
# for feat in feats:
#     df_X[feat] = df[feat]


X = df.iloc[:,:-1].as_matrix()
y = df['instrument'].as_matrix()


####################################################################

# ###### Random Forest, 100 Trees ###############
# model = RandomForestClassifier(n_estimators = 100)
# scores = cross_val_score(model,X,y, cv=10)

####################################################################

###### KNN manhattan ###############
min_max_scaler = MinMaxScaler()
X = min_max_scaler.fit_transform(X)

model = KNeighborsClassifier(n_neighbors = 1,algorithm = 'brute',metric = 'manhattan',weights = 'uniform')
scores = cross_val_score(model,X,y, cv=10)

df_predict = pd.DataFrame()
df_p = pd.read_csv('../../../alt_test_set_text_files/json_and_csv/big_alt_test.csv')

for feat in feats:
    df_predict[feat] = df_p[feat]

X_predict = df_predict.as_matrix()

pardir = '../database/all_recorded_and_downloaded_alt_sounds_processed'
names = np.array([])

import os

folders = os.listdir(pardir)[1:]
for folder in folders:
    tracks = os.listdir(os.path.join(pardir,folder))
    for track in tracks:
        if track[-3:] == 'wav' or track[-3:] == 'WAV':
            names = np.append(names,track[:-4])

df_results['names'] = names
df_results['expected_class'] = df_p['instrument'].as_matrix()
df_results['predicted_class'] = model.predict(X_predict)
#df_results[df_results['expected_class'] == 'crash_choke']

df_results_stats = pd.DataFrame()

instruments = np.unique(y_test)

df_results_stats['class'] = instruments

correct_classification = np.array([])
class_size = np.array([])
for instrument in instruments:
    df_tmp = pd.DataFrame()
    df_tmp = df_results[df_results['expected_class'] == instrument]
    correct_classification = np.append(correct_classification,(len(df_tmp[df_tmp['predicted_class'] == instrument]) / float(df_tmp.shape[0]))*100)
    class_size = np.append(class_size,df_tmp.shape[0])
df_results_stats['correct_classification_%'] = correct_classification
df_results_stats['class_size'] = class_size

####################################################################

from StringIO import StringIO
import subprocess
import os
out = StringIO()
export_graphviz(model, 
    out_file=out, 
    feature_names=['temporal_centroid_mean','temporal_skewness_mean','effective_duration_mean','logattacktime_mean',
             'temporal_kurtosis_mean'], 
    class_names=model.classes_,
    impurity=True,
    proportion=True)
fid = open('tmp.dot','w')
fid.write(out.getvalue())
fid.close()
# Print tree with "dot -Tpng tree.dot -o tree.png"
try:
    os.system('dot -Tpng tmp.dot -o tree.png')
except Exception, e:
    print 'ERROR: could not generate tree.png (%s)' %  e
os.system('rm tmp.dot')


from IPython.display import Image
Image(filename='tree.png') 

X_pred = model.predict(X_test)
import sklearn.metrics
sklearn.metrics.accuracy_score(y_test, X_pred)