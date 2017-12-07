"""
    GameManager is first object instantiated after all of the Panda3D setup
     finishes in main.py
    GameManager controls the high-level state of the game, from the main menu,
     all the way through the game until the win-state. It also bridges the
     connection from local player to the server.
    Code is split into 3 main sections for readability:
    - High-level Flow
    - Local Client to Networking Bridge (Player did something, Server needs to
       be notified)
    - Networking to Local Client Bridge (Server did something, our Local Client
       needs to update)
"""
from objects.localPlayer.PlayerController import PlayerController
from objects.tileMap.TileMap import TileMap, convertDungeonFromString
from panda3d.core import Point2D
from objects.mainMenu.MainMenu import MainMenu
from objects.networking.NetworkHost import NetworkHost
from objects.networking.NetworkClient import NetworkClient
from objects.networking.NetworkMessages import *
from objects.tileMap.TileMapOrbiterCam import TileMapOrbiterCam
from objects.classSelectionMenu.ClassSelectionMenu import ClassSelectionMenu
from objects.gameUI.PartyListUI import PartyListUI
from objects.gameUI.WinScreen import WinScreen
from objects.networking.PlayerInfo import PlayerInfo
from objects.enemy.EnemyController import EnemyController
from objects.item.BagOfTeaPlusThree import BagOfTeaPlusThree
from objects.item.ItemType import ItemType
import random
from objects.defaultConfig.Consts import *
from objects.musicSystem.MusicSystem import MusicSystem

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
        self._partyList = None
        self._winScreen = None
        self._hostPlayerCID = None
        self._musicSystem = MusicSystem()
        self._hostedEnemies = list()

    # === High-level Flow ===
    def startMainMenu (self):
        """ Draws the main menu """
        self._mainMenu = MainMenu(self)
        self._mainMenu.draw()

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

    # === ===

    # === Local Client to Networking Bridge ===
    def onLocalPlayerAction (self, cID, actionID, **kwargs):
        """
            Tell our client/host to update the network with information on the
             action.
        """
        if self._networkHost:
            self._networkHost.syncAction(cID, actionID, **kwargs)
        else:
            self._networkClient.syncAction(actionID, **kwargs)

    def onCreatureDeath (self, creature, amClient):
        """
            Called on the host when a creature's HP drops to or below zero.
            Called on the client when a creature dies on the host and a message
             is received.
            Removes the creature from the tileMap, and, in the hosts case,
             notifies all clients.
        """
        self._tileMap.despawnCreature(creature)
        if not amClient:
            if creature.getItem() != None:
                # Drop item and sync!
                self._networkHost.dropItem(creature.getItem(),
                                           creature.getGridPosition())
            self._networkHost.onCreatureDeath(creature)

    def onCreatureHealthChanged (self, creature):
        """
            Called after the host player updates damage on a creature.
            Sync the health change to all other clients!
        """
        if self.isHost():
            self._networkHost.syncHealthChange(creature.getCID(),
                                               creature.getHealth())

    def updateLocalInfoAndSync (self, info):
        """
            Syncs the local player's info with the server and other
             networkClients.
        """
        if self._networkHost:
            self._networkHost.updateLocalPlayerInfo(info)
        elif self._networkClient:
            self._networkClient.updateLocalPlayerInfo(info)

    def localPlayerWinStateAchieved (self):
        if self.isHost():
            self._networkHost.localPlayerWins()
        else:
            self._networkClient.localPlayerWins()

    def respawnLocalPlayer (self, creature):
        """
            Called when the host or client respawn's their character.
            Tell the rest of the connected players that we've respawned and
             update the tilemap accordingly if we are the host.
            Just updates the tilemap if we are only clients.
        """
        if self._networkHost:
            # Pick a random spawn location:
            newLocation = self._tileMap.getRandomEmptyFloor()
            # Tell host to sync spawn there:
            self._networkHost.onLocalPlayerRespawn(creature, newLocation)
        else:
            self._networkClient.sendPlayerRespawnRequest()
    # === ===

    # === Networking to Local Client Bridge ===
    def onLocalClientJoinedParty (self, myID):
        """ Start the Class Selection screen and sets up camera view """
        self._mainMenu.close()
        # Draw the class selection screen:
        self._classSelectionMenu = ClassSelectionMenu(self, myID)
        self._partyList = PartyListUI()
        self._networkClient.updateLocalPlayerInfo()

    def updatePartyInfo (self, playersInfo, myID):
        """
            Called both on servers and clients when a new person connects.
            Updates the partylistui element with the new info.
        """
        if self._partyList:
            self._partyList.updateInfo(playersInfo, myID)

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
        self._networkHost.registerLocalCID()
        self._hostPlayerCID = self._networkHost.getMyCID()
        # Draw the class selection screen:
        self._classSelectionMenu = ClassSelectionMenu(self, self._hostPlayerCID)
        self._partyList = PartyListUI()
        self._networkHost.updateLocalPlayerInfo()
        # Create the enemies:
        self._createGameEnemies()

    def onWinStateAchieved (self, winnerData):
        """
            Displays the game over GUI and displays a winner.
            Also performs cleanup of the game elements.
        """
        self._winScreen = WinScreen(self, winnerData)
        # If we are host, tell the AI creatures to stop acting:
        if self.isHost():
            for enemy in self._hostedEnemies:
                enemy.deactivateAI()
    # === ===

    # === Game Helpers ===
    def createPlayer (self, playerInfo):
        """
            Called at the end of the class selection menu sequence.
            Create a new player and remove the tileOrbiterCam and classSelection
             UI.
        """
        # Destroy menu stuff and tour camera:
        self._tilemapOrbiterCam.destroy()
        self._classSelectionMenu.close()
        # Pick a random spawn point:
        newSpawnPosition = self._tileMap.getRandomEmptyFloor()
        # Get an ID for this new character:
        if self._networkHost:
            cID = self._networkHost.getMyCID()
        else:
            cID = self._networkClient.getCID()

        newClass = CLASSES_DICT[playerInfo.cClass]
        self._localPlayer = PlayerController(self, cID, newSpawnPosition,
                                             newClass)
        if self._networkHost:
            self._networkHost.spawnGameObject(self._localPlayer.getCharacter())
        else:
            self._networkClient.spawnGameObject(self._localPlayer\
                                                    .getCharacter())

    def _createGameEnemies (self):
        """
            Creates a bunch of enemies and assigns one to be the key holder.
        """
        enemies = []
        for i in range(10):
            newSpawnPosition = self._tileMap.getRandomFloor()
            cID = self._networkHost.registerNewCID()
            newEnemy = EnemyController(self, cID, newSpawnPosition)
            enemies.append(newEnemy.getCharacter())
            # Add these enemies to a list so that we can deactivate them later:
            self._hostedEnemies.append(newEnemy)
            # Sync their spawns:
            self._networkHost.spawnGameObject(newEnemy.getCharacter())
        # One random enemy holds the legendary bag of tea plus three:
        #chosenEnemy = enemies[random.randint(0, len(enemies)-1)]

        # TODO Remove once TP3 is over: (simply makes all enemies hold item)
        for chosenEnemy in enemies:
            chosenEnemy.assignItem(ItemType.BagOfTeaPlusThree)
    # === ===

    # === Get/Set ===
    def getTileMap (self):
        return self._tileMap

    def isHost (self):
        """ Returns whether we are hosting or remote """
        return self._networkHost != None
    # === ===
