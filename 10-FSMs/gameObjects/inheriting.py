from . import Kirby, Controllable
import pygame
from FSMs import EnemyFSM
from utils import vec, magnitude, scale, rectAdd
import numpy as np


class Inheriting(Controllable):
    def __init__(self, position, fileName="", barrier=None, door=None):
        super().__init__(position, fileName, barrier, door)
        self.velocity = vec(0, 0)
        self.wanderingRange = [vec(100, 140), vec(144, 140)]
        self.wandering = EnemyFSM(self, self.wanderingRange)

    def update(self, map, kirbyPosition, seconds):
        ##print("are you there")
        ##print(self.position, self.velocity, "in inheriting pos an vel")
        super().update(seconds)
        self.wandering.update(map, kirbyPosition, seconds)
        pass

    def exit(self):
        return super().exit()

    def see(self, map, kirbyposition):
        barrierRect = map
        kirbyPosition = kirbyposition  # wont work rn, need to solve later
        kirbyRectangle = pygame.Rect(
            *kirbyPosition, 16, 16)  # not self.position
        rangetoward = [0, 0]
        hozVel, verVel = self.velocity
        print("velocity", self.velocity)
        if hozVel > 0:
            rangetoward[0] = 32
        elif hozVel < 0:
            rangetoward[0] = -32
        if verVel > 0:
            rangetoward[1] = 32
        elif verVel < 0:
            rangetoward[1] = -32

        print(rangetoward, "suppose to be 0")
        originalTopLeft = self.position-vec(16, 16)
        widthHeight = vec(16*3, 16*3)
        rangetoward = vec(*rangetoward)
        noMeaningRectangle = pygame.Rect(*originalTopLeft, *widthHeight)
        detectionRectangle = rectAdd(rangetoward, noMeaningRectangle)
        print(detectionRectangle)
        internsectionRect = pygame.Rect.clip(
            detectionRectangle, kirbyRectangle)
        if internsectionRect:
            for br in barrierRect:
                if br.clipline(*self.position, *kirbyPosition):
                    return 0
            return 1
        else:
            return 0
