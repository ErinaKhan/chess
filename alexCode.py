import pygame
import os

class Timer:
    def __init__(self,duration):
        self.duration = duration
        self.startTime = 0
        self.timeElapsed = 0
        self.active = False
        self.pauseTicks = 0

    def start(self):
        self.active = True
        self.startTime = pygame.time.get_ticks()

    def timeout(self):
        self.active = False
        self.startTime = 0

    def pause(self):
        self.active = False
        self.pauseTicks = pygame.time.get_ticks()

    def unpause(self):
        newTicks = pygame.time.get_ticks()
        self.startTime = self.startTime + (newTicks - self.pauseTicks)
        self.active = True

    def update(self):
        if self.active:
            currentTime = pygame.time.get_ticks()
            self.timeElapsed = currentTime - self.startTime
            if self.timeElapsed >= self.duration:
                self.timeout()
            
    def time(self):
        time = self.timeElapsed // 1000 # num of seconds
        durationInSec = self.duration // 1000
        durationInMins = durationInSec // 60
        durationInSec = durationInSec % 60
        minutes = time // 60 
        seconds = time % 60
        return durationInMins - minutes,(durationInSec - seconds) + 60
    
    def drawTimerUI(self,screen, x, y, height, width):
        # Alex's section
        # Coding requirements
        # . put anything you want to draw on the screen in this function
        # . the function should draw a rectangle with the current time inside it
        #   like the timer on chess.com (https://www.chess.com/terms/chess-clocks)
        # -----------------------------------------------------
        # parameters
        # -----------------------------------------------------
        # . the screen is the place the ui should be displayed
        # . x and y are the coordinates to display the image at
        # . length is the length of the timer
        # . width is the width of the timer
        # -----------------------------------------------------
        # resources if stuck below
        # -----------------------------------------------------
        # how to draw rectangle - https://www.geeksforgeeks.org/how-to-draw-rectangle-in-pygame/
        # displaying text to the screen - https://www.youtube.com/watch?v=ndtFoWWBAoE
        # if it says pygame doesnt exist when running then there is a help section on our trello board to help

        minutes,seconds = self.time() # contains the minutes and the seconds the timer should display
        #-----------------------------------------------------


        #-----------------------------------------------------
        # the function shouldn't return any value
        #-----------------------------------------------------

    def drawText(self,screen,text,font,text_col,x,y):
        # also for alex if you choose to use the tutorial for displaying text to the screen
        pass








# dont edit code below 
pygame.init()

os.environ['SDL_VIDEO_CENTERED'] = '1'
info = pygame.display.Info()

SCREEN_WIDTH = info.current_w
SCREEN_HEIGHT = info.current_h

screen = pygame.display.set_mode((SCREEN_WIDTH - 10,SCREEN_HEIGHT- 50),pygame.RESIZABLE)
pygame.display.set_caption('DEMO')

run = True
timerTest = Timer(60000)
timerTest.start()
while run:
    screen.fill((0,0,0))
    timerTest.update()
    timerTest.drawTimerUI(screen,SCREEN_WIDTH // 2,SCREEN_HEIGHT // 2,100,200)
    minutes,seconds = timerTest.time()
    print(f"{minutes} : {seconds}")
    if timerTest.active == False:
        run = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()
