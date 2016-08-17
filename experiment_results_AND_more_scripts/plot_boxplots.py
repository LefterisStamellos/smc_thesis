import pandas as pd, numpy as np, matplotlib.pyplot as plt, seaborn as sns, os,matplotlib.pyplot as plt
# %matplotlib inline

############### BOXPLOTS ##################
df = pd.DataFrame()
df = df.from_csv('answers_for_boxplots.csv')

##### chose categories to plot in box plot
df_1,df_2,df_3 = [pd.DataFrame() for _ in range(3)]
df_1 = df[df['category'] == 'train_under5']
df_2 = df[df['category'] == 'train_over5']
df_3 = df[df['category'] == 'no_train']
df = pd.concat([df_1,df_2,df_3],axis = 0)

##### chose question to plot in box plot

df = df[df['question'] == 'substitutability']

#plot boxpplot
sns.set(style="ticks")
sns.boxplot(x="category", y="response", hue="type", data=df)
sns.despine(offset=10, trim=True)
plt.yticks([0,1,2,3,4],['strongly disagree','disagree','neutral','agree','strongly agree'],fontsize = 16)
plt.legend(fontsize = 20)
plt.xticks([0,1,2],['under 5 y. of training','over 5 y. of training','no training'],fontsize = 20)
plt.ylabel('')
plt.xlabel('')
plt.title('users\' responses to \'substitutability\' question',fontsize = 24,y=1.08)

sns.plt.show()



