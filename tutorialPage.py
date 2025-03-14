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
TUTORIAL_SECTION_WIDTH = INNER_SCREEN_WIDTH * 0.85
TUTORIAL_SECTION_PADDING = 50

back_btn = pygame.image.load(r"imagesMisc\undo.png")
exitButton = utils.Button(20,SCREEN_HEIGHT * 0.8,back_btn,0.25)

def Start():
    running = True
    numberOfSections = 6


    while running:
        screen.fill((219, 200, 167))

        pygame.draw.rect(screen,(206,187,155),((SCREEN_WIDTH - INNER_SCREEN_WIDTH) // 2,0,INNER_SCREEN_WIDTH,SCREEN_HEIGHT))
        addAllSections(numberOfSections)

        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

        if exitButton.drawButton(screen):
            # exit page
            running = False

        pygame.display.update()

def addAllSections(numberOfSections):
    tutorialSectionHeight = 100
    for section in range(numberOfSections):
        startY = tutorialSectionHeight * section
        pygame.draw.rect(screen,(245,245,245),((SCREEN_WIDTH - TUTORIAL_SECTION_WIDTH) // 2,startY * 1.2 + TUTORIAL_SECTION_PADDING,TUTORIAL_SECTION_WIDTH,tutorialSectionHeight),border_radius=10)


def getTutorialSections():
    return []

def getUserTutorialProgress():
    return []
