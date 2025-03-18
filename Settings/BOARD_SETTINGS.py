import Engine
import math

pieceToACN = {
    "ROOK": "R",
    "HORSE": "N",
    "BISHOP": "B",
    "QUEEN": "Q",
    "KING": "K",
    "PAWN": "",
}

class UIEvents(): 
    def __init__(self,boardColours = [(181,136,99),(240,217,181),(230, 112, 112)]):
        self.eventFound = False
        self.isCastling = False
        self.isEnpassant = False
        self.isPromoting = False
        self.sideOfCastling = None
        self.eventData = []
        self.moveList = []
        self.boardColours = boardColours # [blackSquareColour,whiteSquareColour,overlayColour] -> list of 3 rgb tuples

    def changeBoardColour(self,colour):
        pass

    def addMoveToTracker(self,pieceMoving,colour,isCapture,isCheck,startSquare,destinationSquare):
        algebraicChessNotationMove = ""

        if not (self.isCastling or self.isEnpassant or self.isPromoting):            
            algebraicChessNotationMove = algebraicChessNotationMove + pieceToACN[pieceMoving]
            
            if isCapture:
                if pieceMoving == "PAWN":
                    algebraicChessNotationMove = algebraicChessNotationMove + self.squareToFileRank(startSquare)[0]

                algebraicChessNotationMove = algebraicChessNotationMove + "x"

            algebraicChessNotationMove = algebraicChessNotationMove + self.squareToFileRank(destinationSquare)

            if isCheck:
                algebraicChessNotationMove = algebraicChessNotationMove + "+"
        
        elif self.isCastling:
            if self.sideOfCastling == "QUEENSIDE":
                algebraicChessNotationMove = "O-O-O"
            else:
                algebraicChessNotationMove = "O-O"
        elif self.isEnpassant:
            algebraicChessNotationMove = self.squareToFileRank(startSquare)[0] + "x" + self.squareToFileRank(destinationSquare)
            pass
        elif self.isPromoting:
            algebraicChessNotationMove = self.squareToFileRank(destinationSquare) + pieceToACN[Engine.getPieceTypeFromSquare(int(math.pow(2,destinationSquare)))]
            pass
        else:
            return " "

        self.moveList = self.moveList + [algebraicChessNotationMove]


    def squareToFileRank(self, square):
        rank = (square // 8)
        file = square - (rank * 8)
        if Engine.playerColour == "WHITE":
            rank = 8 - rank
            return chr(97 + file)+str(rank) 
        else:
            file = 7 - file
            return chr(97 + file)+str(rank + 1)

    def colourBlindMode(self):
        self.changeBoardColour(None)

    def emitCastleEvent(self,rookMoves,sideOfCastle):
        self.isCastling = True
        self.sideOfCastling = sideOfCastle
        self.eventData = rookMoves

    def emitEnPassantEvent(self,piece):
        self.isEnpassant = True
        self.eventData = [piece]

    def emitPromotionEvent(self,move,colour,piece):
        self.isPromoting = True
        self.eventData = [move,colour,piece]

    def getEvents(self):
        return [self.isCastling,self.isPromoting,self.isEnpassant]
    
    def resetEvents(self):
        self.eventFound = False
        self.isCastling = False
        self.isEnpassant = False
        self.isPromoting = False
        self.sideOfCastling = None
        self.eventData = []

    def getEventData(self):
        return self.eventData
    
    def getMoveList(self):
        return self.moveList