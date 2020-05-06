from basketball_reference_web_scraper import client
from basketball_reference_web_scraper.data import Team
from basketball_reference_web_scraper.data import OutputType
import os
import sqlite3

class Predictor:
    def __init__(self):
        self.sched = {}
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

    def get_schedule_data(self, cur, conn):

        games = client.season_schedule(season_end_year=2020)
        g_id = 0
        for game in games:
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
            cur.execute("CREATE TABLE IF NOT EXISTS " + home_name + "(Game_ID INTEGER, Opponent TEXT, Time_Remaining INTEGER, Total_Score INTEGER, Score_Diff INTEGER, Label TEXT, Score_Rate FLOAT, final_score INTEGER, final_score_diff INTEGER, final_score_rate FLOAT)")
            cur.execute("CREATE TABLE IF NOT EXISTS " + away_name + "(Game_ID INTEGER, Opponent TEXT, Time_Remaining INTEGER, Total_Score INTEGER, Score_Diff INTEGER, Label TEXT, Score_Rate FLOAT, final_score INTEGER, final_score_diff INTEGER, final_score_rate FLOAT)")
            try:
                play_by_play = client.play_by_play(
                        home_team=home_team1,
                        year=date1.year,
                        month=date1.month,
                        day=date1.day)
            except:
                try:
                    play_by_play = client.play_by_play(
                        home_team=home_team1,
                        year=date1.year,
                        month=date1.month,
                        day=(date1.day - 1))
                except:
                    if(date1.year == 2020):
                        break
                    else:
                        print(game)
                        continue

            final_score = home_final + away_final
            final_score_diff = abs(home_final-away_final)
            i = 20
            while(i <(len(play_by_play) - 25)):
                    team = str(play_by_play[i]["home_team"])
                    opponent = str(play_by_play[i]["away_team"])
                    time_rem = ((4-(play_by_play[i]["period"])) * 720) + play_by_play[i]["remaining_seconds_in_period"]
                    total_score = play_by_play[i]["away_score"] + play_by_play[i]["home_score"]
                    score_diff = abs(play_by_play[i]["away_score"] - play_by_play[i]["home_score"])
                    score_rate = total_score/(2880 - time_rem)*60
                    final_score_rate = (final_score/2880)*60
                    label = ""
                    if score_diff < 3:
                        label = "Tossup"
                    elif score_diff < 7:
                        label = "Close"
                    elif score_diff < 11:
                        label = "Getting away"
                    elif score_diff < 20:
                        label = "Big Lead"
                    else:
                        label = "Blowout"

                    cur.execute("INSERT INTO " + home_name + " (Game_ID, Opponent, Time_Remaining, Total_Score, Score_Diff, Label, Score_Rate, final_score, final_score_diff, final_score_rate) VALUES (?,?,?,?,?,?,?,?,?,?)",(g_id, opponent, time_rem, total_score, score_diff, label, score_rate, final_score, final_score_diff, final_score_rate))
                    cur.execute("INSERT INTO " + away_name + " (Game_ID, Opponent, Time_Remaining, Total_Score, Score_Diff, Label, Score_Rate, final_score, final_score_diff, final_score_rate) VALUES (?,?,?,?,?,?,?,?,?,?)",(g_id, team, time_rem, total_score, score_diff, label, score_rate, final_score, final_score_diff, final_score_rate))
                    i+=5
            g_id +=1
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
    p1.get_schedule_data(cur, conn)
   

if __name__ == "__main__":
    main()
