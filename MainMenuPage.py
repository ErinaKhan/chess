import pygame
import os

#pygame intialization
pygame.init()

# ------------------------------------------------------------
os.environ['SDL_VIDEO_CENTERED'] = '1'
info = pygame.display.Info() # get users devices screen dimensions

SCREEN_WIDTH = info.current_w # gets width and height of users devices screen
SCREEN_HEIGHT = info.current_h

screen = pygame.display.set_mode((SCREEN_WIDTH - 10,SCREEN_HEIGHT- 50),pygame.RESIZABLE) # fullscreens the display
# ------------------------------------------------------------

#RGB background
background_colour = (244, 225, 193)

# load the image
chess = None

try:
    chess = pygame.image.load(r"Images\chess123.jpg") # not an error just red highlight on vscode
except:
    chess = pygame.image.load(r"Images/chess123.jpg")
    
# scale the img
chess = pygame.transform.scale_by(chess, 2)

chessrect = chess.get_rect()

# caption of the screen
pygame.display.set_caption('En Passant')


# fill the background color
screen.fill(background_colour)

# define the buttons and color
button_color = (255, 0, 0)  # red
text_color = (255, 255, 255)
font = pygame.font.Font(None, 36)

# create the buttons and sizes
play_button = pygame.Rect((SCREEN_WIDTH - 200) // 2, SCREEN_HEIGHT * 0.65 - 50, 200, 50)  # center button moved lower
options_button = pygame.Rect(SCREEN_WIDTH * 0.95 - 250, 800, 250, 50)  # right button moved lower
learn_button = pygame.Rect(SCREEN_WIDTH * 0.05, 800, 250, 50)  # left button moved lower and made longer (width increased)

# function to draw text on buttons
def draw_text(text, button_rect):
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=button_rect.center)
    screen.blit(text_surface, text_rect)

# variable to keep the game loop running
running = True

# game loop
while running:
    # loop through the event queue
    for event in pygame.event.get():
        # check for QUIT event
        if event.type == pygame.QUIT:
            running = False
        
        # check for mouse click on buttons
        if event.type == pygame.MOUSEBUTTONDOWN:
            if play_button.collidepoint(event.pos):

                import GamePlayBoardPage
                GamePlayBoardPage.drawBoard()

            elif options_button.collidepoint(event.pos):

                pass

            elif learn_button.collidepoint(event.pos):

                import TutorialPage
                TutorialPage.Start()

    # fill the screen with the background color
    screen.fill(background_colour)

    # blit the chess image to the screen
    screen.blit(chess, ((SCREEN_WIDTH - chessrect.width) // 2, 80,chessrect.width,chessrect.height))

    # draw the buttons
    pygame.draw.rect(screen, button_color, play_button)
    pygame.draw.rect(screen, button_color, options_button)
    pygame.draw.rect(screen, button_color, learn_button)

    # draw text on the buttons
    draw_text("Play", play_button)
    draw_text("Options", options_button)
    draw_text("Learn How to Play", learn_button)

    # update the display using flip
    pygame.display.flip()

# Quit
pygame.quit()
