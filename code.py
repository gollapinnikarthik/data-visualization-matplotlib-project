# --------------
import pandas as pd 
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')
# Load the dataset and create column `year` which stores the year in which match was played
data = pd.read_csv(path)
data['year'] = data['date'].apply(lambda x : x[:4])

# Plot the wins gained by teams across all seasons
match_won = data.drop_duplicates(subset = 'match_code', keep = 'first').reset_index(drop = True)
#count the number of unique occurences within a column by value
total_wins = match_won['winner'].value_counts()
plot_wins = total_wins.plot(kind = 'bar', title = "Total number of wins by team across all seasons", figsize = (7, 5))
plt.xlabel('Teams')
plt.ylabel('Frequency of matches won')
plt.xticks(fontsize = 10, rotation = 'vertical')
plt.show()

# Plot Number of matches played by each team through all seasons
match_data = pd.melt(match_won, id_vars = ['match_code', 'year'], value_vars = ['team1', 'team2'])
no_of_matches_played = match_data.value.value_counts()
plt.figure(figsize = (12, 6))
no_of_matches_played.plot(x = no_of_matches_played.index, y = no_of_matches_played, kind = 'bar', title = 'No of macthes played across 9 seaons')
plt.xlabel('Teams')
plt.ylabel('Number of macthes played')
plt.xticks(rotation = 'vertical')

# Top bowlers through all seasons
wickets_taken = data[(data['wicket_kind'] ==  'bowled') | (data['wicket_kind'] ==  'caught') | (data['wicket_kind'] == 'lbw') | (data['wicket_kind'] ==  'caught and bowled')]

bowler_wickets = wickets_taken.groupby(['bowler'])['wicket_kind'].count().sort_values(ascending = False)[:10]
bowler_wickets.plot(x = bowler_wickets.index, y = bowler_wickets, kind = 'bar', colormap = 'Accent', title = 'Top 10 bowlers for all seasons')
plt.xlabel('Top 10 bowlers')
plt.ylabel('No of wickets taken')
plt.xticks(rotation = 'vertical')
plt.show()

# How did the different pitches behave? What was the average score for each stadium?
scores_per_stadium = data.loc[:, ['match_code', 'venue', 'inning', 'total']]

total_matches_won_in_stadium = scores_per_stadium.groupby(['match_code', 'venue', 'inning']).agg({'total' : 'sum'}).reset_index()

average_matches_won_in_stadium = total_matches_won_in_stadium.groupby(['venue', 'inning'])['total'].mean().reset_index()

average_matches_won_in_stadium = average_matches_won_in_stadium[(average_matches_won_in_stadium['inning'] == 1) | (average_matches_won_in_stadium['inning'] == 2)]

plt.figure(figsize = (19, 8))
plt.plot(average_matches_won_in_stadium[average_matches_won_in_stadium['inning'] == 1]['venue'], average_matches_won_in_stadium[average_matches_won_in_stadium['inning'] == 1]['total'], '-b', marker = 'o', ms = 6, lw = 2, label = 'inning1')

plt.plot(average_matches_won_in_stadium[average_matches_won_in_stadium['inning'] == 2]['venue'], average_matches_won_in_stadium[average_matches_won_in_stadium['inning'] == 2]['total'], '-r', marker = 'o', ms = 6, lw = 2, label = 'inning2')
plt.legend(loc = 'upper right', fontsize = 19)
plt.xticks(fontsize = 15, rotation = 90)
plt.xlabel('Venues', fontsize = 18)
plt.ylabel('Average runs scored by venues', fontsize = 16)
plt.show()

# Types of Dismissal and how often they occur
dismissal = data.groupby(['wicket_kind']).count().reset_index()
dismissal = dismissal[['wicket_kind', 'delivery']]
dismissal = dismissal.rename(columns = {'delivery' : 'count'})
fig, (ax_1, ax_2) = plt.subplots(1, 2, figsize = (15, 7))
fig.suptitle("Top 5 Dismissal Kind", fontsize = 14)

dismissal.plot.bar(ax = ax_1, legend = False)
ax_1.set_xticklabels(list(dismissal['wicket_kind']), fontsize = 8)

explode = [0.01, 0.01, 0.1, 0.2, 0.25, 0.4, 0.35, 0.05, 0.05]
properties = ax_2.pie(dismissal['count'], labels = None, startangle = 150, autopct="%1.1f%%", explode = explode)
ax_2.legend(bbox_to_anchor = (1,1), labels = dismissal['wicket_kind'])

# Plot no. of boundaries across IPL seasons
boundaries_data = data.loc[:, ['runs', 'year']]
boundaries_fours = boundaries_data[boundaries_data['runs'] == 4]
fours = boundaries_fours.groupby('year')['runs'].count()

boundaries_sixes = boundaries_data[boundaries_data['runs'] == 6]
sixes = boundaries_sixes.groupby('year')['runs'].count()

plt.figure(figsize = (12, 8))
plt.plot(fours.index, fours, '-b', marker = 'o', ms = 6, lw = 2, label = 'Fours')
plt.plot(sixes.index, sixes, '-r', marker = 'o', ms = 6, lw = 2, label = 'Sixes')
plt.legend(loc = 'upper right', fontsize = 19)
plt.xticks(fontsize = 15, rotation = 90)
plt.xlabel('IPL Seaons', fontsize = 18)
plt.ylabel('Total fours and sixes across seasons', fontsize = 16)
plt.show()

# Average statistics across all seasons
per_match_data = data.drop_duplicates(subset = 'match_code', keep = 'first').reset_index(drop = True)
total_runs_per_seasons = data.groupby('year')['total'].sum()
total_deliveries_per_season = data.groupby('year')['delivery'].count()
no_of_matches_played_per_season = per_match_data.groupby('year')['match_code'].count()

average_runs_per_match = total_runs_per_seasons / no_of_matches_played_per_season
average_balls_per_match = total_deliveries_per_season / no_of_matches_played_per_season
average_balls_per_ball = total_runs_per_seasons / total_deliveries_per_season

avg_total_data = pd.DataFrame([no_of_matches_played_per_season, average_runs_per_match, average_balls_per_match, average_balls_per_ball])
avg_total_data.index = ['No of Matches', 'Average Runs per Match', 'Average Balls Bowled Per Match', 'Average Runs Per Ball']
avg_total_data = avg_total_data.T

avg_total_data.plot(kind = 'bar', figsize = (12, 10), colormap = 'coolwarm')
plt.xlabel('Season')
plt.ylabel('Averages')
plt.legend(loc = 9, ncol = 6)




