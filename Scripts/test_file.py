from basketball_reference_web_scraper.data import Team, OutputType
from basketball_reference_web_scraper import client

from nba_api.stats.static import teams
from nba_api.stats.endpoints import teamyearbyyearstats, leaguestandings, leaguegamefinder, playbyplay
from nba_api.stats.library.parameters import Season, SeasonType

import os
import time
import sqlite3

from datetime import datetime,timezone, timedelta

sched = client.season_schedule(season_end_year=2021)
def utc_to_local(utc_dt):
    utc_dt['start_time'] = utc_dt['start_time'].replace(tzinfo=timezone.utc).astimezone(tz=timezone(-timedelta(hours=5)))
    return utc_dt

eastern = list(map(utc_to_local, sched)) 
now_est = datetime.now(timezone(-timedelta(hours=5)))
#todays_games = list(filter(lambda x: (x['start_time'].month == now_est.month) and (x['start_time'].day == now_est.day), eastern))
todays_games = list(filter(lambda x: (x['start_time'].month == 12) and (x['start_time'].day == 25), eastern))
print(todays_games)
for game in todays_games:
    home = game['home_team'].name
    away = game['away_team'].name
    print(away + " @ " + home)
print(dir(client))