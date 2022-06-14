import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("C:\Rotman_MMA_Summer_Datathon_NWHL.csv")
df = pd.DataFrame(data)

df_goals = df[df['Event'] == 'Goal']
goals_per_player = df_goals["Player"].value_counts()
goals_per_player_sorted = goals_per_player.sort_values(ascending = False)


df_shots = df.loc[df['Event'].isin(['Shot','Goal'])]
shots_goals_per_player = df_shots["Player"].value_counts()
shots_goals_per_player_sorted = shots_goals_per_player.sort_values(ascending = False)


print(goals_per_player_sorted.head())
print(shots_goals_per_player_sorted)


Goals_by_shots = goals_per_player_sorted/shots_goals_per_player_sorted

print(Goals_by_shots.sort_values(ascending = False))
top_10_goal_scorers = Goals_by_shots.sort_values(ascending = False)[:10]
print(top_10_goal_scorers)

top_10_goal_scorers.plot( x="Player", y="count", kind='bar', rot=45, xlabel = "Players", ylabel = "Goal to Goals+Shots Ratio")
plt.xlabel="Player Name"
plt.ylabel = "Goal/Goal+Shots"
plt.show()
