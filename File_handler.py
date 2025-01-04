import keyboard
import random
from os import system, name
from time import sleep

def clear():
   # for windows
   if name == 'nt':
      _ = system('cls')

   # for mac and linux
   else:
      _ = system('clear')

def load(gameType):
    # returns all variables needed by main to run the game
    # colour -> the players colour in the game "White" or "Black"
    # playerTurn -> boolean value 
    # TurnNumber -> is 1 unless the game is loaded from an already started game where it may be different
    # board -> 2d array 
    # the parameter gameType holds all of the settings for the game and will be expanded in the future as gameConfig() grows
    colour = None
    playerTurn = None
    board = None

    if gameType == "new":
        
        board,colour,playerTurn = boardSetup(giveRandomColour())
    elif gameType == "old": # loading a previously played unfinished game or a game from FEN notation
        pass
    elif gameType == "FEN":
        board,colour,playerTurn = FENBoard(getFEN())
    
    return colour,playerTurn,board

def gameConfig():
    # returns the settings for the game as a string
    
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
                b1 = "<"
                b2 = " "
                sleep(1)
                while True:
                    clear()
                    print(f"New Game {b1}")
                    print(f"Load Game from FEN {b2}")
                    if keyboard.read_key() == "enter":
                        clear()
                        if index == 0:
                            return "new"
                        else:
                            return "FEN"
                    elif keyboard.read_key() == "up" and index == 1:
                        index = 0
                        b1 = "<"
                        b2 = " " 
                    elif keyboard.read_key() == "down" and index == 0:
                        index = 1
                        b1 = " "
                        b2 = "<"
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

def boardSetup(playerColour): 
    # returns a 2d array 
    # flips the board depending on what pieces the player has
    board = None
    if playerColour == "WHITE":
        data = FENBoard("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        return data[0],"WHITE",True
    else:
        data = FENBoard("RNBQKBNR/PPPPPPPP/8/8/8/8/pppppppp/rnbqkbnr w KQkq - 0 1")
        return data[0],"BLACK",True

FENlookup = {
    "r": "♖",
    "n": "♘",
    "b": "♗",
    "q": "♕",
    "k": "♔",
    "p": "♙",
    "R": "♜",
    "N": "♞",
    "B": "♝",
    "Q": "♛",
    "K": "♚",
    "P": "♟",
}

def validFEN(fen):
    return fen.count('/') == 7

def getFEN():
    sleep(2)
    fen = ""
    while not validFEN(fen):
        clear()
        fen = input("Enter a valid FEN string in the space below\n\ninput: ")
    return fen

def FENBoard(fenString):
    
    # https://en.wikipedia.org/wiki/Forsyth–Edwards_Notation for more info
    allInfo = fenString.split(' ')
    boardData = allInfo[0].split("/")
    whosTurn = allInfo[1]
    canCastle = allInfo[2]
    enPassant = allInfo[3]
    halfMoves = allInfo[4]
    fullMoves = allInfo[5]

    if whosTurn == "w":
        whosTurn = "WHITE"
    else:
        whosTurn = "BLACK"

    board = [[' ',' ',' ',' ',' ',' ',' ',' '],
             [' ',' ',' ',' ',' ',' ',' ',' '],
             [' ',' ',' ',' ',' ',' ',' ',' '],
             [' ',' ',' ',' ',' ',' ',' ',' '],
             [' ',' ',' ',' ',' ',' ',' ',' '],
             [' ',' ',' ',' ',' ',' ',' ',' '],
             [' ',' ',' ',' ',' ',' ',' ',' '],
             [' ',' ',' ',' ',' ',' ',' ',' ']]

    for i in range(len(boardData)):
       actualIndex = 0
       for j in range(len(boardData[i])):
        
            if boardData[i][j] in ['1','2','3','4','5','6','7','8']:
                numOfTimes = int(boardData[i][j])
                for x in range(numOfTimes):
                    board[i][actualIndex + x] = ' ' 
                actualIndex = actualIndex + numOfTimes - 1
            else:
                piece = FENlookup[boardData[i][j]]
                board[i][actualIndex] = piece
            
            actualIndex = actualIndex + 1

    return board,whosTurn,True

def giveRandomColour():
    if random.randint(0,1) == 0:
        return "WHITE"
    else:
        return "BLACK"
        
def gamesAvailable():
    # returns a string with either 'No games found' or 'N games found' where N is the number of games
    # will show player how many games they have on going
    return "No games found"

