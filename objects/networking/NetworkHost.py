from panda3d.core import QueuedConnectionManager, QueuedConnectionListener,\
                         QueuedConnectionReader, ConnectionWriter
from panda3d.core import ConfigVariableInt, Point2D
from panda3d.core import PointerToConnection, NetAddress, NetDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator
from objects.defaultConfig.DefaultConfig import *
from objects.defaultConfig.Consts import *
from direct.task import Task
from objects.networking.NetworkMessages import *
import socket, json, sys
from .PlayerInfo import PlayerInfo
from objects.characters.CharacterNetworkingUtilities import \
                                                         getCharacterTypeAsClass
from direct.interval.FunctionInterval import Func

class NetworkHost ():
    """
        Handles networking with one or more clients. This class is essentially
         a server that handles the communication of GameManager's game logic.
        One player will have a NetworkHost and the rest of players will have
         NetworkClients.
    """
    def __init__ (self, gameManager):
        self._connManager = QueuedConnectionManager()
        self._loadConfig()
        self._activeConns = [] # Active connections list.
        self._isActive = False
        self._backlog = HOST_MAX_BACKLOG
        self._gameManager = gameManager
        self._playerInfo = dict() # connections by connectionID (cID)
        self._creatures = dict() # Creatures by cID.

        self._creatureIDCount = 0

    def _initListener (self):
        """
            Initializes this NetworkHost's connection listener.
        """
        self._connListener = QueuedConnectionListener(self._connManager, 0)
        self._tcpSocket = connManager.openTCPServerRendezvous(self._portAddress,
                                                              self._backlog)
        self._connListener.addConnection(self._tcpSocket)

    def _loadConfig (self):
        """
            Loads network configuration defaults.
        """
        self._portAddress = ConfigVariableInt("default-port",
                                              DEFAULT_PORT).getValue()

    def startHost (self):
        """
            Finishes initialization and begins listening.
        """
        # Initialize Reader and Writer:
        self._connReader = QueuedConnectionReader(self._connManager, 0)
        self._connWriter = ConnectionWriter(self._connManager, 0)
        # Initialize Listener:
        self._connListener = QueuedConnectionListener(self._connManager, 0)
        self._tcpSocket = self._connManager.openTCPServerRendezvous(
                                            self._portAddress, self._backlog)
        self._connListener.addConnection(self._tcpSocket)
        # Begin handling messages (start listening):
        taskMgr.add(self._onListenerPoll,"Poll the connection listener",-39)
        taskMgr.add(self._onReaderPoll,"Poll the connection reader",-40)
        self._isActive = True
        print ("[Host Started at %s]" % socket.gethostbyname(
                                            socket.gethostname()))

        self._gameManager.onHostInitialized()

    def _onListenerPoll(self, taskdata):
        """
            Updates list of connections based on the listener's current
             findings.
            Does not read messages. See onReaderPoll().
            (Assumes self._connListener has been initialized)
        """
        # Check for new connections:
        if self._connListener.newConnectionAvailable():
            rendezvous = PointerToConnection()
            netAddress = NetAddress()
            newConnection = PointerToConnection()
            # If we have a new connection, add it to our list:
            if self._connListener.getNewConnection(rendezvous,netAddress,
                                                   newConnection):
                newConnection = newConnection.p()
                print ("[Host Received New Connection: %s]" % netAddress)
                self._activeConns.append(newConnection)
                # Begin reading messages from this new connection:
                self._connReader.addConnection(newConnection)
                # activate the onClientConnected functionalities:
                self.onClientConnected(newConnection)
        return Task.cont # Repeat this call on an interval

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

    def sendToClient (self, newMsg, conn, msgType):
        """
            Sends a new message to a client at the other end of conn.
        """
        print("[Server Sending %s message type %s]"%(str(conn), str(msgType)))
        self._connWriter.send(newMsg, conn)

    def sendToAll (self, newMsg, msgType):
        """
            Writes and sends a new message to all connected clients.
        """
        for conn in self._activeConns:
            self.sendToClient(newMsg, conn, msgType)

    def _interpretDatagram (self, datagram):
        """
            Interprets a received datagram and performs actions based on its
             values.
        """
        msg = PyDatagramIterator(datagram)
        msgType = msg.getUint8()
        if msgType == DEBUG_MESSAGE:
            print (msg.getString())
        elif msgType == UPDATE_PLAYER_INFO:
            data = msg.getString()
            self._updatePlayerInfoHandler(datagram.getConnection().this, data)
        elif msgType == SPAWN_CHARACTER:
            data = msg.getString()
            dataDict = json.loads(data)
            self._onSpawnHandler(dataDict)
        elif msgType == SYNC_ACTION:
            data = msg.getString()
            dataDict = json.loads(data)
            self._onActionSyncHandler(dataDict, datagram.getConnection())
        elif msgType == SYNC_RESPAWN:
            data = msg.getString()
            dataDict = json.loads(data)
            self._onRespawnRequestReceived(dataDict)
        elif msgType == WIN_STATE:
            data = msg.getString()
            self._onGameWon(data)

    def isHosting (self):
        """
            Returns whether this NetworkHost is actively hosting.
        """
        return self._isActive

    def registerNewCID (self):
        newCID = "host" + str(self._creatureIDCount)
        self._creatureIDCount += 1
        return newCID

    # === [Local Client to Network] ===
    def onCreatureDeath (self, creature):
        """
            Sends a creature death message to all connected clients.
        """
        msg = createSyncDeathMessage(creature.getCID())
        self.sendToAll(msg, SYNC_DEATH)

    def onLocalPlayerRespawn (self, creature, newLocation):
        """
            Respawns the local player and sends a sync message to all remotes.
        """
        # Fulfill local player request to respawn:
        creature.respawn(newLocation)
        # Refill the creature's HP (Automatically syncs!):
        creature.takeDamage(-1*creature.getMaxHealth())
        # Spawn on all connected clients:
        msg = createRespawnMessage(creature.getCID(), newLocation)
        self.sendToAll(msg, SYNC_RESPAWN)

    def localPlayerWins (self):
        """
            End the game display the
             win screen.
        """
        self._gameManager.onWinStateAchieved(self._playerInfo['host'])
        msg = createWinMessage(self._playerInfo['host'])
        self.sendToAll(msg, WIN_STATE)

    def updateLocalPlayerInfo (self, info=None):
        """
            Updates info for this local player and sends it to all
             connected clients.
        """
        if not info:
            self._playerInfo['host'] = PlayerInfo(cID="host")
        else: # If info == None, we are just initializing.
            self._playerInfo['host'] = info
            infoMsg = createPlayerInfoMessage(info)
            self.sendToAll(infoMsg, UPDATE_PLAYER_INFO)
    # === ===

    # === [Gameplay specific] ===
    def _onGameWon (self, data):
        """
            Boo. A remote client won.
            Oh well. Still have to sync that win across all other clients.
        """
        # Show winner locally:
        winnerData = PlayerInfo(fromJson=data)
        self._gameManager.onWinStateAchieved(winnerData)
        msg = createWinMessage(winnerData)
        self.sendToAll(msg, WIN_STATE)

    def syncAction (self, cID, actionID, **kwargs):
        """
            The local player has performed an action that must be synced across
             the network. Send a message to all clients telling them to perform
             a related action on that character.
        """
        msg = createSyncActionMessage(cID, actionID, **kwargs)
        self.sendToAll(msg, SYNC_ACTION)

    def spawnGameObject (self, gameObject):
        """
            Tracks the given gameObject and sends it to all clients.
        """
        # First, track it locally:
        self._creatures[gameObject.getCID()] = gameObject
        # Send to all clients:
        msg = createSpawnCharacterMessage(gameObject, gameObject.getCID())
        self.sendToAll(msg, SPAWN_CHARACTER)

    def dropItem (self, itemEnum, pos):
        """
            Spawn a new item locally and sync!
        """
        itemID = self.registerNewCID()
        # Create item locally:
        newItem = ITEM_ID_DICT[itemEnum](self._gameManager, itemID, coords=pos)
        self._gameManager.getTileMap().spawnItem(newItem, pos)
        # Track new item:
        self._creatures[itemID] = newItem
        msg = createSpawnItemMessage(newItem)
        self.sendToAll(msg, SPAWN_ITEM)

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
            print("[Server Spawned %s]" % dataDict['objID'])
            #TODO If we have a player info for this player, use their name for the displayName
        else:
            # Ignore Overwrite
            pass
        # Tell all other clients to spawn objects:
        newMsg = createSpawnCharacterMessage(self._creatures[dataDict['objID']],
                                             dataDict['objID'])
        self.sendToAll(newMsg, SPAWN_CHARACTER)

    def _onActionSyncHandler (self, dataDict, msgConn):
        """
            Attempts to queue an action for execution on a target denoted by
             dataDict['objID']
        """
        copyMsg = createSyncActionMessage(**dataDict)

        syncedAction = ACTION_NETWORKING_DICT[dataDict['actionID']]
        # Add a few local variables to dataDict:
        targetObj = self._creatures[dataDict['objID']] # TODO Maybe make this part of dataDict!
        dataDict['tileMap'] = self._gameManager.getTileMap()
        if 'targetCID' in dataDict: # If there is another target:
            # Assign the target:
            dataDict['target'] = self._creatures[dataDict['targetCID']]
        dataDict['isServer'] = True # Let sync function know we are server

        # Create the newAction
        newAction = syncedAction(targetObj, **dataDict)
        targetObj.startAction(newAction) # queue or start the new action
        # Send action to all clients except the client that sent the sync msg:
        for client in self.getAllClientsExcept(msgConn):
            self.sendToClient(copyMsg, client, SYNC_ACTION)

    def _onRespawnRequestReceived (self, dataDict):
        """
            Respawns the remote clients character in a new position and then
             syncs to all clients (including the one who requested).
        """
        newPos = self._gameManager.getTileMap().getRandomEmptyFloor()
        targetObj = self._creatures[dataDict['objID']]
        # Set the target's HP to full and sync that:
        targetObj.takeDamage(-1*targetObj.getMaxHealth())
        targetObj.respawn(newPos)
        # Sync the respawn to all clients:
        newMsg = createRespawnMessage(targetObj.getCID(), newPos)
        self.sendToAll(newMsg, SYNC_RESPAWN)

    def getAllClientsExcept (self, exceptConn):
        clientList = list()
        for conn in self._activeConns:
            if conn != exceptConn:
                clientList.append(conn)
        return clientList

    def onClientConnected (self, clientConn):
        """
            If we have a map and/or any positional data, give it to this client.
            Also signal to the GameManager and all remote clients that a new
             player connected!
        """
        connID = clientConn.this
        tileMap = self._gameManager.getTileMap()
        if tileMap != None:
            data = tileMap.getTileMapStr()
            msg = createMapMessage(data)
            self.sendToClient(msg, clientConn, MAP_MESSAGE)
        # Send player info to the new client:
        for player in self._playerInfo:
            # Don't send an info message about the player to the same player!
            if player != connID:
                newInfoMsg = createPlayerInfoMessage(self._playerInfo[player])
                self.sendToClient(newInfoMsg, clientConn,
                                  UPDATE_PLAYER_INFO)
        # Send all creatures to the new client:
        for creatureID in self._creatures:
            newMsg = createSpawnCharacterMessage(self._creatures[creatureID],
                                                 creatureID)
            self.sendToClient(newMsg, clientConn, SPAWN_CHARACTER)

    def _updatePlayerInfoHandler (self, connID, data=None):
        """
            Adds data to self._playerInfo.
            If info doesn't exist, creates a new one for clientConn.
        """
        if data != None:
            newPlayerData = PlayerInfo(fromJson=data)
        else:
            newPlayerData = PlayerInfo(cID=connID)
        # Update the playerInfo dict with the new data:
        self._playerInfo[newPlayerData.cID] = newPlayerData
        self._gameManager.updatePartyInfo(self._playerInfo, 'host')
        # Send player info to every client:
        for player in self._playerInfo:
            newInfoMsg = createPlayerInfoMessage(self._playerInfo[player])
            #Send every player to every client:
            self.sendToAll(newInfoMsg, UPDATE_PLAYER_INFO)

    def syncHealthChange (self, creatureID, newHealth):
        """
            Called after the host runs a damage/healing action on a creature.
            Lets all clients know to update to a new value.
        """
        data = createSyncHealthMessage(creatureID, newHealth)
        self.sendToAll(data, SYNC_HEALTH)
    # === ===
