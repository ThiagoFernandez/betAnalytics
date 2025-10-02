import random, json, time

#Funciones
def handleBetType(place):
    while True:
        dic = settings[place]
        keys = list(dic.keys())

        for i, k in enumerate(keys, start=1):
            print(f"{i}. {k}")
        print(f"{len(keys)+1}. Add")
        print(f"{len(keys)+2}. Exit")

        try:
            option = int(input(f"Choose 1-{len(keys)+2}: "))

            if 1 <= option <= len(keys):  # opción válida
                return keys[option-1]

            elif option == len(keys)+1:   # Add
                newOption = input("Choose a new option: ").strip().title()
                if newOption in keys:
                    print("Already exists")
                else:
                    dic[newOption] = {}
                    with open("./betSettings.json", "w") as f:
                        json.dump(settings, f, indent=4)
                    print(f"Added {newOption}")
                    return newOption

            elif option == len(keys)+2:   # Exit
                return None

            else:
                print(" Invalid option")

        except ValueError:
            print(" Must be a number")

def handleBetTypeDecision(decision):
    while True:
        dic = settings["betTypeList"][decision]
            


#case 1
def betAdder():
    print(f"{'Welcome to the bet adder':-^60}")
    betType = handleBetType("betTypeList")
    if betType == None:
        print("Back to the menu")
        return None
    else:
        typeBet = settings["betTypeList"][betType]["Options"]
        print(typeBet)
    

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
            "Sport": {},
            "Esport": {}
        }
    }
    with open("./betSettings.json", "w") as f:
        json.dump(settings, f, indent=4)
except json.JSONDecodeError:
    print("Empty file, starting...")
    settings = {
        "betTypeList": {
            "Sport": {},
            "Esport": {}
        }
    }
    


#Main Menu
opciones = ["Add a bet", "Search a bet", "Blacklist", "greenlist", "Bet history", "founds", "statistics", "exit"]

while True:
    for i, items in enumerate(opciones, start=1):
        print(f"{i}. {items}")
    try:
        option = int(input(f"Choose an option between 1-{len(opciones)}: "))
        if option > len(opciones) or option <=0:
            print(f"The option must be between 1-{len(opciones)}\nTry again")
        else:
            break
    except ValueError:
        print(f"The option must be a number\nTry again")
    


match option:
    case 1:
        betAdder()
    case 2:
        print(f"Welcome to the bet searcher")
    case 3:
        print(f"Welcome to the blacklist")
    case 4:
        print(f"Welcome to the greenlist")
    case 5:
        print(f"Welcome to the bet history")
    case 6:
        print(f"Welcome to your founds")
    case 7:
        print(f"Welcome to the statistics")
    case 8:
        print("exit")