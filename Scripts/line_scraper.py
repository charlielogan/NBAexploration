from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import re

driver = webdriver.Chrome()
driver.get("https://www.bovada.lv/sports/live")
soup = BeautifulSoup(driver.page_source, 'html.parser')
home = 'Shenzhen Aviators'
game = soup.find('span', attrs={"class": "name", "text":home}).parent
soup = BeautifulSoup(str(game), 'html.parser')
line = soup.find('sp-total-outcome')
soup = BeautifulSoup(str(line), 'html.parser')
total = soup.find_all('span', attrs={'class':"market-line bet-handicap both-handicaps"})[-1].text
print(total)

"""
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
    """