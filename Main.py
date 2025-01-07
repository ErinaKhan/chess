####################################################################################
#################################### CHESS GAME ####################################
####################################################################################

#-------------------------------------- SETUP --------------------------------------
import Engine
import random
import File_handler as FileHandler
import UI_Handler as UI
import math
#------------------------------------ FUNCTIONS ------------------------------------

def startGame():
    
    # main loop of program
    Engine.precomputeSquaresToEdge()
    colour,playerTurn,newBoard = FileHandler.load(FileHandler.gameConfig()) # loads new game or previous game
    enemyColour = Engine.assignColours(colour)
    Engine.convertToBitBoard(newBoard)

    print(f"\nYour colour is {colour}!\n")
    print("isYourTurn: " + str(playerTurn) + "\n")
    
    UI.drawBoard(None)

    resigning = False

    while True:

        if playerTurn:
            resigning = playersTurn(colour)
        else:
            AITurn(enemyColour)
        
        UI.drawBoard(None)
        
        if hasWon():
            if playerTurn:
                print("You Won")
            else:
                print("You Lost, Better luck next time!")
                
            print("\n\nReturning To Menu...")
            UI.clear()
            startGame()
        else:
            if resigning:
                UI.clear()
                print("thanks for playing!!")
                break
            elif playerTurn:
                print("AI turn")
                playerTurn = False
            else:
                print("Player Turn")
                playerTurn = True

def playersTurn(colour):
    valid = False
    while not valid:
        square,isResigning = selectPiece(colour) 

        if not isResigning:
            legalMoves = Engine.filterMovesBySquare(int(math.log(square,2)),colour)
            valid = len(legalMoves) > 0
            if valid:
                chosenLegalMove = selectDestination(square,legalMoves,UI.createOverlay(legalMoves))
                Engine.updateBoard(square,int(math.pow(2,chosenLegalMove)),colour)
                return False
            else:
                print("\nThis piece cant move, try again")
                UI.sleep(1.5)
        else:
            valid = True
            return True
    
def AITurn(colour):
    moves = Engine.generateAllMoves(colour)
    print(moves)
    index = random.randint(0, len(moves) - 1)
    chosenMove = moves[index]
    print(chosenMove)
    UI.sleep(10)
    Engine.makeMove(int(math.pow(2,chosenMove[0])),int(math.pow(2,chosenMove[1])),colour,False)
    pass

def hasWon(): # code stub
    # someone wins if isInCheck() == True and kingMoves() == []
    return False
                
def mainMenu():
    pass

def validCoordinates(coordinates):
    return len(coordinates) == 2 and coordinates[0].lower() in ['a','b','c','d','e','f','g','h'] and coordinates[1] in ['1','2','3','4','5','6','7','8']

def coordinatesToBinary(coordinates):
    file = ord(coordinates[0].lower()) - 97
    rank = 8 - int(coordinates[1])
    currentSquareIndex = (rank * 8) + file
    currentSquareInBinary = int(math.pow(2,currentSquareIndex))
    return currentSquareInBinary

def selectPiece(colour):
    chosenCoordinates = "XX"
    currentSquareInBinary = None
    while Engine.getColour(currentSquareInBinary) != colour:
        chosenCoordinates = "XX"
        UI.clear()
        UI.drawBoard(None)
        while not validCoordinates(chosenCoordinates):
            chosenCoordinates = input("\n\nEnter the coordinates on the chess board (such as A8,a8,b5 etc...) of the piece you would like to move or type 'resign' to resign\n\nInput: ")
            if chosenCoordinates == "resign":
                return None, True

        currentSquareInBinary = coordinatesToBinary(chosenCoordinates)

    return currentSquareInBinary,False

def selectDestination(square,legalMoves,overlay):
    chosenCoordinates = "XX"
    currentSquareInBinary = None
    legal = False
    while not legal:
        chosenCoordinates = "XX"
        UI.clear()
        UI.drawBoard(overlay)

        while not validCoordinates(chosenCoordinates):
            chosenCoordinates = input(f"\n\nEnter a legal location to move the {Engine.getPieceTypeFromSquare(square)} too\n\nInput: ")
            
        currentSquareInBinary = coordinatesToBinary(chosenCoordinates)
    
        for move in legalMoves:
            if move[1] == int(math.log(currentSquareInBinary,2)):
                legal = True

    return int(math.log(currentSquareInBinary,2))

startGame()


