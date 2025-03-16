######################################################################################################
############################################### ENGINE ###############################################
######################################################################################################
#  
#  in binary every square on the board is accessed by 2 to the power of whatever square it is
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
import random
import UI_Handler as UI
import PROJECT_SETTINGS as settings

global signalGameUIEvents

global currentBoardFullData

#------------------------------------------------------------------------------------------------------------------------

# bitboards

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

#------------------------------------------------------------------------------------------------------------------------

# used for tracking castling

global wKingMoved
global wRooksMoved

global bKingMoved
global bRooksMoved

global wqueenSide
global wkingSide
global bqueenSide
global bkingSide

#------------------------------------------------------------------------------------------------------------------------

# offsets needed for all horizonatal and diagonal moves shown visually in the diagram at the top of the code
# use first 4 indexes for straight line moves like the rook and the last 4 for diagonal moves or all indexes for the queen
directionOffsets = [-8,8,1,-1,-9,9,-7,7]    

# 2d array that stores squares to edge for every square on the board and is pre computed to allow quicker lookup times
global squaresToEdge

global lastMove
global Checkmate

lastMove = [0,0]

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

pieceValue = {
    "PAWN": 1,
    "HORSE": 3,
    "BISHOP": 3,
    "ROOK": 5,
    "QUEEN": 9, 
    "KING": 0
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

    return enemyColour

def switchColours(colour):
    if colour == "WHITE":
        return "BLACK"
    else:
        return "WHITE"

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

def makeMove(square,chosenLegalMove,colour,isFake=False,extraInfo=None):
    updateBoard(square,chosenLegalMove,colour,isFake,extraInfo) # w and b are arrays of piece bitboards [Pawns,Bishops,Horses,Rooks,Queens,King]

    if not isFake:
        global currentBoardFullData
        castlingData = [wkingSide,wqueenSide,wKingMoved,wRooksMoved,bkingSide,bqueenSide,bKingMoved,bRooksMoved]
        whitePiecesData = [whitePawns, whiteBishops, whiteHorses, whiteRooks, whiteQueens, whiteKing]
        blackPiecesData = [blackPawns, blackBishops, blackHorses, blackRooks, blackQueens, blackKing]
        currentBoardFullData = [whitePiecesData,blackPiecesData,castlingData]

def updateBoard(square,chosenLegalMove,colour,isFake,extraInfo):
    global bitWordBoard
    global whitePieces
    global blackPieces
    global lastMove
    global whitePawns
    global blackPawns

    w = [whitePawns, whiteBishops, whiteHorses, whiteRooks, whiteQueens, whiteKing]
    b = [blackPawns, blackBishops, blackHorses, blackRooks, blackQueens, blackKing]

    nonBinSquare = int(math.log(square,2))
    nonBinMove = int(math.log(chosenLegalMove,2))

    if isEnPassant(nonBinSquare,square,nonBinMove):
        enPassant(nonBinMove,nonBinSquare,colour)

        if not settings.isConsoleApplication() and not isFake:
            signalGameUIEvents.emitEnPassantEvent(nonBinMove)
     
    if isCastling(nonBinSquare,square, nonBinMove):
        castle(chosenLegalMove,colour)

        if not settings.isConsoleApplication() and not isFake:
            signalGameUIEvents.emitCastleEvent()


    if colour == "WHITE":
        for i in range(6):

            if square & w[i] != 0:
                # this is the set its in
                w[i] = w[i] ^ square
                w[i] = w[i] | chosenLegalMove
                whiteAssignment(i,w[i])

            if chosenLegalMove & b[i] != 0:

                b[i] = b[i] ^ chosenLegalMove
                blackAssignment(i,b[i])
    else:
        for i in range(6):

            if square & b[i] != 0:
                # this is the set its in
                b[i] = b[i] ^ square
                b[i] = b[i] | chosenLegalMove
                blackAssignment(i,b[i])

            if chosenLegalMove & w[i] != 0:

                w[i] = w[i] ^ chosenLegalMove
                whiteAssignment(i,w[i])

    if isPromoting(chosenLegalMove,nonBinMove): 
        piece = None
        if playerColour == colour:
            if not isFake:
                if not settings.isConsoleApplication():
                    piece = "QUEEN"
                else:
                    piece = UI.askForPromotePiece()

            promote(chosenLegalMove,colour,piece)

            if not settings.isConsoleApplication() and not isFake:
                signalGameUIEvents.emitPromotionEvent(nonBinMove,colour,piece)
        else:
            promote(chosenLegalMove,colour,extraInfo)

    lastMove = [nonBinSquare,nonBinMove]
    whitePieces = whitePawns | whiteBishops | whiteHorses | whiteRooks | whiteQueens | whiteKing
    blackPieces = blackPawns | blackBishops | blackHorses | blackRooks | blackQueens | blackKing
    bitWordBoard = whitePieces | blackPieces
    canCastle(colour)

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
    
def generateAllMoves(turn,isResponses,movesToSearch=[]):
    legalMoves = []
    moves = [] 

    if movesToSearch != []:
        turnIndex = 0
        for i in movesToSearch:
            turnIndex = turnIndex + 1
            if turnIndex % 2 == 1:
                makeMove(int(math.pow(2,i[0])),int(math.pow(2,i[1])),enemyColour,True)  
            else:
                makeMove(int(math.pow(2,i[0])),int(math.pow(2,i[1])),playerColour,True)  

    for file in range(8):
        
        for rank in range(8):

            currentSquareIndex = (rank * 8) + file
            squareBinary = int(math.pow(2,currentSquareIndex))

            if getColour(squareBinary) == turn: # need to change

                pieceType = getPieceTypeFromSquare(squareBinary)

                if pieceType == "ROOK" or pieceType == "BISHOP" or pieceType == "QUEEN":
                    moves = moves + generateSlidingPieceMoves(currentSquareIndex, pieceType,turn)
                elif pieceType == "PAWN":
                    moves = moves + generatePawnMoves(currentSquareIndex, turn)
                elif pieceType == "HORSE":
                    moves = moves + generateHorseMoves(currentSquareIndex,turn)
                elif pieceType == "KING":
                    moves = moves + generateKingMoves(currentSquareIndex,turn)

    if not isResponses:
        for move in moves:            
            makeMove(int(math.pow(2,move[0])),int(math.pow(2,move[1])),turn,True,None)
            if not inCheck(turn,generateAllMoves(switchColours(turn),True,movesToSearch)):
                startValid = move[0] <= 63 and move[0] >= 0 
                endValid = move[1] <= 63 and move[1] >= 0 
                if startValid and endValid:
                    legalMoves = legalMoves + [move]
                
            resetData()

            if movesToSearch != []:
                turnIndex = 0
                for i in movesToSearch:
                    turnIndex = turnIndex + 1
                    if turnIndex % 2 == 1:
                        makeMove(int(math.pow(2,i[0])),int(math.pow(2,i[1])),enemyColour,True)  
                    else:
                        makeMove(int(math.pow(2,i[0])),int(math.pow(2,i[1])),playerColour,True)  


        if len(legalMoves) == 0:
            if inCheck(turn,generateAllMoves(switchColours(turn),True,movesToSearch)):
                if movesToSearch == []:
                    global Checkmate
                    Checkmate = True
            else:
                if movesToSearch == []:
                    UI.clear()
                    UI.stalemateUI()
                    UI.sleep(10)
                        

        return legalMoves
            
    return moves

def generatePawnMoves(startSquare,colour):
    moves = []
    directionEnd = 1
    direction = -1

    binarySquare = int(math.pow(2,startSquare))
    playerOnStartingRank = startSquare >= 48 and startSquare <= 55 and (playerColour == colour)
    enemyOnStartingRank = startSquare >= 8 and startSquare <= 15 and (enemyColour == colour)
    onLeftEdge = startSquare in [0,8,16,24,32,40,48,56]
    onRightEdge = startSquare in [7,15,23,31,39,47,55,63]
    enemyLeft = getColour(binarySquare >> 9) == enemyColour
    enemyRight = getColour(binarySquare >> 7) == enemyColour
    playerLeft = getColour(binarySquare << 7) == playerColour
    playerRight = getColour(binarySquare << 9) == playerColour
    canTakePieceLeft = (enemyLeft and colour == playerColour) or (playerLeft and colour == enemyColour)
    canTakePieceRight = (enemyRight and colour == playerColour) or (playerRight and colour == enemyColour)

    if (playerOnStartingRank) or (enemyOnStartingRank):
        directionEnd = 2
    if playerColour == colour:
        direction = 0
    elif enemyColour == colour:
        direction = 1

    if canTakePieceLeft and not onLeftEdge:
        if playerColour == colour:
            moves = moves + [[startSquare, startSquare - 9]]
        else: 
            moves = moves + [[startSquare, startSquare + 7]]

    if canTakePieceRight and not onRightEdge:
        if playerColour == colour:
            moves = moves + [[startSquare, startSquare - 7]]
        else: 
            moves = moves + [[startSquare, startSquare + 9]]

    if direction != -1:
        for squares in range(directionEnd):
            targetSquare = startSquare + (directionOffsets[direction] * (squares + 1))

            if getColour(int(math.pow(2,targetSquare))) == playerColour:
                break

            if getColour(int(math.pow(2,targetSquare))) == enemyColour:
                break

            moves = moves + [[startSquare,targetSquare]]

        if (startSquare >= 32 and startSquare <= 39 and enemyColour == colour) or (startSquare >= 24 and startSquare <= 31 and playerColour == colour):
            
            if lastMove != None:
                
                if abs(lastMove[1] - startSquare) == 1:
                    if (lastMove[0] >= 8 and lastMove[0] <= 15) and (lastMove[1] == lastMove[0] + 16) and playerColour == colour and getPieceTypeFromSquare(int(math.pow(2,lastMove[1]))) == "PAWN":
                        moves = moves + [[startSquare, lastMove[1] - 8]] 
                    if (lastMove[0] >= 48 and lastMove[0] <= 55) and (lastMove[1] == lastMove[0] - 16) and enemyColour == colour and getPieceTypeFromSquare(int(math.pow(2,lastMove[1]))) == "PAWN":
                        moves = moves + [[startSquare, lastMove[1] + 8]] 
    else: 
        print("ERROR")

    return moves


def generateHorseMoves(startSquare,colour):
    moves = []

    for i in range(4):
        squareBetween = startSquare + (directionOffsets[i] * 2)
        targetSquareLeft = None
        targetSquareRight = None

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
            if (getColour(int(math.pow(2,targetSquareLeft))) != colour) and targetSquareLeft >= 0:
                moves = moves + [[startSquare,targetSquareLeft]]

        if targetSquareRight != None:
            if (getColour(int(math.pow(2,targetSquareRight))) != colour) and targetSquareRight >= 0:
                moves = moves + [[startSquare,targetSquareRight]]
    return moves

def generateKingMoves(startSquare,colour):
    moves = []
    for i in range(8):
        if squaresToEdge[startSquare][i] >= 1:  
            targetSquare = startSquare + directionOffsets[i]

            if getColour(int(math.pow(2,targetSquare))) != colour:
                moves = moves + [[startSquare, targetSquare]]

    kingSide,queenSide = canCastle(colour)
    
    if kingSide:
        if getPieceTypeFromSquare(int(math.pow(2,startSquare + 1))) == "NONE" and getPieceTypeFromSquare(int(math.pow(2,startSquare + 2))) == "NONE":
            moves = moves + [[startSquare, startSquare + 2]]
    if queenSide:
        if getPieceTypeFromSquare(int(math.pow(2,startSquare - 1))) == "NONE" and getPieceTypeFromSquare(int(math.pow(2,startSquare - 2))) == "NONE" and getPieceTypeFromSquare(int(math.pow(2,startSquare - 3))) == "NONE":
            moves = moves + [[startSquare, startSquare - 2]]
    return moves
            
def generateSlidingPieceMoves(startSquare, piece,colour):
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

            if getColour(int(math.pow(2,targetSquare))) == colour:
                break

            moves = moves + [[startSquare,targetSquare]]

            if getColour(int(math.pow(2,targetSquare))) != colour and getColour(int(math.pow(2,targetSquare))) != "NONE":
                break
        
    return moves

def filterMovesBySquare(square, colour):
    squaresMoves = []
    pseudoLegalMoves = generateAllMoves(colour,False)
    for move in pseudoLegalMoves:
        if move[0] == square:
            squaresMoves = squaresMoves + [move]

    return squaresMoves

def isEnPassant(square,binary,chosenLegalMove):
    if (chosenLegalMove - square) % 8 != 0 and getPieceTypeFromSquare(binary) == "PAWN" and getPieceTypeFromSquare(int(math.pow(2,chosenLegalMove))) == "NONE":
        return True
    return False

def enPassant(nonBinMove,nonBinSquare,colour):
    global whitePawns
    global blackPawns

    direction = 0
    if nonBinMove - nonBinSquare > 0:
        direction = -1
    else: 
        direction = 1
    if colour == "WHITE":
        blackPawns = blackPawns ^ int(math.pow(2, nonBinMove + (direction * 8)))
    else:
        whitePawns = whitePawns ^ int(math.pow(2, nonBinMove + (direction * 8)))
    
def isCastling(square,binary, chosenLegalMove):
    legalMoves = [6,2,58,62]
    if (square == 4 or square == 60) and (chosenLegalMove in legalMoves) and getPieceTypeFromSquare(binary) == "KING":
        return True
    return False

def castle(chosenLegalMove,colour):
    placementForRook = int(math.log(chosenLegalMove,2))

    if placementForRook == 6:
        updateBoard(int(math.pow(2,7)),int(math.pow(2,5)),colour,False,None)    
    elif placementForRook == 62:
        updateBoard(int(math.pow(2,63)),int(math.pow(2,61)),colour,False,None)
    elif placementForRook == 2:
        updateBoard(1,8,colour,False,None)
    elif placementForRook == 58:
        updateBoard(int(math.pow(2,56)),int(math.pow(2,59)),colour,False,None)


def isPromoting(binary,chosenLegalMove):
    if ((chosenLegalMove >= 0 and chosenLegalMove <= 7) or (chosenLegalMove >= 56 and chosenLegalMove <= 63)) and getPieceTypeFromSquare(binary) == "PAWN":
        return True
    return False

def promote(chosenLegalMove,colour,piece):
    global whiteHorses
    global whiteBishops
    global whiteRooks
    global whiteQueens
    global whitePawns

    global blackPawns
    global blackHorses
    global blackBishops
    global blackRooks
    global blackQueens

    if colour == "WHITE":
        whitePawns = whitePawns ^ chosenLegalMove
        if piece == "BISHOP":
            whiteBishops = whiteBishops | chosenLegalMove
        elif piece == "HORSE":
            whiteHorses = whiteHorses | chosenLegalMove
        elif piece == "ROOK":
            whiteRooks = whiteRooks | chosenLegalMove
        elif piece == "QUEEN":
            whiteQueens = whiteQueens | chosenLegalMove
    else:
        blackPawns = blackPawns ^ chosenLegalMove
        if piece == "BISHOP":
            blackBishops = blackBishops | chosenLegalMove
        elif piece == "HORSE":
            blackHorses = blackHorses | chosenLegalMove
        elif piece == "ROOK":
            blackRooks = blackRooks | chosenLegalMove
        elif piece == "QUEEN":
            blackQueens = blackQueens | chosenLegalMove

def canCastle(colour):
    global wKingMoved
    global wRooksMoved

    global bKingMoved
    global bRooksMoved

    global whiteRooks
    global whiteKing

    global blackRooks
    global blackKing

    global wqueenSide
    global wkingSide
    global bqueenSide
    global bkingSide

    if colour == "WHITE":
        if whiteRooks != 0:
            if wKingMoved & whiteKing == 0:
                wKingMoved = 0
                wkingSide = False 
                wqueenSide = False
            if wRooksMoved & whiteRooks != whiteRooks:
                if wRooksMoved > whiteRooks:
                    wkingSide = False
                if wRooksMoved < whiteRooks:
                    wqueenSide = False
        return wkingSide,wqueenSide
    else:
        if blackRooks != 0:
            if bKingMoved & blackKing == 0:
                bKingMoved = 0
                bkingSide = False 
                bqueenSide = False
            if bRooksMoved & blackRooks != blackRooks:
                if bRooksMoved < blackRooks:
                    bkingSide = False
                if bRooksMoved > blackRooks:
                    bqueenSide = False
        return bkingSide,bqueenSide

def inCheck(colour,moves):
    global blackKing
    global whiteKing

    if colour == "WHITE":
        if whiteKing == 0:
            return True
        
        kingPos = int(math.log(whiteKing,2))
        
        for i in moves:
            if i[1] == kingPos:
                return True

    else:
        if blackKing == 0:
            return True
       
        kingPos = int(math.log(blackKing,2))

        for i in moves:
            if i[1] == kingPos:
                return True
            
    return False

def evaluate():
    evaluationScore = 0
    for file in range(8):
        for rank in range(8):
            
            currentSquareIndex = (rank * 8) + file
            squareBinary = int(math.pow(2,currentSquareIndex))
            pieceType = getPieceTypeFromSquare(squareBinary)
            colour = getColour(squareBinary) 

            if not pieceType in ["KING","NONE"]:

                if colour == "WHITE":
                    evaluationScore = evaluationScore + pieceValue[pieceType]
                else:
                    evaluationScore = evaluationScore - pieceValue[pieceType]

    return evaluationScore

def getBestEvalMove(colour,currentBestMove,newEvaluation,move):
    eval = evaluate()
    if currentBestMove != None:
        if colour == "WHITE":
            if eval > newEvaluation:
                currentBestMove = move
                newEvaluation = eval
        else:
            if eval < newEvaluation:
                currentBestMove = move
                newEvaluation = eval
    else:
        currentBestMove = move

    return currentBestMove,newEvaluation

def search(moves,colour,searchMoves=[]):
    resetData(searchMoves)

    currentEvaluation = evaluate()
    newEvaluation = currentEvaluation
    extraInfo = None # may contain promotion piece
    bestMove = None

    if len(moves) != 0:
        for i in moves:

            resetData(searchMoves)

            '''if depth != 0:
                currentColour = switchColours(colour)
                depthMove = i
                depthCopy = depth
                depthCopy = depthCopy - 1
                searchMovesCopy = searchMoves
                searchMovesCopy = searchMovesCopy + [depthMove]
                depthMoves = generateAllMoves(currentColour,False,searchMovesCopy)
                depthMove,depthExtraInfo,eval = search(depthMoves,currentColour,depthCopy,startingDepth,searchMovesCopy)
                maxDepthMoves = maxDepthMoves + [depthMove,extraInfo,eval]'''
           
            if isPromoting(int(math.pow(2,i[0])),i[1]):
                for piece in ["BISHOP","ROOK","HORSE","QUEEN"]:
                    resetData(searchMoves)
                    makeMove(int(math.pow(2,i[0])),int(math.pow(2,i[1])),colour,True,piece)
                    bestMove, newEvaluation = getBestEvalMove(colour,bestMove,newEvaluation,i)
                    if bestMove == i:
                        extraInfo = piece
            else:
                makeMove(int(math.pow(2,i[0])),int(math.pow(2,i[1])),colour,True)         
                
            bestMove,newEvaluation = getBestEvalMove(colour,bestMove,newEvaluation,i)     
            resetData()

        
        if newEvaluation == currentEvaluation:
            index = random.randint(0, len(moves) - 1)
            chosenMove = moves[index]
            return chosenMove,extraInfo,newEvaluation
        else:
            return bestMove,extraInfo,newEvaluation
    else:
        return None,None,None


def searchv2(depth,colour,searchMoves = []):
    resetData(searchMoves)

    if depth == 0:
        return evaluate(),searchMoves[0]
    
    moves = generateAllMoves(colour,False,searchMoves)

    if len(moves) == 0:
        pass
    
    bestEval = None
    if colour == "WHITE":
        bestEval = -1000000000
    else:
        bestEval = 1000000000
    bestMove = None

    for move in moves:
        resetData(searchMoves)

        if isPromoting(int(math.pow(2,move[0])),move[1]):
            makeMove(int(math.pow(2,move[0])),int(math.pow(2,move[1])),colour,True,"QUEEN") 
        else:
            makeMove(int(math.pow(2,move[0])),int(math.pow(2,move[1])),colour,True) 

        eval,nextBestMove = searchv2(depth - 1,switchColours(colour),searchMoves + [move])  
        eval = -eval
        bestEval = getBestEvalMove(colour,nextBestMove,bestEval,move)[1]

        if bestEval == eval:
            bestMove = nextBestMove

    return bestEval,bestMove
    
# ------------- plan for final search function that supports depth ----------------------
#
#                    does search call for each branch and 
#                        returns best move for enemy
#         (the start then adds all these moves returned from branches 
#       into list and selects one with lowest eval response from black)
#                        ^       ^        ^        ^
#                        |       |        |        |
#                   Checks every move person searching has
#                        ^       ^        ^        ^
#                        |       |        |        |
#                              Start of search
#
# all above can then be called as many times for different depths
# the above section is of depth 1
#
# ---------------------------------------------------------------------------------------

def searchv3(colour,searchMoves = [],depth = 1):
    #chosenMove,extraInfo,newEvaluation
    resetData(searchMoves)
    startEval = evaluate()
    moves = generateAllMoves(colour,False,searchMoves)
    opponentColour = switchColours(colour)
    allEndDepthMoves = []

    for move in moves:
        resetData(searchMoves)
        opponentMoves = generateAllMoves(opponentColour,False,searchMoves)
        bestOpponentMove, extraInfo, bestOpponentEval = search(opponentMoves,opponentColour,searchMoves + [move])
        
        if depth - 1 != 0:
            bestOpponentEval,newMove,extraInfo = searchv3(colour,searchMoves + [move,bestOpponentMove],depth - 1)
            allEndDepthMoves = allEndDepthMoves + [[bestOpponentEval,move,extraInfo]]
        else:
            allEndDepthMoves = allEndDepthMoves + [[bestOpponentEval,move,extraInfo]]

    bestMove = None
    if len(allEndDepthMoves) > 0:
        bestMove = allEndDepthMoves[0]

    for i in range(len(allEndDepthMoves)):
        if colour == "WHITE":
            if allEndDepthMoves[i][0] > bestMove[0]:
                bestMove = allEndDepthMoves[i]
        else:
            if allEndDepthMoves[i][0] < bestMove[0]:
                bestMove = allEndDepthMoves[i]

    if bestMove != None:
        return bestMove[0],bestMove[1],bestMove[2]
    else:
        return None,None,None
    
    
##################################################################################################################################################################################
##################################################################################################################################################################################
################################################################ Used to create bitboards from 2d array ##########################################################################
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

def convertToBitBoard(board,castlingData,enPassant):

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

    global Checkmate
    Checkmate = False

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

    # castling setup
    global wKingMoved
    global wRooksMoved

    global bKingMoved
    global bRooksMoved

    global wqueenSide
    global wkingSide
    global bqueenSide
    global bkingSide

    wkingSide = "K" in castlingData
    wqueenSide = "Q" in castlingData
    bkingSide = "k" in castlingData
    bqueenSide = "q" in castlingData

    wKingMoved = whiteKing
    wRooksMoved = whiteRooks

    bKingMoved = blackKing
    bRooksMoved = blackRooks

    # enPassant setup

    if "-" not in enPassant:
        file = ord(enPassant[0].lower()) - 97
        rank = 8 - int(enPassant[1])
        direction = 0

        print(rank,file)

        if rank == 2:
            direction = -1
        elif rank == 5:
            direction = 1

        currentSquareIndex = (rank * 8) + file
        cameFrom = currentSquareIndex + (8 * direction) 
        goingTo = currentSquareIndex + (8 * direction * -1) 

        global lastMove
        lastMove = [cameFrom,goingTo] # enables the isEnPassant flag to be triggered when generating moves

        print(enPassant)
        print(lastMove)
        UI.sleep(4)

    # all data together
    global currentBoardFullData
    castlingData = [wkingSide,wqueenSide,wKingMoved,wRooksMoved,bkingSide,bqueenSide,bKingMoved,bRooksMoved]
    whitePiecesData = [whitePawns, whiteBishops, whiteHorses, whiteRooks, whiteQueens, whiteKing]
    blackPiecesData = [blackPawns, blackBishops, blackHorses, blackRooks, blackQueens, blackKing]
    currentBoardFullData = [whitePiecesData,blackPiecesData,castlingData]

def resetData(searchMoves = []): 
    global currentBoardFullData
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

    global wKingMoved
    global wRooksMoved

    global bKingMoved
    global bRooksMoved

    global wqueenSide
    global wkingSide
    global bqueenSide
    global bkingSide

    global whitePieces
    global blackPieces

    whitePawns = currentBoardFullData[0][0]
    whiteBishops = currentBoardFullData[0][1]
    whiteHorses = currentBoardFullData[0][2]
    whiteRooks = currentBoardFullData[0][3]
    whiteQueens = currentBoardFullData[0][4]
    whiteKing = currentBoardFullData[0][5]

    blackPawns = currentBoardFullData[1][0] 
    blackBishops = currentBoardFullData[1][1]
    blackHorses = currentBoardFullData[1][2]
    blackRooks = currentBoardFullData[1][3]
    blackQueens = currentBoardFullData[1][4]
    blackKing = currentBoardFullData[1][5]
    
    wkingSide = currentBoardFullData[2][0] 
    wqueenSide = currentBoardFullData[2][1] 
    wKingMoved = currentBoardFullData[2][2] 
    wRooksMoved = currentBoardFullData[2][3] 
    bkingSide = currentBoardFullData[2][4] 
    bqueenSide = currentBoardFullData[2][5] 
    bKingMoved = currentBoardFullData[2][6] 
    bRooksMoved = currentBoardFullData[2][7] 
    
    whitePieces = whitePawns | whiteBishops | whiteHorses | whiteRooks | whiteQueens | whiteKing
    blackPieces = blackPawns | blackBishops | blackHorses | blackRooks | blackQueens | blackKing
    bitWordBoard = whitePieces | blackPieces

    if searchMoves != []:
        turnIndex = 0
        for j in searchMoves:
            turnIndex = turnIndex + 1
            if turnIndex % 2 == 1:
                makeMove(int(math.pow(2,j[0])),int(math.pow(2,j[1])),enemyColour,True)  
            else:
                makeMove(int(math.pow(2,j[0])),int(math.pow(2,j[1])),playerColour,True) 

def setupUIEvents(eventListener):
    global signalGameUIEvents
    signalGameUIEvents = eventListener