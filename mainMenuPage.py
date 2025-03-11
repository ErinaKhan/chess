import pygame

#pygame intialization
pygame.init()

#RGB background
background_colour = (244, 225, 193)

# dimesnions of screen
screen = pygame.display.set_mode((1280, 960))

# load the image
chess = pygame.image.load("chess123.jpg")
chessrect = chess.get_rect()

# caption of the screen
pygame.display.set_caption('En Passant')

# scale the img
chess = pygame.transform.scale(chess, (1280, 960))

# fill the background color
screen.fill(background_colour)

# define the buttons and color
button_color = (255, 0, 0)  # red
text_color = (255, 255, 255)
font = pygame.font.Font(None, 36)

# create the buttons and sizes
play_button = pygame.Rect(540, 700, 200, 50)  # center button moved lower
options_button = pygame.Rect(1020, 800, 250, 50)  # right button moved lower
learn_button = pygame.Rect(20, 800, 250, 50)  # left button moved lower and made longer (width increased)

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
                pygame.quit()
                import gamePlayBoardPage
                running = False
            elif options_button.collidepoint(event.pos):
                print("Options button clicked!")
            elif learn_button.collidepoint(event.pos):
                print("Learn How to Play button clicked!")

    # fill the screen with the background color
    screen.fill(background_colour)

    # blit the chess image to the screen
    screen.blit(chess, chessrect)

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
