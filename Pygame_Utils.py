import pygame

class Button():

    def __init__(self,x,y,image,scale = 1):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image,(int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.selectable = True
        self.clicked = False
        self.moving = False

    def drawButton(self,screen):

        if not self.selectable:
            return False
        
        action = False
        # get pos of mouse
        pos = pygame.mouse.get_pos()
        # is hovering over button
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                self.moving = True
                action = True


        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        self.moving = False
                
        screen.blit(self.image,self.rect)
        return action
    
    def move(self,screen,x,y):
        print(self.rect)
        self.rect.topleft = (x,y)
        print(self.rect)
        screen.blit(self.image,self.rect)

    def destroy(self):
        self.image.fill((0,0,0,0))
        self.selectable = False
        


class OverlaySquare(Button):
    def __init__(self,coordinates, x, y, colour):
        self.coordinates = coordinates
        self.colour = colour
        self.selectable = True
        self.rect = pygame.Rect(x,y,100,100)
        self.rect.topleft = (x,y)
        self.clicked = False
        self.moving = False
        self.x = x
        self.y = y

    
    def drawButton(self, screen):
        if not self.selectable:
            return

        action = False
        # get pos of mouse
        pos = pygame.mouse.get_pos()
        # is hovering over button
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                self.moving = True
                action = True


        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        self.moving = False
                
        pygame.draw.rect(screen,(self.colour),self.rect)
        return action

    def destroy(self):
        self.rect.scale_by(0,0)
        self.selectable = False

class chessPiece(Button):
    def __init__(self,colour,coordinates,x,y,image,scale = 1):
        self.colour = colour
        self.coordinates = coordinates
        Button.__init__(self,x,y,image,scale)

    def move(self, screen, x, y,newcoords):
        self.coordinates = newcoords
        return super().move(screen, x, y)
    

class TutorialSection():

    def __init__(self,dialogue,title,x,y,image,scale = 1):
        self.title = title
        self.dialogue = dialogue
        Button.__init__(self,x,y,image,scale)

    def loadSection(self):
        pass

    def completedSection(self):
        pass


