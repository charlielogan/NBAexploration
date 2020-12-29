from basketball_reference_web_scraper.data import Team, OutputType
from basketball_reference_web_scraper import client

from nba_api.stats.static import teams
from nba_api.stats.endpoints import teamyearbyyearstats, leaguestandings, leaguegamefinder, playbyplay
from nba_api.stats.library.parameters import Season, SeasonType

import os
import time
import sqlite3

from datetime import datetime,timezone, timedelta
"""
sched = client.season_schedule(season_end_year=2021)
def utc_to_local(utc_dt):
    utc_dt['start_time'] = utc_dt['start_time'].replace(tzinfo=timezone.utc).astimezone(tz=timezone(-timedelta(hours=5)))
    return utc_dt

eastern = list(map(utc_to_local, sched)) 
now_est = datetime.now(timezone(-timedelta(hours=5)))
#todays_games = list(filter(lambda x: (x['start_time'].month == now_est.month) and (x['start_time'].day == now_est.day), eastern))
todays_games = list(filter(lambda x: (x['start_time'].month == 12) and (x['start_time'].day == 25), eastern))

for game in todays_games:
    home = game['home_team'].name
    away = game['away_team'].name
    print(away + " @ " + home)
print(dir(Team))
"""
from bs4 import BeautifulSoup
import requests
from selenium import webdriver

driver = webdriver.Chrome()
driver.get("https://www.espn.com/nba/scoreboard")

soup = BeautifulSoup(driver.page_source, 'html.parser')
events = soup.find(id='scoreboard-page')
event_soup = BeautifulSoup(str(events), 'html.parser')
evs = event_soup.find(id='events')
scores = evs.find_all('article', attrs={'class': 'scoreboard basketball live js-show'})
soup = BeautifulSoup(str(scores), 'html.parser')
home ='KINGS'
away="WARRIORS"
home_team = soup.find('span', text=home.capitalize()).parent.parent.parent.parent.parent
home_soup = BeautifulSoup(str(home_team), 'html.parser')
home_total = home_soup.find('td', attrs={'class': 'total'}).text
print(home_total)

current_scores = {}
"""
for s in scores:
    soup = BeautifulSoup(str(s), 'html.parser')
    away_team = soup.find('tr', attrs={'class': 'away'})
    away_soup = BeautifulSoup(str(away_team), 'html.parser')
    away_name = away_soup.find('span', attrs={'class': 'sb-team-short'}).text
    away_total = away_soup.find('td', attrs={'class': 'total'}).text

    home_team = soup.find('tr', attrs={'class': 'home'})
    home_soup = BeautifulSoup(str(home_team), 'html.parser')
    home_name = home_soup.find('span', attrs={'class': 'sb-team-short'}).text
    home_total = home_soup.find('td', attrs={'class': 'total'}).text

    g = str(away_name + " @ " + home_name)
    current_scores[g] = (away_total, home_total)
print(current_scores)
"""
