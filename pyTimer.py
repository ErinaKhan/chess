from pygame.time import get_ticks

class Timer:
    # get_ticks() returns the point in time your at from when the application was lauched

    def __init__(self,duration):
        self.duration = duration
        self.startTime = 0 # point in time timer started
        self.timeElapsed = 0 # the amount of time the timer has been on for
        self.active = False # whether the timer currently paused
        self.pauseTicks = 0 # time elapsed since timer was paused 
        self.timeRanOut = False

    def start(self):
        self.active = True
        self.startTime = get_ticks()

    def timeout(self):
        self.timeRanOut = True
        self.active = False
        self.startTime = 0

    def pause(self):
        self.active = False
        self.timeRanOut = True
        self.pauseTicks = get_ticks() # point in time the timer stops from when the application was lauched

    def unpause(self):
        # resets start time as the pausing of the timer messes up the get ticks function
        # this is because the get_ticks function is based on when the app was launched not the actual amount of time passed in the timer
        newTicks = get_ticks()
        self.startTime = self.startTime + (newTicks - self.pauseTicks) 
        self.active = True

    def update(self):
        if self.active:
            currentTime = get_ticks()
            self.timeElapsed = currentTime - self.startTime # finds the time passed by the timer
            if self.timeElapsed >= self.duration:
                self.timeout() # clock has ran out of time

    def time(self):
        time = self.timeElapsed // 1000 # num of seconds
        durationInSec = self.duration // 1000
        durationInMins = durationInSec // 60
        durationInSec = durationInSec % 60
        minutes = time // 60 
        seconds = time % 60
        return durationInMins - minutes,(durationInSec - seconds) + 60
    
    def reset(self,duration):
        self.duration = duration
        self.startTime = 0 # point in time timer started
        self.timeElapsed = 0 # the amount of time the timer has been on for
        self.active = False # whether the timer currently paused
        self.pauseTicks = 0 # time elapsed since timer was paused 
        self.timeRanOut = False
        self.start()