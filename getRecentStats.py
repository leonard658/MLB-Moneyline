#from getLineup import *
import pandas as pd
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import requests


def getGeneralBatterStats(lastXDays, playerID, year, month, day, num, extension):
    #lastXDays = 30
    playerID = str(playerID)
    date = datetime(year, month, day)
    dateBack = date - timedelta(days = lastXDays)
    htmlFileLink = "https://baseballsavant.mlb.com/statcast_search?hfPT=&hfAB=&hfGT=R%7C&hfPR=&hfZ=&hfStadium=&hfBBL=&hfNewZones=&hfPull=&hfC=&hfSea=2024%7C2023%7C2022%7C2021%7C2020%7C2019%7C2018%7C2017%7C2016%7C2015%7C2014%7C2013%7C2012%7C2011%7C2010%7C2009%7C2008%7C&hfSit=&player_type=batter&hfOuts=&hfOpponent=&pitcher_throws=&batter_stands=&hfSA=&game_date_gt=" + dateBack.strftime("%Y-%m-%d") + "&game_date_lt=" + date.strftime("%Y-%m-%d") + "&hfMo=&hfTeam=TOR%7CBAL%7CTB%7CBOS%7CNYY%7CCLE%7CKC%7CDET%7CMIN%7CCWS%7CLAA%7CHOU%7COAK%7CSEA%7CTEX%7CATL%7CMIA%7CNYM%7CWSH%7CPHI%7CMIL%7CSTL%7CCHC%7CPIT%7CCIN%7CAZ%7CLAD%7CSF%7CSD%7CCOL%7C&home_road=&hfRO=&position=&hfInfield=&hfOutfield=&hfInn=&hfBBT=&batters_lookup%5B%5D=" + playerID + "&hfFlag=is%5C.%5C.remove%5C.%5C.bunts%7C&metric_1=&group_by=name&min_pitches=0&min_results=0&min_pas=0&sort_col=pitches&player_event_sort=api_p_release_speed&sort_order=desc&chk_game_date_gt=on&chk_team=on&chk_game_date_lt=on&chk_stats_pa=on&chk_stats_abs=on&chk_stats_bip=on&chk_stats_hits=on&chk_stats_k_percent=on&chk_stats_bb_percent=on&chk_stats_swings=on&chk_stats_ba=on&chk_stats_xba=on&chk_stats_obp=on&chk_stats_xobp=on&chk_stats_slg=on&chk_stats_xslg=on&chk_stats_woba=on&chk_stats_xwoba=on&chk_stats_babip=on&chk_stats_iso=on&chk_stats_launch_speed=on&chk_stats_hyper_speed=on&chk_stats_launch_angle=on&chk_stats_hardhit_percent=on#results"
    htmlString = requests.get(htmlFileLink)
    soup = BeautifulSoup(htmlString.content, 'html.parser')
    results = soup.find_all("td", class_ ="tr-data align-right")
    #print(htmlFileLink)
    data = []

    while len(results) > 0:
        data.append(results.pop(0).text.strip())

    try:
        playerData = pd.DataFrame([data], columns=[
        "total_" + str(num) + extension, "pitch_percentage_" + str(num) + extension,"pa_"  + str(num) + extension,"ab_" + str(num) + extension, "bip_" + str(num) + extension,
        "hits_" + str(num) + extension, "k_percentage_" + str(num) + extension, "bb_percentage_" + str(num) + extension, "swings_" + str(num) + extension, "ba_" + str(num) + extension, 
        "xba_" + str(num) + extension, "obp_" + str(num) + extension, "xobp_" + str(num) + extension, "slg_" + str(num) + extension,
        "xslg_" + str(num) + extension, "woba_" + str(num) + extension, "xwoba_" + str(num) + extension, "babip_" + str(num) + extension, "iso_" + str(num) + extension,
        "ev_" + str(num) + extension, "adj_ev_" + str(num) + extension, "launch_angle_" + str(num) + extension, "hard_hit_percentage_" + str(num) + extension
        ])
    except:
        print("plyer has no stats for this search. all values set to -1")
        data = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
        playerData = pd.DataFrame([data], columns=[
        "total_" + str(num) + extension, "pitch_percentage_" + str(num) + extension,"pa_"  + str(num) + extension,"ab_" + str(num) + extension, "bip_" + str(num) + extension,
        "hits_" + str(num) + extension, "k_percentage_" + str(num) + extension, "bb_percentage_" + str(num) + extension, "swings_" + str(num) + extension, "ba_" + str(num) + extension, 
        "xba_" + str(num) + extension, "obp_" + str(num) + extension, "xobp_" + str(num) + extension, "slg_" + str(num) + extension,
        "xslg_" + str(num) + extension, "woba_" + str(num) + extension, "xwoba_" + str(num) + extension, "babip_" + str(num) + extension, "iso_" + str(num) + extension,
        "ev_" + str(num) + extension, "adj_ev_" + str(num) + extension, "launch_angle_" + str(num) + extension, "hard_hit_percentage_" + str(num) + extension
        ])

    return playerData

def getSpecificBatterStats(lastXDays, playerID, year, month, day, num, extension, pitcherHand):
    playerID = str(playerID)
    date = datetime(year, month, day)
    dateBack = date - timedelta(days = lastXDays)
    #print(dateBack)
    if pitcherHand == 'R':
        htmlFileLink = "https://baseballsavant.mlb.com/statcast_search?hfPT=&hfAB=&hfGT=R%7C&hfPR=&hfZ=&hfStadium=&hfBBL=&hfNewZones=&hfPull=&hfC=&hfSea=2024%7C2023%7C2022%7C2021%7C2020%7C2019%7C2018%7C2017%7C2016%7C2015%7C2014%7C2013%7C2012%7C2011%7C2010%7C2009%7C2008%7C&hfSit=&player_type=batter&hfOuts=&hfOpponent=&pitcher_throws=R&batter_stands=&hfSA=&game_date_gt=" + dateBack.strftime("%Y-%m-%d") + "&game_date_lt=" + date.strftime("%Y-%m-%d") + "&hfMo=&hfTeam=TOR%7CBAL%7CTB%7CBOS%7CNYY%7CCLE%7CKC%7CDET%7CMIN%7CCWS%7CLAA%7CHOU%7COAK%7CSEA%7CTEX%7CATL%7CMIA%7CNYM%7CWSH%7CPHI%7CMIL%7CSTL%7CCHC%7CPIT%7CCIN%7CAZ%7CLAD%7CSF%7CSD%7CCOL%7C&home_road=&hfRO=&position=&hfInfield=&hfOutfield=&hfInn=&hfBBT=&batters_lookup%5B%5D="+ playerID + "&hfFlag=is%5C.%5C.remove%5C.%5C.bunts%7C&metric_1=&group_by=name&min_pitches=0&min_results=0&min_pas=0&sort_col=pitches&player_event_sort=api_p_release_speed&sort_order=desc&chk_game_date_gt=on&chk_team=on&chk_game_date_lt=on&chk_stats_pa=on&chk_stats_abs=on&chk_stats_bip=on&chk_stats_hits=on&chk_stats_k_percent=on&chk_stats_bb_percent=on&chk_stats_swings=on&chk_stats_ba=on&chk_stats_xba=on&chk_stats_obp=on&chk_stats_xobp=on&chk_stats_slg=on&chk_stats_xslg=on&chk_stats_woba=on&chk_stats_xwoba=on&chk_stats_babip=on&chk_stats_iso=on&chk_stats_launch_speed=on&chk_stats_hyper_speed=on&chk_stats_launch_angle=on&chk_stats_hardhit_percent=on#results"
    else:
        htmlFileLink = "https://baseballsavant.mlb.com/statcast_search?hfPT=&hfAB=&hfGT=R%7C&hfPR=&hfZ=&hfStadium=&hfBBL=&hfNewZones=&hfPull=&hfC=&hfSea=2024%7C2023%7C2022%7C2021%7C2020%7C2019%7C2018%7C2017%7C2016%7C2015%7C2014%7C2013%7C2012%7C2011%7C2010%7C2009%7C2008%7C&hfSit=&player_type=batter&hfOuts=&hfOpponent=&pitcher_throws=L&batter_stands=&hfSA=&game_date_gt=" + dateBack.strftime("%Y-%m-%d") + "&game_date_lt=" + date.strftime("%Y-%m-%d") + "&hfMo=&hfTeam=TOR%7CBAL%7CTB%7CBOS%7CNYY%7CCLE%7CKC%7CDET%7CMIN%7CCWS%7CLAA%7CHOU%7COAK%7CSEA%7CTEX%7CATL%7CMIA%7CNYM%7CWSH%7CPHI%7CMIL%7CSTL%7CCHC%7CPIT%7CCIN%7CAZ%7CLAD%7CSF%7CSD%7CCOL%7C&home_road=&hfRO=&position=&hfInfield=&hfOutfield=&hfInn=&hfBBT=&batters_lookup%5B%5D="+ playerID + "&hfFlag=is%5C.%5C.remove%5C.%5C.bunts%7C&metric_1=&group_by=name&min_pitches=0&min_results=0&min_pas=0&sort_col=pitches&player_event_sort=api_p_release_speed&sort_order=desc&chk_game_date_gt=on&chk_team=on&chk_game_date_lt=on&chk_stats_pa=on&chk_stats_abs=on&chk_stats_bip=on&chk_stats_hits=on&chk_stats_k_percent=on&chk_stats_bb_percent=on&chk_stats_swings=on&chk_stats_ba=on&chk_stats_xba=on&chk_stats_obp=on&chk_stats_xobp=on&chk_stats_slg=on&chk_stats_xslg=on&chk_stats_woba=on&chk_stats_xwoba=on&chk_stats_babip=on&chk_stats_iso=on&chk_stats_launch_speed=on&chk_stats_hyper_speed=on&chk_stats_launch_angle=on&chk_stats_hardhit_percent=on#results"
    #print(htmlFileLink)
    htmlString = requests.get(htmlFileLink)
    soup = BeautifulSoup(htmlString.content, 'html.parser')
    results = soup.find_all("td", class_ ="tr-data align-right")
    

    #print(htmlFileLink)
    data = []

    while len(results) > 0:
        data.append(results.pop(0).text.strip())

    try:
        playerData = pd.DataFrame([data], columns=[
        "total_vs_hand_" + str(num) + extension, "pitch_percentage_vs_hand_" + str(num) + extension,"pa_vs_hand_" + str(num) + extension,"ab_vs_hand_" + str(num) + extension, "bip_vs_hand_" + str(num) + extension, 
        "hits_vs_hand_" + str(num) + extension, "k_percentage_vs_hand_" + str(num) + extension, "bb_percentage_vs_hand_" + str(num) + extension, "swings_vs_hand_" + str(num) + extension, 
        "ba_vs_hand_" + str(num) + extension, "xba_vs_hand_" + str(num) + extension, "obp_vs_hand_" + str(num) + extension, "xobp_vs_hand_" + str(num) + extension, "slg_vs_hand_" + str(num) + extension,
        "xslg_vs_hand_" + str(num) + extension, "woba_vs_hand_" + str(num) + extension, "xwoba_vs_hand_" + str(num) + extension, "babip_vs_hand_" + str(num) + extension, "iso_vs_hand_" + str(num) + extension,
        "ev_vs_hand_" + str(num) + extension, "adj_ev_vs_hand_" + str(num) + extension, "launch_angle_vs_hand_" + str(num) + extension, "hard_hit_percentage_vs_hand_"  + str(num) + extension
        ])
    except:
        print("plyer has no stats for this search. all values set to -1")
        data = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
        playerData = pd.DataFrame([data], columns=[
        "total_vs_hand_" + str(num) + extension, "pitch_percentage_vs_hand_" + str(num) + extension,"pa_vs_hand_" + str(num) + extension,"ab_vs_hand_" + str(num) + extension, "bip_vs_hand_" + str(num) + extension, 
        "hits_vs_hand_" + str(num) + extension, "k_percentage_vs_hand_" + str(num) + extension, "bb_percentage_vs_hand_" + str(num) + extension, "swings_vs_hand_" + str(num) + extension, 
        "ba_vs_hand_" + str(num) + extension, "xba_vs_hand_" + str(num) + extension, "obp_vs_hand_" + str(num) + extension, "xobp_vs_hand_" + str(num) + extension, "slg_vs_hand_" + str(num) + extension,
        "xslg_vs_hand_" + str(num) + extension, "woba_vs_hand_" + str(num) + extension, "xwoba_vs_hand_" + str(num) + extension, "babip_vs_hand_" + str(num) + extension, "iso_vs_hand_" + str(num) + extension,
        "ev_vs_hand_" + str(num) + extension, "adj_ev_vs_hand_" + str(num) + extension, "launch_angle_vs_hand_" + str(num) + extension, "hard_hit_percentage_vs_hand_"  + str(num) + extension
        ])
    return playerData

def getPitcherStats(lastXDays, playerID, year, month, day, extension):
    playerID = str(playerID)
    date = datetime(year, month, day)
    dateBack = date - timedelta(days = lastXDays)
    htmlFileLink = "https://baseballsavant.mlb.com/statcast_search?hfPT=&hfAB=&hfGT=R%7C&hfPR=&hfZ=&hfStadium=&hfBBL=&hfNewZones=&hfPull=&hfC=&hfSea=2024%7C2023%7C2022%7C2021%7C2020%7C2019%7C2018%7C2017%7C2016%7C2015%7C2014%7C2013%7C2012%7C2011%7C2010%7C2009%7C2008%7C&hfSit=&player_type=pitcher&hfOuts=&hfOpponent=&pitcher_throws=&batter_stands=&hfSA=&game_date_gt=" + dateBack.strftime("%Y-%m-%d") + "&game_date_lt=" + date.strftime("%Y-%m-%d") + "&hfMo=&hfTeam=TOR%7CBAL%7CTB%7CBOS%7CNYY%7CCLE%7CKC%7CDET%7CMIN%7CCWS%7CLAA%7CHOU%7COAK%7CSEA%7CTEX%7CATL%7CMIA%7CNYM%7CWSH%7CPHI%7CMIL%7CSTL%7CCHC%7CPIT%7CCIN%7CAZ%7CLAD%7CSF%7CSD%7CCOL%7C&home_road=&hfRO=&position=&hfInfield=&hfOutfield=&hfInn=&hfBBT=&hfFlag=is%5C.%5C.remove%5C.%5C.bunts%7C&pitchers_lookup%5B%5D=" + playerID + "&metric_1=&group_by=name&min_pitches=0&min_results=0&min_pas=0&sort_col=pitches&player_event_sort=api_p_release_speed&sort_order=desc&chk_game_date_gt=on&chk_team=on&chk_game_date_lt=on&chk_stats_pa=on&chk_stats_abs=on&chk_stats_bip=on&chk_stats_hits=on&chk_stats_k_percent=on&chk_stats_bb_percent=on&chk_stats_swings=on&chk_stats_ba=on&chk_stats_xba=on&chk_stats_obp=on&chk_stats_xobp=on&chk_stats_slg=on&chk_stats_xslg=on&chk_stats_woba=on&chk_stats_xwoba=on&chk_stats_babip=on&chk_stats_iso=on&chk_stats_launch_speed=on&chk_stats_hyper_speed=on&chk_stats_launch_angle=on&chk_stats_hardhit_percent=on#results"
    htmlString = requests.get(htmlFileLink)
    soup = BeautifulSoup(htmlString.content, 'html.parser')
    results = soup.find_all("td", class_ ="tr-data align-right")
    
    data = []

    while len(results) > 0:
        data.append(results.pop(0).text.strip())

    try:
        playerData = pd.DataFrame([data], columns=[
        "total_pitch" + extension, "pitch_percentage_pitch" + extension,"pa_pitch"  + extension,"ab_pitch" + extension, "bip_pitch" + extension, "hits_pitch" + extension, 
        "k_percentage_pitch" + extension, "bb_percentage_pitch" + extension, "swings_pitch" + extension, "ba_pitch" + extension, "xba_pitch" + extension, "obp_pitch" + extension, "xobp_pitch" + extension, "slg_pitch" + extension,
        "xslg_pitch" + extension, "woba_pitch" + extension, "xwoba_pitch" + extension, "babip_pitch" + extension, "iso_pitch" + extension,
        "ev_pitch" + extension, "adj_ev_pitch" + extension, "launch_angle_pitch" + extension, "hard_hit_percentage_pitch" + extension 
        ])
    except:
        print("plyer has no stats for this search. all values set to -1")
        data = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
        playerData = pd.DataFrame([data], columns=[
        "total_pitch" + extension, "pitch_percentage_pitch" + extension,"pa_pitch"  + extension,"ab_pitch" + extension, "bip_pitch" + extension, "hits_pitch" + extension, 
        "k_percentage_pitch" + extension, "bb_percentage_pitch" + extension, "swings_pitch" + extension, "ba_pitch" + extension, "xba_pitch" + extension, "obp_pitch" + extension, "xobp_pitch" + extension, "slg_pitch" + extension,
        "xslg_pitch" + extension, "woba_pitch" + extension, "xwoba_pitch" + extension, "babip_pitch" + extension, "iso_pitch" + extension,
        "ev_pitch" + extension, "adj_ev_pitch" + extension, "launch_angle_pitch" + extension, "hard_hit_percentage_pitch" + extension 
        ])

    return playerData

def getBullpenStats(lastXDays, team, year, month, day, extension):
    date = datetime(year, month, day)
    dateBack = date - timedelta(days = lastXDays)
    htmlFileLink = "https://baseballsavant.mlb.com/statcast_search?hfPT=&hfAB=&hfGT=R%7C&hfPR=&hfZ=&hfStadium=&hfBBL=&hfNewZones=&hfPull=&hfC=&hfSea=2024%7C2023%7C2022%7C2021%7C2020%7C2019%7C2018%7C2017%7C2016%7C2015%7C&hfSit=&player_type=pitcher&hfOuts=&hfOpponent=&pitcher_throws=&batter_stands=&hfSA=&game_date_gt=" + dateBack.strftime("%Y-%m-%d") + "&game_date_lt=" + date.strftime("%Y-%m-%d") + "&hfMo=&hfTeam=" + team +"%7C&home_road=&hfRO=&position=RP&hfInfield=&hfOutfield=&hfInn=&hfBBT=&hfFlag=is%5C.%5C.remove%5C.%5C.bunts%7C&metric_1=&group_by=team&min_pitches=0&min_results=0&min_pas=0&sort_col=pitches&player_event_sort=api_p_release_speed&sort_order=desc&chk_stats_pa=on&chk_stats_abs=on&chk_stats_bip=on&chk_stats_hits=on&chk_stats_k_percent=on&chk_stats_bb_percent=on&chk_stats_swings=on&chk_stats_ba=on&chk_stats_xba=on&chk_stats_obp=on&chk_stats_xobp=on&chk_stats_slg=on&chk_stats_xslg=on&chk_stats_woba=on&chk_stats_xwoba=on&chk_stats_babip=on&chk_stats_iso=on&chk_stats_launch_speed=on&chk_stats_hyper_speed=on&chk_stats_launch_angle=on&chk_stats_hardhit_percent=on#results"
    #print(htmlFileLink)
    htmlString = requests.get(htmlFileLink)
    soup = BeautifulSoup(htmlString.content, 'html.parser')
    results = soup.find_all("td", class_ ="tr-data align-right")
    data = []

    while len(results) > 23:
        data.append(results.pop(0).text.strip())

    playerData = pd.DataFrame([data], columns=[
        "total_bullpen" + extension, "pitch_percentage_bullpen" + extension,"pa_bullpen"  + extension,"ab_bullpen" + extension, "bip_bullpen" + extension, "hits_bullpen" + extension, 
        "k_percentage_bullpen" + extension, "bb_percentage_bullpen" + extension, "swings_bullpen" + extension, "ba_bullpen" + extension, "xba_bullpen" + extension, "obp_bullpen" + extension, "xobp_bullpen" + extension, "slg_bullpen" + extension,
        "xslg_bullpen" + extension, "woba_bullpen" + extension, "xwoba_bullpen" + extension, "babip_bullpen" + extension, "iso_bullpen" + extension,
        "ev_bullpen" + extension, "adj_ev_bullpen" + extension, "launch_angle_bullpen" + extension, "hard_hit_percentage_bullpen" + extension 
        ])
    
    return playerData

#print(getBullpenStats(30, "NYY", 2024, 5, 30, "_home"))

