import pygame

import numpy as np

from . import Drawable, Kirby, Inheriting, BulletInheriting

from utils import vec, RESOLUTION, SpriteManager, textMatching, SoundManager, normalize, magnitude, vec
# if you want to avoid creating objects here and there, you might be able to have an indicator of which character you are choosing in the game engine

levels = ["levelOneText.txt", "levelTwoText.txt",
          "levelThreeText .txt", "levelFourText.txt"]


class GameEngine(object):
    import pygame

    def __init__(self, level="levelOneText.txt"):

        self.size = vec(*RESOLUTION)
        self.background = Drawable((0, 0), "background.png")
        # self.levelOneText = level
        self.level = level
        self.settingImage = [[0]*14 for i in range(14)]
        self.updateMap(level, 0)
        self.barrierRect = []
        self.detectDoor = None
        self.updateLevel()
        self.kirby = Kirby(
            (144, 60), barrier=self.barrierRect, door=self.detectDoor)
        # self.char = BulletInheriting((144, 140), vec(100, 140), vec(144, 140), "2.png",
        # barrier = self.barrierRect, door = self.detectDoor)
        self.endGame = 0
        self.index = 1

        self.chars = self.levellist1
        # if self
        self.wallDefaultImage = SpriteManager.getInstance().getSprite(
            "tiles.png", (4, 4))
        self.ceilDefaultImage = SpriteManager.getInstance().getSprite(
            "tiles.png", (1, 3))

    def updateLevel(self):
        self.barrierRect = []
        if (self.levelOneText):
            for i in range(len(self.levelOneText)):
                for j in range(len(self.levelOneText[0])):
                    if (self.levelOneText[i][j] != ' '):
                        self.barrierRect.append(
                            pygame.Rect((j*16, i*16), (16, 16)))
                        if (self.levelOneText[i][j] == 'dt'):
                            self.detectDoor = pygame.Rect(
                                (j*16, i*16), (16, 16))
        if self.level == levels[0]:
            self.levellist1 = [BulletInheriting((60, 140), vec(60, 80), vec(60, 140), "2.png",
                                                barrier=self.barrierRect, door=self.detectDoor),
                               Inheriting((144, 140), vec(100, 140), vec(144, 140), "1.png",
                                          barrier=self.barrierRect, door=self.detectDoor)]
            self.chars = self.levellist1
        elif self.level == levels[1]:
            self.levelList2 = [BulletInheriting((144, 140), vec(100, 140), vec(190, 140), "2.png",
                                                barrier=self.barrierRect, door=self.detectDoor),
                               # Inheriting((144, 60), vec(100, 60), vec(190, 60), "1.png",
                               # barrier=self.barrierRect, door=self.detectDoor),
                               Inheriting((155, 50), vec(155, 50), vec(155, 120), "1.png",
                                          barrier=self.barrierRect, door=self.detectDoor),
                               BulletInheriting((25, 150), vec(25, 150), vec(25, 60), "2.png",
                                                barrier=self.barrierRect, door=self.detectDoor),
                               BulletInheriting((75, 60), vec(75, 150), vec(75, 60), "2.png",
                                                barrier=self.barrierRect, door=self.detectDoor)
                               ]
            self.chars = self.levelList2
        elif self.level == levels[2]:
            self.levelList3 = [BulletInheriting((100, 60), vec(100, 60), vec(180, 160), "2.png",
                                                barrier=self.barrierRect, door=self.detectDoor),
                               BulletInheriting((180, 107), vec(55, 107), vec(180, 107), "2.png",
                                                barrier=self.barrierRect, door=self.detectDoor),
                               BulletInheriting((25, 150), vec(25, 150), vec(25, 60), "2.png",
                                                barrier=self.barrierRect, door=self.detectDoor),
                               BulletInheriting((55, 150), vec(55, 150), vec(180, 150), "2.png",
                                                barrier=self.barrierRect, door=self.detectDoor)
                               ]
            self.chars = self.levelList3
        else:
            self.chars = []

        # print(self.levelOneText)

    def drawBack(self, drawSurface):
        for i in range(len(self.settingImage)):
            if (self.levelOneText[i][0] == "lc"):
                if (self.levelOneText[i][1] == "wtl" or self.levelOneText[i][1] == "wbl"):
                    # print(levelOneText)
                    drawSurface.blit(self.wallDefaultImage, (0, i*16))
                elif (self.levelOneText[i][1] == "h"):
                    drawSurface.blit(self.ceilDefaultImage, (0, i*16))
            if (self.levelOneText[i][-1] == "rc\n" or self.levelOneText[i][-1] == "rc"):
                if (self.levelOneText[i][-2] == "wtr" or self.levelOneText[i][-2] == "wbr"):
                    # print(levelOneText)
                    drawSurface.blit(self.wallDefaultImage, (13*16, i*16))
                elif (self.levelOneText[i][-2] == "h"):
                    drawSurface.blit(self.ceilDefaultImage, (13*16, i*16))

        for i in range(len(self.settingImage)):
            for j in range(len(self.settingImage[0])):
                drawSurface.blit(self.settingImage[i][j], (j*16, i*16))

    def draw(self, drawSurface):
        self.background.draw(drawSurface)

        self.kirby.draw(drawSurface)
        for char in self.chars:
            char.draw(drawSurface)

    def handleEvent(self, event):

        self.kirby.handleEvent(event)
        # self.char.handleEvent(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            sm = SoundManager.getInstance()
            ch = sm.playSFX("448204__tyops__cartoon-scary-hit.wav")
        '''
        if (self.kirby.inheriting != 2):
            self.kirby.handleEvent(event)
        else:
            self.char.handleEvent(event)
        '''

    def update(self, seconds):
        self.kirby.update(seconds)
        # print("inheriting stage is ", self.kirby.inheriting)
        kirbyRect = pygame.Rect(self.kirby.position, (16, 16))
        # find old velocity and prevent overwriting
        if (type(self.kirby) == BulletInheriting or type(self.kirby) == Inheriting):
            print(self.kirby.position)
            if magnitude(self.kirby.velocity) > 0:
                # self.kirby.velocity  # note it graually decreases
                self.kirby.oldVelocity = vec(*self.kirby.velocity)
                ##print("changed oldVelocity", self.kirby.velocity)
            # print("on time old velocity", self.kirby.oldVelocity)
            # print("magnitude of my velocity", magnitude(self.kirby.velocity))
        for char in self.chars:
            # print(char.oldVelocity)
            # print(char.see(self.barrierRect, self.kirby.position))
            if (type(char) == BulletInheriting and char.see(self.barrierRect, self.kirby.position) == 1):
                self.endGame = 1
            # print(char.oldVelocity)
            charRect = pygame.Rect(char.position, (16, 16))
            if (char is not self.kirby):
                if (type(self.kirby) == BulletInheriting):
                    # print(char.beSeen, char.wanderingRange,
                    # self.kirby.canshoot, self.kirby.successKill)
                    # print(self.kirby.bullet)
                    if (self.kirby.see(self.barrierRect, char.position) == 1):
                        ##print("detect char's position, looks like it's flipped", char.position)
                        char.beSeen = 1
                        self.kirby.canshoot = 1

                    else:
                        self.kirby.canshoot = 0
                        char.beSeen = 0

                    if (char.beSeen == 1):
                        ##self.kirby.canshoot = 1
                        if (self.kirby.successKill == 1):
                            self.chars.remove(char)
                            print("remove becasue being shot")
                            self.kirby.successKill = 0
                            ##self.kirby.bullet = 0
                    else:
                        self.kirby.canshoot = 0
                char.update(seconds, self.barrierRect, self.kirby.position)
                if (pygame.Rect.colliderect(kirbyRect, charRect) == True):
                    if (np.dot(self.kirby.velocity, char.oldVelocity) > 0):
                        if (self.kirby.inheriting == 1):
                            print("inheriting triggered")
                            self.kirby.inheriting = 0
                            self.kirby = char
                            print("remove because hit")
                            self.chars.remove(char)
                        else:
                            pass
                            # print(1)
                            ##self.endGame = 1
                    else:
                        pass
                        # print(2)
                        ##self.endGame = 1
                if magnitude(char.velocity) != 0:  # here is the problem
                    # print("do you go here")
                    char.oldVelocity = char.velocity

        Drawable.updateOffset(self.kirby, self.size)
        for char in self.chars:
            Drawable.updateOffset(char, self.size)

        if (self.kirby.exit == 1):
            self.updateMap(levels[self.index], self.index)
            self.index = self.index+1
            self.updateLevel()
            self.kirby.exit = 0  # change back to zero
            self.kirby.position = (50, 16)
            self.kirby.barrierRect = self.barrierRect

            # self.char.barrierRect = self.barrierRect
            # self.char.detectDoor = self.detectDoor
        # once see
        # if self.char.see(self.barrierRect, self.kirby.position) == 1:
        # self.char.wandering.gochasing()

    def updateMap(self, mapName, index):
        self.level = levels[index]
        levelOneText = open(mapName, 'r')  # local variable
        self.levelOneText = []
        self.levelOneText = [i.split(',')
                             for i in levelOneText.readlines()]
        i, j = 0, 0
        self.settingImage = [[0]*14 for i in range(14)]
        for line in self.levelOneText:
            for word in line:
                if ("\n" in word):
                    word = word[:-1]
                if (word != " "):
                    Image = SpriteManager.getInstance().getSprite(
                        "tiles.png", textMatching[word])
                else:
                    Image = SpriteManager.getInstance().getSprite(
                        "tiles.png", (12, 0))
                self.settingImage[i][j] = Image
                j += 1
            j = 0
            i += 1
