######################################################################################################
############################################### ENGINE ###############################################
######################################################################################################
#
#
#  Representation of how the bitboard method operates 
#  
#  in binary every square on the board is accessed by 2 to the power of whatever square it is
#
#  -------------------------------------------------------------------------------------------------
#  |           |           |           |           |           |           |           |           |
#  |     1     |     2     |     3     |     4     |     5     |     6     |     7     |     8     |
#  |           |           |           |           |           |           |           |           |
#  -------------------------------------------------------------------------------------------------
#  |           |           |           |           |           |           |           |           |
#  |     9     |    1 0    |    1 1    |    1 2    |    1 3    |    1 4    |    1 5    |    1 6    |
#  |           |           |           |           |           |           |           |           |
#  -------------------------------------------------------------------------------------------------
#  |           |           |           |           |           |           |           |           |
#  |    1 7    |    1 8    |    1 9    |    2 0    |    2 1    |    2 2    |    2 3    |    2 4    |
#  |           |           |           |           |           |           |           |           |
#  -------------------------------------------------------------------------------------------------
#  |           |           |           |           |           |           |           |           |
#  |    2 5    |    2 6    |    2 7    |    2 8    |    2 9    |    3 0    |    3 1    |    3 2    |
#  |           |           |           |           |           |           |           |           |
#  -------------------------------------------------------------------------------------------------
#  |           |           |           |           |           |           |           |           |
#  |    3 3    |    3 4    |    3 5    |    3 6    |    3 7    |    3 8    |    3 9    |    4 0    |
#  |           |           |           |           |           |           |           |           |
#  -------------------------------------------------------------------------------------------------
#  |           |           |           |           |           |           |           |           |
#  |    4 1    |    4 2    |    4 3    |    4 4    |    4 5    |    4 6    |    4 7    |    4 8    |
#  |           |           |           |           |           |           |           |           |
#  -------------------------------------------------------------------------------------------------
#  |           |           |           |           |           |           |           |           |
#  |    4 9    |    5 0    |    5 1    |    5 2    |    5 3    |    5 4    |    5 5    |    5 6    |
#  |           |           |           |           |           |           |           |           |
#  -------------------------------------------------------------------------------------------------
#  |           |           |           |           |           |           |           |           |
#  |    5 7    |    5 8    |    5 9    |    6 0    |    6 1    |    6 2    |    6 3    |    6 4    |
#  |           |           |           |           |           |           |           |           |
#  -------------------------------------------------------------------------------------------------
#
#  Things to note from this
#
#  To move upwards you subtract 8 and to move downwards add 8
#  
#  Diagonal movement
#  ---------------------
#  top right    = i - 7 
#  top left     = i - 9
#  bottom right = i + 9
#  bottom left  = i + 7
#
######################################################################################################
######################################################################################################
######################################################################################################
import math

global bitWordBoard
global whitePieces
global blackPieces

global whitePawns
global whiteHorses
global whiteBishops
global whiteRooks
global whiteQueens
global whiteKing

global blackPawns
global blackHorses
global blackBishops
global blackRooks
global blackQueens
global blackKing

global playerColour
global enemyColour

# offsets needed for all horizonatal and diagonal moves shown visually in the diagram at the top of the code
# use first 4 indexes for straight line moves like the rook and the last 4 for diagonal moves or all indexes for the queen
directionOffsets = [-8,8,1,-1,-9,9,-7,7]    

# 2d array that stores squares to edge for every square on the board and is pre computed to allow quicker lookup times
global squaresToEdge

global whosTurn 
whosTurn = "White"

castlingRights = False
enPassantSquare = False

pieceLookup = {
    "BLACKROOK": "♖",
    "BLACKHORSE": "♘",
    "BLACKBISHOP": "♗",
    "BLACKQUEEN": "♕",
    "BLACKKING": "♔",
    "BLACKPAWN": "♙",
    "WHITEROOK": "♜",
    "WHITEHORSE": "♞",
    "WHITEBISHOP": "♝",
    "WHITEQUEEN": "♛",
    "WHITEKING": "♚",
    "WHITEPAWN": "♟",
    "NONENONE": " ",
    "MOVEOVERLAY": "X"
}

def assignColours(plrColour):
    global playerColour
    global enemyColour

    if plrColour == "WHITE":
        playerColour = "WHITE"
        enemyColour = "BLACK"
    else:
        playerColour = "BLACK"
        enemyColour = "WHITE"

def getColour(square):
    if square == None:
        return None
    # input is an int
    if square & whitePieces != 0:
        return "WHITE"
    elif square & blackPieces != 0:
        return "BLACK"
    else:
        return "NONE"

def inCheck(colour):
    if colour == "WHITE":
        pass
    elif colour == "BLACK":
        pass
    else:
        return "ERROR"

def canMove(square):
    return True

def whiteAssignment(i,value):
    global whitePawns
    global whiteHorses
    global whiteBishops
    global whiteRooks
    global whiteQueens
    global whiteKing

    if i == 0:
        whitePawns = value
    elif i == 1:
        whiteBishops = value
    elif i == 2:
        whiteHorses = value
    elif i == 3:
        whiteRooks = value
    elif i == 4:
        whiteQueens = value
    elif i == 5:
        whiteKing = value

def blackAssignment(i,value):
    global blackPawns
    global blackHorses
    global blackBishops
    global blackRooks
    global blackQueens
    global blackKing
    if i == 0:
        blackPawns = value
    elif i == 1:
        blackBishops = value
    elif i == 2:
        blackHorses = value
    elif i == 3:
        blackRooks = value
    elif i == 4:
        blackQueens = value
    elif i == 5:
        blackKing = value    

def updateBoard(square,chosenLegalMove,colour):
    global bitWordBoard
    global whitePieces
    global blackPieces

    w = [whitePawns, whiteBishops, whiteHorses, whiteRooks, whiteQueens, whiteKing]
    b = [blackPawns, blackBishops, blackHorses, blackRooks, blackQueens, blackKing]

    if colour == "WHITE":
        for i in range(6):

            if square & w[i] != 0:
                # this is the set its in
                w[i] = w[i] ^ square
                w[i] = w[i] | chosenLegalMove
                whiteAssignment(i,w[i])

            elif chosenLegalMove & b[i] != 0:

                b[i] = b[i] ^ chosenLegalMove
                blackAssignment(i,b[i])
    else:
        for i in range(6):

            if square & b[i] != 0:
                # this is the set its in
                b[i] = b[i] ^ square
                b[i] = b[i] | chosenLegalMove
                blackAssignment(i,b[i])

            elif chosenLegalMove & w[i] != 0:

                w[i] = w[i] ^ chosenLegalMove
                whiteAssignment(i,w[i])
        
    whitePieces = whitePawns | whiteBishops | whiteHorses | whiteRooks | whiteQueens | whiteKing
    blackPieces = blackPawns | blackBishops | blackHorses | blackRooks | blackQueens | blackKing
    bitWordBoard = whitePieces | blackPieces


def precomputeSquaresToEdge():
    global squaresToEdge
    squaresToEdge = [None] * 64

    for file in range(8):
        
        for rank in range(8):

            north = rank
            south = 7 - rank
            west = file
            east = 7 - file

            northEast = min(north,east)
            southEast = min(south,east)
            southWest = min(south,west)
            northWest = min(north,west)

            currentSquare = (rank * 8) + file

            squaresToEdge[currentSquare] = [north,south,east,west,northWest,southEast,northEast,southWest]   

def getPieceTypeFromSquare(square):
    if (square & (whitePawns | blackPawns)) != 0:
        return "PAWN"   
    elif (square & (whiteRooks | blackRooks)) != 0:
        return "ROOK" 
    elif (square & (whiteBishops | blackBishops)) != 0:
        return "BISHOP" 
    elif (square & (whiteHorses | blackHorses)) != 0:
        return "HORSE" 
    elif (square & (whiteQueens | blackQueens)) != 0:
        return "QUEEN" 
    elif (square & (whiteKing | blackKing)) != 0:
        return "KING" 
    else:
        return "NONE"
    
def generateAllMoves(turn):
    moves = []

    for file in range(8):
        
        for rank in range(8):

            currentSquareIndex = (rank * 8) + file
            squareBinary = int(math.pow(2,currentSquareIndex))

            if getColour(squareBinary) == turn: # need to change

                pieceType = getPieceTypeFromSquare(squareBinary)

                if pieceType == "ROOK" or pieceType == "BISHOP" or pieceType == "QUEEN":
                    moves = moves + generateSlidingPieceMoves(currentSquareIndex, pieceType)
                elif pieceType == "PAWN":
                    moves = moves + generatePawnMoves(currentSquareIndex, turn)
                elif pieceType == "HORSE":
                    moves = moves + generateHorseMoves(currentSquareIndex)
                elif pieceType == "KING":
                    moves = moves + generateKingMoves(currentSquareIndex)


    return moves

def generatePawnMoves(startSquare,colour):
    moves = []
    directionEnd = 1
    direction = -1

    if (startSquare >= 48 and startSquare <= 55 and playerColour) or (startSquare >= 8 and startSquare <= 15 and enemyColour):
        directionEnd = 2

    if playerColour == colour:
        direction = 0
    elif enemyColour == colour:
        direction = 1
    
    if direction != -1:
        for squares in range(directionEnd):
            targetSquare = startSquare + (directionOffsets[direction] * (squares + 1))

            if getColour(int(math.pow(2,targetSquare))) == playerColour:
                break

            if getColour(int(math.pow(2,targetSquare))) == enemyColour:
                break

            moves = moves + [[startSquare,targetSquare]]
    else: 
        print("ERROR")

    return moves

def generateHorseMoves(startSquare):
    moves = []

    for i in range(4):
    
        squareBetween = startSquare + (directionOffsets[i] * 2)
        targetSquareLeft = None
        targetSquareRight = None

        print(f"{i} : {squaresToEdge[startSquare][i]}")

        if i == 0 or i == 1:
            if squaresToEdge[startSquare][3] >= 1:
                targetSquareLeft = squareBetween - 1
            if squaresToEdge[startSquare][2] >= 1:
                targetSquareRight = squareBetween + 1
        else:
            if squaresToEdge[startSquare][i] >= 2:
                targetSquareLeft = squareBetween + directionOffsets[0]
                targetSquareRight = squareBetween + directionOffsets[1]

        if targetSquareLeft != None:
            if (getColour(int(math.pow(2,targetSquareLeft))) != playerColour):
                moves = moves + [[startSquare,targetSquareLeft]]

        if targetSquareRight != None:
            if (getColour(int(math.pow(2,targetSquareRight))) != playerColour):
                moves = moves + [[startSquare,targetSquareRight]]

    print(moves)
    return moves

def generateKingMoves(startSquare):
    moves = []
    for i in range(8):
        if squaresToEdge[startSquare][i] >= 1:  
            targetSquare = startSquare + directionOffsets[i]

            if getColour(int(math.pow(2,targetSquare))) != playerColour:
                moves = moves + [[startSquare, targetSquare]]

    return moves
            

def generateSlidingPieceMoves(startSquare, piece):
    # pieces such as the queen,bishop and rook
    global squaresToEdge
    moves = []
    
    directionStart = 0 
    directionEnd = 8

    if piece == "ROOK": 
        directionStart = 0
        directionEnd = 4
    elif piece == "BISHOP":
        directionStart = 4
        directionEnd = 8

    for direction in range(directionStart, directionEnd):
    
        for squares in range(squaresToEdge[startSquare][direction]):

            targetSquare = startSquare + (directionOffsets[direction] * (squares + 1)) # from start square to edge of board

            if getColour(int(math.pow(2,targetSquare))) == playerColour:
                break

            moves = moves + [[startSquare,targetSquare]]

            if getColour(int(math.pow(2,targetSquare))) == enemyColour:
                break
        
    return moves

def filterMovesBySquare(square, colour):
    squaresMoves = []
    allMoves = generateAllMoves(colour)
   
    for move in allMoves:
        if move[0] == square:
            squaresMoves = squaresMoves + [move]

    return squaresMoves

def evaluate():
    pass

def search():
    pass

##################################################################################################################################################################################
##################################################################################################################################################################################
##################################################################################################################################################################################
##################################################################################################################################################################################

def colourType(piece):
    whitePieces = ['♜','♞','♝','♛','♚','♟']
    blackPieces = ['♖','♘','♗','♕','♔','♙']

    if piece in whitePieces:
        return "WHITE"
    if piece in blackPieces:
        return "BLACK"

def getPieceType(pieceSelected):
    # returns a string that contains the type of piece it is
    # examples are things such as 'rook', 'pawn', 'queens'
    colour = colourType(pieceSelected)
    if pieceSelected in ['♟','♙']:
        return "PAWN",colour
    elif pieceSelected in ['♞','♘']:
        return "HORSE",colour
    elif pieceSelected in ['♝','♗']:
        return "BISHOP",colour
    elif pieceSelected in ['♜','♖']:
        return "ROOK",colour
    elif pieceSelected in ['♛','♕']:
        return "QUEEN",colour
    elif pieceSelected in ['♚','♔']:
        return "KING",colour
    else:
        return "NONE",None

def convertToBitBoard(board):

    global bitWordBoard
    global whitePieces
    global blackPieces
     
    global whitePawns
    global whiteHorses
    global whiteBishops
    global whiteRooks
    global whiteQueens
    global whiteKing

    global blackPawns
    global blackHorses
    global blackBishops
    global blackRooks
    global blackQueens
    global blackKing

    blackPieces = 0
    whitePieces = 0
    
    whitePawns = 0
    whiteHorses = 0
    whiteBishops = 0
    whiteRooks = 0
    whiteQueens = 0
    whiteKing = 0
    blackPawns = 0
    blackHorses = 0
    blackBishops = 0
    blackRooks = 0
    blackQueens = 0 
    blackKing = 0

    i = 0
    for x in range(8):
        for y in range(8):
            currentSquare = getPieceType(board[x][y])

            if currentSquare[0] != "NONE":
                colour = currentSquare[1]
                currentSquare = currentSquare[0]
                valueToAdd = int(math.pow(2,i))
                if colour == "WHITE":
                    if currentSquare == "PAWN":
                        whitePawns = whitePawns + valueToAdd
                    elif currentSquare == "HORSE":
                        whiteHorses = whiteHorses + valueToAdd
                    elif currentSquare == "BISHOP":
                        whiteBishops = whiteBishops + valueToAdd
                    elif currentSquare == "ROOK":
                        whiteRooks = whiteRooks + valueToAdd
                    elif currentSquare == "QUEEN":
                        whiteQueens = whiteQueens + valueToAdd
                    elif currentSquare == "KING":
                        whiteKing = whiteKing + valueToAdd
                else:
                    if currentSquare == "PAWN":
                        blackPawns = blackPawns + valueToAdd
                    elif currentSquare == "HORSE":
                        blackHorses = blackHorses + valueToAdd
                    elif currentSquare == "BISHOP":
                        blackBishops = blackBishops + valueToAdd
                    elif currentSquare == "ROOK":
                        blackRooks = blackRooks + valueToAdd
                    elif currentSquare == "QUEEN":
                        blackQueens = blackQueens + valueToAdd
                    elif currentSquare == "KING":
                        blackKing = blackKing + valueToAdd
            i = i + 1

    whitePieces = whitePawns | whiteBishops | whiteHorses | whiteRooks | whiteQueens | whiteKing
    blackPieces = blackPawns | blackBishops | blackHorses | blackRooks | blackQueens | blackKing
    bitWordBoard = whitePieces | blackPieces

    #print(bin(whitePieces))
    #print(bin(blackPieces))
    #print(bin(whitePawns))
    #print(bin(whiteHorses))
    #print(bin(whiteBishops))
    #print(bin(whiteRooks))
    #print(bin(whiteQueens))
    #print(bin(whiteKing)) 
    #print(bin(blackPawns))
    #print(bin(blackHorses))
    #print(bin(blackBishops))
    #print(bin(blackRooks))
    #print(bin(blackQueens))
    #print(bin(blackKing))
