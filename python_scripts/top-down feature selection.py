import pandas as pd
import numpy as np

feat_df = pd.read_csv('../../../experiment_text_files/json_and_csv/big_experiment.csv')

idiophones = ['crash_choke','crash_edge','hihat_chick','hihat_choke','hihat_closed','hihat_open','ride_bow','ride_bell',
              'cross_stick','rim_hit']
category = np.array([])

for inst in feat_df['instrument']:
    if inst in idiophones:
        category = np.append(category,'idiophone')
    else:
        category = np.append(category,'membranophone')

instruments = np.unique(feat_df['instrument'])

feat_df = feat_df.iloc[:,1:-1]
feat_df['category'] = category

import pandas2arff
pandas2arff.pandas2arff(feat_df,filename='big_experiment_categories_1.arff',wekaname = 'category')