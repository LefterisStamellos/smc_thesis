##### extract median, 1st, 3rd quartiles and interquartile range statistics####

import numpy as np, pandas as pd

# fill a DatFrame with contents of csv with answers 
# changed in a way such that results can be used for 
# plotting box plots
df = pd.DataFrame()
df = pd.read_csv('answers_for_boxplots.csv')
df = df.iloc[:,1:]

# Fill a DataFrame with stats (1st q, median, 3rd q, iqr) for one question, different categories,
# both for random and classifier

# df = df[df['question'] == 'substitutability']
# df = df[df['type'] == 'rand']

# categories = ['no_train','train_under5','train_over5']

# df_rand_stats = pd.DataFrame()
# for c in categories:
#     df_tmp = pd.DataFrame()
#     df_tmp = df[df['category'] == c]
#     df_tmp = df_tmp[df_tmp['type'] == 'rand']
#     med = np.median(df_tmp['response'])
#     q75, q25 = np.percentile(df_tmp['response'], [75 ,25])
#     iqr = q75 - q25
#     df_rand_stats[c] = np.array([q75,med,q25,iqr])
# df_rand_stats.rename({0:'3rd quartile',1:'median',2:'1st quartile',3:'iqr'})

# df_clfr_stats = pd.DataFrame()
# for c in categories:
#     df_tmp = pd.DataFrame()
#     df_tmp = df[df['category'] == c]
#     df_tmp = df_tmp[df_tmp['type'] == 'clfr']
#     med = np.median(df_tmp['response'])
#     q75, q25 = np.percentile(df_tmp['response'], [75 ,25])
#     iqr = q75 - q25
#     df_clfr_stats[c] = np.array([q75,med,q25,iqr])
# df_clfr_stats.rename({0:'3rd quartile',1:'median',2:'1st quartile',3:'iqr'})

# Fill a DataFrame with stats (1st q, median, 3rd q, iqr) for all questions, one category (all),
# both for random and classifier

df = df[df['category'] == 'all']
questions = ['similarity','substitutability','appreciation']

df_rand_stats = pd.DataFrame()
for q in questions:
    df_tmp = pd.DataFrame()
    df_tmp = df[df['question'] == q]
    df_tmp = df_tmp[df_tmp['type'] == 'rand']
    med = np.median(df_tmp['response'])
    q75, q25 = np.percentile(df_tmp['response'], [75 ,25])
    iqr = q75 - q25
    df_rand_stats[q] = np.array([q75,med,q25,iqr])
df_rand_stats.rename({0:'3rd quartile',1:'median',2:'1st quartile',3:'iqr'})

df_clfr_stats = pd.DataFrame()
for q in questions:
    df_tmp = pd.DataFrame()
    df_tmp = df[df['question'] == q]
    df_tmp = df_tmp[df_tmp['type'] == 'clfr']
    med = np.median(df_tmp['response'])
    q75, q25 = np.percentile(df_tmp['response'], [75 ,25])
    iqr = q75 - q25
    df_clfr_stats[q] = np.array([q75,med,q25,iqr])
df_clfr_stats.rename({0:'3rd quartile',1:'median',2:'1st quartile',3:'iqr'})