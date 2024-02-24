import pygame

from . import Drawable, Kirby, Inheriting

from utils import vec, RESOLUTION
# if you want to avoid creating objects here and there, you might be able to have an indicator of which character you are choosing in the game engine


class GameEngine(object):
    import pygame

    def __init__(self):
        self.kirby = Kirby((144, 60))
        self.char = Inheriting((144, 120), "1.png")
        self.size = vec(*RESOLUTION)
        self.background = Drawable((0, 0), "background.png")

    def draw(self, drawSurface):
        self.background.draw(drawSurface)

        self.kirby.draw(drawSurface)
        self.char.draw(drawSurface)

    def handleEvent(self, event):

        self.kirby.handleEvent(event)
        # self.char.handleEvent(event)
        '''
        if (self.kirby.inheriting != 2):
            self.kirby.handleEvent(event)
        else:
            self.char.handleEvent(event)
        '''

    def update(self, seconds, map=None):
        kirbyRect = pygame.Rect(self.kirby.position, (16, 16))
        charRect = pygame.Rect(self.char.position, (16, 16))
        if (pygame.Rect.colliderect(kirbyRect, charRect) == True and self.kirby.inheriting == 1):
            self.kirby.inheriting = 2
            self.kirby = self.char
        if (self.kirby.inheriting != 2):
            self.kirby.update(seconds, map)
        else:
            self.char.update(seconds, map)

        Drawable.updateOffset(self.kirby, self.size)
        Drawable.updateOffset(self.char, self.size)
