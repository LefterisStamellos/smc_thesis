import os
import numpy as np
import pandas as pd
get_ipython().magic(u'matplotlib inline')
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cross_validation import cross_val_score
from sklearn.preprocessing import MinMaxScaler
import pandas2arff

inst = 'crash'

pardir = '../experiment_text_files/big_train_set_files/json_and_csv/1classVSall'
filename = '{inst}_vs_all_nosil.csv'.format(inst = inst)

# pardir = '../experiment_text_files/big_train_set_files/json_and_csv/7_classes'
# filename = 'big_experiment_7classes_no_silence.csv'

feats = ['logattacktime_mean','instrument']

df = pd.read_csv(os.path.join(pardir,filename))
df_feat = pd.DataFrame()
for feat in feats:
    df_feat[feat] = df[feat]

X = df_feat.iloc[:,:-1].as_matrix()

y = df_feat['instrument'].as_matrix()

min_max_scaler = MinMaxScaler()
X = min_max_scaler.fit_transform(X)

###### KNN manhattan ###############
model = KNeighborsClassifier(n_neighbors = 1,algorithm = 'brute',metric = 'manhattan',weights = 'uniform')
scores = cross_val_score(model,X,y, cv=10)

accuracy = round(np.mean(scores),4)


import numpy as np
import seaborn as sns

sns.set(style = "white",palette="muted", color_codes=True,font_scale=3)

ax = sns.boxplot(x=feats[0], y="instrument", data=df_feat,whis=np.inf, palette = ['r','b'])
sns.stripplot(x=feats[0], y="instrument", data=df_feat,jitter=True, size=3, color=".3", linewidth=0)
ax.set_xlabel('log attack time',fontsize = 40)
ax.set_ylabel('')
ax.set(xticklabels=[])

ax.set_title('accuracy rate: {acc}%'.format(acc = accuracy*100),fontsize = 20)
# ax.set_title('accuracy rate: 92.19%',fontsize = 20)

sns.plt.show()