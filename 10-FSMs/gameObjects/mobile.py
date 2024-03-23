from . import Animated
import pygame
from utils import vec, magnitude, scale
import numpy as np


class Mobile(Animated):
    def __init__(self, position, fileName="", barrier=None, doorPosition=None):
        super().__init__(position, fileName)
        self.velocity = vec(0, 0)
        self.maxVelocity = 200
        ##self.barrierRect = []
        self.exit = 0
        self.map = map
        self.barrierRect = barrier
        self.detectDoor = doorPosition
        # self.updateLevel()
        # another class, takes sidebar, setting the startig point, or wideth

    '''def updateLevel(self):
        if (self.map):
            for i in range(len(self.map)):
                for j in range(len(self.map[0])):
                    if (self.map[i][j] != ' '):
                        self.barrierRect.append(
                            pygame.Rect((j*16, i*16), (16, 16)))
                        if (self.map[i][j] == 'dt'):
                            self.detectDoor = pygame.Rect(
                                (j*16, i*16), (16, 16))'''

    def exit(self):
        a = self.exit
        self.exit = 0
        return a

    def update(self, seconds):
        super().update(seconds)
        # self.updateLevel(self.map)
        if magnitude(self.velocity) > self.maxVelocity:
            self.velocity = scale(self.velocity, self.maxVelocity)

        fakePos = self.position+self.velocity * seconds
        '''
        fakePos = fakePos//scale-vec(8, 8)
        ExpectedRect = pygame.Rect(list(map(int, fakePos)), (16, 16)
        # USE THE MAP TO KNOW WHERE KIRBY IS IN COLLISON WITH OTHERS, NO USE OF RECTANGLES AT ALL
        '''
        # barrierPosX, barrierPosY = (
        # fakePos//16).astype(int)  # positin of the barrier
        userPosX, userPosY = (fakePos)
        # check sthe geography
        characterHitBox = pygame.Rect(fakePos, (16, 16))
        for br in self.barrierRect:
            internsectionRect = pygame.Rect.clip(characterHitBox, br)
            barrierPosX, barrierPosY = br.topleft
            ##print(barrierPosX, barrierPosY)
            rectLength = internsectionRect.width
            rectHeight = internsectionRect.height
            if (rectHeight != 0):
                if (br == self.detectDoor):
                    self.exit = 1
                    # self.updateLevel()
                if (rectLength > rectHeight):
                    if (userPosY > barrierPosY):  # crash from bottom
                        self.velocity[1] = min(0, self.velocity[1])
                        userPosY = userPosY+rectHeight
                    elif (userPosY < barrierPosY):  # crash from top
                        self.velocity[1] = max(0, -1*self.velocity[1])
                        userPosY = userPosY-rectHeight

                elif (rectLength < rectHeight):
                    if (userPosX > barrierPosX):  # crash from left
                        self.velocity[0] = min(0, self.velocity[0])
                        userPosX = userPosX+rectLength
                    elif (userPosX < barrierPosX):  # crash fro right
                        self.velocity[0] = max(0, -1*self.velocity[0])
                        userPosX = userPosX-rectLength
                fakePos = vec(userPosX, userPosY)
        self.position = fakePos
    '''
        if (map[barrierPosY][barrierPosX] != ' '):
            characterHitBox = pygame.Rect(fakePos, (16, 16))
            wallHitBox = pygame.Rect(
                vec(barrierPosX*16, barrierPosY*16), (16, 16))
            internsectionRect = pygame.Rect.clip(characterHitBox, wallHitBox)
            rectLength = internsectionRect.width
            rectHeight = internsectionRect.height
            if (rectLength > rectHeight):
                if (userPosX > barrierPosX):  # crash from left
                    self.velocity[0] = min(0, self.velocity[0])
                    userPosX = userPosX+1
                elif (userPosX < barrierPosX):  # crash fro right
                    self.velocity[0] = max(0, -1*self.velocity[0])
                    userPosX = userPosX-1
            elif (rectLength < rectHeight):
                if (userPosY > barrierPosY):  # crash from bottom
                    self.velocity[1] = min(0, self.velocity[1])
                    userPosY = userPosX+1
                elif (userPosY < barrierPosY):  # crash from top
                    self.velocity[1] = max(0, -1*self.velocity[1])
                    userPosY = userPosY-1
            fakePos = vec(userPosX*16, userPosY*16)

            # always just move the collided object by one unit, can use cliprect in pygame and do the longer side
            # relative posistion gives which way the velocity will be reduced
            '''
