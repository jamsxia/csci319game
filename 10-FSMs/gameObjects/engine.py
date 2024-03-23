import pygame

from . import Drawable, Kirby, Inheriting

from utils import vec, RESOLUTION, SpriteManager, textMatching, SoundManager
# if you want to avoid creating objects here and there, you might be able to have an indicator of which character you are choosing in the game engine


class GameEngine(object):
    import pygame

    def __init__(self, level="levelOneText.txt"):

        self.size = vec(*RESOLUTION)
        self.background = Drawable((0, 0), "background.png")
        ##self.levelOneText = level

        self.settingImage = [[0]*14 for i in range(14)]
        self.updateMap(level)
        self.barrierRect = []
        self.detectDoor = None
        self.updateLevel()
        self.kirby = Kirby(
            (144, 60), barrier=self.barrierRect, door=self.detectDoor)
        self.char = Inheriting((144, 140), "1.png",
                               barrier=self.barrierRect, door=self.detectDoor)

        '''
        i, j = 0, 0
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
        '''
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
        self.char.draw(drawSurface)

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
        kirbyRect = pygame.Rect(self.kirby.position, (16, 16))
        charRect = pygame.Rect(self.char.position, (16, 16))
        if (pygame.Rect.colliderect(kirbyRect, charRect) == True and self.kirby.inheriting == 1):
            self.kirby.inheriting = 2
            self.kirby = self.char
        if (self.kirby.inheriting != 2):

            self.kirby.update(seconds)

            self.char.update(self.barrierRect, self.kirby.position, seconds)
            ##print("in kirby", seconds)
        else:

            ##print("you work?")
            self.char.update(self.barrierRect, self.kirby.position, seconds)

        Drawable.updateOffset(self.kirby, self.size)
        Drawable.updateOffset(self.char, self.size)

        if (self.char.exit == 1):
            self.updateMap("levelTwoText.txt")
            self.char.exit = 0  # change back to zero
            ##self.kirby.barrierRect = self.barrierRect
            self.kirby.position = (50, 16)
            self.updateLevel()
            # wall penetrate, change starting position
            self.char.barrierRect = self.barrierRect
            self.char.detectDoor = self.detectDoor

        # once see
        # if self.char.see(self.barrierRect, self.kirby.position) == 1:
            # self.char.wandering.gochasing()

    def updateMap(self, mapName):
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
