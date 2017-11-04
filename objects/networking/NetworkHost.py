from panda3d.core import QueuedConnectionManager, QueuedConnectionListener,\
                         QueuedConnectionReader, ConnectionWriter
from panda3d.core import ConfigVariableInt
from panda3d.core import PointerToConnection, NetAddress, NetDatagram
from objects.defaultConfig.DefaultConfig import *
from direct.task import Task

class NetworkHost ():
    """
        Handles networking with one or more clients. This class is essentially
         a server that handles the communication of GameManager's game logic.
        One player will have a NetworkHost and the rest of players will have
         NetworkClients.
    """
    def __init__ (self):
        self._connManager = QueuedConnectionManager()
        self._loadConfig()
        self._activeConns = [] # Active connections list.
        self._isActive = False

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
        self._backlog = ConfigVariableInt("max-backlog",
                                          DEFAULT_MAX_BACKLOG).getValue()

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
        print ("[Host Started]")

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
                self._activeConnections.append(newConnection)
                # Begin reading messages from this new connection:
                self._connReader.addConnection(newConnection)
        return Task.cont # Repeat this call on an interval

    def _onReaderPoll (self, taskdata):
        """
            Called on an interval to interpret messages from the reader.
        """
        if self._connReader.dataAvailable():
            newDatagram = NetDatagram()
            # Double check to make sure (Multithreading safety):
            if self._connReader.getData(datagram):
                self._interpretDatagram(newDatagram)
        return Task.cont # Repeat this call on an interval

    def _interpretDatagram (self, datagram):
        """
            Interprets a received datagram and performs actions based on its
             values.
        """
        pass

    def isHosting (self):
        """
            Returns whether this NetworkHost is actively hosting.
        """
        return self._isActive
