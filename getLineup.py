import json
import requests
from datetime import *

class gameData:
    def __init__(self):
        self.gamePk = ""
        self.homeID = ""
        self.awayID = ""
        self.homeName = ""
        self.awayName = ""

class batterInfo:
    def __init__(self):
        self.name = ""
        self.ID = ""
        self.posNum = 0
        self.order = 0
    def print(self):
        print(self.name + " ")
        print(str(self.ID) + " ")
        print(str(self.posNum) + " ")
        print(str(self.order) + " ")

class pitcherInfo:
    def __init__(self):
        self.name = ""
        self.ID = ""
        self.hand = ""
    def print(self):
        print(self.name + " ")
        print(str(self.ID) + " ")

class lineUp:
    def __init__(self):
        self.batters = []
        self.pitcher = []
        self.win = False
    def print(self):
        for batter in self.batters:
            batter.print() 
           # print("\n")
        print("\n")
        self.pitcher.print()
        print(self.win)
        

def getStartingPitcher(home, gamePk):
    jsonFileLink = "https://statsapi.mlb.com/api/v1/schedule?gamePk=" + gamePk + "&hydrate=probablePitcher"
    jsonFileRequest = requests.get(jsonFileLink)
    #print(jsonFileLink)
    data = jsonFileRequest.content
    dataJson = json.loads(data)
    pitchHandLink = "https://statsapi.mlb.com"
    try:
        games = dataJson['dates'][0]['games'][0]['teams']
        pitcher = pitcherInfo()
        if home:
            pitcher.name = games['home']['probablePitcher']['fullName']
            pitcher.ID = games['home']['probablePitcher']['id']
            pitchHandLink += games['home']['probablePitcher']['link']
        else:
            pitcher.name = games['away']['probablePitcher']['fullName']
            pitcher.ID = games['away']['probablePitcher']['id']
            pitchHandLink += games['away']['probablePitcher']['link']
        jsonHand = requests.get(pitchHandLink)
        dataHand = jsonHand.content
        dataJsonHand = json.loads(dataHand)
        pitcher.hand = dataJsonHand['people'][0]['pitchHand']['code']
        #print(pitcher.hand)
        return pitcher
    except:
        bad = pitcherInfo()
        bad.name = "None"
        return bad
    
def getStartingLineup(home, gamePk):
    jsonFileLink = "https://statsapi.mlb.com/api/v1/schedule?gamePk=" + gamePk + "&hydrate=lineups"
    jsonFileRequest = requests.get(jsonFileLink)
    #print(jsonFileLink)
    data = jsonFileRequest.content
    dataJson = json.loads(data)
    #try:
    if home:
        allBatters = dataJson['dates'][0]['games'][0]['lineups']['homePlayers']
        teamWin = dataJson['dates'][0]['games'][0]['teams']['home']['isWinner']
    else:
        allBatters = dataJson['dates'][0]['games'][0]['lineups']['awayPlayers']
        teamWin = dataJson['dates'][0]['games'][0]['teams']['away']['isWinner']
    if teamWin == 'true':
        teamWin = 1
    else:
        teamWin = 0
    batters = []
    i = 1
    for player in allBatters:
        curBatter = batterInfo()
        curBatter.ID = player['id']
        curBatter.name = player['fullName']
        curBatter.posNum = player['primaryPosition']['code']
        curBatter.order = i
        batters.append(curBatter)
        i += 1
    return batters, teamWin
    #except:
        #return "game has no lineup set yet/error gettinglineup"

def getJustLineup(home, gamePk):
    jsonFileLink = "https://statsapi.mlb.com/api/v1/schedule?gamePk=" + gamePk + "&hydrate=lineups"
    jsonFileRequest = requests.get(jsonFileLink)
    #print(jsonFileLink)
    data = jsonFileRequest.content
    dataJson = json.loads(data)
    #try:
    if home:
        allBatters = dataJson['dates'][0]['games'][0]['lineups']['homePlayers']
    else:
        allBatters = dataJson['dates'][0]['games'][0]['lineups']['awayPlayers']
    batters = []
    i = 1
    for player in allBatters:
        curBatter = batterInfo()
        curBatter.ID = player['id']
        curBatter.name = player['fullName']
        curBatter.posNum = player['primaryPosition']['code']
        curBatter.order = i
        batters.append(curBatter)
        i += 1
    return batters

def getProbableLineup(home, gamePk, teamId, year, month, day):
    try:
        return getJustLineup(home, gamePk)
    except:
        #print("couldn't get real lineup, searching for previous lineups")
        
        curDate = datetime(year, month, day)
        curDate = curDate - timedelta(days = 1)
        i = 0
        while i < 7:
            
            curGames = getGamePksTeams(curDate.year, curDate.month, curDate.day)
        
            for game in curGames:
                if game.homeID == teamId:
                    print("lineup found from gamePk: " + str(game.gamePk) + " on date: " + str(curDate))
                    return getJustLineup(True, str(game.gamePk))
                elif game.awayID == teamId:
                    print("lineup found from gamePk: " + str(game.gamePk) + " on date: " + str(curDate))
                    return getJustLineup(False, str(game.gamePk))
                
            curDate = curDate - timedelta(days = 1)
            i += 1


def getGamePksTeams(year, month, day):
    jsonFileLink = "https://statsapi.mlb.com/api/v1/schedule?sportId=1&date=" + str(year) + "-" + str(month) + "-" + str(day) + "&gameType=R&fields=dates,games,gamePk,teams,away,home,team,id,name"
    jsonFileRequest = requests.get(jsonFileLink)
    #print(jsonFileLink)
    data = jsonFileRequest.content
    dataJson = json.loads(data)
    games = dataJson['dates'][0]['games']

    allGameData = []

    for game in games:
        temp = gameData()
        temp.gamePk = game['gamePk']
        temp.awayID = game['teams']['away']['team']['id']
        temp.homeID = game['teams']['home']['team']['id']
        temp.awayName = game['teams']['away']['team']['name']
        temp.homeName = game['teams']['home']['team']['name']
        allGameData.append(temp)

    return allGameData

def getPitcherAndLineup(home, gamePk):
    lineup = lineUp()
    lineup.batters, lineup.win = getStartingLineup(home, gamePk)
    lineup.pitcher = getStartingPitcher(home, gamePk)
    return lineup


#listofDats = getGamePksTeams("2024", "5", "31")
#print(listofDats.pop().gamePk)
#lineip = getPitcherAndLineup(False, "745331")
#getStartingPitcher(False, "745331")

#lineip.print()

#for x in getProbableLineup(False, "747009", 147, 2024, 7, 14):
#    x.print()
