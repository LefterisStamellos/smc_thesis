
# coding: utf-8

# In[ ]:

import os

import numpy as np

import pandas as pd

# %matplotlib inline

from mpl_toolkits.mplot3d import Axes3D

import matplotlib.pyplot as plt

import matplotlib.cm as cm

import seaborn as sns

from sklearn.neighbors import KNeighborsClassifier

from sklearn.cross_validation import cross_val_score

from sklearn.preprocessing import MinMaxScaler


# In[ ]:

# one = 'snare'

# pardir = '../experiment_text_files/big_train_set_files/json_and_csv/1classVSall'
# filename = '{inst}_vs_all_nosil.csv'.format(inst = one)

pardir = '../experiment_text_files/big_train_set_files/json_and_csv/7_classes'
filename = 'big_experiment_7classes_no_silence.csv'

# feats = ['pitch_mean','spectral_kurtosis_mean','spectral_skewness_mean','spectral_centroid_mean',
#          'pitch_instantaneous_confidence_mean','spectral_energyband_middle_low_mean','mfcc_mean_1','mfcc_mean_2',
#          'mfcc_mean_3','mfcc_mean_4','mfcc_mean_5','gfcc_mean_1','gfcc_mean_2','der_av_after_max_mean',
#          'logattacktime_mean','instrument']

feats =['pitch_instantaneous_confidence_mean','effective_duration_mean','zerocrossingrate_mean','instrument']

df = pd.read_csv(os.path.join(pardir,filename))

df_feat = pd.DataFrame()

for feat in feats:
    df_feat[feat] = df[feat]


# In[ ]:

# import pandas2arff

# pandas2arff.pandas2arff(df_feat,filename='rim_vs_all_15feats.arff',wekaname = 'instrument')


# In[ ]:

X = df_feat.iloc[:,:-1].as_matrix()

y = df_feat['instrument'].as_matrix()


# In[ ]:

min_max_scaler = MinMaxScaler()
X = min_max_scaler.fit_transform(X)

###### KNN manhattan ###############
model = KNeighborsClassifier(n_neighbors = 1,algorithm = 'brute',metric = 'manhattan',weights = 'uniform')
scores = cross_val_score(model,X,y, cv=10)

accuracy = np.mean(scores)


# In[ ]:

accuracy


# In[ ]:

crash = df_feat[df_feat['instrument'] == 'crash']
crash_matrix = crash.iloc[:,:-1].as_matrix()

ride = df_feat[df_feat['instrument'] == 'ride']
ride_matrix = ride.iloc[:,:-1].as_matrix()

hihat = df_feat[df_feat['instrument'] == 'hihat']
hihat_matrix = hihat.iloc[:,:-1].as_matrix()

rim = df_feat[df_feat['instrument'] == 'rim']
rim_matrix = rim.iloc[:,:-1].as_matrix()

snare = df_feat[df_feat['instrument'] == 'snare']
snare_matrix = snare.iloc[:,:-1].as_matrix()

tom = df_feat[df_feat['instrument'] == 'tom']
tom_matrix = tom.iloc[:,:-1].as_matrix()

kick = df_feat[df_feat['instrument'] == 'kick']
kick_matrix = kick.iloc[:,:-1].as_matrix()


# In[ ]:

# red = df_feat[df_feat['instrument'] == one]
# red_matrix = red.iloc[:,-2:-1].as_matrix()

# # blue = df_feat[df_feat['instrument'] == 'not_'+one]
# blue = df_feat[df_feat['instrument'] != one]
# blue_matrix = blue.iloc[:,-2:-1].as_matrix()


# In[ ]:

# x_red = np.ravel(red.iloc[:,:1].as_matrix())
# y_red = np.ravel(red.iloc[:,1:2].as_matrix())
# z_red = np.ravel(red.iloc[:,2:3].as_matrix())

# x_blue = np.ravel(blue.iloc[:,:1].as_matrix())
# y_blue = np.ravel(blue.iloc[:,1:2].as_matrix())
# z_blue = np.ravel(blue.iloc[:,2:3].as_matrix())

# fig = plt.figure(figsize=(14,12))
# ax = fig.add_subplot(111, projection='3d')

# ax.scatter(x_red, y_red, z_red, c='r',label = one)
# ax.scatter(x_blue, y_blue, z_blue, c='b',label = 'not '+one)

# ax.set_zlabel('mean zero crossing rate',fontsize = 24)
# ax.set_ylabel('mean spectral entropy',fontsize = 24)
# ax.set_xlabel('mean spectral energy of mid low band',fontsize = 24)
# ax.set(xticklabels=[])
# ax.set(yticklabels=[])
# ax.set(zticklabels=[])

# plt.legend(fontsize = 24)

# ax.view_init(30,45)

# # plt.title('{inst} : Classification accuracy = {acc}%'.format(inst = one, acc = round(accuracy*100.0,2)),fontsize = '16',y=1.08)
# plt.title('Classification accuracy = {acc}%'.format(acc = round(accuracy*100.0,2)),fontsize = '20',y=1.08)


# plt.show()


# In[ ]:

x_crash = np.ravel(crash.iloc[:,:1].as_matrix())
y_crash = np.ravel(crash.iloc[:,1:2].as_matrix())
z_crash = np.ravel(crash.iloc[:,2:3].as_matrix())

x_ride = np.ravel(ride.iloc[:,:1].as_matrix())
y_ride = np.ravel(ride.iloc[:,1:2].as_matrix())
z_ride = np.ravel(ride.iloc[:,2:3].as_matrix())

x_hihat = np.ravel(hihat.iloc[:,:1].as_matrix())
y_hihat = np.ravel(hihat.iloc[:,1:2].as_matrix())
z_hihat = np.ravel(hihat.iloc[:,2:3].as_matrix())

x_rim = np.ravel(rim.iloc[:,:1].as_matrix())
y_rim = np.ravel(rim.iloc[:,1:2].as_matrix())
z_rim = np.ravel(rim.iloc[:,2:3].as_matrix())

x_snare = np.ravel(snare.iloc[:,:1].as_matrix())
y_snare = np.ravel(snare.iloc[:,1:2].as_matrix())
z_snare = np.ravel(snare.iloc[:,2:3].as_matrix())

x_tom = np.ravel(tom.iloc[:,:1].as_matrix())
y_tom = np.ravel(tom.iloc[:,1:2].as_matrix())
z_tom = np.ravel(tom.iloc[:,2:3].as_matrix())

x_kick = np.ravel(kick.iloc[:,:1].as_matrix())
y_kick = np.ravel(kick.iloc[:,1:2].as_matrix())
z_kick = np.ravel(kick.iloc[:,2:3].as_matrix())

fig = plt.figure(figsize=(14,12))
ax = fig.add_subplot(111, projection='3d')

ax.scatter(x_crash, y_crash, z_crash, c='b',label = 'crash')
ax.scatter(x_ride, y_ride, z_ride, c=sns.xkcd_rgb['deep turquoise'],label = 'ride')
ax.scatter(x_hihat, y_hihat, z_hihat, c='r',label = 'hihat')
ax.scatter(x_rim, y_rim, z_rim, c=sns.xkcd_rgb['soft pink'],label = 'rim')
ax.scatter(x_snare, y_snare, z_snare, c=sns.xkcd_rgb['radioactive green'],label = 'snare')
ax.scatter(x_tom, y_tom, z_tom, c=sns.xkcd_rgb['golden yellow'] ,label = 'tom')
ax.scatter(x_kick, y_kick, z_kick, c=sns.xkcd_rgb['bright aqua'],label = 'kick')

# ax.set_xlabel(np.array(df_feat.T.index)[0])
# ax.set_ylabel(np.array(df_feat.T.index)[1])
# ax.set_zlabel(np.array(df_feat.T.index)[2])
ax.set_zlabel('mean zero crossing rate',fontsize = 24)
ax.set_ylabel('effective duration',fontsize = 24)
ax.set_xlabel('mean pitch instantaneous confidence',fontsize = 24)
ax.set(xticklabels=[])
ax.set(yticklabels=[])
ax.set(zticklabels=[])

plt.legend(fontsize = 20)

ax.view_init(45,45)

# plt.title('{inst} : Classification accuracy = {acc}%'.format(inst = one, acc = round(accuracy*100.0,2)),fontsize = '16',y=1.08)
plt.title('Classification accuracy = {acc}%'.format(acc = round(accuracy*100.0,2)),fontsize = '18',y=1.08)


plt.show()


# In[ ]:

# plt.ylim([-1,2])
# val = 0. # this is the value where you want the data to appear on the y-axis.
# sctr1, = plt.plot(red_matrix, np.zeros_like(red_matrix) + 1, 'ro',label = one)
# sctr2, = plt.plot(blue_matrix, np.zeros_like(blue_matrix) + 0, 'bo',label = 'not '+one)

# plt.xlabel('pitch instantaneous confidence',fontsize = 'large')

# # Create a legend for the first line.
# first_legend = plt.legend(handles=[sctr1], loc=1)

# # Add the legend manually to the current Axes.
# ax = plt.gca().add_artist(first_legend)

# # Create another legend for the second line.
# fig = plt.legend(handles=[sctr2], loc=4)
# fig.axes.get_yaxis().set_visible(False)

# plt.show()


# In[ ]:

# plt.ylim([-1,7])

# sctr1, = plt.plot(crash_matrix, np.zeros_like(crash_matrix) + 0, 'ro',label = 'crash')
# sctr2, = plt.plot(ride_matrix, np.zeros_like(ride_matrix) + 1, 'bo',label = 'ride')
# sctr3, = plt.plot(hihat_matrix, np.zeros_like(hihat_matrix) + 2, 'go',label = 'hihat')
# sctr4, = plt.plot(rim_matrix, np.zeros_like(rim_matrix) + 3, 'co',label = 'rim')
# sctr5, = plt.plot(snare_matrix, np.zeros_like(snare_matrix) + 4, 'mo',label = 'snare')
# sctr6, = plt.plot(tom_matrix, np.zeros_like(tom_matrix) + 5, 'yo',label = 'tom')
# sctr7, = plt.plot(kick_matrix, np.zeros_like(kick_matrix) + 6, 'ko',label = 'kick')

# plt.title('pitch instantaneous confidence',fontsize = '22')

# y = list(np.arange(0,7))
# tix = ['crash','ride','hihat','rim','snare','tom','kick']

# plt.yticks(y,tix,fontsize = '16')
# plt.show()


# In[ ]:

# sns.set(color_codes=True)
# np.random.seed(sum(map(ord, "distributions")))

# sns.pairplot(df_feat,hue="instrument")

# # colors = ['blue','red','bright aqua','deep turquoise','soft pink','radioactive green','golden yellow']

# # sns.pairplot(df_feat,hue="instrument",palette = sns.xkcd_palette(colors))

# # df_X = pd.DataFrame()

# # for i in range(3):
# #     df_X[df_feat.T.index[i]] = X[:,i]

# # df_X['instrument'] = y

# # sns.pairplot(df_X,hue="instrument")


# sns.plt.show()


# In[ ]:



