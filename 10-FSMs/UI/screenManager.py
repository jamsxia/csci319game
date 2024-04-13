from FSMs import ScreenManagerFSM
from . import TextEntry, EventMenu
from utils import vec, RESOLUTION, SoundManager
from gameObjects.engine import GameEngine

from pygame.locals import *


class ScreenManager(object):

    def __init__(self, level="levelOneText.txt"):
        self.level = level
        self.game = GameEngine(level)  # Add your game engine here!
        self.state = ScreenManagerFSM(self)
        self.pausedText = TextEntry(vec(0, 0), "Paused")
        self.bulletNum = TextEntry(vec(0, 0), "Paused")
        ##self.pausedText = TextEntry(vec(0, 0), "Paused")
        ##self.bulletNum= TextEntry(vec(0, 0), "Paused")

        size = self.pausedText.getSize()
        midpoint = RESOLUTION // 2 - size
        self.pausedText.position = vec(*midpoint)

        self.mainMenu = EventMenu("background.png", fontName="default8")
        self.infoMenu = EventMenu("background.png", fontName="default8")
        self.mainMenu.addOption("start", "Press 1 to start Game",
                                RESOLUTION // 2 - vec(0, 50),
                                lambda x: x.type == KEYDOWN and x.key == K_1,
                                center="both")
        self.mainMenu.addOption("exit", "Press 2 to exit Game",
                                RESOLUTION // 2,
                                lambda x: x.type == KEYDOWN and x.key == K_2,
                                center="both")
        self.mainMenu.addOption("info", "Press I to see instructions",
                                RESOLUTION // 2 + vec(0, 50),
                                lambda x: x.type == KEYDOWN and x.key == K_i,
                                center="both")
        self.infoMenu.addOption("warning", "click esq to close info",
                                RESOLUTION // 2 - vec(0, 90),
                                None,
                                center="both")
        self.infoMenu.addOption("movement", "move: arrows",
                                RESOLUTION // 2 - vec(0, 40),
                                None,
                                center="both")
        self.infoMenu.addOption("shoot", "shoot:s (u have bullet(s)?",
                                RESOLUTION // 2,
                                None,
                                center="both")
        self.infoMenu.addOption("inheriting", "taking over: space",
                                RESOLUTION // 2 + vec(0, 40),
                                None,
                                center="both")

    def draw(self, drawSurf):
        if self.state.isInGame():
            self.game.draw(drawSurf)
            self.game.drawBack(drawSurf)
            if self.state == "paused":
                self.pausedText.draw(drawSurf)
        elif self.state == "mainMenu":
            self.mainMenu.draw(drawSurf)
        elif self.state == "info":
            self.infoMenu.draw(drawSurf)

    def handleEvent(self, event):
        sm = SoundManager.getInstance()
        # print(self.state)
        if self.state in ["game", "paused"]:
            if (event.type == KEYDOWN and event.key == K_m):
                self.state.quitGame()

            elif event.type == KEYDOWN and event.key == K_p:
                self.state.pause()

            else:
                self.game.handleEvent(event)
            if (event.type == KEYDOWN and event.key == K_i):
                self.state.openInfo()
        elif self.state == "mainMenu":
            choice = self.mainMenu.handleEvent(event)

            if choice == "start":
                self.state.startGame()
                sm.playBGM("Goblin_Tinker_Soldier_Spy.mp3")
            elif choice == "exit":
                return "exit"
            if event.type == KEYDOWN and event.key == K_i:
                self.state.openInfo()

        if (self.state == "info"):
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                self.state.closeInfo()

    def update(self, seconds):
        if self.state == "game":
            self.game.update(seconds)
        elif self.state == "mainMenu":
            self.mainMenu.update(seconds)
        if self.game.endGame == 1:
            self.game = GameEngine(self.level)  # copy
