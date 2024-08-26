#import tensorflow as tf
import pandas as pd
from ProcessLast20StatsOBJ import statsOBJ

#train with games from lines 340-2230

def getLast20GameData(teamName, gameNum, maindf):
    awayGames = maindf[maindf['visiting_team'] == teamName]
    homeGames = maindf[maindf['home_team'] == teamName]

    last20GamesDf = awayGames[awayGames['visiting_team_game_number'] == gameNum-20]
    if last20GamesDf.empty:
        last20GamesDf = homeGames[homeGames['home_team_game_number'] == gameNum-20]
    
    for i in range(gameNum - 19, gameNum):
        temp = awayGames[awayGames['visiting_team_game_number'] == i]
        if temp.empty:
            temp = homeGames[homeGames['home_team_game_number'] == i]
        last20GamesDf = last20GamesDf._append(temp, ignore_index = True)

    #print(last20GamesDf)
    return last20GamesDf

def produceDfLast20(last20, teamName):
    awayGames = last20[last20['visiting_team'] == teamName]
    #print(awayGames)
    homeGames = last20[last20['home_team'] == teamName]
    
    # print(homeGames)

    stats = statsOBJ()
    
    #Offensive stats
    awayHits = awayGames['visiting_hits'].sum()
    homeHits = homeGames['home_hits'].sum()
    hits = awayHits + homeHits

    abs = awayGames['visiting_at_bats'].sum() + homeGames['home_at_bats'].sum()
    doubles = awayGames['visiting_doubles'].sum() + homeGames['home_doubles'].sum()
    triples = awayGames['visiting_triples'].sum() + homeGames['home_triples'].sum()
    hrs = awayGames['visiting_homeruns'].sum() + homeGames['home_homeruns'].sum()
    walks = awayGames['visiting_walks'].sum() + homeGames['home_walks'].sum()
    hbp = awayGames['visiting_hit_by_pitch'].sum() + homeGames['home_hit_by_pitch'].sum()
    sacrifices = awayGames['visiting_sac_hits'].sum() + homeGames['home_sac_hits'].sum()

    stats.RunScored = awayGames['visiting_team_score'].sum() + homeGames['home_team_score'].sum()
    stats.EarnedRunScored = awayGames['visiting_team_earned_runs'].sum() + homeGames['home_team_earned_runs'].sum()
    stats.LOB = awayGames['visiting_left_on_base'].sum() + homeGames['home_left_on_base'].sum()
    stats.PitchersUsed_against = awayGames['home_pitchers_used'].sum() + homeGames['visiting_pitchers_used'].sum()
    stats.setBA(abs, hits)
    stats.setSLG(abs, hits, doubles, triples, hrs)
    stats.setOBP(abs, hits, walks, hbp, sacrifices)

    #Defensive stats
    awayHitsAllowed = awayGames['home_hits'].sum()
    homeHitsAllowed = homeGames['visiting_hits'].sum()
    hitsAllowed = awayHitsAllowed + homeHitsAllowed

    absAgainst = awayGames['home_at_bats'].sum() + homeGames['visiting_at_bats'].sum()
    doublesAllowed = awayGames['home_doubles'].sum() + homeGames['visiting_doubles'].sum()
    triplesAllowed = awayGames['home_triples'].sum() + homeGames['visiting_triples'].sum()
    hrsAllowed = awayGames['home_homeruns'].sum() + homeGames['visiting_homeruns'].sum()
    walksAllowed = awayGames['home_walks'].sum() + homeGames['visiting_walks'].sum()
    hbpAllowed = awayGames['home_hit_by_pitch'].sum() + homeGames['visiting_hit_by_pitch'].sum()
    sacrificesAllowed = awayGames['home_sac_hits'].sum() + homeGames['visiting_sac_hits'].sum()

    stats.RunScored_against = awayGames['home_team_score'].sum() + homeGames['visiting_team_score'].sum()
    stats.EarnedRunScored_against = awayGames['home_team_earned_runs'].sum() + homeGames['visiting_team_earned_runs'].sum()
    stats.LOB_against = awayGames['home_left_on_base'].sum() + homeGames['visiting_left_on_base'].sum()
    stats.PitchersUsed = awayGames['visiting_pitchers_used'].sum() + homeGames['home_pitchers_used'].sum()
    stats.setBA_against(absAgainst, hitsAllowed)
    stats.setSLG_against(absAgainst, hitsAllowed, doublesAllowed, triplesAllowed, hrsAllowed)
    stats.setOBP_against(absAgainst, hitsAllowed, walksAllowed, hbpAllowed, sacrificesAllowed)
    stats.errors = awayGames['visiting_errors'].sum() + homeGames['home_errors'].sum()

    #win
    for ind in awayGames.index:
        if awayGames['visiting_team_score'][ind] > awayGames['home_team_score'][ind]:
            stats.wins += 1
            
    for ind in homeGames.index:
        if homeGames['home_team_score'][ind] > homeGames['visiting_team_score'][ind]:
            stats.wins += 1
    

    data = [
    stats.BA,
    stats.SLG,
    stats.OBP,
    stats.LOB,
    stats.RunScored,
    stats.EarnedRunScored,
    stats.PitchersUsed_against,
    stats.BA_against,
    stats.SLG_against,
    stats.OBP_against,
    stats.LOB_against,
    stats.RunScored_against,
    stats.EarnedRunScored_against,
    stats.errors,
    stats.PitchersUsed,
    stats.wins
    ]

    last20Df = pd.DataFrame([data], columns=[
    "BA", "SLG", "OBP", "LOB", "RunScored", "EarnedRunScored", "PitchersUsedAgainst",
    "BA_against", "SLG_against", "OBP_against", "LOB_against", "RunScored_against",
    "EarnedRunScored_against", "errors", "PitchersUsed", "wins"
    ])
    #print(last20Df)
    return last20Df

def processGame(maindf, lineNum):
    home_team = maindf['home_team'][lineNum]
    visiting_team = maindf['visiting_team'][lineNum]

    home_team_game_num = maindf['home_team_game_number'][lineNum]
    visiting_team_game_num = maindf['visiting_team_game_number'][lineNum]

    home_stats = produceDfLast20(getLast20GameData(home_team, home_team_game_num, maindf), home_team)
    visiting_stats = produceDfLast20(getLast20GameData(visiting_team, visiting_team_game_num, maindf), visiting_team)


    stats_concated = pd.concat([home_stats, visiting_stats], axis=1)
    #print(stats_concated)

    
    if maindf['home_team_score'][lineNum] > maindf['visiting_team_score'][lineNum]:
        home_win = pd.read_csv('1.txt')
    else:
        home_win = pd.read_csv('0.txt')
    #print(home_win)
    final_line = pd.concat([stats_concated, home_win], axis=1)
    #print(final_line)

    return final_line

def produceFullData(maindf, startPos, endPos):
    train_data = processGame(maindf, startPos)
    
    for i in range(startPos+1, endPos):
        temp = processGame(maindf, i)
        train_data = train_data._append(temp, ignore_index = True)

    return train_data

def main():
    maindf = pd.read_csv('gl2021.txt', header=None)
    features = [
    "date",
    "num_of_game",
    "day_of_week",
    "visiting_team",
    "visiting_league",
    "visiting_team_game_number",
    "home_team",
    "home_league",
    "home_team_game_number",
    "visiting_team_score",
    "home_team_score",
    "game_length_outs",
    "day_night",
    "completion_info",
    "forfeit_info",
    "protest_info",
    "park_id",
    "attendance",
    "game_time_minutes",
    "visiting_line_score",
    "home_line_score",
    "visiting_at_bats",
    "visiting_hits",
    "visiting_doubles",
    "visiting_triples",
    "visiting_homeruns",
    "visiting_rbi",
    "visiting_sac_hits",
    "visiting_sac_flies",
    "visiting_hit_by_pitch",
    "visiting_walks",
    "visiting_intentional_walks",
    "visiting_strikeouts",
    "visiting_stolen_bases",
    "visiting_caught_stealing",
    "visiting_double_plays",
    "visiting_triple_plays",
    "visiting_left_on_base",
    "visiting_pitchers_used",
    "visiting_individual_earned_runs",
    "visiting_team_earned_runs",
    "visiting_wild_pitches",
    "visiting_balks",
    "visiting_putouts",
    "visiting_assists",
    "visiting_errors",
    "visiting_passed_balls",
    "visiting_double_plays_defense",
    "visiting_triple_plays_defense",
    "home_at_bats",
    "home_hits",
    "home_doubles",
    "home_triples",
    "home_homeruns",
    "home_rbi",
    "home_sac_hits",
    "home_sac_flies",
    "home_hit_by_pitch",
    "home_walks",
    "home_intentional_walks",
    "home_strikeouts",
    "home_stolen_bases",
    "home_caught_stealing",
    "home_double_plays",
    "home_triple_plays",
    "home_left_on_base",
    "home_pitchers_used",
    "home_individual_earned_runs",
    "home_team_earned_runs",
    "home_wild_pitches",
    "home_balks",
    "home_putouts",
    "home_assists",
    "home_errors",
    "home_passed_balls",
    "home_double_plays_defense",
    "home_triple_plays_defense",
    "home_plate_umpire_id",
    "home_plate_umpire_name",
    "first_base_umpire_id",
    "first_base_umpire_name",
    "second_base_umpire_id",
    "second_base_umpire_name",
    "third_base_umpire_id",
    "third_base_umpire_name",
    "left_field_umpire_id",
    "left_field_umpire_name",
    "right_field_umpire_id",
    "right_field_umpire_name",
    "visiting_manager_id",
    "visiting_manager_name",
    "home_manager_id",
    "home_manager_name",
    "winning_pitcher_id",
    "winning_pitcher_name",
    "losing_pitcher_id",
    "losing_pitcher_name",
    "saving_pitcher_id",
    "saving_pitcher_name",
    "game_winning_rbi_batter_id",
    "game_winning_rbi_batter_name",
    "visiting_starting_pitcher_id",
    "visiting_starting_pitcher_name",
    "home_starting_pitcher_id",
    "home_starting_pitcher_name",
    "visiting_starting_player_1_id",
    "visiting_starting_player_1_name",
    "visiting_starting_player_1_position",
    "visiting_starting_player_2_id",
    "visiting_starting_player_2_name",
    "visiting_starting_player_2_position",
    "visiting_starting_player_3_id",
    "visiting_starting_player_3_name",
    "visiting_starting_player_3_position",
    "visiting_starting_player_4_id",
    "visiting_starting_player_4_name",
    "visiting_starting_player_4_position",
    "visiting_starting_player_5_id",
    "visiting_starting_player_5_name",
    "visiting_starting_player_5_position",
    "visiting_starting_player_6_id",
    "visiting_starting_player_6_name",
    "visiting_starting_player_6_position",
    "visiting_starting_player_7_id",
    "visiting_starting_player_7_name",
    "visiting_starting_player_7_position",
    "visiting_starting_player_8_id",
    "visiting_starting_player_8_name",
    "visiting_starting_player_8_position",
    "visiting_starting_player_9_id",
    "visiting_starting_player_9_name",
    "visiting_starting_player_9_position",
    "home_starting_player_1_id",
    "home_starting_player_1_name",
    "home_starting_player_1_position",
    "home_starting_player_2_id",
    "home_starting_player_2_name",
    "home_starting_player_2_position",
    "home_starting_player_3_id",
    "home_starting_player_3_name",
    "home_starting_player_3_position",
    "home_starting_player_4_id",
    "home_starting_player_4_name",
    "home_starting_player_4_position",
    "home_starting_player_5_id",
    "home_starting_player_5_name",
    "home_starting_player_5_position",
    "home_starting_player_6_id",
    "home_starting_player_6_name",
    "home_starting_player_6_position",
    "home_starting_player_7_id",
    "home_starting_player_7_name",
    "home_starting_player_7_position",
    "home_starting_player_8_id",
    "home_starting_player_8_name",
    "home_starting_player_8_position",
    "home_starting_player_9_id",
    "home_starting_player_9_name",
    "home_starting_player_9_position",
    "additional_info",
    "acquisition_info"
]
    maindf.columns=features

    features_for_basic_to_drop = [
    "date",
    "num_of_game",
    "day_of_week",
    "visiting_league",
    "home_league",
    "game_length_outs",
    "day_night",
    "completion_info",
    "forfeit_info",
    "protest_info",
    "park_id",
    "attendance",
    "visiting_line_score",
    "home_line_score",
    "visiting_sac_flies",
    "visiting_intentional_walks",
    "visiting_stolen_bases",
    "visiting_caught_stealing",
    "visiting_double_plays",
    "visiting_triple_plays",
    "visiting_individual_earned_runs",
    "visiting_wild_pitches",
    "visiting_balks",
    "visiting_putouts",
    "visiting_assists",
    "visiting_passed_balls",
    "visiting_double_plays_defense",
    "visiting_triple_plays_defense",
    "home_sac_flies",
    "home_intentional_walks",
    "home_stolen_bases",
    "home_caught_stealing",
    "home_double_plays",
    "home_triple_plays",
    "home_individual_earned_runs",
    "home_wild_pitches",
    "home_balks",
    "home_putouts",
    "home_assists",
    "home_passed_balls",
    "home_double_plays_defense",
    "home_triple_plays_defense",
    "home_plate_umpire_id",
    "home_plate_umpire_name",
    "first_base_umpire_id",
    "first_base_umpire_name",
    "second_base_umpire_id",
    "second_base_umpire_name",
    "third_base_umpire_id",
    "third_base_umpire_name",
    "left_field_umpire_id",
    "left_field_umpire_name",
    "right_field_umpire_id",
    "right_field_umpire_name",
    "visiting_manager_id",
    "visiting_manager_name",
    "home_manager_id",
    "home_manager_name",
    "winning_pitcher_id",
    "winning_pitcher_name",
    "losing_pitcher_id",
    "losing_pitcher_name",
    "saving_pitcher_id",
    "saving_pitcher_name",
    "game_winning_rbi_batter_id",
    "game_winning_rbi_batter_name",
    "visiting_starting_pitcher_name",
    "home_starting_pitcher_name",
    "visiting_starting_player_1_id",
    "visiting_starting_player_1_name",
    "visiting_starting_player_1_position",
    "visiting_starting_player_2_id",
    "visiting_starting_player_2_name",
    "visiting_starting_player_2_position",
    "visiting_starting_player_3_id",
    "visiting_starting_player_3_name",
    "visiting_starting_player_3_position",
    "visiting_starting_player_4_id",
    "visiting_starting_player_4_name",
    "visiting_starting_player_4_position",
    "visiting_starting_player_5_id",
    "visiting_starting_player_5_name",
    "visiting_starting_player_5_position",
    "visiting_starting_player_6_id",
    "visiting_starting_player_6_name",
    "visiting_starting_player_6_position",
    "visiting_starting_player_7_id",
    "visiting_starting_player_7_name",
    "visiting_starting_player_7_position",
    "visiting_starting_player_8_id",
    "visiting_starting_player_8_name",
    "visiting_starting_player_8_position",
    "visiting_starting_player_9_id",
    "visiting_starting_player_9_name",
    "visiting_starting_player_9_position",
    "home_starting_player_1_id",
    "home_starting_player_1_name",
    "home_starting_player_1_position",
    "home_starting_player_2_id",
    "home_starting_player_2_name",
    "home_starting_player_2_position",
    "home_starting_player_3_id",
    "home_starting_player_3_name",
    "home_starting_player_3_position",
    "home_starting_player_4_id",
    "home_starting_player_4_name",
    "home_starting_player_4_position",
    "home_starting_player_5_id",
    "home_starting_player_5_name",
    "home_starting_player_5_position",
    "home_starting_player_6_id",
    "home_starting_player_6_name",
    "home_starting_player_6_position",
    "home_starting_player_7_id",
    "home_starting_player_7_name",
    "home_starting_player_7_position",
    "home_starting_player_8_id",
    "home_starting_player_8_name",
    "home_starting_player_8_position",
    "home_starting_player_9_id",
    "home_starting_player_9_name",
    "home_starting_player_9_position",
    "additional_info",
    "acquisition_info"
]
    
    maindf.drop(labels=features_for_basic_to_drop, axis=1, inplace=True)

    test = produceFullData(maindf, 340, 2230)
    test.to_csv('2021TrainingData.csv', index=False)
    print(test)
    #produceDfLast20(getLast20GameData('NYN', 51, maindf), 'NYN')
    

main()