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
TUTORIAL_SECTION_WIDTH = INNER_SCREEN_WIDTH * 0.7
TUTORIAL_SECTION_PADDING = 80

back_btn = None
arrowU = None
arrowD = None
completedTick = None

try:
    back_btn = pygame.image.load(r"Images\undo.png")
    arrowU = pygame.image.load(r"Images\arrow_up.png")
    arrowD = pygame.image.load(r"Images\arrow_down.png")
    completedTick = pygame.image.load(r"Images\completed.png")
except:
    back_btn = pygame.image.load(r"Images/undo.png")
    arrowU = pygame.image.load(r"Images/arrow_up.png")
    arrowD = pygame.image.load(r"Images/arrow_down.png")
    completedTick = pygame.image.load(r"Images/completed.png")

exitButton = utils.Button(20,SCREEN_HEIGHT * 0.8,back_btn,0.25)
arrowButtonUp = utils.Button(SCREEN_WIDTH * 0.82,SCREEN_HEIGHT * 0.08,arrowU,0.35)
arrowButtonDown = utils.Button(SCREEN_WIDTH * 0.82,SCREEN_HEIGHT * 0.8,arrowD,0.35)

allSections = []
sectionButtons = []

def Start():
    allSections.clear()
    sectionButtons.clear()
    running = True
    numberOfSections = 7
    index = 0
    inTutorial = False
    inPractice = False
    clicked = False
    buttonSelectedIndex = -1

    completedSections = getUserTutorialProgress()

    fontSize = 64
    font = pygame.font.Font(None, fontSize)

    getTutorialSections()
    getSectionRects(numberOfSections)

    while running:
        screen.fill((219, 200, 167))

        if not inTutorial:

            pygame.draw.rect(screen,(206,187,155),((SCREEN_WIDTH - INNER_SCREEN_WIDTH) // 2,0,INNER_SCREEN_WIDTH,SCREEN_HEIGHT))

            if arrowButtonUp.drawButton(screen):
                if index - 1 >= 0:
                    index = index - 1

            if arrowButtonDown.drawButton(screen):
                if index + 7 < len(allSections):
                    index = index + 1

            if not clicked:
                buttonSelectedIndex = drawButtons(numberOfSections,index,completedSections)
            
                if buttonSelectedIndex > -1:
                    clicked = True
                    inTutorial = True
        else:
            inner = pygame.draw.rect(screen,(206,187,155),((SCREEN_WIDTH - INNER_SCREEN_WIDTH) // 2,0,INNER_SCREEN_WIDTH,SCREEN_HEIGHT))
            surface = font.render(allSections[buttonSelectedIndex][0], True, (0,0,0))
            rect = surface.get_rect(center=(inner.midtop[0],inner.midtop[1] + 64))
            screen.blit(surface, rect)
            renderTextCenteredAt(allSections[buttonSelectedIndex][1],font,(0,0,0),inner.centerx,inner.centery,inner.width - 30,fontSize)
            play_button = pygame.Rect((SCREEN_WIDTH - 200) // 2, SCREEN_HEIGHT * 0.85 - 50, 250, 50)

            newButton = pygame.draw.rect(screen,(107, 70, 44),play_button)
            surface = font.render("Practice", True, (255,255,255))
            rect = surface.get_rect(center=newButton.center)
            screen.blit(surface, rect)

            pos = pygame.mouse.get_pos()
            if newButton.collidepoint(pos):
                if pygame.mouse.get_pressed()[0] == 1 and not inPractice:
                    inPractice = True
                    import GamePlayBoardPage
                    GamePlayBoardPage.drawBoard(allSections[buttonSelectedIndex][2])
                    inPractice = False
                    completedSections = completedSections + [allSections[buttonSelectedIndex][0]]
                    saveSections(completedSections)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if exitButton.drawButton(screen):
            if inTutorial:
                inTutorial = False
                clicked = False
                buttonSelectedIndex = -1
            else:
                running = False

        pygame.display.update()


def getSectionRects(sectionsToDisplay):
    tutorialSectionHeight = 100
    for i in range(sectionsToDisplay):
        startY = tutorialSectionHeight * i
        buttonRect = pygame.Rect((SCREEN_WIDTH - TUTORIAL_SECTION_WIDTH) // 2,startY * 1.2 + TUTORIAL_SECTION_PADDING,TUTORIAL_SECTION_WIDTH,tutorialSectionHeight)
        sectionButtons.append(buttonRect)

def drawButtons(sectionsToDisplay,index,completed):
    font = pygame.font.Font(None, 36)
    for i in range(sectionsToDisplay):
        button = sectionButtons[i]
        newButton = pygame.draw.rect(screen,(245,245,245),button,border_radius=10)
        surface = font.render(allSections[i+index][0], True, (0,0,0))
        rect = surface.get_rect(center=button.center)
        screen.blit(surface, rect)
        pos = pygame.mouse.get_pos()

        if allSections[i+index][0] in completed:
            tickRect = completedTick.get_rect()
            screen.blit(completedTick,(button.right - (tickRect.width * 1.5),button.centery - (tickRect.height// 2),tickRect.width,tickRect.height))

        # is hovering over button
        if newButton.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                clicked = True
                print(allSections[i+index][0] + " Clicked")
                return i+index
                
    return -1

def getTutorialSections():
    tutorialData = None
    try:
        tutorialData = open(r"Tutorial\Dialogue.txt","r")
    except:
        tutorialData = open(r"Tutorial/Dialogue.txt","r")

    for section in tutorialData.readlines():
        if section.count(':') != 0:
            newSection = section.split(':') # array containing [title of section, text to display, board for demo]
            allSections.append([newSection[0],newSection[1],newSection[2]])

    tutorialData.close()


def renderTextCenteredAt(text, font, colour, x, y, allowed_width,fontSize = 64):

    #reference https://stackoverflow.com/questions/49432109/how-to-wrap-text-in-pygame-using-pygame-font-font

    # first, split the text into words
    words = text.split()

    # now, construct lines out of these words
    lines = []
    while len(words) > 0:
        # get as many words as will fit within allowed_width
        lineWords = []
        while len(words) > 0:
            lineWords.append(words.pop(0))
            fw, fh = font.size(' '.join(lineWords + words[:1]))
            if fw > allowed_width:
                break

        # add a line consisting of those words
        line = ' '.join(lineWords)
        lines.append(line)

    # now we've split our text into lines that fit into the width, actually
    # render them

    # we'll render each line below the last, so we need to keep track of
    # the culmative height of the lines we've rendered so far
    i = 0
    yOffset = fontSize
    centeringOffset = (len(lines) * fontSize) // 2
    for line in lines:
        fw, fh = font.size(line)

        # (tx, ty) is the top-left of the font surface
        tx = x - fw / 2
        ty = y + (yOffset * i) - centeringOffset

        surface = font.render(line, True, colour)
        screen.blit(surface, (tx, ty))
        i = i + 1


def getUserTutorialProgress():
    tutorialData = None
    try:
        tutorialData = open(r"Data\UserTutorialProgress.txt","r")
    except:
        tutorialData = open(r"Data/UserTutorialProgress.txt","r")

    data = tutorialData.readline()
    if data == "":
        return []
    else:
        data = data.split(",")

    tutorialData.close()

    return data

def saveSections(completedSections):
    # the program needs to write into tutorialData every string in the array completedSections
    # shouldnt return any value
    tutorialData = None
    try:
        tutorialData = open(r"Data\UserTutorialProgress.txt","w")
    except:
        tutorialData = open(r"Data/UserTutorialProgress.txt","w")
        
    #---- code here -----

    data = ""

    for i in completedSections:
        data = data + i + ","

    tutorialData.write(data)
    # -------------------

    tutorialData.close()