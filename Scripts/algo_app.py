import streamlit as st
from datetime import datetime,timezone, timedelta
from basketball_reference_web_scraper import client
import pickle

ppg = {}
oppg = {}
teams = sorted(['LAKERS',
'BUCKS',
'CLIPPERS',
'RAPTORS',
'CELTICS',
'NUGGETS',
'ROCKETS',
'HEAT',
'PACERS',
'JAZZ',
'SIXERS',
'THUNDER',
'NETS',
'MAVERICKS',
'MAGIC',
'GRIZZLIES',
'BLAZERS',
'WIZARDS',
'SPURS',
'HORNETS',
'BULLS',
'PELICANS',
'SUNS',
'KNICKS',
'KINGS',
'PISTONS',
'TIMBERWOLVES',
'HAWKS',
'CAVALIERS',
'WARRIORS'
])




sched = client.season_schedule(season_end_year=2021)
def utc_to_local(utc_dt):
    utc_dt['start_time'] = utc_dt['start_time'].replace(tzinfo=timezone.utc).astimezone(tz=timezone(-timedelta(hours=5)))
    return utc_dt

eastern = list(map(utc_to_local, sched)) 
now_est = datetime.now(timezone(-timedelta(hours=5)))
#todays_games = list(filter(lambda x: (x['start_time'].month == now_est.month) and (x['start_time'].day == now_est.day), eastern))
todays_games = list(filter(lambda x: (x['start_time'].month == 12) and (x['start_time'].day == 25), eastern))
print(todays_games)
homes = []
aways = []
for game in todays_games:
    homes.append(game['home_team'].name)
    aways.append(game['away_team'].name)

todays_games = list(zip(homes, aways))

with open('../data/ppg_avgs.csv', 'r', newline='') as csvfile:
    rows = csvfile.readlines()
    for row in rows:
        spl = row.split(',')
        teamname = spl[0]
        ppg[teamname] = float(spl[1])
        oppg[teamname] = float(spl[2])

st.title("Quarterly total Predictor")

game = st.selectbox("Select game: ", todays_games)

quarter = st.selectbox("Select quarter: ", ('1', '2', '3'))
with open('../Models/predict_{}.sav'.format(quarter), 'rb') as pickle_file:
    regression_model_2 = pickle.load(pickle_file)

home_score = st.number_input("Enter home team score ", value=0, step=1)
away_score = st.number_input("Enter away team score ", value=0, step=1)


avg_scored = (ppg[home] + ppg[away])/2
avg_allowed = (oppg[home] + oppg[away])/2


total_score = home_score + away_score
diff = abs(home_score-away_score)

ans = regression_model_2.predict([[total_score, diff, avg_scored, avg_allowed]])

st.success("Estimated total final: " + str(ans[0]))

