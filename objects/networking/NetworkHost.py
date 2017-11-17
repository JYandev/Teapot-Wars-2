from panda3d.core import QueuedConnectionManager, QueuedConnectionListener,\
                         QueuedConnectionReader, ConnectionWriter
from panda3d.core import ConfigVariableInt
from panda3d.core import PointerToConnection, NetAddress, NetDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator
from objects.defaultConfig.DefaultConfig import *
from objects.defaultConfig.Consts import *
from direct.task import Task
from objects.networking.NetworkMessages import *
import socket, json, sys

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

    def sendToClient (self, conn, msgType, command, large=False):
        """
            Writes and sends a new message to a client at the other end of conn.
        """
        if large:
            newMsg = createLargeMessage(msgType, command)
        else:
            newMsg = createMessage(msgType, command)
        print("[Server Sending %s message type %s]"%(str(conn), str(msgType)))
        self._connWriter.send(newMsg, conn)

    def sendToAll (self, conn, msgType, command, large=False):
        """
            Writes and sends a new message to all connected clients.
        """
        for conn in self._activeConns:
            self.sendToClient(conn, msgType, command, large)

    def _interpretDatagram (self, datagram):
        """
            Interprets a received datagram and performs actions based on its
             values.
        """
        msg = PyDatagramIterator(datagram)
        if msg.getUint8() == DEBUG_MESSAGE:
            print (msg.getString())

    def isHosting (self):
        """
            Returns whether this NetworkHost is actively hosting.
        """
        return self._isActive

    # === [Gameplay specific] ===:
    def onClientConnected (self, clientConn):
        """
            If we have a map and/or any positional data, give it to this client.
        """
        tileMap = self._gameManager.getTileMap()
        if tileMap != None:
            data = tileMap.getTileMapStr()
            self.sendToClient(clientConn, MAP_MESSAGE, data, True)
    # === ===
