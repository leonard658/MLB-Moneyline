import concurrent.futures
import multiprocessing
from getOptimalBets import getOneGameData
from getLineup import gameData, getGamePksTeams


if __name__ == "__main__":  # confirms that the code is under main function
    year = 2024
    month= 7
    day = 14
    gamestdy = getGamePksTeams(year, month, day)

    #with concurrent.future.ProcessPoolExecutor() as executor:
    #    results =  executor.map(getOneGameData, gamestdy, year, month, day)
#
 #       for result in results:
  #          print(result)

    outGames = []
    for game in gamestdy:
        process = multiprocessing.Process(
            target=getOneGameData,
            args=(game, year, month, day,)
        )
        outGames.append(process)

    for j in outGames:
        j.start()

    for j in outGames:
        j.join()