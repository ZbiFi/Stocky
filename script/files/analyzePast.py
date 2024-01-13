from numpy import mean

from script.files import LoadArchiveDataFromFile
import datetime as dt

def conditions(isBuy, conditionBuy, conditionSell, data):

    if isBuy:
        match conditionBuy:
            case 0:
                if data == 'BUY':
                    return True
            case 1:
                if data == 'BUY1':
                    return True
            case 2:
                if data == 'BUY2':
                    return True
            case 3:
                if data == 'BUY3':
                    return True
            case 4:
                if data == 'BUY1' or data == 'BUY2' or data == 'BUY3' or data == 'BUY':
                    return True
            case _:
                return False

    else:
        match conditionSell:
            case 0:
                if data == 'SELL':
                    return True
            case 1:
                if data == 'SELL1':
                    return True
            case 2:
                if data == 'SELL2':
                    return True
            case 3:
                if data == 'SELL3':
                    return True
            case 4:
                if data == 'SELL1' or data == 'SELL2' or data == 'SELL3' or data == 'SELL':
                    return True
            case _:
                return False
    return False

def findBestOptions():

    returnedROIValues = []
    for i in range(5):
        for j in range(5):
            part1 = round(analyzePast(i, j, False)[2]/100, 2)
            part2 = 1+round(analyzePast(i, j, False)[3]/100, 2)
            part3 = 1-round(analyzePast(i, j, False)[2]/100, 2)
            part4 = round(analyzePast(i, j, False)[4]/100, 2)

            profilorLoss = (part1*part2)+(part3*part4)
            returnedROIValues.append([i, j, round(float(profilorLoss), 3), round(analyzePast(i, j, False)[2]/100, 2), round(analyzePast(i, j, False)[3]/100, 2), round(analyzePast(i, j, False)[4]/100, 2)])

    cutOff0 = False
    cutOff1 = False
    cutOff2 = False
    headers = ['BUY TYPE', 'SELL TYPE', 'SUM PROFIT IN %', 'EFFICIENCY', 'PROFIT FROM CLOSED TRANS', 'PROFIT FROM OPEN TRANS IN DIFF']
    format_row = "{:<30}" * (len(headers))
    print(f'Analysis from {dt.datetime.now().date() - dt.timedelta(days = 1)} to {dt.datetime.now().date() - dt.timedelta(days = 365)}')
    print(format_row.format(*headers))
    returnedROIValuesSorted = sorted(returnedROIValues, key=lambda x: x[2], reverse=True)
    for row in returnedROIValuesSorted:
        if row[2] >= 1.2 and not cutOff0:
            print('STRONG STRATEGIES!')
            cutOff0=True
        if row[2] < 1.2 and not cutOff1:
            print('MEDIUM STRATEGIES!')
            cutOff1=True
        if row[2] < 1.1 and not cutOff2:
            print('WEAK STRATEGIES!')
            cutOff2=True
        print(format_row.format(*row))

    print(f'EFFICIENCY to miara ile tranzakcji zostało zamkniętych w ostatnim roku (wymagana para buy and sell) do ilości trakzakcji kupna, co nie zostało zamknięte ląduje w OPEN TRANS')
    return

def analyzePast(conditionBuyValue= 4, conditionSellValue=4, manual= True):

    #CONDITION FOR EFFIENCY ANALYSE  <0;3> lower value for restrictive

    archiveData = LoadArchiveDataFromFile.loadArchiveDataFromFile(0)
    # print(archiveData)

    # SORT BY DATE ASC (past->now)
    sortedData = sorted(archiveData, key=lambda x: x[1])
    # print(sortedData)

    # SEGREGATE BY COMPANY NAMES AND SPLIT INTO SUBLISTS
    indexes = [index for index, _ in enumerate(sortedData) if sortedData[index][1] != sortedData[index - 1][1]]
    indexes.append(len(sortedData))
    final = [sortedData[indexes[i]:indexes[i + 1]] for i, _ in enumerate(indexes) if i != len(indexes) - 1]

    pairFound = []
    pairWithLastKnownValue = []
    buySignal = 0

    #LOOK AND COUNT FOR BUYS, SELLS AND PAIRS OF B/S
    for companyData in final:
        sortedByDate = sorted(companyData, key=lambda x: x[0])
        foundBuyFlag = False
        foundBuy = []
        foundSellFlag = False
        foundSell = []
        lastData = None

        for data in sortedByDate:
            if conditions(True, conditionBuyValue, conditionSellValue, data[len(data)-1]) and not foundBuyFlag:
                foundBuyFlag = True
                foundBuy = data
                buySignal += 1
            if conditions(False, conditionBuyValue, conditionSellValue, data[len(data)-1]) and not foundSellFlag and foundBuyFlag:
                foundSellFlag = True
                foundSell = data
            lastData = data
            if foundBuyFlag and foundSellFlag:
                foundBuyFlag = False
                foundSellFlag = False
                pairFound.append([foundBuy, foundSell])

        if foundBuyFlag and not foundSellFlag:
            pairWithLastKnownValue.append([foundBuy, lastData])

    profitsList = []
    for pair in pairFound:
        # print(pair)
        profit = round((float(pair[1][3]) / float(pair[0][3]) * 100) - 100, 2)
        profitsList.append(profit)
        # print('Profit: ' + str(profit) + ' Expected: ' + str(pair[0][13]))
    restOpenList = []
    for pair in pairWithLastKnownValue:
        # print(pair)
        profit = round((float(pair[1][3]) / float(pair[0][3]) * 100), 2)
        restOpenList.append(profit)
    # print(restOpenList)
    if buySignal > 0:
        efficiencyReturnValue = round((len(pairFound) / buySignal) * 100, 2)
    else:
        efficiencyReturnValue = 0
    if len(profitsList) > 0:
        avarageProfitReturnValue = round(float(mean(profitsList)), 2)
    else:
        avarageProfitReturnValue = 0
    if len(restOpenList) > 0:
        avarageChangeForValueForOpen = round(float(mean(restOpenList)), 2)
    else:
        avarageChangeForValueForOpen = 0

    part1 = round(efficiencyReturnValue / 100, 2)
    part2 = 1 + round(avarageProfitReturnValue / 100, 2)
    part3 = 1 - round(efficiencyReturnValue / 100, 2)
    part4 = round(avarageChangeForValueForOpen / 100, 2)

    profilorLoss = round((part1 * part2) + (part3 * part4), 3)

    if manual:

        full = not True

        print('Buy signals: ' + str(buySignal))
        print('Pairs found: ' + str(len(pairFound)))
        print('ConditionBuy: ' + str(conditionBuyValue))
        print('ConditionSell: ' + str(conditionSellValue))
        print('Efficiency: ' + str(efficiencyReturnValue) + '%')
        print('Average profit: ' + str(avarageProfitReturnValue) + '%')
        print('Average change of value for rest open: ' + str(avarageChangeForValueForOpen) + '%')
        print('Profit/Loss: ' + str(profilorLoss))

        i=0
        print(f'SUCCESSFUL pairs (CLOSED)')
        for pair in pairFound:
            i+=1
            profit = round((float(pair[1][3]) / float(pair[0][3]) * 100), 2)
            if full:
                print(f'{i} {pair}')
                print(f'{i} profit/loss {profit}')
            else:
                print(f'{i} {pair[0][1]} B: {[pair[0][0],pair[0][2], pair[0][3]]} S: {[pair[1][0], pair[1][2], pair[1][3]]} Profit/Loss {profit}')

        print()
        print(f'LEFTOVER pair (OPEN)')
        for pair in pairWithLastKnownValue:
            i += 1
            profit = round((float(pair[1][3]) / float(pair[0][3]) * 100), 2)
            if full:
                print(f'{i} {pair}')
                print(f'{i} profit/loss {profit}')
            else:
                print(f'{i} {pair[0][1]} B: {[pair[0][0],pair[0][2], pair[0][3]]} S: {[pair[1][0], pair[1][2], pair[1][3]]} Profit/Loss {profit}')

    return [conditionBuyValue, conditionSellValue, efficiencyReturnValue, avarageProfitReturnValue, avarageChangeForValueForOpen, pairFound, pairWithLastKnownValue]

analyzePast(3,0)
# findBestOptions()