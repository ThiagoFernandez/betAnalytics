import json, time, datetime, random, shutil

#START
try: # json with the bet history
    with open("./data.json", "r") as f:
        data=json.load(f)
        print("The data was found ")
except FileNotFoundError:
    print("The data was not found")
    data = {}
    with open("./data.json", "w") as f:
        json.dump(data, f, indent=4)
except json.JSONDecodeError:
    print("Empy file, starting...")
    data = {}

try: #json with the bet settings
    with open("./betSettings.json", "r") as f:
        settings = json.load(f)
        print("The settings was found")
except FileNotFoundError:
    print("The settings was not found\nCreating a new")
    settings = {
        "betTypeList": {
            "Sport": {"Options": {}, "Detalle":{}},
            "Esport": {"Options": {},"Detalle":{} }, 
        }
    }
    with open("./betSettings.json", "w") as f:
        json.dump(settings, f, indent=4)
except json.JSONDecodeError:
    print("Empty file, starting...")
    settings = {
        "betTypeList": {
            "Sport": {"Options": {}, "Detalle":{}},
            "Esport": {"Options": {},"Detalle":{} }
        }
    }

def saveAll():
    with open("data.json", "w") as f:
        json.dump(data, f, indent=4)
    with open("betSettings.json", "w") as f:
        json.dump(settings, f, indent=4)
    return None

def backupData():
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    shutil.copy("./data.json", f"./backups/data_{timestamp}.json")

#print(settings["Sport"])
#opciones
#print(settings["Sport"]["Options"][0])  # Basketball
#print(settings["Esport"]["Options"][1]) # Valorant

#detalle
#print(settings["Sport"]["Detalle"]["Basketball"])# {'Competitions': ['NBA', 'EuroLeague'], 'Leagues': ['Liga ACB', 'CBA']}
#print(settings["Sport"]["Detalle"]["Football"])# {'Competitions': ['Champions League', 'Copa Libertadores'], 'Leagues': ['Premier League', 'La Liga']}

#competiciones o liga
#print(settings["Sport"]["Detalle"]["Basketball"]["Leagues"])
#print(settings["Sport"]["Detalle"]["Basketball"]["Competitions"])

users = list(data.keys())
if not users:
    newUser = input("Write your UserName: ").title().strip()
    activeUser = newUser
    data[activeUser]={
        "wallet": 0,
        "bets": {}
    }
    with open("./data.json", "w") as f:
        json.dump(data, f, indent=4)
else:
    for i, items in enumerate(users, start=1):
        print(f"{i}. {items}")
    print(f"{len(users)+1}. Add")
    while True:
        try:
            optionActiveUser = int(input("Choose an user: "))
            if optionActiveUser == len(users)+1:
                newUser = input("Write your UserName: ").title().strip()
                if newUser not in users:
                    activeUser = newUser
                    data[activeUser]={
                        "wallet": 0,
                        "bets": {}
                    }
                    with open("./data.json", "w") as f:
                        json.dump(data, f, indent=4)
                    break
                else:
                    print(f"{newUser} is already an user")
            elif optionActiveUser >len(users)+1 or optionActiveUser<=0:
                print(f"The option must be between 1-{len(users)+1}\nTry again")
            else:
                activeUser = users[optionActiveUser-1]
                break
        except ValueError:
            print("The option must be a number")


#//////////MAKING A BET//////////////
def validateBetType(diccionario):#STEP1
    keys=list(diccionario.keys())
    #print(keys)
    if not keys:
        print(f"1. Add\n2. Exit")
        while True:
            try:
                option = int(input("Choose an option between 1-2: "))
                if option >2 or option <1:
                    print(f"The option must be between 1-2\nTry again")
                elif option == 1:
                    newOption = input("Write the new option: ").title().strip()
                    keys.append(newOption)
                    settings[newOption] = {"Options": {}, "Detalle": {}}
                    with open("./betSettings.json", "w") as f:
                        json.dump(settings, f, indent=4)
                    return keys[-1]
                else:
                    return None
            except ValueError:
                print(f"The option must be a number\nTry again")
        
    for i, items in enumerate(keys, start=1):
        print(f"{i}. {items}")
    print(f"{len(keys)+1}. Add\n{len(keys)+2}. Exit")
    while True:
        try:
            keyOption = int(input(f"Choose between 1 and {len(keys)+2}: "))
            if keyOption > len(keys):
                if keyOption == len(keys)+1:
                    newOption = input("Write the new option: ").strip().title()
                    if newOption not in keys:
                        keys.append(newOption)
                        settings[newOption] = {"Options": {}, "Detalle": {}}
                        with open("./betSettings.json", "w") as f:
                            json.dump(settings, f, indent=4)
                        return keys[-1]
                    else:
                        print(f"{newOption} is already an option\nTry again")     
                elif keyOption == len(keys)+2:
                    return None
                else:
                    print(f"The option must be between 1-{len(keys)+2}\nTry again")        
            elif keyOption <=0:
                print(f"The option must be between 1-{len(keys)+2}\nTry again")  
            else:
                return keys[keyOption-1]
        except ValueError:
            print("The option must be a number")


def validateBetDiscipline(a):#STEP2
    lista=list(settings[a]["Options"])
    if not lista:
        print(f"1. Add\n2. Exit")
        while True:
            try:
                option = int(input("Choose an option between 1-2: "))
                if option >2 or option <1:
                    print(f"The option must be between 1-2\nTry again")
                elif option == 1:
                    newOption = input("Write the new option: ").title().strip()
                    lista.append(newOption)
                    settings[a]["Options"] = lista
                    hasCompetitionsLeagues = input(f"Has {newOption} competitions and leagues?\nyes or no: ").strip().lower()
                    while True:
                        if hasCompetitionsLeagues == "yes":
                            settings[a]["Detalle"][newOption] = {"Competitions": {}, "Leagues":{}} 
                            break
                        elif hasCompetitionsLeagues == "no":
                            settings[a]["Detalle"][newOption] = {"TeamsPlayers": {"Teams": {"List": [], "Markets": []}, "Players": {"List": [], "Markets": []}}}
                            break
                        else:
                            print("The option must be yes or no | try again")
                    with open("./betSettings.json", "w") as f:
                        json.dump(settings, f, indent=4)
                    return settings[a]["Options"][-1]
                else:
                    return None
            except ValueError:
                print(f"The option must be a number\nTry again")
    for i, items in enumerate(settings[a]["Options"], start=1):
        print(f"{i}. {items}")
    print(f"{len(settings[a]["Options"])+1}. Add\n{len(settings[a]["Options"])+2}. Exit")
    while True:
        try:
            disciplineOption = int(input(f"Choose between 1-{len(settings[a]["Options"])+2}: "))

            if disciplineOption>len(settings[a]["Options"]):
                if disciplineOption == len(settings[a]["Options"])+1:
                    newDiscipline = input("Write the new option: ").strip().title()
                    if newDiscipline not in settings[a]["Options"]:
                        lista.append(newDiscipline)
                        settings[a]["Options"] = lista
                        settings[a]["Detalle"][newDiscipline] = {"Competitions": {}, "Leagues":{}}
                        with open("./betSettings.json", "w") as f:
                            json.dump(settings, f, indent=4)
                        return settings[a]["Options"][-1]
                    else:
                        print(f"{newDiscipline} is already an option\nTry again")
                elif disciplineOption == len(settings[a]["Options"])+2:
                    return None
                else:
                    print(f"The option must be between 1-{len(settings[a]["Options"])+2}\nTry again")
            elif disciplineOption <=0:
                print(f"The option must be between 1-{len(settings[a]["Options"])+2}\nTry again")
            else:
                return settings[a]["Options"][disciplineOption-1]
            
        except ValueError:
            print("The option must be a number | Try again")


def validateBetFormat(a, b):#STEP 3
    lista = list(settings[a]["Detalle"][b].keys())
    if not lista:
        print("1. Add\n2. Exit")
        while True:
            try:
                option = int(input("Choose an option between 1-2: "))
                if option == 1:
                    newOption = input("Write the new option: ").title().strip()
                    if newOption not in lista:
                        lista.append(newOption)
                        settings[a]["Detalle"][b][newOption] = []
                        with open("./betSettings.json", "w") as f:
                            json.dump(settings, f, indent=4)
                        return newOption
                elif option == 2:
                    return None
                else:
                    print("The option must be between 1-2 | Try again")
            except ValueError:
                print("The option must be a number | Try again")
    for i, items in enumerate(lista, start=1):
        print(f"{i}. {items}")
    print(f"{len(lista)+1}. Exit")

    while True:
        try:
            formatOption = int(input(f"Choose between 1-{len(settings[a]["Detalle"][b])+2}: "))
            if formatOption ==3:
                return None
            elif formatOption >3 or formatOption<=0:
                print(f"The option must be between 1-{len(lista)}\nTry again")
            else:
                return lista[formatOption-1]               
        except ValueError:
            print(f"The option must be a number\nTry again")


def validateCompetitionsLeagues(a, b, c): #STEP 4
    lista = list(settings[a]["Detalle"][b][c].keys())
    if not lista:
        print(f"1. Add\n2. Exit")
        while True:
            try:
                option = int(input("Choose an option between 1-2: "))
                if option ==1:
                    newOption=input("Write the new option: ").title().strip()
                    settings[a]["Detalle"][b][c][newOption]= {"TeamsPlayers": {"Teams": {"List":[], "Markets":[]}, "Players": {"List":[], "Markets":[]}}}
                    with open("./betSettings.json", "w") as f:
                        json.dump(settings, f, indent=4)
                    lista.append(newOption)
                    return lista[-1]
                elif option == 2:
                    return None
                else:
                    print("The option must be between 1-2 | Try again")
            except ValueError:
                print("The option must be a number | Try again")
    for i, items in enumerate(lista, start=1):
        print(f"{i}. {items}")
    print(f"{len(lista)+1}. Add\n{len(lista)+2}. Exit")

    while True:
            try:
                competitionLeagueOption = int(input(f"Choose an option between 1-{len(lista)+2}: "))
                if competitionLeagueOption > len(lista):
                    if competitionLeagueOption == len(lista)+1:
                        newOption = input("Write the new option: ").title().strip()
                        if newOption not in lista:
                            newOption=input("Write the new option: ").title().strip()
                            settings[a]["Detalle"][b][c][newOption]= {"TeamsPlayers": {"Teams": {"List":[], "Markets":[]}, "Players": {"List":[], "Markets":[]}}}
                            with open ("./betSettings.json", "w") as f:
                                json.dump(settings, f, indent=4)
                            lista.append(newOption)
                            return lista[-1]
                        else:
                            print(f"{newOption} is already an option")
                    elif competitionLeagueOption == len(lista)+2:
                        return None
                    else:
                        print(f"The option must be between 1-{len(lista)+2} | Try again")
                elif competitionLeagueOption <=0:
                    print(f"The option must be between 1-{len(lista)+2} | Try again")
                else:
                    return lista[competitionLeagueOption-1]

            except ValueError:
                print("The option must be a number | Try again")


def validateTeamPlayerBet(a, b, c, d): #STEP 5
    lista = list(settings[a]["Detalle"][b][c][d]["TeamsPlayers"].keys())
    print("The bet is for a Team or for a Player?")
    for i, items in enumerate(lista, start=1):
        print(f"{i}. {items}")
    while True:
        try:
            option =int(input(f"Choose an option between 1-2: "))
            if option >len(lista) or option <=0:
                print(f"The option must be between 1-{len(lista)}")
            else:
                print(lista[option-1])
                return lista[option-1]
        except ValueError:
            print("The option must be a number | Try again")

def validateTeamPlayerList(a, b, c, d, e): #STEP 6
    lista = settings[a]["Detalle"][b][c][d]["TeamsPlayers"][e]["List"]
    for i, items in enumerate(lista, start=1):
        print(f"{i}. {items}")
    print(f"{len(lista)+1}. Add\n{len(lista)+2}. Exit")
    
    while True:
        try:
            betListOption = int(input(f"Choose an option between 1-{len(lista)+2}: "))
            if betListOption > len(lista):
                if betListOption == len(lista)+1:
                    newOption = input("Write the new option: ").title().strip()
                    if newOption not in lista:
                        lista.append(newOption)
                        settings[a]["Detalle"][b][c][d]["TeamsPlayers"][e]["List"] = lista
                        with open("./betSettings.json", "w") as f:
                            json.dump(settings, f, indent=4)
                        return lista[-1]
                    else:
                        print(f"{newOption} is already an option")
                elif betListOption == len(lista)+2:
                    return None
                else:
                    print(f"The option must be between 1-{len(lista)+2} | Try again")
            elif betListOption <=0:
                print(f"The option must be between 1-{len(lista)+2} | Try again")
            else:
                return lista[betListOption-1]
        except ValueError:
            print("The option must be a number | Try again")


def validateBetMarket(a, b, c, d, e): #STEP 7
    lista = settings[a]["Detalle"][b][c][d]["TeamsPlayers"][e]["Markets"]
    if not lista:
        print("1. Add\n2. Exit")
        while True:
            try:
                option = int(input("Choose an option between 1-2: "))
                if option == 1:
                    newOption = input("Write the new market: ").title().strip()
                    lista.append(newOption)
                    settings[a]["Detalle"][b][c][d]["TeamsPlayers"][e]["Markets"] = lista
                    with open("./betSettings.json", "w") as f:
                        json.dump(settings, f, indent=4)
                    return newOption
                elif option == 2:
                    return None
                else:
                    print("The option must be between 1-2 | Try again")
            except ValueError:
                print("The option must be a number | Try again")
    for i, items in enumerate(lista, start=1):
        print(f"{i}. {items}")
    print(f"{len(lista)+1}. Add\n{len(lista)+2}. Exit")
    
    while True:
        try:
            betMarketOption = int(input(f"Choose an option between 1-{len(lista)+2}: "))
            if betMarketOption > len(lista):
                if betMarketOption == len(lista)+1:
                    newOption = input("Write the new option: ").title().strip()
                    if newOption not in lista:
                        lista.append(newOption)
                        settings[a]["Detalle"][b][c][d]["TeamsPlayers"][e]["Markets"] = lista
                        with open("./betSettings.json", "w") as f:
                            json.dump(settings, f, indent=4)
                        return lista[-1]
                    else:
                        print(f"{newOption} is already an option")
                elif betMarketOption == len(lista)+2:
                    return None
                else:
                    print(f"The option must be between 1-{len(lista)+2} | Try again")
            elif betMarketOption <=0:
                print(f"The option must be between 1-{len(lista)+2} | Try again")
            else:
                return lista[betMarketOption-1]
        except ValueError:
            print("The option must be a number | Try again")


def validateBetAmount(): #STEP 8
    while True:
        try:
            amount = float(input("Write the bet amount: "))
            if amount > data[activeUser]["wallet"]:
                print(f"The amount typed is more than what you have in your wallet\nYour limit is:{data[activeUser]["wallet"]}")
            elif amount <=0:
                print("The amount cannot be 0 or less")
            else:
                return amount
        except ValueError:
            print("The amount must be a number | Try again ")

def validateBetCuote(): #STEP 9
    while True:
        try:
            cuote = float(input("Write the cuote: "))
            if cuote <1:
                print(f"The cuote can not be less than 1")
            elif cuote ==1:
                print(f"The cuote can not be equal 1")
            else:
                return cuote
        except ValueError:
            print("The cuote must be a number | Try again")

def validateBetResult(): #STEP 10
    lista = ["Win", "Loss", "CashOut", "Cancelled", "To Be Defined"]
    for i, items in enumerate(lista, start=1):
        print(f"{i}. {items}")
    while True:
        try:
            option = int(input(f"Choose an option between 1-{len(lista)}: "))
            if option >len(lista) or option <=0:
                print(f"The option must be between 1-{len(lista)} | Try again")
            else:
                return lista[option-1]
        except ValueError:
            print("The option must be a number | Try again")

def validateBetProfit(a, c, r, au): #STEP 11
    if "wallet" not in data[au]:
        data[au]["wallet"] = 0
    if r == "Win":
        profit = a * c
        data[au]["wallet"] += profit - a
        return profit
    elif r == "Loss":
        profit = 0
        data[au]["wallet"]-= a
        return profit
    elif r == "To Be Defined":
        profit = "TBD"
        return profit
    elif r == "Cancelled":
        profit = "bet cancelled"
        return profit
    else:
        while True:
            try:
                limit = a * c
                amountCashed = int(input("Write the amount cashed: "))
                if amountCashed > limit or amountCashed <0:
                    print(f"The amount cashed cannot be less than 0 or higher than {profit}\nTry again")
                else:
                    profit = amountCashed - a
                    return profit
            except ValueError:
                print(f"The amount cashed must be a number\nTry again")



def saveBet(a, b, c, d, e, f, g, h, i, j, k, l): #STEP 12
    while True:
        betName = input("Write a name for the bet: ").title().strip()
        betNamesList = list(data[activeUser].keys())
        if betName not in betNamesList:
            currentTime = time.localtime()
            formattedTime = time.strftime("%Y-%m-%d", currentTime)
            data[activeUser]["bets"][betName] = {
                    "betType": a,
                    "betDiscipline": b,
                    "betFormat": c,
                    "betCompetitionLeague": d,
                    "betTeamPlayer": e,
                    "betTeamPlayerOption": f,
                    "betMarket": g,
                    "betMarketResult": h,
                    "betAmount": i,
                    "betCuote": j,
                    "betResult": k,
                    "betProfit": l,
                    "betTime": formattedTime

                }
            option=input(f"This is the result:\n{data[activeUser]["bets"][betName]}\nDo you want to save it?\nyes or no: ").strip().lower()
            if option == "yes":
                with open("./data.json", "w") as f:
                    json.dump(data, f, indent=4)
                print("Bet saved")
                return None
            else:
                return None
        else:
            print(f"That name already exist\nTry again")

#/////////////////////////////////////////
#MAIN OPTIONS
def makeBet(au): #OPTION 1
    #add a bet
    print(f"{'Welcome to the main menu':-^60}")

    print(f"{'VALIDATE BET TYPE MENU':-^60}")
    betType=validateBetType(settings) #STEP1
    if betType == None:
        print("Bye bye")

    print(f"{'VALIDATE BET DISCIPLINE MENU':-^60}")
    betDiscipline = validateBetDiscipline(betType) #STEP2
    if betDiscipline== None:
        print("Bye bye")
        return None
    #print(f"{betDiscipline}")

    print(f"{'VALIDATE BET FORMAT MENU':-^60}")
    betFormat = validateBetFormat(betType, betDiscipline)#STEP3
    if betFormat == None:
        print("Bye bye")
        return None
    #print(f"{betFormat}")

    print(f"{'VALIDATE BET COMPETITIONS/LEAGUES MENU':-^60}")
    betCompetitionLeague = validateCompetitionsLeagues(betType, betDiscipline, betFormat)#STEP4
    if betCompetitionLeague == None:
        print("Bye bye")
        return None

    print(f"{'VALIDATE BET TEAM/PLAYER MENU':-^60}")
    betTeamPlayer = validateTeamPlayerBet(betType, betDiscipline, betFormat, betCompetitionLeague)#STEP5
    if betTeamPlayer == None:
        print("Bye bye")
        return None
    
    print(f"{'VALIDATE BET TEAM/PLAYER LIST OPTION MENU':-^60}")
    betTeamPlayerListOption = validateTeamPlayerList(betType, betDiscipline, betFormat, betCompetitionLeague, betTeamPlayer)#STEP6
    if betTeamPlayerListOption == None:
        print("Bye bye")
        return None
    
    print(f"{'VALIDATE BET MARKET MENU':-^60}")
    betMarket = validateBetMarket(betType, betDiscipline, betFormat, betCompetitionLeague, betTeamPlayer) #STEP7
    if betMarket == None:
        print("Bye bye")
        return None

    print(f"{'VALIDATE BET MARKET RESULT MENU':-^60}")
    betMarketResult = input("Write the result chosen: ")
    if betMarketResult == None:
        print("Bye bye")
        return None

    print(f"{'VALIDATE BET AMOUNT MENU':-^60}")
    betAmount = validateBetAmount()
    if betAmount == None:
        print("Bye bye")
        return None

    print(f"{'VALIDATE BET CUOTE MENU':-^60}")
    betCuote = validateBetCuote()
    if betCuote == None:
        print("Bye bye")
        return None

    print(f"{'VALIDATE BET RESULT MENU':-^60}")
    betResult = validateBetResult()
    if betResult == None:
        print("Bye bye")
        return None
    
    print(f"{'VALIDATE BET PROFIT MENU':-^60}")
    betProfit = validateBetProfit(betAmount, betCuote, betResult, au)
    


    print(f"{'VALIDATE THE BET MENU':-^60}")
    saveBet(betType, betDiscipline, betFormat, betCompetitionLeague, betTeamPlayer ,betTeamPlayerListOption, betMarket, betMarketResult, betAmount, betCuote, betResult, betProfit)


def changeBetResult(a):
    lista = list(data[a]["bets"].keys())
    if not lista:
        print("You did not make any bet yet")
        return None
    for i, items in enumerate(lista, start=1):
        print(f"{i}. {items}")
    print(f"{len(lista)+1}. Exit")

    while True:
        try:
            option = int(input("Choose an option: "))
            if option == len(lista)+1:
                return None
            else:
                betName = lista[option-1]
                # la sigo despues, me quede sin bateria
                while True:
                    newResult = validateBetResult()
                    if newResult == data[a]["bets"][betName]["betResult"]:
                        print("Cannot choose the same result | Choose another one")
                    else:
                        break
                data[a]["bets"][betName]["betResult"] = newResult
                validateBetProfit(data[a]["bets"][betName]["betAmount"], data[a]["bets"][betName]["betCuote"], data[a]["bets"][betName]["betResult"], a)
                print(f"Bet after the change:\n{data[a]["bets"][betName]}")
                while True:
                    try:
                        yesno = input(f"Do you want to save it?\nyes or no: ").strip().lower() 
                        if yesno == "yes":
                            with open("./data.json", "w") as f:
                                json.dump(data, f, indent=4)
                            return None
                        else:
                            return None
                    except KeyError:
                        print("Error, try again")   
        except ValueError:
            print(f"The option must be a number\nTry again")

def displayWallet(au):
    print(f"User: {au} - Money Available: {data[au]["wallet"]}")
    return None

def addMoney(au):
    while True:
        print(f"How much money do you want to add?")
        money = float(input("Write the amount: "))
        if money <0:
            print("You cannot add less than 0")
        elif money ==0:
            print("You cannot add 0")
        else:
            data[au]["wallet"] += money
            with open("data.json", "w") as f:
                json.dump(data, f, indent=4)
            return

def withdrawMoney(au):
    while True:
        print(f"How much money do you want to withdraw?")
        money = float(input("Write the amount: "))
        if money <0:
            print("You cannot withdraw less than 0")
        elif money ==0:
            print("You cannot withdraw 0")
        elif money > data[au]["wallet"]:
            print(f"You cannot withdraw more money that you have\nYour limit is: {data[au]["wallet"]}")
        else:
            data[au]["wallet"] -= money
            with open("data.json", "w") as f:
                json.dump(data, f, indent=4)
            return
def walletMenu(au):
    print(f"{'WALLET MENU':-^60}")
    while True:
        print(f"1. SEE YOUR WALLET\n2. Add money\n3. Withdraw money\n4. Exit")
        try:
            menuOption = int(input("Choose between 1-4: "))
            if menuOption >0 or menuOption <=4:
                match menuOption:
                    case 1:
                        print("You have selected the option 1 | SEE YOUR WALLET")
                        displayWallet(au)
                    case 2:
                        print("You have selected the option 2 | ADD MONEY")
                        addMoney(au)
                    case 3:
                        print("You have selected the option 3 | WITHDRAW MONEY")
                        withdrawMoney(au)
                    case 4:
                        print("Back to the main menu")
                        return None
            else:
                print(f"The option must be between 1 - 4\nTry again")
        except ValueError:
            print(f"The option must be a number\nTry again")

def seeAllBets(au):
    names = list(data.get(au, {}).get("bets", {}).keys())
    for i, name in enumerate(names, start=1):
        print(f"{i}. {name}")
    print(f"You made a total of {len(names)}")

def filterBets(au):
    names = list(data.get(au, {}).get("bets", {}).keys())
    while True:
        try:
            startTimeYear = int(input("Write the start year: "))
            startTimeMonth = int(input("Write the start month: "))
            startTimeDay = int(input("Write the start day: "))
            finalTimeYear = int(input("Write the final year: "))
            finalTimeMonth = int(input("Write the final month: "))
            finalTimeDay = int(input("Write the final day: "))
        except ValueError:
            print(" One of the date fields was not a number | Try again")
            continue
        try:
            fechaPiso = datetime.date(startTimeYear, startTimeMonth, startTimeDay)
            fechaPiso = datetime.date(startTimeYear, startTimeMonth, startTimeDay)
            fechaTecho = datetime.date(finalTimeYear, finalTimeMonth, finalTimeDay)
        except ValueError:
            print("One of the date components is out of range | Try again")
            continue
        break
    fechasFiltradas = []
    for betName in names:
        betTimeStr = data[au]["bets"][betName].get("betTime", "")
        try:
            betDate = datetime.datetime.strptime(betTimeStr, "%Y-%m-%d").date()
        except Exception:
            print(f"Error parsing date for bet {betName}, skipping...")
            continue
        if fechaPiso <= betDate <= fechaTecho:
            bet = data[au]["bets"][betName]
            fechasFiltradas.append({
                                    "betName": betName,
                                    "betDate": bet.get("betTime", "N/A"),
                                    "betResult": bet.get("betResult", "N/A"),
                                    "betProfit": bet.get("betProfit", "N/A")
                                })
        if fechasFiltradas:
            print("Bets within the selected time range: ")
            for bet in fechasFiltradas:
                print(f"-{bet['betName']} | {bet['betDate']} | {bet['betResult']} | Profit: {bet['betProfit']}")
        else:
            print("No bets found in that time range")

def deleteBet(au):
    names = list(data[au]["bets"].keys())
    for i, name in enumerate(names, start=1):
        print(f"{i}. {name}")
    while True:
        try:
            option = int(input(f"Choose an option between 1-{len(names)}: "))
            if option > len(names) or option <=0:
                print(f"The option must be between 1-{len(names)}\nTry again")
            else:
                betName = names[option-1]
                confirm = input(f"Are you sure you want to delete the bet {betName}?\nyes or no: ").strip().lower()
                if confirm == "yes":
                    del data[au]["bets"][betName]
                    with open("./data.json", "w") as f:
                        json.dump(data, f, indent=4)
                    print("Bet deleted")
                    return None
                else:
                    print("Bet not deleted")
                    return None
        except ValueError:
            print(f"The option must be a number\nTry again")
            continue
        

def betHistoryMenu(au):
    print(f"{'BET HISTORY MENU':-^60}")
    while True:
        print(f"1. SEE ALL YOUR BETS\n2. FILTER BETS FOR X SPAN TIME\n3. DELETE A BET\n4. EXIT")
        try:
            menuOption = int(input("Choose between 1-4: "))
            names = list(data.get(au, {}).get("bets", {}).keys())
            if menuOption > 0 and menuOption <= 4:
                match menuOption:
                    case 1:
                        print("You have selected the option 1 | SEE ALL YOUR BETS")
                        seeAllBets(au)
                    case 2:
                        print("You have selected the option 2 | FILTER BETS FOR X SPAN TIME")
                        filterBets(au)
                    case 3:
                        print("You have selected the option 3 | DELETE A BET")
                        deleteBet(au)
                        #This is the next step to do, now I do not have time cuz Ive to study for an exam
                    case 4:
                        print("Back to the menu")
                        return
            else:
                print("The option must be between 1-4\nTry again")
        except ValueError:
            print(f"The option must be a number\nTry again")

def statsProfit(au):
    names = list(data[au]["bets"].keys())
    total = 0
    for name in names:
        if data[au]["bets"][name]["betResult"] == "Win" or data[au]["bets"][name]["betResult"] == "Loss" or data[au]["bets"][name]["betResult"] == "CashOut":
            total += data[au]["bets"][name]["betProfit"]
    print(f"Profit: {total}")
    return total

def statsWinrate(au):
    names = list(data[au]["bets"].keys())
    apuestasDefinidas = 0
    wins = 0
    for name in names:
        if data[au]["bets"][name]["betResult"] == "Win" or data[au]["bets"][name]["betResult"] == "Loss":
            apuestasDefinidas+=1
            if data[au]["bets"][name]["betResult"] == "Win":
                wins+=1
    winrate = (wins/apuestasDefinidas) * 100
    print(f"Winrate: {winrate:.2f}%")
    

def statsTotalInvested(au):
    bets = list(data[au]["bets"].keys())
    total = 0
    for bet in bets:
        total += data[au]["bets"][bet]["betAmount"]
    print(f"You invested: {total} during {len(total)}")
    return total

def statsRoi(au):
    profit = statsProfit(au)
    amount = statsTotalInvested(au)
    roi = ((profit-amount)/ amount) * 100
    print(f"Your ROI is: {roi} ")
    return None

def betStatsMenu(au):
    print(f"{'BET STATS MENU':-^60}")
    while True:
        try:
            print(f"1. PROFIT\n2. WINRATE\n3. TOTAL INVESTED\n4. ROI\n5. EXIT")
            menuOption = int(input("Choose between 1-3: "))
            if menuOption > 0 and menuOption <=5:
                match menuOption:
                    case 1:
                        print("You have selected the option 1 | PROFIT")
                        statsProfit(au)
                    case 2:
                        print("You have selected the option 2 | WINRATE")
                        statsWinrate(au)
                    case 3:
                        print("You have selected the option 3 | TOTAL INVESTED")
                        statsTotalInvested(au)
                    case 4:
                        print("You have selected the option 4 | ROI")
                        statsRoi(au)
                    case 5:
                        print("Back to the menu")
                        return
            else:
                print(f"The option must be between 1-3\nTry again")
        except ValueError:
            print(f"The option must be a number\nTry again")

def betDecide():
    print(f"Write your options so we can decide for you\nExamples(YES-NO-1-2)")
    cont=0
    options = []
    while True:
        cont+=1
        print("EXIT to finish")
        option = input(f"Option number {cont}: ").strip().lower()
        if option == "exit":
            break
        else:
            options.append(option)
    index = random.randint(1, len(options))
    result = options[index]
    print(f"The result is: {result}\nBless you whigga")
    return None

#/////////////////////////////
#MAIN MENU
def mainMenu(au):
    print(f"Welcome {au}")
    print(f"{'BET ANALYTICS MENU':-^60}")
    while True:
        print(f"1. MAKE A BET\n2. CHANGE BET RESULT\n3. GO TO WALLET\n4. BET HISTORY\n5. BET STATS\n6. BET DECIDE\n7. EXIT")
        try:
            menuOption = int(input("Choose between 1-n: "))
            if menuOption >0 and menuOption <=7:
                match menuOption:
                    case 1:
                        print("You have selected the option 1 | MAKE A BET")
                        makeBet(au)
                    case 2:
                        print("You have selected the option 2 | CHANGE BET RESULT")
                        changeBetResult(au)
                    case 3:
                        print("You have selected the option 3 | GO TO WALLET")
                        walletMenu(au)
                    case 4:
                        print("You have selected the option 4| BET HISTORY")
                        betHistoryMenu(au)
                    case 5:
                        print("You have selected the option 5 | BET STATS")
                        betStatsMenu(au)
                    case 6:
                        print("You have selected the option 6 | BET DECIDE")
                        betDecide()
                    case 7:
                        saveAll()
                        backupData()
                        print("CLOSING...")
                        return None
            else:
                print(f"The option must be between 1 - n\nTry again")
        except ValueError:
            print(f"The option must be a number\nTry again")

mainMenu(activeUser)