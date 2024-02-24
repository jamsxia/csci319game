from . import Mobile
from FSMs import WalkingFSM, AccelerationFSM
from utils import vec, RESOLUTION

from pygame.locals import *

import pygame
import numpy as np


class Kirby(Mobile):
    def __init__(self, position):
        super().__init__(position, "kirby.png")

        # Animation variables specific to Kirby
        self.framesPerSecond = 2
        self.nFrames = 2

        self.nFramesList = {
            "moving": 4,
            "standing": 2
        }

        self.rowList = {
            "moving": 1,
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
        if event.type == JOYAXISBUTTON:
            if event.axis == 0 and event.value < 0.1:
                self.UD.stop_increase()
                self.UD.decrease()

            elif event.axis == 0 and event.value > 0.1:
                self.UD.stop_decrease()
                self.UD.increase()

            elif event.key == 0:
                self.LR.stop_all()

            elif event.axis == 1 and event.value < 0.1:
                self.LR.stop_increase()
                self.LR.increase()
            elif event.axis == 1 and event.value > 0.1:
                self.LR.stop_decrease()
                self.LR.decrease()
            '''
        elif event.type == JOYBUTTONUP:
            if event.key == 11:
                self..stop_decrease()

            elif event.key == 12:
                self.UD.stop_increase()

            elif event.key == 13:
                self.LR.stop_decrease()

            elif event.key == 14:
                self.LR.stop_increase()
'''

    def update(self, seconds):
        self.LR.update(seconds)
        self.UD.update(seconds)

        super().update(seconds)

    def updateMovement(self):
        pass
