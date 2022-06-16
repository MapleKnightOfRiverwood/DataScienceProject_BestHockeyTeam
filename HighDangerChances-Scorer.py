#!/usr/bin/env python
# coding: utf-8

# In[285]:


import numpy as np
import pandas as pd
df = pd.read_csv('Data')


# In[286]:


df_scorer2 = df.loc[(df['Event']=="Goal")]


# In[287]:


df_scorer2=df_scorer2[["Player","Event","X Coordinate","Y Coordinate","Detail 1"]]


# In[288]:


df_scorer2.head()


# In[289]:


#df_scorer2 = df_scorer2.loc[(df_scorer2['X Coordinate']<150) | (df_scorer2['X Coordinate']>190)]



# In[290]:


df_scorer2.shape


# In[291]:


df_scorer2["Player"].value_counts()


# In[292]:


# create a list of our conditions
conditions = [
    (df_scorer2['X Coordinate'] <= 150),
    (((df_scorer2['X Coordinate'] > 150) & (df_scorer2['X Coordinate'] < 190))  & ((df_scorer2['Y Coordinate'] >= 64) & (df_scorer2['Y Coordinate'] < 21))),
    (df_scorer2['X Coordinate'] > 190)
    ]

# create a list of the values we want to assign for each condition
values = ['High Danger', 'High Danger', 'High Danger']

# create a new column and use np.select to assign values to it using our lists as arguments
df_scorer2['Goal_Type'] = np.select(conditions, values)

# display updated DataFrame
df_scorer2.head()


# In[293]:


#df_scorer2 = df_scorer2[df_scorer2["Shot_Type"].str.contains("Risky") == True]
df_scorer2.shape


# In[294]:


df_scorer2.replace({'Goal_Type': {'0': "Non-High Danger"}},inplace=True)


# In[295]:


df_scorer2.head()


# In[296]:


df_scorer2 = df_scorer2.reset_index()
df_scorer2 = df_scorer2.pivot_table(index='Player',columns='Goal_Type',values='index',aggfunc='count',fill_value=0)


# In[297]:


df_scorer2.reset_index(inplace=True)
df_scorer2 = df_scorer2.loc[df_scorer2["High Danger"] >=1]


# In[298]:


df_scorer2.shape


# In[299]:


df_scorer2['Total']=df_scorer2['Non-High Danger']+df_scorer2['High Danger']
df_scorer2.sort_values(by=['Total'],ascending=False,inplace=True)


# In[300]:


df_scorer2.head()


# In[301]:


df_scorer2.drop(columns={"Total"},inplace=True)
df_scorer2.plot.bar(x='Player', stacked=True, title='Goals Made (High Danger vs Non-High Danger)')
plt.savefig('GoalsMade_HighRisk.png', bbox_inches='tight')


# In[276]:


df_scorer2["Total"] = df_scorer2["High Risk"]+df_scorer2["Non-High Risk"]
df_scorer2["Risky Goal%"] = (df_scorer2["High Risk"]/df_scorer2["Total"])*100


# In[277]:


df_scorer2=df_scorer2.loc[df_scorer2['Risky Goal%']<100]
df_scorer2.head()


# In[278]:


df_scorer2= df_scorer2.sort_values('Risky Goal%',ascending=False)


# In[283]:


import matplotlib.pyplot as plt

plt.bar(df_scorer2['Player'], df_scorer2['Risky Goal%'], color = 'orange')
plt.title('High-Danger Chances Metric (%) by player')
plt.xlabel('Player')
plt.ylabel('High-Danger Chances Metric (%)')
plt.xticks(rotation = 90)
plt.savefig('HighRiskGoal%.png', bbox_inches='tight')


# Scorer 2 - Mallory Souliotis - 3 shots in 6 Games - of which she converted 66.7% of the shots which were taken outside of the high danger score hence increasing its risk metric. Hence, apart from scoring a lot of goals, she is also specifically skilled enough to convert a high percentage of difficult shots. 

# In[ ]:




