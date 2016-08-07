import os
import numpy as np
import pandas as pd
get_ipython().magic(u'matplotlib inline')
import matplotlib.pyplot as plt

feat1 = 'spectral_flatness_db_mean'
feat2 = 'spectral_crest_mean'

pardir = '../experiment_text_files/big_train_set_files/json_and_csv/7_classes'

filename = 'big_experiment_7classes_no_silence.csv'

df = pd.read_csv(os.path.join(pardir,filename))

x = df[feat1].as_matrix()
y = df[feat2].as_matrix()

plt.plot(x,y,'mo')
plt.xlabel(feat1,fontsize = 'large')
plt.ylabel(feat2,fontsize = 'large')
plt.show()