###### process data in participants' answers in such a way that they can be used to plot box plots

import pandas as pd, numpy as np, os, json, csv

#load json with participants' answers into a dictionary
with open('answers.json') as data_file:    
    data = json.load(data_file)

questions = ['similarity','substitutability','appreciation']
responses = ['strong_disagree','disagree','neutral','agree','strong_agree']
types = ['clfr','rand']
categories = ['all','composers','non composers','drummers','non drummers','not trained','trained under 5','trained over 5']
boxplot_dict = {}

df = pd.DataFrame()
for q in questions:
    df_q = pd.DataFrame()
    for key, values in data.items():
        df_step = pd.DataFrame()
        if key!='step1':
            for user, resp in values.items():
                df_user = pd.DataFrame()
                if (int(key[4:]) < 12):
                    typ = 'clfr'
                else:
                    typ = 'rand'
                for i in range(3):
                    df_tmp = pd.DataFrame()
                    df_tmp['question'] = [q]
                    df_tmp['category'] = [data['step1'][user][i]]
                    df_tmp['response'] = [responses.index(resp[questions.index(q)])]
                    df_tmp['type'] = [typ]
                    df_user = pd.concat([df_user,df_tmp],axis=0)
                df_tmp = pd.DataFrame()
                df_tmp['question'] = [q]
                df_tmp['category'] = ['all']
                df_tmp['response'] = [responses.index(resp[questions.index(q)])]
                df_tmp['type'] = [typ]
                df_user = pd.concat([df_user,df_tmp],axis=0)
                df_step = pd.concat([df_step,df_user],axis=0)
        df_q = pd.concat([df_q,df_step],axis=0)
    df = pd.concat([df,df_q],axis=0)

#dump to csv
df.to_csv('answers_for_boxplots.csv')