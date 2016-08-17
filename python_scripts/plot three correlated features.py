import os
import numpy as np
import pandas as pd
# %matplotlib inline
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

feat1 = 'spectral_flatness_db_mean'
feat2 = 'spectral_crest_mean'
feat3 = 'spectral_entropy_mean'

pardir = '../experiment_text_files/big_train_set_files/json_and_csv/7_classes'

filename = 'big_experiment_7classes_no_silence.csv'

df = pd.read_csv(os.path.join(pardir,filename))

x = df[feat1].as_matrix()
y = df[feat2].as_matrix()
z = df[feat3].as_matrix()

fig = plt.figure(figsize=(14,12))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(x, y, z, c='m', marker='^')

ax.set_xlabel(feat1)
ax.set_ylabel(feat2)
ax.set_zlabel(feat3)

ax.view_init(30,120)

plt.show()