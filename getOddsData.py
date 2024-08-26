import pandas as pd
import requests
from bs4 import BeautifulSoup
import json

teamId_to_oddsShark = {
    108: 26998,
    109: 27007,
    110: 27008,
    111: 27021,
    112: 27020,
    113: 27000,
    114: 27024,
    115: 27004,
    116: 26999,
    117: 27023,
    118: 27006,
    119: 27015,
    120: 27017,
    121: 27014,
    133: 27016,
    134: 27013,
    135: 26996,
    136: 27011,
    137: 26997,
    138: 27019,
    139: 27003,
    140: 27002,
    141: 27010,
    142: 27005,
    143: 26995,
    144: 27009,
    145: 27018,
    146: 27022,
    147: 27001,
    158: 27012
}

def getMoneyLine(home: bool, gamePk):
    monthToNum = {
        "04" : "Apr",
        "05" : "May",
        "06" : "Jun",
        "07" : "Jul",
        "08" : "Aug",
        "09" : "Sep",
        "10" : "Oct",
        "11" : "Nov"
    }
    
    jsonFileLink = "https://statsapi.mlb.com/api/v1/schedule?gamePk=" + gamePk
    jsonFileRequest = requests.get(jsonFileLink)
    #print(jsonFileLink)
    data = jsonFileRequest.content
    dataJson = json.loads(data)
    date = dataJson['dates'][0]['date']
    year = date[0:4]
    month = date[5:7]
    day = date[8:10]
    if day[0] == '0':
        day = day[1:2]
    if home:
        teamID = dataJson['dates'][0]['games'][0]['teams']['home']['team']['id']
    else:
        teamID = dataJson['dates'][0]['games'][0]['teams']['away']['team']['id']

    #print(date)
    #print("""<td class="td">""" + monthToNum[month] + " " + day + ", " + year + "</td>")
    #print(teamID)
    oddsLink = "https://www.oddsshark.com/stats/gamelog/baseball/mlb/" + str(teamId_to_oddsShark[teamID]) + "?season=" + year
    #print(oddsLink)
    oddsHTML = requests.get(oddsLink)
    soup = BeautifulSoup(oddsHTML.content, 'html.parser')
    allDat= soup.find_all("td")
    line = ""
    i = 0
    #print("""<td class="td">""" + monthToNum[month] + " " + day + ", " + year + "</td>")
    for point in allDat:
        #print(point)
        if str(point) == """<td class="td">""" + monthToNum[month] + " " + day + ", " + year + "</td>":
            #print("yes")
            i += 1
        elif i == 5:
            strLine = str(point)
            line = strLine[15:19]
            #print(line)
            break
        elif i > 0:
            i += 1
        
    #print(line)
    return line

def lineToDecimal(line):
    decimal = 0
    if line[0] == '+':
        num = int(line[1:])
        decimal = 100 / (num + 100)
    elif line[0] == '-':
        num = int(line[1:])
        decimal = num / (num + 100)
    else:
        print("Error in line input")
    return decimal

def buildImpliedHomeWin(gamePk):
    homeML = getMoneyLine(True, gamePk)
    #print(homeML)
    awayML = getMoneyLine(False, gamePk)
    #print(awayML)
    homeDec = lineToDecimal(homeML)
    awayDec = lineToDecimal(awayML)

    vig = (homeDec + awayDec) - 1
    #print(vig)
    
    combinedOdds = homeDec - (vig / 2) 

    return combinedOdds, homeDec, awayDec

def buildDat(): 
    mainDf = pd.read_csv('2024test.csv')
    oddsDf = pd.DataFrame(data = [], columns = ["homeDec", "awayDec", "combinedOdds"])
    #print(oddsDf)

    for ind in mainDf.index:
        print(ind)
        #print(mainDf['gamePk'][ind])
        combinedOdds, homeDec, awayDec = buildImpliedHomeWin(str(mainDf['gamePk'][ind]))
        data = [homeDec, awayDec, combinedOdds]
        oddsCur = pd.DataFrame([data], columns = ["homeDec", "awayDec", "combinedOdds"])
        #print(oddsCur)
        oddsDf = pd.concat([oddsDf, oddsCur], axis=0)
        #print(oddsDf)

    oddsDf.to_csv('oddsBackup2024.csv', index=False)

    mainDf = pd.concat([mainDf, oddsDf], axis=1)
    mainDf.to_csv('2024testWOdds.csv', index=False)




#lineToDecimal("+150")
#print(getMoneyLine(False, "745331"))
#print(teamId_to_oddsShark[147])
#df1 = pd.read_html('https://www.oddsshark.com/stats/gamelog/baseball/mlb/27024?season=2020')[0] # [0]
#print(df1)
#buildDat()
#print(buildImpliedHomeWin("716606"))

mainDf = pd.read_csv('2024test.csv')
oddsDf = pd.read_csv('oddsBackup2024.csv')
mainDf = pd.concat([mainDf, oddsDf], axis=1)
mainDf.to_csv('C2024testWithOdds.csv', index=False)