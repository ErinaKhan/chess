class UIEvents(): 
    def __init__(self,boardColours = [(181,136,99),(240,217,181),(230, 112, 112)]):
        self.eventFound = False
        self.isCastling = False
        self.isEnpassant = False
        self.isPromoting = False
        self.eventData = []
        self.boardColours = boardColours # [blackSquareColour,whiteSquareColour,overlayColour] -> list of 3 rgb tuples

    def changeBoardColour(self,colour):
        pass

    def colourBlindMode(self):
        self.changeBoardColour(None)

    def emitCastleEvent(self,rookMoves):
        self.isCastling = True
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
        self.eventData = []

    def getEventData(self):
        return self.eventData
