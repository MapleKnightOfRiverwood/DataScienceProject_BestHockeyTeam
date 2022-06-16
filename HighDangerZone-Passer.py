#!/usr/bin/env python
# coding: utf-8

# Passes into high danger zone so that scoring can be easy
# 

# In[48]:


import numpy as np
import pandas as pd
df = pd.read_csv('Data')


# In[49]:


df_passer2 = df.loc[(df['Event']=="Play") | (df['Event']=="Incomplete Play")]


# In[50]:


df_passer2=df_assist[["Player","Event","X Coordinate","Y Coordinate","X Coordinate 2","Y Coordinate 2"]]







# In[51]:


df_passer2.shape


# In[52]:


df_passer2 = df_passer2.loc[(df_passer2['X Coordinate 2']>150) & (df_passer2['X Coordinate 2']<190) & (df_passer2['X Coordinate']<150) & (df_passer2['Y Coordinate 2']>=21) & (df_passer2['Y Coordinate 2']<=64)]



# In[53]:


df_passer2['Event'].value_counts()


# In[42]:


import matplotlib as plot
graph = df_passer2['Player'].value_counts()[:10].plot(kind='bar')
graph.set_ylabel('No. of Successful Passes into High Danger Zone')
graph.set_xlabel('Player')
graph.set_title('Player vs No. of Successful Passes into High Danger Zone')
graph.figure.savefig('SuccesfulPassesintoHighDangerZone.png', bbox_inches='tight')


# Passer 2 - Kaleigh Fratkin 
# Reason - Number of successfull passes into the high danger zone. Easier to make a goal from these regions. McKenna Brand is an equally if not better play maker but choosing her as our scorer number 3 as she has a good play history with Christina Putigna and is able to receive her assists and convert them to goals

# In[ ]:




