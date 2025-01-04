####################################################################################
#################################### CHESS GAME ####################################
####################################################################################

#-------------------------------------- SETUP --------------------------------------
import Engine
import File_handler as FileHandler
import UI_Handler as UI
#------------------------------------ FUNCTIONS ------------------------------------

def startGame():
    
    # main loop of program
    global board
    
    colour,playerTurn,newBoard = FileHandler.load(FileHandler.gameConfig()) # loads new game or previous game

    board = newBoard

    Engine.convertToBitBoard(board)

    print(f"\nYour colour is {colour}!\n")
    print("isYourTurn: " + str(playerTurn) + "\n")
    
    UI.drawBoard()

    resigning = False

    while True:

        UI.sleep(5)

        if playerTurn:
            resigning = playersTurn(colour)
        else:
            AITurn()
        
        UI.drawBoard()
        
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
    pass

def AITurn():
    pass

def hasWon(): # code stub
    # someone wins if isInCheck() == True and kingMoves() == []
    return False
                
def mainMenu():
    pass

def selectPiece(colour):
    pass

startGame()