####################################################################################
#################################### CHESS GAME ####################################
####################################################################################

#-------------------------------------- SETUP --------------------------------------
import keyboard
import random
import AI_engine as AI

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
pixelWidth = 4
pixelHeight = 1

#------------------------------------ FUNCTIONS ------------------------------------

def startGame():
    
    # main loop of program
    
    colour,playerTurn,TurnNumber = load(gameConfig()) # loads new game or previous game

    print(f"\nYour colour is {colour}!\n")

    print("isYourTurn: " + str(playerTurn) + "\nTurnNumber: " + str(TurnNumber) + "\n")
    
    printBoard(colour)

    resigning = False

    while True:
        
        print(playerTurn)
        sleep(2)

        if playerTurn:
            resigning = playersTurn()
        else:
            AI.AITurn()
        
        printBoard(colour)
        
        if hasWon():

            if playerTurn:
                print("You Won")
            else:
                print("You Lost, Better luck next time!")
                
            print("\n\nReturning To Menu...")
            clear()
            startGame()

        else:
            if resigning:
                print("thanks for playing!!")
                break
            elif playerTurn:
                playerTurn = False
            else:
                playerTurn = True
            
        
def load(gameType):
    colour = None
    playerTurn = None
    TurnNumber = None
    
    if gameType == "new":
        
        colour = giveRandomColour()
        playerTurn = False
        TurnNumber = 1
        
        if colour == "White":
            playerTurn = True
            
        boardSetup(colour)
    else: # loading a previously played unfinished game
        pass
    
    return colour,playerTurn,TurnNumber

def gameConfig():
    index = 0
    b1 = "<"
    b2 = " "
    sleep(1)
    while True:
        print(f"New Game {b1}")
        print(f"Load Game ({gamesAvailable()}) {b2}")
        
        if keyboard.read_key() == "enter":
            clear()
            if index == 0:
                return "new"
            else:
                return "old"
        elif keyboard.read_key() == "up" and index == 1:
            index = 0
            b1 = "<"
            b2 = " " 
        elif keyboard.read_key() == "down" and index == 0:
            index = 1
            b1 = " "
            b2 = "<"
        clear()

def playersTurn(): # code stub
    isResigning = playerOptionsUI()
    if isResigning == "resign":
        return True
    else:
        return False

def hasWon(): # code stub
    return False

def boardSetup(playerColour): # needs to flip the board depending on what pieces the player has
    global board
    if playerColour == "White":
        board = [['♖','♘','♗','♕','♔','♗','♘','♖'],
                 ['♙','♙','♙','♙','♙','♙','♙','♙'],
                 [' ',' ',' ',' ',' ',' ',' ',' '],
                 [' ',' ',' ',' ',' ',' ',' ',' '],
                 [' ',' ',' ',' ',' ',' ',' ',' '],
                 [' ',' ',' ',' ',' ',' ',' ',' '],
                 ['♟','♟','♟','♟','♟','♟','♟','♟'],
                 ['♜','♞','♝','♛','♚','♝','♞','♜']]
    else:
        board = [['♜','♞','♝','♛','♚','♝','♞','♜'],
                 ['♙','♙','♙','♙','♙','♙','♙','♙'],
                 [' ',' ',' ',' ',' ',' ',' ',' '],
                 [' ',' ',' ',' ',' ',' ',' ',' '],
                 [' ',' ',' ',' ',' ',' ',' ',' '],
                 [' ',' ',' ',' ',' ',' ',' ',' '],
                 ['♟','♟','♟','♟','♟','♟','♟','♟'],
                 ['♖','♘','♗','♕','♔','♗','♘','♖']]
                
    
def gamesAvailable(): # code stub
    # will show player how many games they have on going
    return "No games found"

def movePiece(whereToo, whereFrom):
    pass
    
def giveRandomColour():
    if random.randint(0,1) == 0:
        return "White"
    else:
        return "Black"
        
def mainMenu():
    index = 0
    b1 = "<"
    b2 = " "
    while True:
        mainMenuUI()
        print(f"------------------------  Play game    {b1} -----------------------")
        print(f"------------------------  Exit game    {b2} -----------------------")
        print("----------------------------------------------------------------")
        print("------------------------enter to select-------------------------")
        print("----------------------------------------------------------------")
    
        if keyboard.read_key() == "enter":
            clear()
            startGame()
            break
        elif keyboard.read_key() == "up" and index == 1:
            index = 0
            b1 = "<"
            b2 = " "
        elif keyboard.read_key() == "down" and index == 0:
            index = 1
            b1 = " "
            b2 = "<"
        clear()

def piece(x,y):
    return board[x][y]

####################################################################################
######################################## UI ########################################
####################################################################################

def playerOptionsUI():
    userInput = ""
    validMove = False
    resigning = False

    while not validMove and not resigning:
        userInput = str(input("\ntype a coordinate on the chess board (such as A8,a8,b5 etc...) of the piece you would like to move or 'resign' to resign\n\nInput: "))

        # the two different flags for inputs
        validMove = len(userInput) == 2 and userInput[0].lower() in ['a','b','c','d','e','f','g','h'] and userInput[1] in ['1','2','3','4','5','6','7','8']
        resigning = userInput.lower() == "resign"

    return userInput

def info():
    pass

def padding(): # to be wrapped around the pieces in the squares so the pieces are perfectly centred on the x axis
    return (pixelWidth) * " "

def line(lineType): 
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
    
def printBoard(playerColour):
    line("top")
    for x in range(boardHeight):
        line(x)
        fillSquare()
        print(f"\n{8 - x} |", end = "")
        for y in range(boardWidth):
            print(f"{padding()}{piece(x,y)}{padding()}|", end = "")
        fillSquare()
    line(1)

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

clear()
AI.info()
mainMenu()