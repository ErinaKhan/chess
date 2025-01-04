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
directionOffsets = [8,-8, 1, -1, 7, -7, 9, -9]  

# 2d array that stores squares to edge for every square on the board and is pre computed to allow quicker lookup times
global squaresToEdge

global whosTurn 
whosTurn = "White"
castlingRights = False
enPassantSquare = False

# actual size of board (8x8) 64 squares total
boardWidth = 8
boardHeight = 8

# used for the sizing of the ui on screen measured in characters
pixelWidth = 5
pixelHeight = 1

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
    "NONENONE": " "
}

def validateCoordinates(coordinates): 
    # tuple input
    # boolean output
    validFiles = ['a','b','c','d','e','f','g','h']
    validRanks = ['1','2','3','4','5','6','7','8']
    rank = coordinates[0]
    file = coordinates[1]

    if (rank in validRanks) and (file in validFiles):
        return True
    else:
        return False

def convertCoordinates(coordinates): 
    # tuple input
    # int output
    file = ord(coordinates[0].upper()) - 65
    rank = 8 - int(coordinates[1])
    posOnBitboard = (rank * 8) + file
    bitboardValue = int(math.pow(2,64 - posOnBitboard - 1))
    return bitboardValue

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
    # input is an int
    if square & whitePieces != 0:
        return "WHITE"
    elif square & blackPieces != 0:
        return "BLACK"
    else:
        return "NONE"

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

def selectSquare(x):
    pass

def generateAllMoves():
    moves = []

    for file in range(8):
        
        for rank in range(8):

            currentSquareIndex = (rank * 8) + file
            squareBinary = int(math.pow(2,64 - currentSquareIndex - 1))

            if getColour(squareBinary) == whosTurn:

                pieceType = getPieceTypeFromSquare(squareBinary)

                if pieceType == "ROOK" or pieceType == "BISHOP" or pieceType == "QUEEN":

                    moves = moves + generateSlidingPieceMoves(squareBinary, pieceType)


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

            targetSquare = startSquare + directionOffsets[direction] * (squares + 1) # from start square to edge of board

            if getColour(targetSquare) == playerColour:
                break

            moves = moves + [startSquare,targetSquare]

            if getColour(targetSquare) == enemyColour:
                break

    return moves

def pawnPieceMoves():
    pass

def evaluate():
    pass

def search():
    pass

def AITurn():
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
                if colour != "WHITE":
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
    
def drawBoard():
    line("top")
    for rank in range(boardHeight):
        line(rank)
        fillSquare()
        print(f"\n{8 - rank} |", end = "")
        for file in range(boardWidth):
            currentSquareIndex = (rank * 8) + file
            squareBinary = int(math.pow(2,64 - currentSquareIndex - 1))
            colour = str(getColour(squareBinary))
            piece = str(getPieceTypeFromSquare(squareBinary))
            print(f"{padding()}{pieceLookup[colour+piece]}{padding()}|", end = "")
        fillSquare()
    line(1)