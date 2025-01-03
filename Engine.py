######################################################################################################
############################################### ENGINE ###############################################
######################################################################################################
#
#
#  Representation of how the bitboard method operates 
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

whiteTurn = False
castlingRights = False
enPassantSquare = False

def colourType(piece):
    whitePieces = ['♜','♞','♝','♛','♚','♟']
    blackPieces = ['♖','♘','♗','♕','♔','♙']

    if piece in whitePieces:
        return "WHITE"
    if piece in blackPieces:
        return "BLACK"

def pieceType(pieceSelected):
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
            currentSquare = pieceType(board[x][y])

            if currentSquare[0] != "NONE":
                colour = currentSquare[1]
                currentSquare = currentSquare[0]
                valueToAdd = int(math.pow(2,i))
                if colour != "WHITE":
                    print("white")
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

def upwardsPawnPush():
    pass

def downwardsPawnPush():
    pass

def diagonalMoves():
    pass

def horizontalMoves():
    pass

def evaluate():
    pass

def search():
    pass

def AITurn():
    pass