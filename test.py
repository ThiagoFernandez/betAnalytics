import json

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
            "Esport": {"Options": {},"Detalle":{} }
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


def validateBetType(diccionario):
    keys=list(diccionario.keys())
    print(keys)
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
            
def validateBetDiscipline(a):
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
                            settings[a]["Detalle"][newOption] = {"Competitions": [], "Leagues": [], "Markets":[]}
                            break
                        elif hasCompetitionsLeagues == "no":
                            settings[a]["Detalle"][newOption] = {"Markets":[]}
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
                        settings[a]["Detalle"][newDiscipline] = {"Competitions": [], "Leagues": [], "Markets": []}
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

def validateBetFormat(a, b):
    lista = list(settings[a]["Detalle"][b].keys())
    for i, items in enumerate(lista[:-1], start=1):
        print(f"{i}. {items}")
    print(f"{len(lista[:-1])+1}. Exit")

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

def validateCompetitionsLeagues(a, b, c):
    lista = settings[a]["Detalle"][b][c]
    if not lista:
        print(f"1. Add\n2. Exit")
        while True:
            try:
                option = int(input("Choose an option between 1-2: "))
                if option ==1:
                    newOption=input("Write the new option: ").title().strip()
                    lista.append(newOption)
                    settings[a]["Detalle"][b][c] = lista
                    with open("./betSettings.json", "w") as f:
                        json.dump(settings, f, indent=4)
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
                            lista.append(newOption)
                            settings[a]["Detalle"][b][c] = lista
                            with open ("./betSettings.json", "w") as f:
                                json.dump(settings, f, indent=4)
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
                    return lista[competitionLeagueOption]

            except ValueError:
                print("The option must be a number | Try again")



def validateBetMarket(a, b):
    lista = settings[a]["Detalle"][b]["Markets"]
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
                        settings[a]["Detalle"][b]["Markets"] = lista
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
                return lista[betMarketOption]
        except ValueError:
            print("The option must be a number | Try again")

def saveBet(a, b, c, d, e):
    result = {
        "betType": a,
        "betDiscipline": b,
        "betFormat": c,
        "betCompetitionLeague": d,
        "betMarket": e
    }
    option=input(f"This is the result:\n{result}\,Do you want to save it?\nyes or no: ").strip().lower()
    if option == "yes":
        with open("./data.json", "w") as f:
            json.dump(result, f, indent=4)
        print("Bet saved")
        return None


def mainMenu():
    #add a bet
    print(f"{'Welcome to the main menu':-^60}")

    betType=validateBetType(settings)
    if betType == None:
        print("Bye bye")

    betDiscipline = validateBetDiscipline(betType)
    if betDiscipline== None:
        print("Bye bye")
        return None
    print(f"{betDiscipline}")

    betFormat = validateBetFormat(betType, betDiscipline)
    if betFormat == None:
        print("Bye bye")
        return None
    print(f"{betFormat}")

    betCompetitionLeague = validateCompetitionsLeagues(betType, betDiscipline, betFormat)
    if betCompetitionLeague == None:
        print("Bye bye")
        return None

    print(f"{settings[betType]["Detalle"][betDiscipline][betFormat]}")
    betMarket = validateBetMarket(betType, betDiscipline)
    if betMarket == None:
        print("Bye bye")
        return None
    saveBet(betType, betDiscipline, betFormat, betCompetitionLeague, betMarket)
    
mainMenu()