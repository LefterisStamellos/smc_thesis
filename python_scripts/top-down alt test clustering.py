import pandas as pd
import numpy as np
import os
from sklearn.cluster import Birch
from shutil import copyfile
from sklearn import cluster

path = '../database/recorded_and_downloaded_alt_sounds_processed'

folders = os.listdir(path)[1:]
filenames = np.array([])

for folder in folders:
    tracks = os.listdir(os.path.join(path,folder))
    for track in tracks:
        if (track[-3:] == 'wav' or track[-3:] == 'WAV'):
            filenames = np.append(filenames,track)

os.mkdir('../database/all_recorded_and_downloaded_alt_sounds_processed')

for folder in folders:
    tracks = os.listdir(os.path.join(path,folder))
    for track in tracks:
        if (track[-3:] == 'wav' or track[-3:] == 'WAV'):
            copyfile(os.path.join(path,folder,track),os.path.join('../database/all_recorded_and_downloaded_alt_sounds_processed',track))

new_feat_df = pd.read_csv('../../../alt_test_set_text_files/json_and_csv/alt_test_all.csv')

X = new_feat_df.as_matrix()

cluster.Birch()
model = cluster.Birch()

fit_predict = model.fit_predict(X)
fit_predict_sorted = np.argsort(fit_predict)

sorted_filenames = np.array([])
for i in fit_predict_sorted:
    sorted_filenames = np.append(sorted_filenames,filenames[i])

cluster_labels = np.unique(fit_predict)
cluster_folders = np.array([])
for label in cluster_labels:
    new_folder = '../database/all_recorded_and_downloaded_alt_sounds_processed/LEVEL1_cluster_' + str(label)
    cluster_folders = np.append(cluster_folders,new_folder)
    os.mkdir(new_folder)

for i in range(len(fit_predict)):
    copyfile('../database/all_recorded_and_downloaded_alt_sounds_processed/' + sorted_filenames[i],
            '../database/all_recorded_and_downloaded_alt_sounds_processed/LEVEL1_cluster_' + str(fit_predict[i]) + '/' + sorted_filenames[i])