from . import Kirby, Controllable
import pygame
from FSMs import EnemyFSM
from utils import vec, magnitude, scale, rectAdd
import numpy as np


class Inheriting(Controllable):
    def __init__(self, position, wanderA, wanderB, fileName="", barrier=None, door=None):
        super().__init__(position, fileName, barrier, door)
        self.velocity = vec(0, 0)
        self.wanderingRange = [wanderA, wanderB]
        self.wandering = EnemyFSM(self, self.wanderingRange)
        self.oldVelocity = vec(1, 1)
        self.beSeen = 0

    def update(self, seconds=None, map=None, kirbyPosition=None):
        ##print("are you there")
        ##print(self.position, self.velocity, "in inheriting pos an vel")
        if (self.velocity[0] < -1):
            self.flipImage[0] = True
        elif (self.velocity[0] > 1):
            self.flipImage[0] = False
        super().update(seconds)
        if (type(kirbyPosition) != type(None)):
            self.wandering.update(map, kirbyPosition, seconds)
        pass

    def catch(self, kirbyPosition, second):
        kirbyRectangle = pygame.Rect(
            *kirbyPosition, 16, 16)
        myRectangle = pygame.Rect(self.position, 16, 16)
        internsectionRect = pygame.Rect.clip(
            kirbyRectangle, myRectangle)
        if (internsectionRect):
            return 1

    def exit(self):
        return super().exit()

    def see(self, map, kirbyposition):
        barrierRect = map
        ##print("kirby position is", kirbyposition)
        kirbyPosition = kirbyposition  # wont work rn, need to solve later
        kirbyRectangle = pygame.Rect(
            *kirbyPosition, 16, 16)  # not self.position
        rangetoward = [0, 0]
        hozVel, verVel = self.velocity
        ##print("velocity", self.velocity)
        if hozVel > 0:
            rangetoward[0] = 32
        elif hozVel < 0:
            rangetoward[0] = -32
        if verVel > 0:
            rangetoward[1] = 32
        elif verVel < 0:
            rangetoward[1] = -32

        ##print(rangetoward, "suppose to be 0")
        originalTopLeft = self.position-vec(16, 16)
        widthHeight = vec(16*3, 16*3)
        rangetoward = vec(*rangetoward)
        noMeaningRectangle = pygame.Rect(*originalTopLeft, *widthHeight)
        detectionRectangle = rectAdd(rangetoward, noMeaningRectangle)
        # print(detectionRectangle)
        internsectionRect = pygame.Rect.clip(
            detectionRectangle, kirbyRectangle)
        if internsectionRect:
            for br in barrierRect:
                if br.clipline(*self.position, *kirbyPosition):
                    return 0
            return 1
        else:
            return 0
