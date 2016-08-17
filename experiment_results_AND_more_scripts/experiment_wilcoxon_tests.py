##### fill csv with wilcoxon tests on experimental results

# %matplotlib inline
import pandas as pd, numpy as np, matplotlib.pyplot as plt, seaborn as sns, os, json,matplotlib.pyplot as plt
from scipy.stats import wilcoxon

#load json with participants' answers into a dictionary
with open('answers_curated.json') as data_file:    
    data = json.load(data_file)

questions = ['similarity','substitutability','appreciation']
categories = ['all','composers','non composers','drummers','non drummers','not trained','trained under 5','trained over 5']

wilcoxon_dict = {}
for category in categories:
    wilcoxon_dict[category] = {questions[0]:(),questions[1]:(),questions[2]:()}

for category in categories:
    for question in questions:
        x1 = data['clfr'][category][question]
        x2 = data['rand'][category][question]
        (a,b) = wilcoxon(x1, x2)
        wilcoxon_dict[category][question] = (a,round(b,4))

#load json with participants' answers into a dictionary
with open('wilcoxon.json','w') as data_file:    
    json.dump(data,data_file)

df = pd.DataFrame() 
df = df.from_dict(wilcoxon_dict)
df.T.to_csv('wilcoxon.csv')