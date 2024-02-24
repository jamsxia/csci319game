from . import Mobile, Drawable
from FSMs import WalkingFSM, AccelerationFSM
from utils import vec, RESOLUTION

from pygame.locals import *

import pygame
import numpy as np
from os.path import join


class Controllable(Mobile):
    def __init__(self, position, img="kirby.png"):
        super().__init__(position, img)

        self.hatOffset = vec(-3, -6)
        self.hat = Drawable(position, "hat.png")
        self.hat.image = pygame.transform.flip(self.hat.image, True, False)
        self.ghost = Drawable(position, "kirby2.png", (0, 3))

        # Animation variables specific to Kirby
        self.framesPerSecond = 2
        self.nFrames = 2
        self.inheriting = 0  # 0 means not activated ## 1 means activated 2 means inherited
        self.nFramesList = {
            "moving": 1,
            "standing": 1
        }

        self.rowList = {
            "moving": 0,
            "standing": 0
        }

        self.framesPerSecondList = {
            "moving": 8,
            "standing": 2
        }
        self.FSManimated = WalkingFSM(self)
        self.LR = AccelerationFSM(self, axis=0)
        self.UD = AccelerationFSM(self, axis=1)

    def handleEvent(self, event):
        if event.type == KEYDOWN:
            if event.key == K_UP:
                self.UD.decrease()

            elif event.key == K_DOWN:
                self.UD.increase()

            elif event.key == K_LEFT:
                self.LR.decrease()

            elif event.key == K_RIGHT:
                self.LR.increase()

            elif event.key == K_SPACE:
                self.inheriting = 1

        elif event.type == KEYUP:
            if event.key == K_UP:
                self.UD.stop_decrease()

            elif event.key == K_DOWN:
                self.UD.stop_increase()

            elif event.key == K_LEFT:
                self.LR.stop_decrease()

            elif event.key == K_RIGHT:
                self.LR.stop_increase()

    def update(self, seconds, map=None):
        self.LR.update(seconds)
        self.UD.update(seconds)
        # do something here changes inheriting to 2 if collide with other inheriting objects
        # THINKING  of having a list of all inheriting objects and take it as one of the argument, the same treatment as map
        super().update(seconds, map)
        self.hat.position = self.hatOffset+self.position
        self.ghost.position = self.position

    def draw(self, drawSurface):
        if (self.inheriting == 0):
            super(). draw(drawSurface)
            self.hat.draw(drawSurface)
        elif (self.inheriting == 1):
            self.ghost.draw(drawSurface)
        else:
            # trigger havn't done yet, should never be 2 rn
            self.hat.draw(drawSurface)

    def updateMovement(self):
        pass
