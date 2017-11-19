from objects.localPlayer.PlayerController import PlayerController
from objects.tileMap.TileMap import TileMap, convertDungeonFromString
from panda3d.core import Point2D
from objects.mainMenu.MainMenu import MainMenu
from objects.networking.NetworkHost import NetworkHost
from objects.networking.NetworkClient import NetworkClient
from objects.networking.NetworkMessages import *
from objects.tileMap.TileMapOrbiterCam import TileMapOrbiterCam
from objects.classSelectionMenu.ClassSelectionMenu import ClassSelectionMenu

class GameManager ():
    """
        Controls all game state and flow.
        This class has two main modes: a client mode, and a server mode.
    """
    def __init__ (self):
        self._networkHost = None
        self._networkClient = None
        self._mainMenu = None
        self._classSelectionMenu = None
        self._tilemapOrbiterCam = None
        self._tileMap = None
        self._localPlayer = None

    def startMainMenu (self):
        """ Draws the main menu """
        self._mainMenu = MainMenu(self)
        self._mainMenu.draw()

    def getTileMap (self):
        return self._tileMap

    def startHostGame (self):
        """
            Initializes the NetworkHost and begins the game process.
        """
        # If we somehow are already hosting, do nothing:
        if self._networkHost and self._networkHost.isHosting(): return
        self._networkHost = NetworkHost(self)
        self._networkHost.startHost()

    def startJoinGame (self, ipAddress):
        """
            Creates and starts the NetworkClient and begins the game process.
        """
        # TODO Safety check for client already connected, etc.
        self._networkClient = NetworkClient(self)
        self._networkClient.startClient(ipAddress)

    # --- Networking Interface ---
    def onClientJoinedParty (self):
        """ Start the Class Selection screen and sets up camera view """
        self._networkClient.sendMessage(DEBUG_MESSAGE, "Yo, Server! Gimme Map!")
        self._mainMenu.close()
        # Draw the class selection screen:
        self._classSelectionMenu = ClassSelectionMenu(self)
        #TODO Create part of the player UI (PartyList)

    def onClientFirstReceivedMap (self, dungeonString):
        """
            Called when the active client gets new map data from the host.
            Only should be called once in a client's lifetime.
            We received a string of tiles and their values. Convert into
             a TileMap
        """
        self._tileMap = TileMap(dungeonString)
        self._tilemapOrbiterCam = TileMapOrbiterCam(self._tileMap)

    def onHostInitialized (self):
        """
            Generates a dungeon and shares it with clients. Starts the class
             selection menu and sets up the view for the game.
        """
        self._mainMenu.close()
        self._tileMap = TileMap() # Generate dungeon
        # Create camera controller for visual tour of generated dungeon:
        self._tilemapOrbiterCam = TileMapOrbiterCam(self._tileMap)
        # Draw the class selection screen:
        self._classSelectionMenu = ClassSelectionMenu(self)
        #TODO Create part of the player UI (PartyList)

    def createPlayer (self, newName, newClass):
        """
            Called at the end of the class selection menu sequence.
            Create a new player and remove the tileOrbiterCam and classSelection
             UI.
        """
        self._tilemapOrbiterCam.destroy()
        self._classSelectionMenu.close()
        #TODO Tell other players to spawn an object with newName and newClass
        newSpawnPosition = self._tileMap.getRandomFloor() #TODO Make this get the dungeon's spawn position
        self._localPlayer = PlayerController(newSpawnPosition, self)
