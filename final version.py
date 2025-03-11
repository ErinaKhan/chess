import pygame

# pygame initialization
pygame.init()

# dimensions of screen
screen = pygame.display.set_mode((1280, 960))

# load the images
chess = pygame.image.load("chess123.jpg")
start_img = pygame.image.load("start_btn.png").convert_alpha()
exit_img = pygame.image.load("exit_btn.png").convert_alpha()

# scale the images
chess = pygame.transform.scale(chess, (1280, 960))

# caption of the screen
pygame.display.set_caption('En Passant')

# button class
class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
    def draw(self):
        # draw button
        action = False
        pos = pygame.mouse.get_pos()
        
        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                print("button clicked")
                action = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        screen.blit(self.image, (self.rect.x, self.rect.y))
        return action

# create button instances with adjusted positions
start_button = Button(640 - start_img.get_width() // 2, 700, start_img, 0.75)  # Centered horizontally
exit_button = Button(960, 700, exit_img, 0.65)  # Positioned on the right

# variable to keep the game loop running
running = True

# game loop
while running:
    screen.blit(chess, (0, 0))
    if start_button.draw():
        print("start")
    if exit_button.draw():
        print("exit")

    # loop through the event queue
    for event in pygame.event.get():
        # check for QUIT event
        if event.type == pygame.QUIT:
            running = False

    # update the display using flip
    pygame.display.flip()

# Quit
pygame.quit()
