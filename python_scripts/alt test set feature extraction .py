import pandas as pd,numpy as np,os,yaml
#https://github.com/saurabhnagrecha/Pandas-to-ARFF
import pandas2arff

#path to csv file containing sounds' extracted features
pardir = '../experiment_text_files/alt_test_set_text_files/json_and_csv/with_unspecified'

#csv file containing sounds' extracted features
filename = 'alt_test_with_unspecified.csv'

df = pd.read_csv(os.path.join(pardir,filename))
feat_df = pd.DataFrame()

#list of features we intend to keep 
feats = ['spectral_centroid_mean','spectral_entropy_mean','gfcc_mean_2','logattacktime_mean','spectral_skewness_mean',
         'spectral_energyband_middle_low_mean','scvalleys_var_2','effective_duration_mean',
         'pitch_instantaneous_confidence_mean']

for feat in feats:
    feat_df[feat] = df[feat]

exported_csv_fname = 'alt_test_with_unspecified_9FEATS_nosil'
feat_df.to_csv(exported_csv_fname + '.csv')

exported_arff_fname = 'alt_test_with_unspecified_9FEATS_nosil'
pandas2arff.pandas2arff(feat_df,filename=exported_arff_fname + '.arff',wekaname = 'instrument')