#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 17:56:53 2022

@author: rongmichael

Script for the 2022 Datathon project, part top 2 faceoff players.
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def cal_se(p, n):
    return (p*(1-p))/np.sqrt(n)

def check_court(row):
    if row['Home_Team'] == row['Team']:
        return 'Home'
    else:
        return 'Away'

###############load the file. If running this script with the data file 
###############in the same folder, you do not need to change the script.
        #######Otherwise, please put the entire path into the file name insead.
df = pd.read_csv('NWHL.csv', header = 0)
###############


#####Initial data clean up
df.columns = df.columns.str.replace(' ','_')
face_off = df[df.Event == 'Faceoff Win']


######1st Analysis: win percentage vs SE
w_l_dict = {}
### w_l_dict = {'player_1': [w_number, l_number]}
for index, row in face_off.iterrows():
    if row['Player'] not in w_l_dict:
        w_l_dict[row['Player']] = [1,0]
    
    elif row['Player'] in w_l_dict:
        w_l_dict[row['Player']][0] += 1
     
    if row['Player_2'] not in w_l_dict:
        w_l_dict[row['Player_2']] = [0,1]
    
    elif row['Player_2'] in w_l_dict:
        w_l_dict[row['Player_2']][1] += 1

face_off_perc = {}
### only include players who played 10 or more games
### face_off_perc = {'player_1': [percentage, Standard Error]}
for player in w_l_dict:
    if sum(w_l_dict[player]) >= 20:
       face_off_perc[player] =  [w_l_dict[player][0]/sum(w_l_dict[player])]
       face_off_perc[player].append(cal_se(face_off_perc[player][0], 
                                           sum(w_l_dict[player])))


players = list(face_off_perc)
perc = []
se = []
for i in list(face_off_perc.values()):
    perc.append(i[0])
    se.append(i[1])
fig, ax = plt.subplots()
ax.scatter(perc, se)
rect = patches.Rectangle((0.6, 0.01), 0.15, 0.04, linewidth=1, edgecolor='r', 
                         facecolor='none')
ax.add_patch(rect)
plt.xlabel('Faceoff Win Percentage')
plt.ylabel('Standard Error')
plt.title('Faceoff Win Percentage Vs Standard Error')
#plt.savefig('1st_test.png', dpi=300)  
plt.show()  

fig, ax = plt.subplots()
ax.scatter(perc, se)
plt.xlim(0.6)
for i in range(len(perc)):
    if perc[i] > 0.6:
        if players[i] == 'Cailey Hutchison':
            ax.annotate(players[i], (perc[i], se[i]), xytext = (perc[i]-0.015, 
                                                                se[i]+0.0025))
        else:
            ax.annotate(players[i], (perc[i], se[i]), xytext = (perc[i]+0.002, 
                                                                se[i]-0.0025))
plt.xlabel('Faceoff Win Percentage')
plt.ylabel('Standard Error')
plt.title('Faceoff Win Percentage Vs Standard Error Zoom In')
#plt.savefig('1st_test_zoom.png', dpi=300)  
plt.show() 



###### We pick out top 4 players from this analysis:
###### 1: Jillian Dempsey
###### 2: Tereza Vanisova
###### 3: Shiann Darkangelo\ Cailey Hutchison \ Taytum Clairmont


######2nd Analysis: game played and faceoff per game
# top_players = {player: {game_date_1, game_date_2, ..}}
# where game_date_1 = {'court':'', 'face_off_num': 0, 'win':0, 'loss':0}
#top_players = {'Emma Vlasic':{} 'Jordan Juron':{}, 'Cailey Hutchison':{},
#               'Jillian Dempsey':{}}
top_players_game_dict = {}
top_players = ['Jillian Dempsey', 'Tereza Vanisova', 'Shiann Darkangelo', 
               'Cailey Hutchison', 'Taytum Clairmont']
for top_player in top_players:
    player_dict = {}
    #filter out individual player faceoff win games
    player_win_games = face_off[face_off.Player == top_player]
    for index, row in player_win_games.iterrows():
        if row['game_date'] not in player_dict:
            player_dict[row['game_date']]= {'court': check_court(row), 
                                            'face_off_num': 1, 'win':1, 
                                            'loss':0}
        else:
            player_dict[row['game_date']]['win'] += 1
            player_dict[row['game_date']]['face_off_num'] += 1
    
    #filter out individual player faceoff loss games
    player_loss_games = face_off[face_off.Player_2 == top_player]
    for index, row in player_loss_games.iterrows():
        if row['game_date'] not in player_dict:
            player_dict[row['game_date']]= {'court': check_court(row), 
                                            'face_off_num': 1, 'win':0, 
                                            'loss':1}
        else:
            player_dict[row['game_date']]['loss'] += 1  
            player_dict[row['game_date']]['face_off_num'] += 1
    top_players_game_dict[top_player] = player_dict



######3rd Analysis: Get the faceoff stats from different location and combine 
######them into 3 separate zones  
######Get the location of the faceoff event
# top_player_faceoff_loc = {'Player_1': {(x,y):[win_num, loss_num]}}
exceptions = []
top_player_faceoff_loc = {}
top_3_players = ['Jillian Dempsey', 'Tereza Vanisova', 'Shiann Darkangelo'] 

for top_player in top_3_players:
    #Location of the faceoff dots
    loc = {(31,20):[0, 0], (169, 20):[0, 0], 
       (31, 64):[0, 0], (169, 64):[0, 0],
       (100, 42):[0, 0], 
       (80, 64):[0, 0], (120, 64):[0, 0],
       (80, 20):[0, 0], (120, 20):[0, 0]}
    #############for the winning plays
    player_win_games = face_off[face_off.Player == top_player]
    for index, row in player_win_games.iterrows():
        loc_holder = (row['X_Coordinate'], row['Y_Coordinate'])
        if loc_holder in loc:
            loc[loc_holder][0] += 1 
        elif loc_holder not in loc:
            if (row['X_Coordinate'], row['Y_Coordinate'] + 1) in loc:
                loc[(row['X_Coordinate'], row['Y_Coordinate'] + 1)][0] += 1 
            elif (row['X_Coordinate'], row['Y_Coordinate'] - 1) in loc:
                loc[(row['X_Coordinate'], row['Y_Coordinate'] - 1)][0] += 1 
            else:
                exceptions.append(loc_holder)
    
    #############for the lossing plays
    player_loss_games = face_off[face_off.Player_2 == top_player]
    for index, row in player_loss_games.iterrows():
        loc_holder = (row['X_Coordinate'], row['Y_Coordinate'])
        if loc_holder in loc:
            loc[loc_holder][1] += 1 
        elif loc_holder not in loc:
            if (row['X_Coordinate'], row['Y_Coordinate'] + 1) in loc:
                loc[(row['X_Coordinate'], row['Y_Coordinate'] + 1)][1] += 1 
            elif (row['X_Coordinate'], row['Y_Coordinate'] - 1) in loc:
                loc[(row['X_Coordinate'], row['Y_Coordinate'] - 1)][1] += 1 
            else:
                exceptions.append(loc_holder)
    top_player_faceoff_loc[top_player] = loc
                
                
###############categorize result into different zones, and calculate 
###############the percentage
for player in top_player_faceoff_loc:
    count = 0
    for i in top_player_faceoff_loc[player]:
        count += sum(top_player_faceoff_loc[player][i])
    print(count)
    
# top_player_faceoff_summary = {'Player_1': {'off':[win_%, plays, total_%]}, 
#                               'def':{}, 'neu':{}}
top_player_faceoff_summary = {}

location = {'off': [(169, 20), (169, 64)],
            'def': [(31, 20), (31, 64)],
            'neu': [(100, 42), (80, 64), (120, 64), (80, 20), (120, 20)]}
for player in top_player_faceoff_loc:
    zone = {'off':[], 'def':[], 'neu':[]}
    total_plays = 0
    for loc in location:
        plays = 0
        win = 0
        for coor in location[loc]:
            stats = top_player_faceoff_loc[player][coor]
            plays += sum(stats)
            win += stats[0]
        zone[loc]= [win/plays, plays]
        total_plays += plays
        #print(total_plays)
    for i in zone:
        #print(zone[i][1])
        zone[i].append(zone[i][1]/total_plays)
    top_player_faceoff_summary[player] = zone
        




    
    
    
    
