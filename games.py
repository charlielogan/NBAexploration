from basketball_reference_web_scraper import client
from basketball_reference_web_scraper.data import Team
from basketball_reference_web_scraper.data import OutputType

from nba_api.stats.static import teams
from nba_api.stats.endpoints import teamyearbyyearstats
from nba_api.stats.endpoints import leaguestandings

import os
import sqlite3


class Predictor:
    def __init__(self):
        self.team_dict = {}
        self.ppg = {}
        self.oppg = {}

    def get_schedule_data(self, cur, conn, endyear):

        nba_teams = teams.get_teams()
        for team in nba_teams:
            name = team['nickname'].split()[-1].upper()
            if name == '76ERS':
                name = 'SIXERS'

            self.team_dict[name] = team['id']

        stan = leaguestandings.LeagueStandings(season=endyear-1).get_dict()
        for d in stan['resultSets']:
            for l in d['rowSet']:
                name = l[4].split()[-1].upper()
                if(name == '76ERS'):
                    name = 'SIXERS'
                points = l[56]
                opoints = l[57]
                self.ppg[name] = points
                self.oppg[name] = opoints


        games = client.season_schedule(season_end_year=endyear)
        g_id = 0
        for game in games:
            true_day = 0
            true_month = 0
            true_year = 0
            home_team1 = game['home_team']
            home_name = home_team1.value.split()[-1]
            home_final = game["home_team_score"]
            if(home_name == "76ERS"):
                home_name = "SIXERS"
            away_team = game['away_team']
            away_name = away_team.value.split()[-1]
            away_final = game["away_team_score"]
            if(away_name == "76ERS"):
                away_name = "SIXERS"
            date1 = game['start_time']
            cur.execute("CREATE TABLE IF NOT EXISTS " + home_name + "(game_ID INTEGER, time_remaining INTEGER, end_minutes_played INTEGER, turnovers FLOAT, attempt_3pt FLOAT, made_3pt FLOAT, percent_3pt FLOAT, fg_made FLOAT, fg_attempt FLOAT, fg_percent FLOAT, ft_made FLOAT, ft_attempt FLOAT, ft_percent FLOAT, total_score INTEGER, score_diff INTEGER, score_rate FLOAT, final_score INTEGER, home_ppg FLOAT, home_oppg FLOAT, away_ppg FLOAT, away_oppg FLOAT)")
            try:
                true_day = date1.day
                true_month = date1.month
                true_year = date1.year
                play_by_play = client.play_by_play(
                        home_team=home_team1,
                        year=date1.year,
                        month=date1.month,
                        day=date1.day)

            except:
                try:
                    true_day = date1.day-1
                    true_month = date1.month
                    true_year = date1.year
                    play_by_play = client.play_by_play(
                        home_team=home_team1,
                        year=date1.year,
                        month=date1.month,
                        day=(date1.day - 1))

                except:
                    print(game)
                    continue

            final_score = home_final + away_final
            end_3pt_attempt = 0
            end_3pt_made = 0
            end_minutes_played = 0
            end_attempt_ft = 0
            end_made_ft = 0
            end_attempt_fg = 0
            end_made_fg = 0
            end_turnovers = 0
            
            box_score = client.team_box_scores(
            year=true_year,
            month=true_month,
            day=true_day)
            for box in box_score:
                if(box['team'] == home_team1):
                    end_3pt_attempt = box["attempted_three_point_field_goals"]
                    end_3pt_made = box["made_three_point_field_goals"]
                    end_minutes_played = box["minutes_played"]
                    end_attempt_ft = box['attempted_free_throws']
                    end_made_ft = box['made_free_throws']
                    end_attempt_fg = box['attempted_field_goals']
                    end_made_fg = box['made_field_goals']
                    end_turnovers = box['turnovers']
                    break
                
            for box in box_score:
                if(box['team'] == away_team):
                    end_3pt_attempt += box["attempted_three_point_field_goals"]
                    end_3pt_made += box["made_three_point_field_goals"]
                    end_attempt_ft += box['attempted_free_throws']
                    end_made_ft += box['made_free_throws']
                    end_attempt_fg += box['attempted_field_goals']
                    end_made_fg += box['made_field_goals']
                    end_turnovers += box['turnovers']
                    break
            
            percent_3pt = float(end_3pt_made)/float(end_3pt_attempt)
            fg_percent = float(end_made_fg)/float(end_attempt_fg)
            ft_percent = float(end_made_ft)/float(end_attempt_ft)
            i = 20
            while(i <(len(play_by_play) - 25)):
                    time_rem = ((4-(play_by_play[i]["period"])) * 720) + play_by_play[i]["remaining_seconds_in_period"]
                    total_score = play_by_play[i]["away_score"] + play_by_play[i]["home_score"]
                    score_diff = abs(play_by_play[i]["away_score"] - play_by_play[i]["home_score"])
                    score_rate = total_score/(2880 - time_rem)
                    turnovers = end_turnovers
                    attempt_3pt = end_3pt_attempt
                    made_3pt = end_3pt_made
                    #fg_attempt = float(end_attempt_fg*(2880-time_rem))/2880
                    fg_attempt = end_attempt_fg
                    fg_made = end_made_fg
                    ft_attempt = end_attempt_ft
                    ft_made = end_made_ft
                    

                    cur.execute("INSERT INTO " + home_name + " (game_ID, time_remaining, end_minutes_played, turnovers, attempt_3pt, made_3pt, percent_3pt, fg_made, fg_attempt, fg_percent, ft_made, ft_attempt, ft_percent, total_score, score_diff, score_rate, final_score, home_ppg, home_oppg, away_ppg, away_oppg) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(g_id, time_rem, end_minutes_played, turnovers, attempt_3pt, made_3pt, percent_3pt, fg_made, fg_attempt, fg_percent, ft_made, ft_attempt, ft_percent, total_score, score_diff, score_rate, final_score, self.ppg[home_name], self.oppg[home_name], self.ppg[away_name], self.oppg[away_name]))
                    i+=5
            g_id +=1
            print(date1)
        conn.commit()
            
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
    p1.get_schedule_data(cur, conn, 2020)
    p1.get_schedule_data(cur, conn, 2019)
    p1.get_schedule_data(cur, conn, 2018)
    p1.get_schedule_data(cur, conn, 2017)
   

if __name__ == "__main__":
    main()
