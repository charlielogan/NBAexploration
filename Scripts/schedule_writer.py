from basketball_reference_web_scraper import client
from basketball_reference_web_scraper.data import Team
from basketball_reference_web_scraper.data import OutputType
import csv
from datetime import datetime, timezone
from nba_api.stats.endpoints import teamyearbyyearstats, leaguestandings, leaguegamefinder, playbyplay
from nba_api.stats.static import teams

ppg = {}
oppg = {}
abbrevs = {}
team_dict = {}

# CHANGE YEAR
stan = leaguestandings.LeagueStandings(season=2019).get_dict()
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

"""
self.teams = [(Team.ATLANTA_HAWKS, "Atlanta_Hawks"),
            (Team.BOSTON_CELTICS, "Boston_Celtics"),
            (Team.BROOKLYN_NETS, "Brooklyn_Nets"),
            (Team.CHARLOTTE_HORNETS, "Charlotte_Hornets"),
            (Team.CHICAGO_BULLS, "Chicago_Bulls"),
            (Team.CLEVELAND_CAVALIERS, "Cleveland_Cavaliers"),
            (Team.DALLAS_MAVERICKS, "Dallas_Mavericks"),
            (Team.DENVER_NUGGETS, "Denver_Nuggets"),
            (Team.DETROIT_PISTONS, "Detroit_Pistons"),
            (Team.GOLDEN_STATE_WARRIORS, "Golden_State_Warriors"),
            (Team.HOUSTON_ROCKETS, "Houston_Rockets"),
            (Team.INDIANA_PACERS, "Indiana_Pacers"),
            (Team.LOS_ANGELES_CLIPPERS, "Los_Angeles_Clippers"),
            (Team.LOS_ANGELES_LAKERS, "Los_Angeles_Lakers"),
            (Team.MEMPHIS_GRIZZLIES, "Memphis_Grizzlies"),
            (Team.MIAMI_HEAT, "Miami_Heat"),
            (Team.MILWAUKEE_BUCKS, "Milwaukee_Bucks"),
            (Team.MINNESOTA_TIMBERWOLVES, "Minnesota_Timberwolves"),
            (Team.NEW_ORLEANS_PELICANS, "New_Orleans_Pelicans"),
            (Team.NEW_YORK_KNICKS, "New_York_Knicks"),
            (Team.OKLAHOMA_CITY_THUNDER, "Oklahoma_City_Thunder"),
            (Team.ORLANDO_MAGIC, "Orlando_Magic"),
            (Team.PHILADELPHIA_76ERS, "Philadelphia_76ers"),
            (Team.PHOENIX_SUNS, "Phoenix_Suns"),
            (Team.PORTLAND_TRAIL_BLAZERS, "Portland_Trail_Blazers"),
            (Team.SACRAMENTO_KINGS, "Sacremento_Kings"),
            (Team.SAN_ANTONIO_SPURS, "San_Antonio_Spurs"),
            (Team.TORONTO_RAPTORS, "Toronto_Raptors"),
            (Team.UTAH_JAZZ, "Utah_Jazz"),
            (Team.WASHINGTON_WIZARDS, "Washington_Wizards")
            ]

        


with open('restart.csv', 'w', newline='') as csvfile:
    games = client.season_schedule(season_end_year=2020)
    g_id = 0
    for game in games:
        home_team1 = game['home_team']
        home_name = home_team1.value.split()[-1]
        if(home_name == "76ERS"):
            home_name = "SIXERS"
        away_team = game['away_team']
        away_name = away_team.value.split()[-1]
        if(away_name == "76ERS"):
            away_name = "SIXERS"
        date1 = game['start_time']
        row = [date1, away_team, home_team1]
        writer = csv.writer(csvfile)
        writer.writerow(row)

    """

g = []


with open('../data/ppg_avgs.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for key in ppg.keys():
        row = [key, ppg[key], oppg[key]]
        writer.writerow(row)




