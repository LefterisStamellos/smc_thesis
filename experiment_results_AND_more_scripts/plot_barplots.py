#### plot two types of bar plots for experimental results

import pandas as pd, numpy as np, matplotlib.pyplot as plt, seaborn as sns, os,matplotlib.pyplot as plt
# %matplotlib inline

############# BAR CHARTS ##########################
df_tmp = pd.DataFrame()
df_tmp = pd.read_json('answers_for_barplots.json')

# choose category (all,composers, non drummers, ....) and question
df_bar = pd.DataFrame()
df_bar['clfr'] = df_tmp['all']['clfr']['appreciation']
df_bar['rand'] = df_tmp['all']['rand']['appreciation']

# plot stacked bar chart
legend_labels = ['strongly disagree','disagree','neutral','agree','strongly agree']
ax = df_bar.transpose().plot.bar(stacked=True,ylim=(-20, 270),color=sns.color_palette('muted'),yticks = [],xticks = [])
plt.xticks(np.arange(2),['classifier','random'],fontsize = 20)
handles, labels = ax.get_legend_handles_labels()
labels = legend_labels
ax.legend(reversed(handles),reversed(labels),loc = 'upper right',fontsize = 20)
ax.set_axis_bgcolor('white')
plt.xlim([-0.5,2])
plt.title('users\' responses to \'appreciation\' question', fontsize = 24, x = 0.4)
plt.show()

############### SIMPLE BAR PLOTS ######################

# df_bar['responses'] = ['strongly disagree','disagree','neutral','agree','strongly agree']

# # plot simple bar plot
# sns.set_style("whitegrid")
# ax = sns.barplot(x="responses", y="rand", data=df_bar)
# plt.ylabel('')
# plt.xlabel('')
# plt.xticks(fontsize = 20)
# plt.title('users\' with under 5 years of musical training responses to \'substitutability\' question for random sounds', fontsize = 20)
# sns.plt.show()