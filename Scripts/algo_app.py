import streamlit as st

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




with open('../data/ppg2019_20.csv', 'r', newline='') as csvfile:
    rows = csvfile.readlines()
    for row in rows:
        spl = row.split(',')
        teamname = spl[0]
        ppg[teamname] = float(spl[1])
        oppg[teamname] = float(spl[2])

st.title("Quarterly total Predictor")

quarter = st.selectbox("Select quarter: ", ('1', '2', '3'))
with open('../Models/predict_{}.sav'.format(quarter), 'rb') as pickle_file:
    regression_model_2 = pickle.load(pickle_file)

home_score = st.number_input("Enter home team score ", value=0, step=1)
away_score = st.number_input("Enter away team score ", value=0, step=1)

home = st.selectbox("Select Home Team: ", teams)
away = st.selectbox("Select Away Team: ", teams)

avg_scored = (ppg[home] + ppg[away])/2
avg_allowed = (oppg[home] + oppg[away])/2


total_score = home_score + away_score
diff = abs(home_score-away_score)

ans = regression_model_2.predict([[total_score, diff, avg_scored, avg_allowed]])

st.success("Estimated total final: " + str(ans[0]))

