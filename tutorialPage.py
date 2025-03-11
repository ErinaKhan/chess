import pygame
import os
import Pygame_Utils as utils

pygame.init()

os.environ['SDL_VIDEO_CENTERED'] = '1'
info = pygame.display.Info()

SCREEN_WIDTH = info.current_w
SCREEN_HEIGHT = info.current_h

screen = pygame.display.set_mode((SCREEN_WIDTH - 10,SCREEN_HEIGHT- 50),pygame.RESIZABLE)
pygame.display.set_caption('DEMO')

INNER_SCREEN_WIDTH = SCREEN_WIDTH * 0.8

back_btn = pygame.image.load(r"imagesMisc\undo.png")
exitButton = utils.Button(20,SCREEN_HEIGHT * 0.8,back_btn,0.25)

def Start():
    running = True

    while running:
        screen.fill((219, 200, 167))

        pygame.draw.rect(screen,(206,187,155),((SCREEN_WIDTH - INNER_SCREEN_WIDTH) // 2,0,INNER_SCREEN_WIDTH,SCREEN_HEIGHT))

        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

        if exitButton.drawButton(screen):
            # exit page
            running = False

        pygame.display.update()

def getTutorialSections():
    pass

def drawTutorialUI():
    pass
