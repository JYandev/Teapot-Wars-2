from objects.localPlayer.PlayerController import PlayerController
from objects.tileMap.TileMap import TileMap
from panda3d.core import Point2D

class GameManager ():
    """
        Controls all game state and flow.
        This class has two main modes: a client mode, and a server mode.
    """
    def __init__ (self):
        self.runTest()

    def startMainMenu (self):
        pass

    def runTest (self):
        self._tileMap = TileMap()
        spawnPoint = self._tileMap.getRandomFloor()
        self._localPlayer = PlayerController(spawnPoint, self)

    def getTileMap (self):
        return self._tileMap
