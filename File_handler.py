import random
import UI_Handler as UI

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
    UI.sleep(1)
    option = UI.generateMenu(["New Game","Load Game"])

    if option == 0:
        UI.sleep(1)
        option = UI.generateMenu(["New Game", "Load game from FEN"])
        if option == 0: 
            return "new"
        else:
            return "FEN"
    else:
        return "old"
    
def boardSetup(playerColour): 
    # returns a 2d array 
    # flips the board depending on what pieces the player has
    if playerColour == "WHITE":
        data = FENBoard("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        return data[0],"WHITE",True
    else:
        data = FENBoard("RNBQKBNR/PPPPPPPP/8/8/8/8/pppppppp/rnbqkbnr b KQkq - 0 1")
        return data[0],"BLACK",False

def validFEN(fen):
    return fen.count('/') == 7

def getFEN():
    UI.sleep(2)
    fen = ""
    while not validFEN(fen):
        UI.clear()
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
    playerTurn = False

    if whosTurn == "w":
        whosTurn = "WHITE"
        playerTurn = True
    else:
        whosTurn = "BLACK"
        playerTurn = False

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
    
    return board,whosTurn,playerTurn

def giveRandomColour():
    if random.randint(0,1) == 0:
        return "WHITE"
    else:
        return "BLACK"
        
def gamesAvailable():
    # returns a string with either 'No games found' or 'N games found' where N is the number of games
    # will show player how many games they have on going
    return "No games found"

