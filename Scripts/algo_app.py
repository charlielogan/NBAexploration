import streamlit as st
from datetime import datetime,timezone, timedelta
from basketball_reference_web_scraper import client
import pickle
from bs4 import BeautifulSoup
from selenium import webdriver


def utc_to_local(utc_dt):
    utc_dt['start_time'] = utc_dt['start_time'].replace(tzinfo=timezone.utc).astimezone(tz=timezone(-timedelta(hours=5)))
    return utc_dt

@st.cache
def initialize_data():
    ppg = {}
    oppg = {}
    sched = client.season_schedule(season_end_year=2021)

    eastern = list(map(utc_to_local, sched)) 
    #now_est = datetime.now(timezone(-timedelta(hours=5)))
    #todays_games = list(filter(lambda x: (x['start_time'].month == now_est.month) and (x['start_time'].day == now_est.day), eastern))
    todays_games = list(filter(lambda x: (x['start_time'].month == 12) and (x['start_time'].day == 25), eastern))
    homes = []
    aways = []
    for game in todays_games:
        homes.append(game['home_team'].name)
        aways.append(game['away_team'].name)

    todays_games = list(zip(homes, aways))
    todays_games = list(map(lambda x: x[0].split('_')[-1] + " @ " + x[1].split('_')[-1], todays_games))



    with open('../data/ppg_avgs.csv', 'r', newline='') as csvfile:
        rows = csvfile.readlines()
        for row in rows:
            spl = row.split(',')
            teamname = spl[0]
            ppg[teamname] = float(spl[1])
            oppg[teamname] = float(spl[2])
    return todays_games, ppg, oppg

@st.cache
def get_current_score(away_team, home_team):
    driver = webdriver.Chrome()
    driver.get("https://www.espn.com/nba/scoreboard")
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    events = soup.find(id='scoreboard-page')
    event_soup = BeautifulSoup(str(events), 'html.parser')
    evs = event_soup.find(id='events')
    scores = evs.find_all('article', attrs={'class': 'scoreboard basketball live js-show'})
    home_score = 0
    away_score = 0
    current_scores = {}

    for s in scores:
        soup = BeautifulSoup(str(s), 'html.parser')
        away_team = soup.find('tr', attrs={'class': 'away'})
        away_soup = BeautifulSoup(str(away_team), 'html.parser')
        away_name = away_soup.find('span', attrs={'class': 'sb-team-short'}).text
        if away_name.upper() != away_team:
            print(away_name.upper())
            print(away_team)
            continue
        away_total = away_soup.find('td', attrs={'class': 'total'}).text
        

        home_team = soup.find('tr', attrs={'class': 'home'})
        home_soup = BeautifulSoup(str(home_team), 'html.parser')
        #home_name = home_soup.find('span', attrs={'class': 'sb-team-short'}).text
        home_total = home_soup.find('td', attrs={'class': 'total'}).text

        return away_total, home_total
    
    return (0,0)
    
todays_games, ppg, oppg = initialize_data()

st.title("Quarterly total Predictor")

game = st.selectbox("Select game: ", todays_games)
away = game.split(" @ ")[0]
home = game.split(" @ ")[1]


quarter = st.selectbox("Select quarter: ", ('1', '2', '3'))
with open('../Models/predict_{}.sav'.format(quarter), 'rb') as pickle_file:
    regression_model_2 = pickle.load(pickle_file)

avg_scored = (ppg[home.upper()] + ppg[away.upper()])/2
avg_allowed = (oppg[home.upper()] + oppg[away.upper()])/2

away_score = int(st.number_input("Enter {} score".format(away.capitalize())))
home_score = int(st.number_input("Enter {} score".format(home.capitalize())))



total_score = home_score + away_score
diff = abs(home_score-away_score)
if quarter == '1' or quarter == '2':
    ans = regression_model_2.predict([[total_score, avg_scored, avg_allowed]])
    
else:
    ans = regression_model_2.predict([[diff, total_score, avg_scored, avg_allowed]])
    
st.success("Estimated total final: " + str(ans[0]))