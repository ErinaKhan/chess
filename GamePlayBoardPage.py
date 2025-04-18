import pygame
import Engine
import os
import math
import Pygame_Utils as utils
import pyTimer as timer
import File_handler as FileHandler
import Settings.BOARD_SETTINGS as gameSettings


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
pygame.display.set_caption('Play')

SQUARE_SIZE = 100
OUTERBOARD_OFFSET = 15
BOARD_START_X = int((SCREEN_WIDTH - (SQUARE_SIZE * 8)) / 2)
BOARD_START_Y = int((SCREEN_HEIGHT - (SQUARE_SIZE * 8)) / 2)
BLACK_SQUARE_COLOUR = (181,136,99)
WHITE_SQUARE_COLOUR = (240,217,181)
OVERLAY_SQUARE_COLOUR = (230, 112, 112)

PIECE_SIZE = SQUARE_SIZE - (0.1 * SQUARE_SIZE)
PIECE_PLACEMENT = int((SQUARE_SIZE - PIECE_SIZE) / 2)

pawn_white = None
rook_white = None
knight_white = None
bishop_white = None
king_white = None
queen_white = None
pawn_black = None
rook_black = None
knight_black = None
bishop_black = None
king_black =None
queen_back =None
back_btn =None
help_btn =None
home_btn = None

try: # for windows users
    pawn_white = pygame.image.load(r"ChessPieces\wp.png")
    rook_white = pygame.image.load(r"ChessPieces\wr.png")
    knight_white = pygame.image.load(r"ChessPieces\wn.png")
    bishop_white = pygame.image.load(r"ChessPieces\wb.png")
    king_white = pygame.image.load(r"ChessPieces\wk.png")
    queen_white = pygame.image.load(r"ChessPieces\wq.png")

    pawn_black = pygame.image.load(r"ChessPieces\bp.png")
    rook_black = pygame.image.load(r"ChessPieces\br.png")
    knight_black = pygame.image.load(r"ChessPieces\bn.png")
    bishop_black = pygame.image.load(r"ChessPieces\bb.png")
    king_black = pygame.image.load(r"ChessPieces\bk.png")
    queen_back = pygame.image.load(r"ChessPieces\bq.png")

    back_btn = pygame.image.load(r"Images\undo.png")
    help_btn = pygame.image.load(r"Images\help.png")
    home_btn = pygame.image.load(r"Images\home.png")
except: # for mac users
    pawn_white = pygame.image.load(r"ChessPieces/wp.png")
    rook_white = pygame.image.load(r"ChessPieces/wr.png")
    knight_white = pygame.image.load(r"ChessPieces/wn.png")
    bishop_white = pygame.image.load(r"ChessPieces/wb.png")
    king_white = pygame.image.load(r"ChessPieces/wk.png")
    queen_white = pygame.image.load(r"ChessPieces/wq.png")

    pawn_black = pygame.image.load(r"ChessPieces/bp.png")
    rook_black = pygame.image.load(r"ChessPieces/br.png")
    knight_black = pygame.image.load(r"ChessPieces/bn.png")
    bishop_black = pygame.image.load(r"ChessPieces/bb.png")
    king_black = pygame.image.load(r"ChessPieces/bk.png")
    queen_back = pygame.image.load(r"ChessPieces/bq.png")

    back_btn = pygame.image.load(r"Images/undo.png")
    help_btn = pygame.image.load(r"Images/help.png")
    home_btn = pygame.image.load(r"Images/home.png")


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

allPieces = []

def drawPiece(boardx,boardy,i,j):
    currentSquareIndex = (i * 8) + j
    squareBinary = int(math.pow(2,currentSquareIndex))
    colour = str(Engine.getColour(squareBinary))
    piece = str(Engine.getPieceTypeFromSquare(squareBinary))
    
    if colour+piece != "NONENONE": # if not empty square
        new_piece = image_lookup[colour+piece]
        new_piece = pygame.transform.scale(new_piece, (100,100))
        pieceButton = utils.chessPiece(colour,currentSquareIndex,boardx,boardy,new_piece)
        return pieceButton

def drawPieces():

    for i in range(8):
        for j in range(8):
            boardx = BOARD_START_X + (SQUARE_SIZE * j)
            boardy = BOARD_START_Y + (SQUARE_SIZE * i)
            piece = drawPiece(boardx,boardy,i,j)
            if piece != None:
                allPieces.append(piece)


def drawBoard(fen=""):

    settings = setup(fen)

    allPieces.clear()
    
    running = True
    overlay = []
    newOverlay = []
    overlaySquares = []
    trackedMoves = []
    selectedPiece = None
    playerTurn = Engine.playerColour == "WHITE"
    i = 0
    text = ""
    drawPieces()

    timerMins = 0.05
    AIMoveDelayTimer = timer.Timer(int(timerMins * 60 * 1000))

    gameTimerMins = 4
    AITimer = timer.Timer(int(gameTimerMins * 60 * 1000))
    PlayerTimer = timer.Timer(int(gameTimerMins * 60 * 1000))

    AIMoveDelayTimer.start()   
    PlayerTimer.start()
    AITimer.start()

    while running:

        screen.fill((219, 200, 167))

        if PlayerTimer.active:
            PlayerTimer.update()

        if AITimer.active:
            AITimer.update()

        if exitButton.drawButton(screen):
            # exit page
            running = False

        if helpButton.drawButton(screen):
            # do help stuff
            import TutorialPage 
            TutorialPage.Start()

        # draws outer edge to the board
        pygame.draw.rect(screen,(107, 70, 44),(BOARD_START_X - OUTERBOARD_OFFSET,BOARD_START_Y - OUTERBOARD_OFFSET,(SQUARE_SIZE * 8) + (2 * OUTERBOARD_OFFSET),(SQUARE_SIZE * 8) + (2 * OUTERBOARD_OFFSET)),border_radius=10)

        # if the piece selected is different to the current piece selected it will add the new squares to a list so they can be higlighted red later    
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

        #-------------------------------------------------------------------------------------------
        # draws all of the squares in the board aswell as pieces

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
        #-------------------------------------------------------------------------------------------

        if not Engine.Checkmate and not Engine.Stalemate:
            if playerTurn: # runs the players turn
                AITimer.pause()
                AIMoveDelayTimer.pause()
                for square in overlaySquares:
                    if square.drawButton(screen) and selectedPiece != None :
                        start = int(math.pow(2,selectedPiece.coordinates))
                        destination = int(math.pow(2,square.coordinates))
                        Engine.makeMove(start,destination,selectedPiece.colour,False,None)
                        allPieces[allPieces.index(selectedPiece)].move(screen,square.x,square.y,square.coordinates)
                        disposeOfPiece(Engine.enemyColour,square.coordinates)
                        playerTurn = False
                        selectedPiece = None
                        newOverlay = []
                        allMoves = []
                        trackedMoves = settings.getMoveList()
                        AITimer.unpause()
            else: # runs the AIs turn
                PlayerTimer.pause()
                AIMoveDelayTimer.unpause()
                if AIMoveDelayTimer.active:
                    AIMoveDelayTimer.update()

                if AIMoveDelayTimer.timeRanOut: # timer delay so the AI doesnt always move instantly
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
                                allPieces[allPieces.index(piece)].move(screen,x,y,chosenMove[1])
                                disposeOfPiece(Engine.playerColour,chosenMove[1])
                    else:
                        running = False

                    trackedMoves = settings.getMoveList()
                    AIMoveDelayTimer.reset(int(timerMins * 60 * 1000))
                    PlayerTimer.unpause()
        else:
            running = False # if its checkmate the game stops running
        
        for piece in allPieces:
            if piece.drawButton(screen) and piece.colour == Engine.playerColour: # if the player selects a piece of their colour
                allMoves = Engine.filterMovesBySquare(piece.coordinates,piece.colour) # gets where they can move
                selectedPiece = piece
                newOverlay = []
                for move in allMoves:
                    newOverlay = newOverlay + [move[1]] # adds to new overlay

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        allEvents = settings.getEvents()
        if allEvents != [False,False,False]: #[castling,promoting,enpassant]
            data = settings.getEventData()

            if allEvents[0]:
                castle(data[0],data[1])

            if allEvents[1]:
                promote(data[0],data[1],data[2])

            if allEvents[2]:
                passant(data[0])

            print(allEvents)
            settings.resetEvents()


        PlayerTimer.drawTimerUI(screen,SCREEN_WIDTH * 0.2,SCREEN_HEIGHT * 0.8,60,100)
        AITimer.drawTimerUI(screen,SCREEN_WIDTH * 0.2,SCREEN_HEIGHT * 0.1,60,100)
        drawMoveTracker(trackedMoves)
        pygame.display.update()

    if Engine.Checkmate or Engine.Stalemate:
        winLossScreen(playerTurn)

def drawMoveTracker(moves):
    trackerRect = pygame.Rect(BOARD_START_X + (SQUARE_SIZE * 9)  + (2 * OUTERBOARD_OFFSET) ,BOARD_START_Y - OUTERBOARD_OFFSET,(SQUARE_SIZE * 3)  + (2 * OUTERBOARD_OFFSET),(SQUARE_SIZE * 8) + (2 * OUTERBOARD_OFFSET))
    pygame.draw.rect(screen,(219, 219, 219),trackerRect,border_radius=10)
    fontSize = 24
    font = pygame.font.Font(None, fontSize)
    fullMoveNum = 0
    for i in range(len(moves)):
        if i != 0 and (i + 1) % 2 == 0:
            surface = font.render(str(i // 2 + 1) + ". " + moves[i - 1] + "  " + moves[i], True, (0,0,0))
            rect = surface.get_rect(center=(trackerRect.midtop[0],(trackerRect.midtop[1]) + fontSize +((i // 2) * fontSize)))
            screen.blit(surface, rect)
            fullMoveNum = (i + 1) // 2
    
    if len(moves) % 2 != 0:
        surface = font.render(str(fullMoveNum + 1) + ". " + moves[-1], True, (0,0,0))
        rect = surface.get_rect(center=(trackerRect.midtop[0],(trackerRect.midtop[1]) + fontSize + (fullMoveNum * fontSize)))
        screen.blit(surface, rect)
        
def opponentTurn(colour):
    moves = Engine.generateAllMoves(colour,False)
    chosenMove,extraInfo,newEvaluation = Engine.search(moves,colour)
    if len(moves) > 0:
        Engine.makeMove(int(math.pow(2,chosenMove[0])),int(math.pow(2,chosenMove[1])),colour,False,extraInfo)    
        return chosenMove
   
    return None

def disposeOfPiece(colour,disposeSquare):
    for piece in allPieces:
        if piece.coordinates == disposeSquare and (colour == piece.colour or colour == "ANY"):
            allPieces[allPieces.index(piece)].destroy()

def removeOverlay(overlay):
    for square in overlay:
        overlay[overlay.index(square)].destroy()

def setup(fen=""):
    Engine.precomputeSquaresToEdge()
    colour,playerTurn,newBoard,castlingData,enPassant = FileHandler.load(FileHandler.gameConfig(fen != ""),fen) # loads new game or previous game
    enemyColour = Engine.assignColours(colour)
    Engine.convertToBitBoard(newBoard,castlingData,enPassant)
    settings = gameSettings.UIEvents()
    Engine.setupUIEvents(settings)
    return settings

def winLossScreen(turn):
    running = True

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
        if Engine.Stalemate:
            text_surface = font.render("Stalemate", True, (0,0,0))
        else:
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

def castle(rookStart,rookEnd):
    for piece in allPieces:
        if piece.coordinates == rookStart:
            x = rookEnd % 8
            y = int(rookEnd // 8)
            x = BOARD_START_X + (SQUARE_SIZE * x)
            y = BOARD_START_Y + (SQUARE_SIZE * y)
            allPieces[allPieces.index(piece)].move(screen,x,y,rookEnd)

def promote(coordinate,colour,newPiece):
    print(coordinate)
    for piece in allPieces:
        if piece.coordinates == coordinate:
            piece.changeImage(pygame.transform.scale(image_lookup[colour+newPiece], (100,100)))

def passant(pieceToDestroy):
    for piece in allPieces:
        if piece.coordinates == pieceToDestroy:
            disposeOfPiece("ANY",pieceToDestroy)
