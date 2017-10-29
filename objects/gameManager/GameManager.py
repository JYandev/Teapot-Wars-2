from objects.localPlayer.PlayerController import PlayerController
from objects.tileMap.TileMap import TileMap
from panda3d.core import Point2D

from direct.gui.DirectGui import DirectFrame
from direct.gui.DirectGui import DirectButton

TITLE_SCREEN_BACKGROUND_PATH = "objects/mainMenu/TitleScreen.png"

class GameManager ():
    """
        Controls all game state and flow.
        This class has two main modes: a client mode, and a server mode.
    """
    def __init__ (self):
        pass

    def startMainMenu (self):
        _drawMainMenu()

    def runTest (self):
        self._tileMap = TileMap()
        spawnPoint = self._tileMap.getRandomFloor()
        self._localPlayer = PlayerController(spawnPoint, self)

    def getTileMap (self):
        return self._tileMap

def _drawMainMenu ():
    """
        Sets up main menu and draws GUI to screen.
        Only supports aspect ratios >= 1 (where width is at least height)
    """
    # Set background color to black to cover any possible incorrect scaling:
    #base.setBackgroundColor(0,0,0)
    winWidth = base.getAspectRatio() * 2
    backgroundFrame = DirectFrame(parent=base.a2dTopLeft,
                                  frameSize=(0,winWidth, -2, 0),
                                  frameTexture=TITLE_SCREEN_BACKGROUND_PATH)
    b = DirectButton(parent=backgroundFrame,
                     pos=(0, 0, 0),
                     frameSize=(0, winWidth/2, -1, 0),
                     text = ("Host Game"), )
    b2 = DirectButton(parent=backgroundFrame,
                     pos=(winWidth/2, 0, 0),
                     frameSize=(0, winWidth/2, -1, 0),
                     text = ("Host Game"), )
