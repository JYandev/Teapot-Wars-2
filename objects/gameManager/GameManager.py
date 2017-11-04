from objects.localPlayer.PlayerController import PlayerController
from objects.tileMap.TileMap import TileMap
from panda3d.core import Point2D
from objects.mainMenu.MainMenu import MainMenu
from objects.networking.NetworkHost import NetworkHost
from objects.networking.NetworkClient import NetworkClient

class GameManager ():
    """
        Controls all game state and flow.
        This class has two main modes: a client mode, and a server mode.
    """
    def __init__ (self):
        self._networkHost = None
        self._networkClient = None

    def startMainMenu (self):
        mainMenu = MainMenu(self)
        mainMenu.draw()

    def runTest (self):
        self._tileMap = TileMap()
        spawnPoint = self._tileMap.getRandomFloor()
        self._localPlayer = PlayerController(spawnPoint, self)

    def getTileMap (self):
        return self._tileMap

    def startHostGame (self):
        """
            Initializes the NetworkHost and begins the game process.
        """
        # If we somehow are already hosting, do nothing:
        if self._networkHost and self._networkHost.isHosting():
            return
        self._networkHost = NetworkHost()
        self._networkHost.startHost()

    def startJoinGame (self, ipAddress):
        """
            Creates and starts the NetworkClient and begins the game process.
        """
        self._networkClient = NetworkClient()
        self._networkClient.startClient()
