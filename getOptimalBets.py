import pandas as pd
import numpy as np
import lightgbm as lgbm
from lightgbm import Booster
from datetime import *
from getLineup import gameData, getGamePksTeams
from buildData import buildWholeGameDataNoWin


#Json format for each game
#Hometeam:
#   name:
#   starting_pitcher
#   odds_win:
#   0%_edge_odds:
#   5%_edge_odds:
#   10%_edge_odds:
#   20%_edge_odds:
#Awayteam:
#   name:
#   starting_pitcher
#   odds_win:
#   5%_edge_odds:
#   5%_edge_odds:
#   10%_edge_odds:
#   20%_edge_odds:
#game_time:


def impliedOddsToAmerican(impliedOdds):
    if impliedOdds > 0 and impliedOdds < 1:
        amOdds = "+100"
        if impliedOdds < .5:
            return "+" + str(round((100 / impliedOdds) - 100))
        elif impliedOdds > .5:
            return "-" + str(round(-((100 * impliedOdds) / (impliedOdds - 1))))
        return amOdds
    else:
        return "N/A"

def getModelOdds(mainDf):
    model = lgbm.Booster(model_file='NoFeatureEngineering.txt')
    prediction = model.predict(mainDf)[0]
    return prediction

def condenseGameData(fullDf):
    irrelevant_stats = [
    "total_1_home", 
    "pitch_percentage_1_home", 
    "total_vs_hand_1_home", 
    "pitch_percentage_vs_hand_1_home", 
    "total_2_home", 
    "pitch_percentage_2_home", 
    "total_vs_hand_2_home", 
    "pitch_percentage_vs_hand_2_home", 
    "total_3_home", 
    "pitch_percentage_3_home", 
    "total_vs_hand_3_home", 
    "pitch_percentage_vs_hand_3_home", 
    "total_4_home", 
    "pitch_percentage_4_home", 
    "total_vs_hand_4_home", 
    "pitch_percentage_vs_hand_4_home", 
    "total_5_home", 
    "pitch_percentage_5_home", 
    "total_vs_hand_5_home", 
    "pitch_percentage_vs_hand_5_home", 
    "total_6_home", 
    "pitch_percentage_6_home", 
    "total_vs_hand_6_home", 
    "pitch_percentage_vs_hand_6_home", 
    "total_7_home", 
    "pitch_percentage_7_home", 
    "total_vs_hand_7_home", 
    "pitch_percentage_vs_hand_7_home", 
    "total_8_home", 
    "pitch_percentage_8_home", 
    "total_vs_hand_8_home", 
    "pitch_percentage_vs_hand_8_home", 
    "total_9_home", 
    "pitch_percentage_9_home", 
    "total_vs_hand_9_home", 
    "pitch_percentage_vs_hand_9_home", 
    "total_pitch_home", 
    "pitch_percentage_pitch_home", 
    "total_pitch_home_1", 
    "pitch_percentage_pitch_home_1", 
    "total_bullpen_home", 
    "pitch_percentage_bullpen_home", 
    "total_1_away", 
    "pitch_percentage_1_away", 
    "total_vs_hand_1_away", 
    "pitch_percentage_vs_hand_1_away", 
    "total_2_away", 
    "pitch_percentage_2_away", 
    "total_vs_hand_2_away", 
    "pitch_percentage_vs_hand_2_away", 
    "total_3_away", 
    "pitch_percentage_3_away", 
    "total_vs_hand_3_away", 
    "pitch_percentage_vs_hand_3_away", 
    "total_4_away", 
    "pitch_percentage_4_away", 
    "total_vs_hand_4_away", 
    "pitch_percentage_vs_hand_4_away", 
    "total_5_away", 
    "pitch_percentage_5_away", 
    "total_vs_hand_5_away", 
    "pitch_percentage_vs_hand_5_away", 
    "total_6_away", 
    "pitch_percentage_6_away", 
    "total_vs_hand_6_away", 
    "pitch_percentage_vs_hand_6_away", 
    "total_7_away", 
    "pitch_percentage_7_away", 
    "total_vs_hand_7_away", 
    "pitch_percentage_vs_hand_7_away", 
    "total_8_away", 
    "pitch_percentage_8_away", 
    "total_vs_hand_8_away", 
    "pitch_percentage_vs_hand_8_away", 
    "total_9_away", 
    "pitch_percentage_9_away", 
    "total_vs_hand_9_away", 
    "pitch_percentage_vs_hand_9_away", 
    "total_pitch_away", 
    "pitch_percentage_pitch_away", 
    "total_pitch_away_1", 
    "pitch_percentage_pitch_away_1", 
    "total_bullpen_away", 
    "pitch_percentage_bullpen_away"
]

    mainDf = fullDf.drop(labels = irrelevant_stats, axis = 1)
    return mainDf  

def getTodaysBets(year, month, day):
    gamestdy = getGamePksTeams(year, month, day)
    allGamesJsonList = []

    excludeGames = []
    
    for game in gamestdy:
        if game.gamePk in excludeGames:
            print("Game on exclude games: " + str(game.gamePk))
            continue
        gameJson = getOneGameData(game, year, month, day)
        allGamesJsonList.append(gameJson)
    
    return allGamesJsonList

def getOneGameData(game, year, month, day):
    print(game.gamePk)
    curGame, homePitch, awayPitch = buildWholeGameDataNoWin(str(game.gamePk), year, month, day, game.homeID, game.awayID)
    
    #print(curGame['total_1_home'][0])
    condensedData = condenseGameData(curGame) 

    condensedData = condensedData.replace('--', -1)

    condensedData = condensedData.astype(float)
    #print(condensedData.dtypes)

    homeWinOdds = getModelOdds(condensedData)
    home0Percent = impliedOddsToAmerican(homeWinOdds)
    home5Percent = impliedOddsToAmerican(homeWinOdds - .05)
    home10Percent = impliedOddsToAmerican(homeWinOdds - .1)
    home20Percent = impliedOddsToAmerican(homeWinOdds - .2)

    awayWinOdds = 1 - homeWinOdds
    away0Percent = impliedOddsToAmerican(awayWinOdds)
    away5Percent = impliedOddsToAmerican(awayWinOdds - .05)
    away10Percent = impliedOddsToAmerican(awayWinOdds - .1)
    away20Percent = impliedOddsToAmerican(awayWinOdds - .2)

    homeJson = {
            "name": game.homeName,
            "starting_pitcher": homePitch,
            "odds_win": homeWinOdds,
            "0_percent_edge": home0Percent,
            "5_percent_edge": home5Percent,
            "10_percent_edge": home10Percent,
            "20_percent_edge": home20Percent,
        }
    awayJson = {
            "name": game.awayName,
            "starting_pitcher": awayPitch,
            "odds_win": awayWinOdds,
            "0_percent_edge": away0Percent,
            "5_percent_edge": away5Percent,
            "10_percent_edge": away10Percent,
            "20_percent_edge": away20Percent,
        }
    gameJson = {
            "away_team": awayJson,
            "home_team": homeJson,
        }

#print("*")
    print(gameJson)
    return gameJson
print(getTodaysBets(2024, 9, 11))



