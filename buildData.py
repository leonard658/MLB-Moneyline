import pandas as pd
from datetime import *
from getRecentStats import getPitcherStats, getGeneralBatterStats, getSpecificBatterStats, getBullpenStats
from getLineup import batterInfo, pitcherInfo, lineUp, getStartingLineup, getStartingPitcher, getGamePksTeams, getPitcherAndLineup, getProbableLineup


team_abbs = {
    108: "LAA",
    109: "AZ",
    110: "BAL",
    111: "BOS",
    112: "CHC",
    113: "CIN",
    114: "CLE",
    115: "COL",
    116: "DET",
    117: "HOU",
    118: "KC",
    119: "LAD",
    120: "WSH",
    121: "NYM",
    133: "OAK",
    134: "PIT",
    135: "SD",
    136: "SEA",
    137: "SF",
    138: "STL",
    139: "TB",
    140: "TEX",
    141: "TOR",
    142: "MIN",
    143: "PHI",
    144: "ATL",
    145: "CWS",
    146: "MIA",
    147: "NYY",
    158: "MIL",
}


def buildBatterData(battingOrder, playerID, year, month, day, pitcherHand, extension):
    playerGen = getGeneralBatterStats(28, playerID, year, month, day, battingOrder, extension)
    #print(playerGen)
    playerSpecific = getSpecificBatterStats(365, playerID, year, month, day, battingOrder, extension, pitcherHand)
    allStats = pd.concat([playerGen, playerSpecific], axis=1)
    #print(playerDf)

    return allStats


def buildWholeGameDataNoWin(gamePk, year, month, day, homeTeamID, awayTeamID):
    importantInfo = pd.DataFrame()

    home_batters = getProbableLineup(True, gamePk, homeTeamID, year, month, day)
    home_pitcher = getStartingPitcher(True, gamePk)
    away_batters = getProbableLineup(False, gamePk, awayTeamID, year, month, day)
    away_pitcher = getStartingPitcher(False, gamePk)

    for batter in home_batters:
        #print(batter.ID)
        temp = buildBatterData(batter.order, batter.ID, year, month, day, away_pitcher.hand, "_home")
        importantInfo = pd.concat([importantInfo, temp], axis=1)
        #print(temp)
    importantInfo = pd.concat([importantInfo, getPitcherStats(30, home_pitcher.ID, year, month, day, "_home")], axis=1)
    importantInfo = pd.concat([importantInfo, getPitcherStats(365, home_pitcher.ID, year, month, day, "_home_1")], axis=1)
    importantInfo = pd.concat([importantInfo, getBullpenStats(21, team_abbs.get(int(homeTeamID)), year, month, day, "_home")], axis=1)

    for batter in away_batters:
        #print(batter.ID)
        temp = buildBatterData(batter.order, batter.ID, year, month, day, home_pitcher.hand, "_away")
        importantInfo = pd.concat([importantInfo, temp], axis=1)
    importantInfo = pd.concat([importantInfo, getPitcherStats(30, away_pitcher.ID, year, month, day, "_away")], axis=1)
    importantInfo = pd.concat([importantInfo, getPitcherStats(365, away_pitcher.ID, year, month, day, "_away_1")], axis=1)
    importantInfo = pd.concat([importantInfo, getBullpenStats(21, team_abbs.get(int(awayTeamID)), year, month, day, "_away")], axis=1)

    return importantInfo, home_pitcher.name, away_pitcher.name


def buildWholeGameData(gamePk, year, month, day, homeTeamID, awayTeamID):
    importantInfo = pd.DataFrame()

    home_lineup = getPitcherAndLineup(True, gamePk)
    home_pitcher = home_lineup.pitcher
    away_lineup = getPitcherAndLineup(False, gamePk)
    away_pitcher = away_lineup.pitcher

    for batter in home_lineup.batters:
        #print(batter.ID)
        temp = buildBatterData(batter.order, batter.ID, year, month, day, away_pitcher.hand, "_home")
        importantInfo = pd.concat([importantInfo, temp], axis=1)
        #print(temp)
    importantInfo = pd.concat([importantInfo, getPitcherStats(30, home_pitcher.ID, year, month, day, "_home")], axis=1)
    importantInfo = pd.concat([importantInfo, getPitcherStats(365, home_pitcher.ID, year, month, day, "_home_1")], axis=1)
    importantInfo = pd.concat([importantInfo, getBullpenStats(21, team_abbs.get(int(homeTeamID)), year, month, day, "_home")], axis=1)

    for batter in away_lineup.batters:
        temp = buildBatterData(batter.order, batter.ID, year, month, day, home_pitcher.hand, "_away")
        importantInfo = pd.concat([importantInfo, temp], axis=1)
    importantInfo = pd.concat([importantInfo, getPitcherStats(30, away_pitcher.ID, year, month, day, "_away")], axis=1)
    importantInfo = pd.concat([importantInfo, getPitcherStats(365, away_pitcher.ID, year, month, day, "_away_1")], axis=1)
    importantInfo = pd.concat([importantInfo, getBullpenStats(21, team_abbs.get(int(awayTeamID)), year, month, day, "_away")], axis=1)
    
    
    homeWin = pd.DataFrame([[home_lineup.win]], columns=['home_win'])
    importantInfo = pd.concat([importantInfo, homeWin], axis=1)
    
    return importantInfo

def buildTimeFrame(sYear, sMonth, sDay, eYear, eMonth, eDay):
    startDate = datetime(sYear, sMonth, sDay)
    endDate = datetime(eYear, eMonth, eDay)
    trainData = pd.DataFrame()
    while startDate <= endDate:
        gamestdy = getGamePksTeams(startDate.year, startDate.month, startDate.day)
        for game in gamestdy:
            temp = pd.DataFrame([[startDate]], columns=['date'])
            temp = pd.concat([temp, buildWholeGameData(str(game.gamePk), startDate.year, startDate.month, startDate.day, game.homeID, game.awayID)], axis = 1)
            trainData = pd.concat([trainData, temp], axis = 0)
            print("*")
        startDate = startDate + timedelta(days = 1)
    return trainData

#gamestdy = getGamePksTeams(2024, 6, 13)
#trainData = buildWholeGameData("745331", 2024, 5, 31, "147", "137")
#for game in gamestdy:
   # trainData = pd.concat([trainData, buildWholeGameData(str(game.gamePk), 2024, 6, 13)], axis = 0)
   # print("*")
#print(trainData)
#trainData.to_csv('tester.csv', index=False)


#trainData = buildTimeFrame(2024, 6, 20, 2024, 6, 20)
#trainData.to_csv('tester.csv', index=False)
#print(trainData)

