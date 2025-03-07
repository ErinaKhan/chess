from pygame.time import get_ticks

class Timer:
    def __init__(self,duration):
        self.duration = duration
        self.startTime = 0
        self.timeElapsed = 0
        self.active = False
        self.pauseTicks = 0

    def start(self):
        self.active = True
        self.startTime = get_ticks()

    def timeout(self):
        self.active = False
        self.startTime = 0

    def pause(self):
        self.active = False
        self.pauseTicks = get_ticks()

    def unpause(self):
        newTicks = get_ticks()
        self.startTime = self.startTime + (newTicks - self.pauseTicks)
        self.active = True

    def update(self):
        if self.active:
            currentTime = get_ticks()
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
