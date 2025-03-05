import pygame
import Engine
import os
import math
import Pygame_Utils as utils

pygame.init()

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

'''white = (232,46,46), black = (0,0,0)
white = (99,228,247), black (0,0,0)
White = (187, 207, 186), Black = (80, 158, 74)
White = (184, 129, 77), Black = (184, 88, 77)
White = (97, 245, 167), Black = (34, 148, 242)
White = (0,0,0), Black = (255,255,255)
White = (235,236,208), Black = (119,149,86) - chess.com board
White = (240,217,181), Black = (181,136,99) - lichess board'''

clock = pygame.time.Clock

exitButton = utils.Button(20,SCREEN_HEIGHT * 0.8,back_btn,0.25)
helpButton = utils.Button(SCREEN_WIDTH * 0.95,10,help_btn,0.15)

#pawn_rect.topleft = (BOARD_START_X,BOARD_START_Y + SQUARE_SIZE)

allPieces = []

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

def drawBoard():
    running = True
    overlay = []
    newOverlay = []
    overlaySquares = []
    selectedPiece = None
    drawPieces()

    while running:

        
        screen.fill((219, 200, 167))
        drawMoveTracker()

        if exitButton.drawButton(screen):
            # exit page
            running = False

        if helpButton.drawButton(screen):
            # do help stuff
            pass

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
                currentSquareIndex = (i * 8) + j

                
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
        
        for square in overlaySquares:
            if square.drawButton(screen) and selectedPiece != None:
                print(f"{selectedPiece.coordinates} is going to {square.coordinates}")
                start = int(math.pow(2,selectedPiece.coordinates))
                destination = int(math.pow(2,square.coordinates))
                Engine.makeMove(start,destination,selectedPiece.colour,False,None)
                allPieces[allPieces.index(selectedPiece)].move(screen,square.x,square.y,square.coordinates)
                selectedPiece = None
                newOverlay = []
                

        for piece in allPieces:
            if piece.drawButton(screen):
                allMoves = Engine.filterMovesBySquare(piece.coordinates,piece.colour)
                selectedPiece = piece
                newOverlay = []
                for move in allMoves:
                    newOverlay = newOverlay + [move[1]]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.update()
            

    pygame.quit()

def drawMoveTracker():
    pygame.draw.rect(screen,(219, 219, 219),(BOARD_START_X + (SQUARE_SIZE * 9)  + (2 * OUTERBOARD_OFFSET) ,BOARD_START_Y - OUTERBOARD_OFFSET,(SQUARE_SIZE * 3)  + (2 * OUTERBOARD_OFFSET),(SQUARE_SIZE * 8) + (2 * OUTERBOARD_OFFSET)),border_radius=10)


drawBoard()