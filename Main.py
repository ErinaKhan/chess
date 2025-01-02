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
pixelWidth = 5
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
                clear()
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
        pieceImage = piece(pieceSelected[0],pieceSelected[1])
        movePiece(pieceImage, pieceSelected, colour)

def hasWon(): # code stub
    # someone wins if isInCheck() == True and kingMoves() == []
    return False

def pieceType(pieceSelected):
    # returns a string that contains the type of piece it is
    # examples are things such as 'rook', 'pawn', 'queens'
    if pieceSelected in ['♟','♙']:
        return "Pawn"
    elif pieceSelected in ['♞','♘']:
        return "Horse"
    elif pieceSelected in ['♝','♗']:
        return "Bishop"
    elif pieceSelected in ['♜','♖']:
        return "Rook"
    elif pieceSelected in ['♛','♕']:
        return "Queen"
    elif pieceSelected in ['♚','♔']:
        return "King"
    pass
                
def validMoves(pieceSelected, whereFrom):
    # returns all valid moves the piece can do
    moveType = pieceType(pieceSelected)
    moves = []

    print(moveType)
    print(whereFrom)
    if moveType == "Pawn":
        moves = pawnMoves(whereFrom)
    elif moveType == "Horse":
        moves = horseMoves(whereFrom)
    elif moveType == "Bishop":
        moves = bishopMoves(whereFrom)
    elif moveType == "Rook":
        moves = rookMoves(whereFrom)
    elif moveType == "King":
        moves = kingMoves(whereFrom)
    elif moveType == "Queen":
        moves = bishopMoves(whereFrom) + rookMoves(whereFrom)
    else:
        print("An error has occured")
        print(f"piece of type {moveType} not recognised")

    print(moves) 
    input()
    return moves

def pawnMoves(start):
    moves = []
    onespace = (start[0] - 1,start[1])

    if not headbutts(onespace) and not outOfBounds(onespace):
        moves = moves + [onespace]
    
    if start[0] == 6: 
        # the pawn can move a max of two spaces forwards 
        twospace = (start[0] - 2,start[1])
        
        if not headbutts(twospace) and not headbutts(onespace) and not outOfBounds(twospace):
            moves = moves + [twospace]

    return moves

def horseMoves(start):
    p1 = (start[0] - 2,start[1] + 1)
    p2 = (start[0] - 2,start[1] - 1)
    p3 = (start[0] + 2,start[1] + 1)
    p4 = (start[0] + 2,start[1] - 1)
    p5 = (start[0] + 1,start[1] + 1)
    p6 = (start[0] + 1,start[1] - 1)
    p7 = (start[0] + 1,start[1] + 1)
    p8 = (start[0] + 1,start[1] - 1)
    fullSet = [p1,p2,p3,p4,p5,p6,p7,p8]
    moves = []

    for i in fullSet:
        if not headbutts(i) and not outOfBounds(i):
            moves = moves + [i]

    return moves

def rookMoves(start):
    # finds all horizontal moves first
    # then finds all vertical moves 

    i = start[1]
    moves = []

    while True:
        i = i + 1
        point = (start[0],i)
        if headbutts(point) or outOfBounds(point):
            break
        else:
            moves = moves + [point]

    i = start[1]
            
    while True:
        i = i - 1
        point = (start[0],i)
        if headbutts(point) or outOfBounds(point):
            break
        else:
            moves = moves + [point]

    i = start[0]

    while True:
        i = i + 1
        point = (i,start[1])
        if headbutts(point) or outOfBounds(point):
            break
        else:
            moves = moves + [point]

    i = start[0]

    while True:
        i = i - 1
        point = (i,start[1])
        if headbutts(point) or outOfBounds(point):
            break
        else:
            moves = moves + [point]
        
    return moves

def bishopMoves(start):
    moves = []
    point = (start[0] - 1,start[1] + 1)
    while True:
        if headbutts(point) or outOfBounds(point):
            break
        moves = moves + [point]
        point = (point[0] - 1,point[1] + 1)

    point = (start[0] + 1,start[1] + 1)
    while True:
        if headbutts(point) or outOfBounds(point):
            break
        moves = moves + [point]
        point = (point[0] + 1,point[1] + 1)

    point = (start[0] + 1,start[1] - 1)
    while True:
        if headbutts(point) or outOfBounds(point):
            break
        moves = moves + [point]
        point = (point[0] + 1,point[1] - 1)

    point = (start[0] - 1,start[1] - 1)
    while True:
        if headbutts(point) or outOfBounds(point):
            break
        moves = moves + [point]
        point = (point[0] - 1,point[1] - 1)

    return moves

def kingMoves(start):
    p1 = (start[0] + 1,start[1])
    p2 = (start[0] - 1,start[1])
    p3 = (start[0],start[1] + 1)
    p4 = (start[0],start[1] + 1)
    p5 = (start[0] + 1,start[1] + 1)
    p6 = (start[0] - 1,start[1] + 1)
    p7 = (start[0] + 1,start[1] - 1)
    p8 = (start[0] - 1,start[1] - 1)
    fullSet = [p1,p2,p3,p4,p5,p6,p7,p8]
    moves = []

    for i in fullSet:
        if not headbutts(i) and not outOfBounds(i):
            moves = moves + [i]

    return moves

def headbutts(coordinates):
    try:
        return piece(coordinates[0],coordinates[1]) != " "
    except:
        return True

def movePiece(pieceSelected, whereFrom, pieceColour):
    print("you selected " + pieceSelected + " " + chr(whereFrom[1] + 65) + str(8 - whereFrom[0]))
    moves = validMoves(pieceSelected,whereFrom)
    validInput = False
    canMoveToLocation = False

    while not validInput or not canMoveToLocation:
        userInput = input("\nEnter a valid coordinate on the chess board to move your piece too: ")
        validInput = len(userInput) == 2 and userInput[0].lower() in ['a','b','c','d','e','f','g','h'] and userInput[1] in ['1','2','3','4','5','6','7','8']
        
        if validInput:
            location = (8 - int(userInput[1]), ord(userInput[0].upper()) - 65) 
        
            canMoveToLocation = location in moves

    print(f"can move to location: {userInput}")
    input()

def isInCheck():
    # returns true or false
    pass

def outOfBounds(coordinates):
    return coordinates[0] < 0 or coordinates[0] > 7 or coordinates[1] < 0 or coordinates[1] > 7

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
            if index == 0:
                clear()
                startGame()
            else:
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

def setSquare(x,y,new):
    global board
    board[x][y] = new

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

    if resigning:
        return "resigning"
    else:
        return x,y

####################################################################################
######################################## UI ########################################
####################################################################################

def moveOverlay(selectedPiece):
    # a ui that overlays X's over the board in the spots where the currently selected piece can move
    pass

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
print((1,2) == (1,2))
print((1,2) == (1,3))
print((1,2) in [(1,2)])
print((1,2) in [(1,3)])
print((3,2) in [(5,2),(4,2)])
mainMenu()