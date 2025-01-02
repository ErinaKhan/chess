####################################################################################
#################################### CHESS GAME ####################################
####################################################################################

#-------------------------------------- SETUP --------------------------------------
import keyboard

import AI_engine as AI
import File_handler as FileHandler

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

whitePieces = ['♜','♞','♝','♛','♚','♟']
blackPieces = ['♖','♘','♗','♕','♔','♙']

#------------------------------------ FUNCTIONS ------------------------------------

def startGame():
    
    # main loop of program
    global board
    
    colour,playerTurn,TurnNumber,newBoard = FileHandler.load(FileHandler.gameConfig()) # loads new game or previous game

    board = newBoard

    print(f"\nYour colour is {colour}!\n")
    print("isYourTurn: " + str(playerTurn) + "\nTurnNumber: " + str(TurnNumber) + "\n")
    
    printBoard(colour)

    resigning = False

    while True:

        if playerTurn:
            resigning = playersTurn(colour)
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

def playersTurn(colour): # code stub
    
    pieceSelected = selectPiece(colour) # will return coordinates of piece to move or a message saying the players 'resigning'

    if pieceSelected == "resigning":
        print("resigning...")
        sleep(2)
        return True
    else:
        print("you selected " + piece(pieceSelected[0],pieceSelected[1]))
        sleep(1)
        movePiece()

def hasWon(): # code stub
    return False

def pieceType():
    # returns a string that contains the type of piece it is
    # examples are things such as 'rook', 'pawn', 'queens'
    pass

def canMove(pieceToMove, location):
    # returns true or false
    pass
                
def validMove(whereToo, whereFrom):
    # returns true or false
    # checks if the piece can move to the location given
    pass 

def movePiece(whereToo, whereFrom):
    pass

def isInCheck():
    # returns true or false
    pass

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
    # returns a string of the piece ASCII or a blank space " "
    return board[x][y]

def selectPiece(colour):
    # returns 'resigning' or the x and y coordinates of selected piece 

    x = -1
    y = -1

    userInput = ""

    #-----------------------
    # flags for valid input
    #-----------------------
    validMove = False
    resigning = False
    isValidPiece = False
    playerWhite = True
    #-----------------------

    if colour == "Black":
        playerWhite = False

    while (not validMove or not isValidPiece) and not resigning:
        clear()
        printBoard(colour)
        userInput = str(input("\n\nEnter the coordinates on the chess board (such as A8,a8,b5 etc...) of the piece you would like to move or type 'resign' to resign\n\nInput: "))

        validMove = len(userInput) == 2 and userInput[0].lower() in ['a','b','c','d','e','f','g','h'] and userInput[1] in ['1','2','3','4','5','6','7','8']
        resigning = userInput.lower() == "resign"
    
        if validMove and not resigning:
            x = 8 - int(userInput[1])
            y = ord(userInput[0].lower()) - 97

            isBlack = piece(x,y) in blackPieces
            isWhite = piece(x,y)  in whitePieces

            isValidPiece = (isBlack and not playerWhite) or (isWhite and playerWhite)

            if not isValidPiece: 
                print("\nCan only select one of your pieces")
                sleep(1)

    print("valid!")
    sleep(1)
    if resigning:
        return "resigning"
    else:
        return x,y


####################################################################################
######################################## UI ########################################
####################################################################################

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
mainMenu()