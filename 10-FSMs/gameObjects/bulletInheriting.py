from . import Kirby, Controllable, Inheriting
import pygame
from FSMs import EnemyFSM
from utils import vec, magnitude, scale, rectAdd
import numpy as np
from pygame.locals import *


class BulletInheriting(Inheriting):
    def __init__(self, position, wanderA, wanderB, fileName="", barrier=None, door=None):
        super().__init__(position, wanderA, wanderB,
                         fileName, barrier, door)
        self.canshoot = 0
        self.bullet = 1
        self.successKill = 0

    def update(self, seconds=None, map=None, kirbyPosition=None):
        ##print("are you there")
        ##print(self.position, self.velocity, "in inheriting pos an vel")

        super().update(seconds, map, kirbyPosition)
        # print("yo")
        pass

    def handleEvent(self, event):
        super().handleEvent(event)
        if event.type == KEYDOWN and event.key == K_s and self.bullet == 1:
            print("shootTrigger")
            self.bullet = 0
            print("in handle", self.canshoot)
            if (self.canshoot == 1):
                self.successKill = 1

    def see(self, map, kirbyposition):
        barrierRect = map
        ##print("kirby position is", kirbyposition)
        kirbyPosition = kirbyposition  # wont work rn, need to solve later
        kirbyRectangle = pygame.Rect(
            *kirbyPosition, 16, 16)  # not self.position
        rangetoward = [0, 0]
        widthHeight = [16, 16]
        hozVel, verVel = self.oldVelocity
        ##print("velocity", self.velocity)
        if hozVel > 0:
            rangetoward[0] = 16
            widthHeight[0] = 64
        elif hozVel < 0:
            rangetoward[0] = -64
            widthHeight[0] = 64
        if verVel > 0:
            rangetoward[1] = 16
            widthHeight[1] = 64
        elif verVel < 0:
            rangetoward[1] = -64
            widthHeight[1] = 64

        ##print(rangetoward, "suppose to be 0")
        originalTopLeft = self.position
        widthHeight = vec(*widthHeight)
        rangetoward = vec(*rangetoward)

        noMeaningRectangle = pygame.Rect(*originalTopLeft, *widthHeight)
        detectionRectangle = rectAdd(rangetoward, noMeaningRectangle)
        # print(detectionRectangle)
        internsectionRect = pygame.Rect.clip(
            detectionRectangle, kirbyRectangle)
        if internsectionRect:
            for br in barrierRect:
                if br.clipline(*self.position, *kirbyPosition):
                    ##print("hit the wall")
                    return 0  # see why it returns these
            return 1
        else:
            ###print("did not see enemy")
            return 0
