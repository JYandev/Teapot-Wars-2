from panda3d.core import QueuedConnectionManager, QueuedConnectionReader,\
                         ConnectionWriter
from panda3d.core import ConfigVariableInt, Point2D
from panda3d.core import PointerToConnection, NetAddress, NetDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator
from direct.task import Task
from objects.defaultConfig.DefaultConfig import *
from objects.defaultConfig.Consts import *
from objects.networking.NetworkMessages import *
import sys
from objects.networking.PlayerInfo import PlayerInfo
from objects.characters.CharacterNetworkingUtilities import \
                                                         getCharacterTypeAsClass
from direct.interval.FunctionInterval import Func

class NetworkClient ():
    """
        All remote clients will have one of these in their GameManager. This
         class communicates with a server (NetworkHost) to update game state.
    """

    def __init__ (self, gameManager):
        self._connManager = QueuedConnectionManager()
        self._timeout = CLIENT_TIMEOUT
        self._loadConfig()
        self._gameManager = gameManager
        self._playerInfo = dict() # Party Member Info
        self._creatures = dict() # Creates by cID.
        self._connection = None

    def _loadConfig (self):
        """
            Loads network configuration defaults.
        """
        self._portAddress = ConfigVariableInt("default-port",
                                              DEFAULT_PORT).getValue()

    def startClient (self, ipAddress):
        """
            Finishes client init and attempts a connection.
        """
        # Initialize Reader and Writer:
        self._connReader = QueuedConnectionReader(self._connManager, 0)
        self._connWriter = ConnectionWriter(self._connManager, 0)
        # Initialize connection:
        self._connection = self._connManager.openTCPClientConnection(
                            ipAddress, self._portAddress, self._timeout)
        if self._connection:
            print ("[Client Connected]")
            self._connReader.addConnection(self._connection)
            # Begin handling messages (start listening):
            taskMgr.add(self._onReaderPoll,"Poll the connection reader",
                        -40)
            self._gameManager.onLocalClientJoinedParty(self._connection\
                .this) # GameManager callback

    def _onReaderPoll (self, taskdata):
        """
            Called on an interval to interpret messages from the reader.
        """
        if self._connReader.dataAvailable():
            newDatagram = NetDatagram()
            # Double check to make sure (Multithreading safety):
            if self._connReader.getData(newDatagram):
                self._interpretDatagram(newDatagram)
        return Task.cont # Repeat this call on an interval

    def sendMessage (self, msg, msgType):
        """
            Sends a given message to the server.
        """
        print("[Client Sending %s message type %s]"%(str(self._connection),
                                                     str(msgType)))
        self._connWriter.send(msg, self._connection)

    def _interpretDatagram (self, datagram):
        """
            Interprets a received datagram and performs actions based on
             its values.
        """
        msg = PyDatagramIterator(datagram)
        msgType = msg.getUint8()
        if msgType == DEBUG_MESSAGE:
            print(msg.getString())
        elif msgType == MAP_MESSAGE:
            print("[Client Received Map Data]")
            if self._gameManager.getTileMap() == None:
                data = msg.getString32()
                self._gameManager.onClientFirstReceivedMap(data)
        elif msgType == UPDATE_PLAYER_INFO:
            data = msg.getString()
            self._updatePlayerInfoHandler(data)
        elif msgType == SPAWN_CHARACTER:
            data = msg.getString()
            dataDict = json.loads(data)
            self._onSpawnHandler(dataDict)
        elif msgType == SYNC_ACTION:
            data = msg.getString()
            dataDict = json.loads(data)
            self._onActionSyncHandler(dataDict)
        elif msgType == SYNC_HEALTH:
            data = msg.getString()
            dataDict = json.loads(data)
            self._onHealthSyncHandler(dataDict)
        elif msgType == SYNC_DEATH:
            data = msg.getString()
            dataDict = json.loads(data)
            self._onDeathSyncHandler(dataDict)
        elif msgType == SYNC_RESPAWN:
            data = msg.getString()
            dataDict = json.loads(data)
            self._onRespawnPermissionGranted(dataDict)
        elif msgType == SPAWN_ITEM:
            data = msg.getString()
            dataDict = json.loads(data)
            self._onItemSpawned(dataDict)
        elif msgType == WIN_STATE:
            data = msg.getString()
            self._onGameWon(data)

    def _onGameWon (self, data):
        """
            Show the win state achieved screen with the specified playerinfo as
             the winner details.
        """
        newPlayerData = PlayerInfo(fromJson=data)
        self._gameManager.onWinStateAchieved(newPlayerData)

    def _onItemSpawned(self, dataDict):
        """ The server spawned an item, handle spawning on this client """
        itemType = ITEM_ID_DICT[dataDict['itemType']]
        itemID = dataDict['objID']
        newPos = Point2D(dataDict['pos'][0], dataDict['pos'][1])
        # Create item locally:
        newItem = itemType(self._gameManager, itemID, coords=newPos)
        self._gameManager.getTileMap().spawnItem(newItem, newPos)
        # Track new item:
        self._creatures[itemID] = newItem

    def _onDeathSyncHandler(self, dataDict):
        """ Handles syncing of death for the given creature """
        deadCreature = self._creatures[dataDict['objID']]
        # Play death sequence on this character:
        deadCreature.deathSequence(amClient=True)

    def _onHealthSyncHandler (self, dataDict):
        """ Handles syncing of health values for creatures """
        print ("_onHealthSyncHandler")
        newHealth = dataDict['newHealth']
        affectedCreature = self._creatures[dataDict['objID']]

        affectedCreature.onHPModified(newHealth)

    def _onSpawnHandler (self, dataDict):
        """ Handles networking spawning characters """
        # Spawn object locally if the object at cID doesn't already exist.
        if not dataDict['objID'] in self._creatures.keys():
            # Spawn object of charType at pos
            objectType = getCharacterTypeAsClass(dataDict['charType'])
            newPos = Point2D(dataDict['pos'][0], dataDict['pos'][1])
            newChar = objectType(parentCtrlr=None, cID=dataDict['objID'],
                                 gameManager=self._gameManager, coords=newPos)
            self._creatures[dataDict['objID']] = newChar
            self._gameManager.getTileMap().spawnObject(newChar, newPos)
            print("[Client Spawned %s]" % dataDict['objID'])
            # If we have a player info for this player, use their name for the
            #  displayName:
            print (dataDict['objID'], self._playerInfo)
            if dataDict['objID'] in self._playerInfo:
                newName = self._playerInfo[dataDict['objID']].cName
                newChar.setNameDisplay(newName)
        else:
            # Ignore Overwrite
            pass

    def _updatePlayerInfoHandler (self, data):
        """
            Update our player list with a player info given by data.
        """
        newPlayerData = PlayerInfo(fromJson=data)
        self._playerInfo[newPlayerData.cID] = newPlayerData
        self._gameManager.updatePartyInfo(self._playerInfo,
                                          self._connection.this)
        # Update the creature's floating display name (unless it is ours):
        ignoreThisUpdate = False
        if self._gameManager._localPlayer:
            if newPlayerData.cID == self._gameManager._localPlayer\
                            .getCharacter().getCID():
                ignoreThisUpdate = True
        if not ignoreThisUpdate and newPlayerData.cID in self._creatures:
            self._creatures[newPlayerData.cID]\
                .setNameDisplay(newPlayerData.cName)

    def _onRespawnPermissionGranted (self, dataDict):
        """
            Respawn the given character at the given location.
        """
        targetObj = self._creatures[dataDict['objID']]
        newPos = Point2D(dataDict['pos'][0], dataDict['pos'][1])
        targetObj.respawn(newPos)

    def _onActionSyncHandler (self, dataDict):
        """
            Attempts to queue an action for execution on a target denoted by
             dataDict['objID']
        """
        syncedAction = ACTION_NETWORKING_DICT[dataDict['actionID']]
        # Add a few local variables to dataDict:
        targetObj = self._creatures[dataDict['objID']] # TODO Maybe make this part of dataDict!
        dataDict['tileMap'] = self._gameManager.getTileMap()
        if 'targetCID' in dataDict: # If there is another target:
            # Assign the target:
            dataDict['target'] = self._creatures[dataDict['targetCID']]
        dataDict['isServer'] = False # Let sync function know we are remote

        # Create the newAction
        newAction = syncedAction(targetObj, **dataDict)
        targetObj.startAction(newAction) # queue or start the new action

    def updateLocalPlayerInfo (self, info=None):
        """
            Updates info for this local player and sends it to the server.
        """
        if not info:
            initData = PlayerInfo(cID=self._connection.this)
            self._playerInfo[self._connection.this] = initData
            infoMsg = createPlayerInfoMessage(initData)
            self.sendMessage(infoMsg, UPDATE_PLAYER_INFO)
        else:
            infoMsg = createPlayerInfoMessage(info)
            self.sendMessage(infoMsg, UPDATE_PLAYER_INFO)

    def syncAction (self, actionID, **kwargs):
        """
            The local player has performed an action that must be synced across
             the network. Send a message to all clients telling them to perform
             a related action on that character.
        """
        msg = createSyncActionMessage(self._connection.this, actionID, **kwargs)
        self.sendMessage(msg, SYNC_ACTION)

    def sendPlayerRespawnRequest (self):
        msg = createRespawnRequest(self._connection.this)
        self.sendMessage(msg, SYNC_RESPAWN)

    def localPlayerWins (self):
        """
            Tell host we won. Then wait for a response.
        """
        msg = createWinMessage(self._playerInfo[self._connection.this])
        self.sendMessage(msg, WIN_STATE)

    def spawnGameObject (self, gameObject):
        """
            Tracks the given gameObject and sends it to the server
        """
        # First, track it locally:
        self._creatures[self.getCID()] = gameObject
        # Tell server to spawn it for them and everyone else:
        msg = createSpawnCharacterMessage(gameObject, self.getCID())
        self.sendMessage(msg, SPAWN_CHARACTER)

    def getCID(self):
        return self._connection.this
