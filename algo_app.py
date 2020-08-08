import streamlit as st
from nba_api.stats.endpoints import teamyearbyyearstats, leaguestandings, leaguegamefinder, playbyplay
from nba_api.stats.static import teams
import pickle

ppg = {}
oppg = {}
abbrevs = {}
team_dict = {}

stan = leaguestandings.LeagueStandings().get_dict()
for d in stan['resultSets']:
    for l in d['rowSet']:
        name = l[4].split()[-1].upper()
        if(name == '76ERS'):
            name = 'SIXERS'
        points = l[56]
        opoints = l[57]
        ppg[name] = points
        oppg[name] = opoints
        
nba_teams = teams.get_teams()
for team in nba_teams:
    name = team['nickname'].split()[-1].upper()
    if name == '76ERS':
        name = 'SIXERS'
    team_dict[name] = team['id']
    abbrevs[team['abbreviation']] = name

st.title("Quarterly total Predictor")

quarter = option = st.selectbox("Select quarter: ", ('1', '2', '3'))
with open('predict_{}.sav'.format(quarter), 'rb') as pickle_file:
    regression_model_2 = pickle.load(pickle_file)

home_score = st.number_input("Enter home team score ", value=0, step=1)
away_score = st.number_input("Enter away team score ", value=0, step=1)
home = st.selectbox("Select Home Team: ", ('ATL',
'BKN', 
'BOS',
'CHA',
'CHI',
'CLE',
'DAL',
'DEN',
'DET',
'GSW',
'HOU',
'IND',
'LAC',
'LAL',
'MEM',
'MIA',
'MIL',
'MIN',
'NOP',
'NYK',
'OKC',
'PHI',
'PHX',
'POR',
'SAC',
'SAS',
'TOR',
'UTA',
'WAS'))
away = st.selectbox("Select Away Team: ", ('ATL',
'BKN', 
'BOS',
'CHA',
'CHI',
'CLE',
'DAL',
'DEN',
'DET',
'GSW',
'HOU',
'IND',
'LAC',
'LAL',
'MEM',
'MIA',
'MIL',
'MIN',
'NOP',
'NYK',
'OKC',
'ORL',
'PHI',
'PHX',
'POR',
'SAC',
'SAS',
'TOR',
'UTA',
'WAS'))

avg_scored = (ppg[abbrevs[home]] + ppg[abbrevs[away]])/2
avg_allowed = (oppg[abbrevs[home]] + oppg[abbrevs[away]])/2


total_score = home_score + away_score
diff = abs(home_score-away_score)

ans = regression_model_2.predict([[total_score, diff, avg_scored, avg_allowed]])

st.success("Estimated total final: " + str(ans[0]))

