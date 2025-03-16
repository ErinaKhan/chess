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
TUTORIAL_SECTION_PADDING = 80

back_btn = pygame.image.load(r"imagesMisc\undo.png")
arrowU = pygame.image.load(r"imagesMisc\arrow_up.png")#
arrowD = pygame.image.load(r"imagesMisc\arrow_down.png")
exitButton = utils.Button(20,SCREEN_HEIGHT * 0.8,back_btn,0.25)
arrowButtonUp = utils.Button(SCREEN_WIDTH * 0.85,SCREEN_HEIGHT * 0.08,arrowU,0.35)
arrowButtonDown = utils.Button(SCREEN_WIDTH * 0.85,SCREEN_HEIGHT * 0.8,arrowD,0.35)

allSections = []
sectionButtons = []

def Start():
    running = True
    numberOfSections = 7
    index = 0

    getTutorialSections()
    getSectionRects(numberOfSections)

    while running:
        screen.fill((219, 200, 167))

        pygame.draw.rect(screen,(206,187,155),((SCREEN_WIDTH - INNER_SCREEN_WIDTH) // 2,0,INNER_SCREEN_WIDTH,SCREEN_HEIGHT))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if exitButton.drawButton(screen):
            # exit page
            running = False

        if arrowButtonUp.drawButton(screen):
            if index - 1 >= 0:
                index = index - 1

        if arrowButtonDown.drawButton(screen):
            if index + 7 < len(allSections):
                index = index + 1

        drawButtons(numberOfSections,index)

        pygame.display.update()


def getSectionRects(sectionsToDisplay):
    tutorialSectionHeight = 100
    for i in range(sectionsToDisplay):
        startY = tutorialSectionHeight * i
        buttonRect = pygame.Rect((SCREEN_WIDTH - TUTORIAL_SECTION_WIDTH) // 2,startY * 1.2 + TUTORIAL_SECTION_PADDING,TUTORIAL_SECTION_WIDTH,tutorialSectionHeight)
        sectionButtons.append(buttonRect)

def drawButtons(sectionsToDisplay,index):
    font = pygame.font.Font(None, 36)
    for i in range(sectionsToDisplay):
        button = sectionButtons[i]
        newButton = pygame.draw.rect(screen,(245,245,245),button,border_radius=10)
        surface = font.render(allSections[i+index][0], True, (0,0,0))
        rect = surface.get_rect(center=button.center)
        screen.blit(surface, rect)

def getTutorialSections():
    tutorialData = open("tutorial\dialogue.txt","r")
    for section in tutorialData.readlines():
        if section.count(':') != 0:
            newSection = section.split(':') # array containing [title of section, text to display, board for demo]
            allSections.append([newSection[0],newSection[1],newSection[2]])

    tutorialData.close()


def getUserTutorialProgress():
    return []
