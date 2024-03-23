import pygame
from UI import ScreenManager
from utils import RESOLUTION, UPSCALED, SpriteManager

textMatching = {"tc": (1, 2), "lc": (0, 1), "rc": (2, 1), "bc": (1, 0), "wtl": (
    0, 4), "wbl": (0, 5), "wmt": (1, 4), "wmb": (1, 5), "wtr": (2, 4), "wbr": (2, 5), "h": (1, 3), "v": (3, 1), "c": (3, 3), "dw": (4, 4)}

levelOneText = 1


def main():
    # Initialize the module
    pygame.init()

    pygame.font.init()

    # Get the screen
    screen = pygame.display.set_mode(list(map(int, UPSCALED)))
    drawSurface = pygame.Surface(list(map(int, RESOLUTION)))
    ##initial_level = "levelOneText.txt"
    gameEngine = ScreenManager()
    # kirby=gameEngine.kirby()
    '''
    levelOneText = open("levelOneText.txt", 'r')
    levelOneText = [i.split(',')
                    for i in levelOneText.readlines()]
    # print(levelOneText)
    # print(levelOneText[1][-2])
    settingImage = [[0]*14 for i in range(14)]
    i, j = 0, 0
    for line in levelOneText:
        for word in line:
            if ("\n" in word):
                word = word[:-1]
            if (word != " "):
                Image = SpriteManager.getInstance().getSprite(
                    "tiles.png", textMatching[word])
            else:
                Image = SpriteManager.getInstance().getSprite(
                    "tiles.png", (12, 0))
            settingImage[i][j] = Image
            j += 1
        j = 0
        i += 1
    wallDefaultImage = SpriteManager.getInstance().getSprite(
        "tiles.png", (4, 4))
    ceilDefaultImage = SpriteManager.getInstance().getSprite(
        "tiles.png", (1, 3))
    '''
    RUNNING = True
    # print(textMatching[" "] == None)
    while RUNNING:

        gameEngine.draw(drawSurface)
        # drawSurface.blit(testImage, (0, 16))
        # drawSurface.blit(testImage, (0, 32))
        pygame.transform.scale(drawSurface,
                               list(map(int, UPSCALED)),
                               screen)
        pygame.display.flip()
        gameClock = pygame.time.Clock()

        # event handling, gets all event from the eventqueue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                # change the value to False, to exit the main loop
                RUNNING = False
            else:
                result = gameEngine.handleEvent(event)

                if result == "exit":
                    RUNNING = False

        gameClock.tick(60)
        seconds = gameClock.get_time() / 1000
        gameEngine.update(seconds)

    pygame.quit()


if __name__ == '__main__':
    main()
