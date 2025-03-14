import pygame
import Engine
import os
import math
import Pygame_Utils as utils
import pyTimer as timer
import File_handler as FileHandler
import GAME_SETTINGS as gameSettings

pygame.init()

Engine.precomputeSquaresToEdge()
colour,playerTurn,newBoard,castlingData,enPassant = FileHandler.load(FileHandler.gameConfig()) # loads new game or previous game
enemyColour = Engine.assignColours(colour)
Engine.convertToBitBoard(newBoard,castlingData,enPassant)

os.environ['SDL_VIDEO_CENTERED'] = '1'
info = pygame.display.Info()

SCREEN_WIDTH = info.current_w
SCREEN_HEIGHT = info.current_h

screen = pygame.display.set_mode((SCREEN_WIDTH - 10,SCREEN_HEIGHT- 50),pygame.RESIZABLE)
pygame.display.set_caption('DEMO')

SQUARE_SIZE = 100
OUTERBOARD_OFFSET = 15
BOARD_START_X = int((SCREEN_WIDTH - (SQUARE_SIZE * 8)) / 2)
BOARD_START_Y = int((SCREEN_HEIGHT - (SQUARE_SIZE * 8)) / 2)
BLACK_SQUARE_COLOUR = (181,136,99)
WHITE_SQUARE_COLOUR = (240,217,181)
OVERLAY_SQUARE_COLOUR = (230, 112, 112)

PIECE_SIZE = SQUARE_SIZE - (0.1 * SQUARE_SIZE)
PIECE_PLACEMENT = int((SQUARE_SIZE - PIECE_SIZE) / 2)

pawn_white = pygame.image.load(r"chessPieces\wp.png")
rook_white = pygame.image.load(r"chessPieces\wr.png")
knight_white = pygame.image.load(r"chessPieces\wn.png")
bishop_white = pygame.image.load(r"chessPieces\wb.png")
king_white = pygame.image.load(r"chessPieces\wk.png")
queen_white = pygame.image.load(r"chessPieces\wq.png")

pawn_black = pygame.image.load(r"chessPieces\bp.png")
rook_black = pygame.image.load(r"chessPieces\br.png")
knight_black = pygame.image.load(r"chessPieces\bn.png")
bishop_black = pygame.image.load(r"chessPieces\bb.png")
king_black = pygame.image.load(r"chessPieces\bk.png")
queen_back = pygame.image.load(r"chessPieces\bq.png")

back_btn = pygame.image.load(r"imagesMisc\undo.png")
help_btn = pygame.image.load(r"imagesMisc\help.png")
home_btn = pygame.image.load(r"imagesMisc\home.png")


image_lookup = {
    "BLACKROOK": rook_black,
    "BLACKHORSE": knight_black,
    "BLACKBISHOP": bishop_black,
    "BLACKQUEEN": queen_back,
    "BLACKKING": king_black,
    "BLACKPAWN": pawn_black,
    "WHITEROOK": rook_white,
    "WHITEHORSE": knight_white,
    "WHITEBISHOP": bishop_white,
    "WHITEQUEEN": queen_white,
    "WHITEKING": king_white,
    "WHITEPAWN": pawn_white,
    "NONENONE": None,
    "MOVEOVERLAY": None
}

'''potential colour schemes

white = (232,46,46), black = (0,0,0)
white = (99,228,247), black (0,0,0)
White = (187, 207, 186), Black = (80, 158, 74)
White = (184, 129, 77), Black = (184, 88, 77)
White = (97, 245, 167), Black = (34, 148, 242)
White = (0,0,0), Black = (255,255,255)
White = (235,236,208), Black = (119,149,86) - chess.com board
White = (240,217,181), Black = (181,136,99) - lichess board'''

exitButton = utils.Button(20,SCREEN_HEIGHT * 0.8,back_btn,0.25)
helpButton = utils.Button(SCREEN_WIDTH * 0.95,10,help_btn,0.15)

#pawn_rect.topleft = (BOARD_START_X,BOARD_START_Y + SQUARE_SIZE)

allPieces = []
timerMins = 4
timerExample = timer.Timer(timerMins * 60 * 1000)

def drawPiece(boardx,boardy,i,j):
    currentSquareIndex = (i * 8) + j
    squareBinary = int(math.pow(2,currentSquareIndex))
    colour = str(Engine.getColour(squareBinary))
    piece = str(Engine.getPieceTypeFromSquare(squareBinary))
    
    if colour+piece != "NONENONE":
        new_piece = image_lookup[colour+piece]
        new_piece = pygame.transform.scale(new_piece, (100,100))
        pieceButton = utils.chessPiece(colour,currentSquareIndex,boardx,boardy,new_piece)
        #new_piece = pygame.transform.scale(new_piece, (90,90))
        #pygame.draw.rect(screen,(232,46,46),(boardx + PIECE_PLACEMENT,boardy + PIECE_PLACEMENT,PIECE_SIZE,PIECE_SIZE))
        #screen.blit(new_piece,(boardx + PIECE_PLACEMENT,boardy + PIECE_PLACEMENT))
        return pieceButton

def drawPieces():

    for i in range(8):
        for j in range(8):
            boardx = BOARD_START_X + (SQUARE_SIZE * j)
            boardy = BOARD_START_Y + (SQUARE_SIZE * i)
            piece = drawPiece(boardx,boardy,i,j)
            if piece != None:
                allPieces.append(piece)


timerExample.start()

def drawBoard():

    allPieces.clear()
    
    running = True
    overlay = []
    newOverlay = []
    overlaySquares = []
    selectedPiece = None
    playerTurn = Engine.playerColour == "WHITE"
    i = 0
    text = ""
    drawPieces()

    while running:

        screen.fill((219, 200, 167))
        drawMoveTracker()

        if timerExample.active:
            timerExample.update()
            minutes,seconds = timerExample.time()
            print(f"time {minutes} : {seconds} ")
            print(text)

        if exitButton.drawButton(screen):
            # exit page
            running = False

        if helpButton.drawButton(screen):
            # do help stuff
            if text == "un paused":
                text = "paused"
                timerExample.pause()
            else:
                text = "un paused"
                timerExample.unpause()
            i = i + 1

        pygame.draw.rect(screen,(107, 70, 44),(BOARD_START_X - OUTERBOARD_OFFSET,BOARD_START_Y - OUTERBOARD_OFFSET,(SQUARE_SIZE * 8) + (2 * OUTERBOARD_OFFSET),(SQUARE_SIZE * 8) + (2 * OUTERBOARD_OFFSET)),border_radius=10)

        if overlay != newOverlay:
            overlay = newOverlay
            overlaySquares = []
            for square in overlay:
                #create new overlay square
                x = (square) % 8
                y = int(square // 8)
                boardx = BOARD_START_X + (SQUARE_SIZE * x)
                boardy = BOARD_START_Y + (SQUARE_SIZE * y)
                newSquare = utils.OverlaySquare(square,boardx,boardy,OVERLAY_SQUARE_COLOUR)
                overlaySquares = overlaySquares + [newSquare]

            

        for i in range(8):

            for j in range(8):
                boardx = BOARD_START_X + (SQUARE_SIZE * j)
                boardy = BOARD_START_Y + (SQUARE_SIZE * i)
                
                if i % 2 == 0:
                    if j % 2 == 0:
                        pygame.draw.rect(screen,(WHITE_SQUARE_COLOUR),(boardx,boardy,SQUARE_SIZE,SQUARE_SIZE))
                    else:
                        pygame.draw.rect(screen,(BLACK_SQUARE_COLOUR),(boardx,boardy,SQUARE_SIZE,SQUARE_SIZE))
                else:
                    if j % 2 == 0:
                        pygame.draw.rect(screen,(BLACK_SQUARE_COLOUR),(boardx,boardy,SQUARE_SIZE,SQUARE_SIZE))
                    else:
                        pygame.draw.rect(screen,(WHITE_SQUARE_COLOUR),(boardx,boardy,SQUARE_SIZE,SQUARE_SIZE))

        if not Engine.Checkmate:
            if playerTurn:
                for square in overlaySquares:
                    if square.drawButton(screen) and selectedPiece != None :
                        print(f"{selectedPiece.coordinates} is going to {square.coordinates}")
                        start = int(math.pow(2,selectedPiece.coordinates))
                        destination = int(math.pow(2,square.coordinates))
                        Engine.makeMove(start,destination,selectedPiece.colour,False,None)
                        allPieces[allPieces.index(selectedPiece)].move(screen,square.x,square.y,square.coordinates)
                        disposeOfPiece(Engine.enemyColour,square.coordinates)
                        #allPieces[allPieces.index(selectedPiece)].destroy() <- this will get rid of a piece if taken
                        playerTurn = False
                        selectedPiece = None
                        newOverlay = []
                        allMoves = []
            else:
                playerTurn = True
                selectedPiece = None
                newOverlay = []
                removeOverlay(overlaySquares)
                chosenMove = opponentTurn(Engine.enemyColour)
                if chosenMove != None:
                    for piece in allPieces:
                        if piece.coordinates == chosenMove[0]:
                            x = (chosenMove[1]) % 8
                            y = int(chosenMove[1] // 8)
                            x = BOARD_START_X + (SQUARE_SIZE * x)
                            y = BOARD_START_Y + (SQUARE_SIZE * y)

                            print(f"{chosenMove[0]} is going to {chosenMove[1]}")
                            allPieces[allPieces.index(piece)].move(screen,x,y,chosenMove[1])
                            disposeOfPiece(Engine.playerColour,chosenMove[1])
        else:
            running = False
        
        for piece in allPieces:
            if piece.drawButton(screen) and piece.colour == Engine.playerColour:
                allMoves = Engine.filterMovesBySquare(piece.coordinates,piece.colour)
                selectedPiece = piece
                newOverlay = []
                for move in allMoves:
                    newOverlay = newOverlay + [move[1]]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.update()

    winLossScreen(playerTurn)

def drawMoveTracker():
    pygame.draw.rect(screen,(219, 219, 219),(BOARD_START_X + (SQUARE_SIZE * 9)  + (2 * OUTERBOARD_OFFSET) ,BOARD_START_Y - OUTERBOARD_OFFSET,(SQUARE_SIZE * 3)  + (2 * OUTERBOARD_OFFSET),(SQUARE_SIZE * 8) + (2 * OUTERBOARD_OFFSET)),border_radius=10)

def opponentTurn(colour):
    moves = Engine.generateAllMoves(colour,False)
    #chosenMove,extraInfo,eval = Engine.search(moves,colour)
    #chosenMove,extraInfo,newEvaluation = Engine.search(moves,colour,1,1)
    #newEvaluation,chosenMove = Engine.searchv2(2,colour)
    #print(Engine.search(moves,colour,1,1))
    #chosenMove,extraInfo = Engine.searchWithDepth(2,colour,moves)
    chosenMove,extraInfo,newEvaluation = Engine.search(moves,colour)
    if len(moves) > 0:
        Engine.makeMove(int(math.pow(2,chosenMove[0])),int(math.pow(2,chosenMove[1])),colour,False,extraInfo)    
        return chosenMove
   
    return None

def disposeOfPiece(colour,disposeSquare):
    for piece in allPieces:
        if piece.coordinates == disposeSquare and colour == piece.colour:
            allPieces[allPieces.index(piece)].destroy()

def removeOverlay(overlay):
    for square in overlay:
        overlay[overlay.index(square)].destroy()

def setup():
    Engine.precomputeSquaresToEdge()
    colour,playerTurn,newBoard,castlingData,enPassant = FileHandler.load(FileHandler.gameConfig()) # loads new game or previous game
    enemyColour = Engine.assignColours(colour)
    Engine.convertToBitBoard(newBoard,castlingData,enPassant)

def winLossScreen(turn):
    running = True
    timerExample.pause()

    while running:
        size = (SQUARE_SIZE * 6) + (2*OUTERBOARD_OFFSET)
        locationX = (SCREEN_WIDTH - size) // 2
        locationY = (SCREEN_HEIGHT - size) // 2
        pygame.draw.rect(screen,(219, 200, 167),(locationX,locationY,size,size),border_radius=10)
        size = (SQUARE_SIZE * 6)
        locationX = (SCREEN_WIDTH - size) // 2
        locationY = (SCREEN_HEIGHT - size) // 2
        checkmateScreen = pygame.draw.rect(screen,(255,255,255),(locationX,locationY,size,size),border_radius=10)
        font = pygame.font.Font(None, 120)
        if turn:
            text_surface = font.render("You Win", True, (0,0,0))
        else: 
            text_surface = font.render("You Lose", True, (0,0,0))

        text_rect = text_surface.get_rect(center=(checkmateScreen.center[0],checkmateScreen.top + 60))
        screen.blit(text_surface, text_rect)
        homeButton = utils.Button(0,0,home_btn,0.3)
        homeButton.move(screen,checkmateScreen.centerx - (homeButton.rect.width// 2),checkmateScreen.centery - (homeButton.rect.height // 2) + 180)
        if homeButton.drawButton(screen):
            running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.update()