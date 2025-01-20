import keyboard
import Engine
import math

from os import system, name
from time import sleep
def clear():
   # for windows
   if name == 'nt':
      _ = system('cls')

   # for mac and linux
   else:
      _ = system('clear')

# actual size of board (8x8) 64 squares total
boardWidth = 8
boardHeight = 8

# used for the sizing of the ui on screen measured in characters
pixelWidth = 5
pixelHeight = 1

def padding(): # to be wrapped around the pieces in the squares so the pieces are perfectly centred on the x axis
    return (pixelWidth) * " "

def line(lineType): 
    # always returns a string
    # this is a function that can display different types of lines based on the parameter lineType
    # accepted parameters are 0, top, padding and if any other input is inputed it will return a simple line
    # all parameters are shown visually below
    # 'padding' parameter is used to centre the peice on the y axis
    #
    #  ------- <- 0 and the else clause
    #  |     | <- 'padding' 
    #  |     |
    #  |     | <- 'padding'
    #  ------- <- 0 and else clause
    #
    # the only difference between 0 and the else clause is wether the line should start on the next line or current line
    # only the first line of the board uses the 0 input into the function
    
    if lineType == 0:
        print(("  " +(((pixelWidth * 2) + 3) * "-") * boardWidth)[:-7],end = "")
        
    elif lineType == "top": # gets the alphabet at the top of the board            
        print("  ", end="")
        for i in range(boardWidth):
            print(" " + padding() + chr(i+65) + padding(),end="")
        print("\n",end="")
        
    elif lineType == "padding":
        print("\n  |" + (padding() + " " + padding() + "|") * boardWidth, end = "")
        
    else:
        print(("\n  " + (((pixelWidth * 2) + 3) * "-") * boardWidth)[:-7],end = "")
        
def fillSquare(): # padding for the inside of the squares
    for i in range(pixelHeight):
        line("padding")

def createOverlay(moves):
    overlay = []
    for move in moves:
        overlay = overlay + [move[1]]
    return overlay

def drawBoard(overlay): # need to have an overlay variable with a list of moves to draw X's on
    line("top")
    for rank in range(boardHeight):
        line(rank)
        fillSquare()
        print(f"\n{8 - rank} |", end = "")
        for file in range(boardWidth):
            currentSquareIndex = (rank * 8) + file
            squareBinary = int(math.pow(2,currentSquareIndex))
            colour = str(Engine.getColour(squareBinary))
            piece = str(Engine.getPieceTypeFromSquare(squareBinary))
            if overlay != None:
                if currentSquareIndex in overlay:
                    print(f"{padding()}X{padding()}|", end = "")
                else:
                    print(f"{padding()}{Engine.pieceLookup[colour+piece]}{padding()}|", end = "")
            else:
                print(f"{padding()}{Engine.pieceLookup[colour+piece]}{padding()}|", end = "")
        fillSquare()
    line(1)

def generateMenu(textOptions):
    # input an array of options
    # returns the index of the chosen option
    currentIndex = 0
    maxIndex = len(textOptions)
    while True:
        clear()
        for option in range(maxIndex):
            if option == currentIndex:
                print(f"{textOptions[option]} <")
            else:
                print(f"{textOptions[option]}")
        if keyboard.read_key() == "enter":
            break
        if keyboard.read_key() == "up" and currentIndex > 0:
            currentIndex = currentIndex - 1
        elif keyboard.read_key() == "down" and currentIndex + 1 < maxIndex:
            currentIndex = currentIndex + 1
    
    return currentIndex

def askForPromotePiece():
    valid = False
    pieces = ["BISHOP","HORSE","ROOK","QUEEN"]
    while not valid:
        pieceToBecome = input("\n\nPick a piece for your PAWN to promote too (type: rook,horse,bishop or queen): ").upper()    
        for i in range(len(pieces)):
            if pieceToBecome == pieces[i]:
                valid = True
                return pieceToBecome
            
def load():
    for x in range(2):
        for i in range(4):
            print("loading" + ("." * i))
            sleep(0.5)
            clear()

def starterGameInfo(colour):
    clear()
    sleep(0.8)
    if colour == "WHITE":
        print(" __   __                __        ___     _ _       ")
        print(" \\ \\ / /__  _   _ _ __  \\ \\      / / |__ (_) |_ ___ ")
        print("  \\ V / _ \\| | | | '__|  \ \\ /\\ / /| '_ \\| | __/ _ \\")
        print("   | | (_) | |_| | |      \ V  V / | | | | | ||  __/")
        print("   |_|\\___/ \\__,_|_|       \\_/\\_/  |_| |_|_|\\_\\____|")
    else:
        print(" __   __                 ____  _            _    ")
        print(" \\ \\ / /__  _   _ _ __  | __ )| | __ _  ___| | __")
        print("  \\ V / _ \\| | | | '__| |  _ \\| |/ _` |/ __| |/ /")
        print("   | | (_) | |_| | |    | |_) | | (_| | (__|   < ")
        print("   |_|\\___/ \\__,_|_|    |____/|_|\\__,_|\\___|_|\\_\\")

    while keyboard.read_key() != "enter":
        pass

    clear()
    
def checkmateUI():
    print("   ____ _               _      __  __       _         _ ")
    print("  / ___| |__   ___  ___| | __ |  \\/  | __ _| |_ ___  | |")
    print(" | |   | '_ \\ / _ \\/ __| |/ / | |\\/| |/ _` | __/ _ \\ | |")
    print(" | |___| | | |  __/ (__|   <  | |  | | (_| | ||  __/ |_|")
    print("  \\____|_| |_|\\___|\\___|_|\\_\\ |_|  |_|\\__,_|\\__\\___| (_)")

def winLossUI(hasWon):
    checkmateUI()
    print("\n")

    if hasWon:
        print(" __   __           __        ___         _ ")
        print(" \\ \\ / /__  _   _  \\ \\      / (_)_ __   | |")
        print("  \\ V / _ \\| | | |  \\ \\ /\\ / /| | '_ \\  | |")
        print("   | | (_) | |_| |   \\ V  V / | | | | | |_|")
        print("   |_|\\___/ \\__,_|    \\_/\\_/  |_|_| |_| (_)")
    else:
        print(" __   __            _              _     _ ")
        print(" \\ \\ / /__  _   _  | |    ___  ___| |_  | |")
        print("  \\ V / _ \\| | | | | |   / _ \\/ __| __| | |")
        print("   | | (_) | |_| | | |__| (_) \\__ \\ |_  |_|")
        print("   |_|\\___/ \\__,_| |_____\\___/|___/\\__| (_)")

def stalemateUI():
    print("  ____  _        _                      _         _ ")
    print(" / ___|| |_ __ _| | ___ _ __ ___   __ _| |_ ___  | |")
    print(" \\___ \\| __/ _` | |/ _ \\ '_ ` _ \\ / _` | __/ _ \\ | |")
    print("  ___) | || (_| | |  __/ | | | | | (_| | ||  __/ |_|")
    print(" |____/ \\__\\__,_|_|\\___|_| |_| |_|\\__,_|\\__\\___| (_)")

def mainMenuUI():
    print("----------------------------------------------------------------")
    print("----------------------------------------------------------------")
    print("----------------------------------------------------------------")
    print("|                    ____ _  _ ____ ____ ____                  |")
    print("|                    |    |__| |___ [__  [__                   |")
    print("|                    |___ |  | |___ ___] ___]                  |")
    print("|                                                              |")
    print("----------------------------------------------------------------")
    print("----------------------------------------------------------------")
    print("----------------------------------------------------------------")
    print("|                                                     _:_      |")
    print("|                                                    '-.-'     |")
    print("|                                           ()      __.'.__    |")
    print("|                                        .-:--:-.  |_______|   |")
    print("|                                 ()      \____/    \=====/    |")
    print("|                                 /\      {====}     )___(     |")
    print("|                      (\\=,      //\\\\      )__(     /_____\\    |")
    print("|      __    |'-'-'|  //  .\\    (    )    /____\\     |   |     |")
    print("|     /  \\   |_____| (( \\_  \\    )__(      |  |      |   |     |")
    print("|     \\__/    |===|   ))  `\\_)  /____\\     |  |      |   |     |")
    print("|    /____\\   |   |  (/     \\    |  |      |  |      |   |     |")
    print("|     |  |    |   |   | _.-'|    |  |      |  |      |   |     |")
    print("|     |__|    )___(    )___(    /____\\    /____\\    /_____\\    |")
    print("|    (====)  (=====)  (=====)  (======)  (======)  (=======)   |")
    print("|    }===={  }====={  }====={  }======{  }======{  }======={   |")
    print("|   (______)(_______)(_______)(________)(________)(_________)  |")
    print("----------------------------------------------------------------")
    print("----------------------------------------------------------------")
    print("----------------------------------------------------------------")
    print("----------------------------------------------------------------")
    print("--------------------- press ENTER to start ---------------------")
    print("----------------------------------------------------------------")
    print("----------------------------------------------------------------")
    print("----------------------------------------------------------------")
    while keyboard.read_key() != "enter":
        if keyboard.read_key() == "esc" or keyboard.read_key() == "backspace":
            return False
    return True