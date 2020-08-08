from basketball_reference_web_scraper.data import Team, OutputType

from nba_api.stats.static import teams
from nba_api.stats.endpoints import teamyearbyyearstats, leaguestandings, leaguegamefinder, playbyplay
from nba_api.stats.library.parameters import Season, SeasonType

import os
import time
import sqlite3


class Predictor:
    def __init__(self):
        self.team_dict = {}
        self.ppg = {}
        self.oppg = {}
        self.abbrevs = {}


    def get_schedule_data(self, cur, conn, year):

        nba_teams = teams.get_teams()
        for team in nba_teams:
            
            name = team['nickname'].split()[-1].upper()
            if name == '76ERS':
                name = 'SIXERS'

            self.team_dict[name] = team['id']
            self.abbrevs[team['abbreviation']] = name

        stan = leaguestandings.LeagueStandings(season=year).get_dict()
        for d in stan['resultSets']:
            for l in d['rowSet']:
                name = l[4].split()[-1].upper()
                if(name == '76ERS'):
                    name = 'SIXERS'
                points = l[56]
                opoints = l[57]
                self.ppg[name] = points
                self.oppg[name] = opoints

        for team in self.team_dict:
            cur.execute("CREATE TABLE IF NOT EXISTS " + team + "(game_ID INTEGER, game_date STRING, TO_1 INTEGER, three_m1 INTEGER, three_a1 INTEGER, ts_1 INTEGER, diff_1 INTEGER, TO_2 INTEGER, three_m2 INTEGER, three_a2 INTEGER, ts_2 INTEGER, diff_2 INTEGER, TO_3 INTEGER, three_m3 INTEGER, three_a3 INTEGER, ts_3 INTEGER, diff_3 INTEGER, ts_final INTEGER, home_ppg FLOAT, home_oppg FLOAT, away_ppg FLOAT, away_oppg FLOAT)")

            g = leaguegamefinder.LeagueGameFinder(team_id_nullable=self.team_dict[team], season_nullable = year, season_type_nullable=SeasonType.regular)
            games_dict = g.get_normalized_dict()
            games = games_dict['LeagueGameFinderResults']

            for game in games:

                if(game['MATCHUP'].split()[1] == '@'):
                    continue

                if game['MATCHUP'].split()[-1] not in self.abbrevs:
                    continue

                try:
                    to_1, three_m1, three_a1, ts_1, diff_1 = get_play_by_play_stats(1, game)
                    if ts_1 == 0:
                        continue
                    to_2, three_m2, three_a2, ts_2, diff_2 = get_play_by_play_stats(2, game)
                    to_2 += to_1
                    three_m2 += three_m1
                    three_a2 += three_a1
                    to_3, three_m3, three_a3, ts_3, diff_3 = get_play_by_play_stats(3, game)
                    to_3 += to_2
                    three_m3 += three_m2
                    three_a3 += three_a2

                    final_score = game['PTS'] + (game['PTS'] - game["PLUS_MINUS"])

                    home_ppg = self.ppg[team]
                    home_oppg = self.oppg[team]
                    
                    away_ppg = self.ppg[self.abbrevs[game['MATCHUP'].split()[-1]]]
                    away_oppg = self.oppg[self.abbrevs[game['MATCHUP'].split()[-1]]]
                    
                    cur.execute("INSERT INTO " + team + " (game_ID, game_date, TO_1, three_m1, three_a1, ts_1, diff_1, TO_2, three_m2, three_a2, ts_2, diff_2, TO_3, three_m3, three_a3, ts_3, diff_3, ts_final, home_ppg, home_oppg, away_ppg, away_oppg) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                        (game['GAME_ID'], game['GAME_DATE'], to_1, three_m1, three_a1, ts_1, diff_1, to_2, three_m2, three_a2, ts_2, diff_2, to_3, three_m3, three_a3, ts_3, diff_3, final_score, home_ppg, home_oppg, away_ppg, away_oppg))

                    print(game['GAME_DATE'])
                    time.sleep(2)
                except:
                    print(game)


            conn.commit()

def get_play_by_play_stats(quarter, game):
        
        turnovers = 0
        three_attempt = 0
        three_make = 0       
        try:
            pbp = playbyplay.PlayByPlay(game['GAME_ID'], start_period=quarter, end_period=quarter)
        except: 
            print("ERROR")
            print(quarter)
            print(game)
            return
        time.sleep(2)
        dic = pbp.get_normalized_dict()['PlayByPlay']
        if len(dic) == 0:
            return (0, 0, 0, 0, 0)
        try:
            for x in dic:
                if  x['VISITORDESCRIPTION'] != None:

                    if 'Turnover' in x['VISITORDESCRIPTION']:
                        turnovers += 1

                    elif '3PT' in x['VISITORDESCRIPTION']:
                        three_attempt += 1
                        if 'MISS' not in x['VISITORDESCRIPTION']:
                            three_make += 1

                if x['HOMEDESCRIPTION'] != None:

                    if 'Turnover' in x['HOMEDESCRIPTION']:
                        turnovers += 1

                    elif '3PT' in x['HOMEDESCRIPTION']:
                        three_attempt += 1
                        if 'MISS' not in x['HOMEDESCRIPTION']:
                            three_make += 1
            
            i = len(dic) - 1
            while dic[i]['SCORE'] == None:
                i -= 1
            away_final = int(dic[i]['SCORE'].split("-")[0])
            home_final = int(dic[i]['SCORE'].split("-")[1])
            return (turnovers, three_make, three_attempt, away_final+home_final, abs(away_final-home_final))
        except:
            print("ERROR")
            print(game)
            print(dic)
            
def main():
    p1 = Predictor()
    try:
        path = os.path.dirname(os.path.abspath(__file__))
        f = open(path + "/Prediction.db")
        conn = sqlite3.connect(f)
        cur = conn.cursor()
    except:
        path = os.path.dirname(os.path.abspath(__file__))
        conn = sqlite3.connect(path+'/'+ "Prediction.db")
        cur = conn.cursor()
    #p1.get_schedule_data(cur, conn, "2019-20")
    p1.get_schedule_data(cur, conn, "2018-19")
    p1.get_schedule_data(cur, conn, "2017-18")
    p1.get_schedule_data(cur, conn, "2016-17")
   

if __name__ == "__main__":
    main()
