#!/usr/bin/env python
# coding: utf-8

# In[67]:


import numpy as np
import pandas as pd
df = pd.read_csv('Data')


# In[68]:


df.head()


# In[69]:


df_assist = df.loc[(df['Event']=="Goal") | (df['Event']=="Play") | (df['Event']=="Shot") ]


# In[70]:


df_assist=df_assist[["Home Team","Team","Player","Player 2","Event","Clock","X Coordinate","Y Coordinate","X Coordinate 2","Y Coordinate 2","Period"]]


# In[71]:


df_assist.reset_index(drop=True,inplace=True)


# In[72]:


column_list = df_assist.columns.values.tolist()
assist_pair = pd.DataFrame(columns=column_list)
df_assist.head()


# In[73]:


count =0 
assist_pair.drop(assist_pair.index[0:],axis=0,inplace = True)
for index,row in df_assist.iterrows():
    if (df_assist.loc[index, 'Event'] == "Goal") or (df_assist.loc[index, 'Event'] == "Shot") :
        
        if index!=0 and (df_assist.loc[index-1,'Event']=="Play") and (df_assist.loc[index-1,'Team'] == df_assist.loc[index,'Team']) and (df_assist.loc[index-1,'Player 2'] == df_assist.loc[index,'Player']) and (df_assist.loc[index-1,'Period'] == df_assist.loc[index,'Period']) :
            assist_pair = assist_pair.append(df_assist.loc[index -1])
            assist_pair = assist_pair.append(df_assist.loc[index])
        
            
            #print(index)
            #count+=1
        
assist_pair.head()


# In[74]:


assist_pair.reset_index(drop=True,inplace=True)


# In[75]:


for index, row in assist_pair.iterrows():
    if index!=0 and (assist_pair.loc[index-1,'Event']=="Play"):
        if assist_pair.loc[index,'Event']=="Goal":
            assist_pair.at[index-1,"Event"]= "Successful Assist"
        elif index!=0 and (assist_pair.loc[index,'Event']=="Shot"):
            assist_pair.at[index-1,"Event"]= "Unsuccessful Assist"
      


# In[76]:


assist_pair = assist_pair[assist_pair["Event"].str.contains("Goal") == False]
assist_pair = assist_pair[assist_pair["Event"].str.contains("Shot") == False]
assist_pair.shape


# In[77]:


assist_pair["Event"].value_counts()


# In[78]:


assist_pair["player_pair"] = assist_pair[['Player', 'Player 2']].agg('-'.join, axis=1)
assist_pair.head()


# In[79]:


assist_pair['player_pair'].value_counts()


# In[80]:


pair_groupedby = assist_pair[["player_pair","Event"]]


# In[81]:


pair_groupedby = pair_groupedby.reset_index()
pair_groupedby = pair_groupedby.pivot_table(index='player_pair',columns='Event',values='index',aggfunc='count',fill_value=0)


# In[82]:


pair_groupedby['Total Assist']= pair_groupedby['Successful Assist']+pair_groupedby['Unsuccessful Assist']


# In[83]:


pair_groupedby = pair_groupedby.loc[pair_groupedby["Successful Assist"] >1]


# In[84]:


pair_groupedby.reset_index(inplace=True)
pair_groupedby.sort_values("Total Assist",inplace=True)


# In[85]:


pair_groupedby.drop(columns={"Total Assist"},inplace=True)


# In[102]:


import matplotlib.pyplot as plt
graph=pair_groupedby.plot.bar(x='player_pair', stacked=True, title='Successful vs Unsuccessful Assists by Player')
plt.xticks(rotation = 60)
plt.ylabel ("No. of Assists")
plt.xlabel ("Player Pair")
graph.figure.savefig('AssistRatio.png', bbox_inches='tight')


# In[87]:


prime_passer= df.loc[(df['Player']=="Kelly Babstock") | (df['Player']=="Taytum Clairmont") | (df['Player']=="Christina Putigna")  | (df['Player']=="McKenna Brand") ]



# In[88]:


prime_passer.head()
import math
prime_passer["X distance"] = (((prime_passer["X Coordinate 2"] - prime_passer["X Coordinate"])**2))
prime_passer["Y distance"] = (((prime_passer["Y Coordinate 2"] - prime_passer["Y Coordinate"])**2))

prime_passer["distance"] = ((prime_passer['X distance']+ prime_passer['Y distance'])**(1/2))


# In[89]:


prime_passer = prime_passer[['Player','distance','Event']]


# In[90]:


prime_passer=prime_passer.loc[(prime_passer['Event']=="Play")|(prime_passer['Event']=="Incomplete Play")]


# In[91]:


prime_passer.head()


# In[92]:


prime_passer_distance=prime_passer.copy()
prime_passer_distance.drop(columns={'Event'},inplace = True)
prime_passer_distance=prime_passer_distance.groupby("Player").mean()
prime_passer_distance.reset_index(inplace=True)
distance_list = prime_passer_distance['distance']


# In[93]:


prime_passer_distance.head()


# In[94]:


prime_passer.head()


# In[95]:


print(distance_list)


# In[96]:


prime_passer.reset_index(inplace=True)
prime_passer_ratio = prime_passer.pivot_table(index='Player',columns='Event',values='index',aggfunc='count',fill_value=0)

prime_passer_ratio.reset_index(inplace=True)
prime_passer_ratio['distance']= distance_list
prime_passer_ratio.head()


# In[97]:


prime_passer_ratio["accuracy"]= (prime_passer_ratio["Play"]/(prime_passer_ratio["Play"]+prime_passer_ratio["Incomplete Play"]))*100


# In[98]:


start = 1
end = 10
width = end - start
prime_passer_ratio["distance"]=1+((prime_passer_ratio["distance"]-prime_passer_ratio["distance"].min())/(prime_passer_ratio["distance"].max()-prime_passer_ratio["distance"].min()))* width + start
prime_passer_ratio['puck_recovery']=[103/6,36/4,112/6,68/6]
prime_passer_ratio["puck_recovery"]=1+((prime_passer_ratio["puck_recovery"]-prime_passer_ratio["puck_recovery"].min())/(prime_passer_ratio["puck_recovery"].max()-prime_passer_ratio["puck_recovery"].min()))* width + start
prime_passer_ratio["accuracy"]=1+((prime_passer_ratio["accuracy"]-prime_passer_ratio["accuracy"].min())/(prime_passer_ratio["accuracy"].max()-prime_passer_ratio["accuracy"].min()))* width + start
prime_passer_ratio.head()


# In[100]:


prime_passer_ratio['dump_in_out']=[21/6,7/4,25/6,15/6]
prime_passer_ratio['zone_entry']=[42/6,19/4,56/6,26/6]


# In[101]:


prime_passer_ratio["dump_in_out"]=1+((prime_passer_ratio["dump_in_out"]-prime_passer_ratio["dump_in_out"].min())/(prime_passer_ratio["dump_in_out"].max()-prime_passer_ratio["dump_in_out"].min()))* width + start
prime_passer_ratio["zone_entry"]=1+((prime_passer_ratio["zone_entry"]-prime_passer_ratio["zone_entry"].min())/(prime_passer_ratio["zone_entry"].max()-prime_passer_ratio["zone_entry"].min()))* width + start
prime_passer_ratio.head()


# In[ ]:





# In[33]:


pip install -U kaleido


# In[38]:


import plotly.express as px
fig = px.scatter(prime_passer_ratio, x="distance", y="accuracy",labels=dict(distance="Avg. Distance Covered by Pass", accuracy="Play Accuracy %"), hover_data=['Player'], title="Relation between Accuracy% of Plays and Average distance covered by passes by Player")
fig.update_layout(hovermode="closest")
fig.update_traces(marker=dict(size=12,
                              line=dict(width=2,
                                        color='DarkSlateGrey')),
                  selector=dict(mode='markers'))
fig.write_image("Accuracy%vsDistance.png")
#fig.figure.savefig('Accuracy%vsDistance.png', bbox_inches='tight')
fig.show()


# Passer 1 - Mckenna Brand - 1. Accuracy of plays vs pass distance 2. Number of assists
# Scorer 3 - Jillian Dempesey - 1. Forms good assist pair with Mckenna Brand and attempts maximum number of shots hence is a good receiver of passes from Mckenna Brand who is out primary play maker and also a good high danger passer

# In[ ]:




