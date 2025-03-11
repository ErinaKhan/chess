import random
import UI_Handler as UI

CONSOLE_APPLICATION = True

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
    castlingData = None
    enPassant = None

    if gameType == "new":
        board,colour,playerTurn,castlingData,enPassant = boardSetup(giveRandomColour())
    elif gameType == "old": # loading a previously played unfinished game
        numOfGames,games,gameNames = gamesAvailable()
        if numOfGames != 0:
            UI.sleep(1)
            board,colour,playerTurn,castlingData,enPassant = FENBoard(games[UI.generateMenu(gameNames)])
            print("\nLoading game...")
            UI.sleep(1)
    elif gameType == "FEN":
        board,colour,playerTurn,castlingData,enPassant = FENBoard(getFEN())
    
    return colour,playerTurn,board,castlingData,enPassant

def gameConfig():
    # returns the settings for the game as a string
    if not CONSOLE_APPLICATION:
        return "new"

    UI.sleep(1)
    option = UI.generateMenu(["New Game","Load Game [" + str(gamesAvailable()[0]) + " available]"])

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
        return data[0],"WHITE",True,data[3],data[4]
    else:
        data = FENBoard("RNBQKBNR/PPPPPPPP/8/8/8/8/pppppppp/rnbqkbnr b KQkq - 0 1")
        return data[0],"BLACK",False,data[3],data[4]

def validFEN(fen):
    fields = fen.split()
    if len(fields) != 6:
        return False  # FEN must have exactly 6 parts
    
    piece_placement, active_color, castling, en_passant, halfmove, fullmove = fields
    
    # Check if the board has 8 rows
    ranks = piece_placement.split('/')
    if len(ranks) != 8:
        return False
    
    # Check if each rank adds up to 8 squares
    for rank in ranks:
        count = 0
        for char in rank:
            if char.isdigit():
                count += int(char)
            else:
                count += 1
        if count != 8:
            return False
    
    # Check if active color is 'w' or 'b'
    if active_color not in ('w', 'b'):
        return False
    
    # Check castling rights (must be valid or '-')
    valid_castling = set("KQkq-")
    if any(c not in valid_castling for c in castling):
        return False
    
    # Check en passant target square (must be valid or '-')
    valid_en_passant = [f"{c}{n}" for c in "abcdefgh" for n in "36"] + ["-"]
    if en_passant not in valid_en_passant:
        return False
    
    # Check if halfmove and fullmove are numbers
    if not (halfmove.isdigit() and fullmove.isdigit()):
        return False
    
    return True

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
    
    return board,whosTurn,playerTurn,canCastle,enPassant

def giveRandomColour():
    if random.randint(0,1) == 0:
        return "WHITE"
    else:
        return "BLACK"
        
def gamesAvailable():
    # returns a string with either 'No games found' or 'N games found' where N is the number of games
    # will show player how many games they have on going
    saveFile = None 
    games = []
    gameNames = []
    numOfGames = 0
    try:
        saveFile = open("saveFile.txt","rt")

        for game in saveFile:
            numOfGames = numOfGames + 1
            game = game.split(",")
            games = games + [game[0]]
            gameNames = gameNames + [game[1]]

        saveFile.close()
    except:
        print("File doesnt exist")

    if numOfGames == 0:
        numOfGames = "No games"

    return numOfGames,games,gameNames

