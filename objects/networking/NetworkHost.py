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
        self._creatures = dict() # Creates by cID.

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
            self._onActionSyncHandler(dataDict)

    def isHosting (self):
        """
            Returns whether this NetworkHost is actively hosting.
        """
        return self._isActive

    def registerNewCID (self):
        newCID = "host" + str(self._creatureIDCount)
        self._creatureIDCount += 1
        return newCID

    # === [Gameplay specific] ===
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
        msg = createSpawnCharacterMessage(gameObject, gameObject.getCID())
        self.sendToAll(msg, SPAWN_CHARACTER)

    def _onSpawnHandler (self, dataDict):
        """ Handles networking spawning characters """
        # Spawn object locally if the object at cID doesn't already exist.
        if not 'objID' in self._creatures.keys():
            # Spawn object of charType at pos
            objectType = getCharacterTypeAsClass(dataDict['charType'])
            newPos = Point2D(dataDict['pos'][0], dataDict['pos'][1])
            newChar = objectType(parentCtrlr=None, cID=dataDict['objID'],
                                 coords=newPos)
            self._creatures[dataDict['objID']] = newChar
        else:
            #TODO Overwrite the old object
            pass

    def _onActionSyncHandler (self, dataDict):
        """
            Attempts to queue an action for execution on a target denoted by
             dataDict['objID']
        """
        syncedAction = ACTION_NETWORKING_DICT[dataDict['actionID']]
        # Add a few local variables to dataDict:
        targetObj = self._creatures[dataDict['objID']] # TODO Maybe make this part of dataDict!
        dataDict['tileMap'] = self._gameManager.getTileMap()

        # Create the newAction
        newAction = syncedAction(targetObj, **dataDict)
        targetObj.startAction(newAction) # queue or start the new action

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
            # Don't send an info message about the player to the same player!
            newInfoMsg = createPlayerInfoMessage(self._playerInfo[player])
            self.sendToAll(newInfoMsg, UPDATE_PLAYER_INFO)

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
