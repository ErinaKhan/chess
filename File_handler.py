import keyboard
import random
from os import system, name
from time import sleep

def clear():
   # for windows
   if name == 'nt':
      _ = system('cls')

   # for mac and linux
   else:
      _ = system('clear')

def load(gameType):
    colour = None
    playerTurn = None
    TurnNumber = None
    board = None

    if gameType == "new":
        
        colour = giveRandomColour()
        playerTurn = False
        TurnNumber = 1
        
        if colour == "White":
            playerTurn = True
            
        board = boardSetup(colour)
    else: # loading a previously played unfinished game
        pass
    
    return colour,playerTurn,TurnNumber,board

def gameConfig():
    index = 0
    b1 = "<"
    b2 = " "
    sleep(1)
    while True:
        print(f"New Game {b1}")
        print(f"Load Game ({gamesAvailable()}) {b2}")
        
        if keyboard.read_key() == "enter":
            clear()
            if index == 0:
                return "new"
            else:
                return "old"
        elif keyboard.read_key() == "up" and index == 1:
            index = 0
            b1 = "<"
            b2 = " " 
        elif keyboard.read_key() == "down" and index == 0:
            index = 1
            b1 = " "
            b2 = "<"
        clear()

def boardSetup(playerColour): # needs to flip the board depending on what pieces the player has
    board = None

    if playerColour == "White":
        board = [['♖','♘','♗','♕','♔','♗','♘','♖'],
                 ['♙','♙','♙','♙','♙','♙','♙','♙'],
                 [' ',' ',' ',' ',' ',' ',' ',' '],
                 [' ',' ',' ',' ',' ',' ',' ',' '],
                 [' ',' ',' ',' ',' ',' ',' ',' '],
                 [' ',' ',' ',' ',' ',' ',' ',' '],
                 ['♟','♟','♟','♟','♟','♟','♟','♟'],
                 ['♜','♞','♝','♛','♚','♝','♞','♜']]
    else:
        board = [['♜','♞','♝','♛','♚','♝','♞','♜'],
                 ['♟','♟','♟','♟','♟','♟','♟','♟'],
                 [' ',' ',' ',' ',' ',' ',' ',' '],
                 [' ',' ',' ',' ',' ',' ',' ',' '],
                 [' ',' ',' ',' ',' ',' ',' ',' '],
                 [' ',' ',' ',' ',' ',' ',' ',' '],
                 ['♙','♙','♙','♙','♙','♙','♙','♙'],
                 ['♖','♘','♗','♕','♔','♗','♘','♖']]
    return board

def giveRandomColour():
    if random.randint(0,1) == 0:
        return "White"
    else:
        return "Black"
        
def gamesAvailable(): # code stub
    # will show player how many games they have on going
    return "No games found"
