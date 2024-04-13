from . import AbstractGameFSM
from statemachine import State


class ScreenManagerFSM(AbstractGameFSM):
    mainMenu = State(initial=True)
    game = State()
    paused = State()
    info = State()

    pause = game.to(paused) | paused.to(game) | \
        mainMenu.to.itself(internal=True)

    startGame = mainMenu.to(game)
    quitGame = game.to(mainMenu) | \
        paused.to.itself(internal=True)
    openInfo = mainMenu.to(info) | game.to(info) | paused.to(info)
    closeInfo = info.to(game) | info.to(mainMenu) | info.to(paused)
    # def on_enter_info(self):

    def isInGame(self):
        return self == "game" or self == "paused"

    def on_enter_game(self):
        self.obj.game.kirby.updateMovement()
