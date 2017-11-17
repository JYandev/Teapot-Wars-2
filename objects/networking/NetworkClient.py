from panda3d.core import QueuedConnectionManager, QueuedConnectionReader,\
                         ConnectionWriter
from panda3d.core import ConfigVariableInt
from panda3d.core import PointerToConnection, NetAddress, NetDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator
from direct.task import Task
from objects.defaultConfig.DefaultConfig import *
from objects.defaultConfig.Consts import *
from objects.networking.NetworkMessages import *
import sys

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
            taskMgr.add(self._onReaderPoll,"Poll the connection reader",-40)
            self._gameManager.onClientJoinedParty() # GameManager callback

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

    def sendMessage (self, msgType, command):
        """
            Writes and sends a new message to the server.
        """
        newMsg = createMessage(msgType, command)
        print("[Client Sending %s message type %s]"%(str(self._connection),
                                                     str(msgType)))
        self._connWriter.send(newMsg, self._connection)

    def _interpretDatagram (self, datagram):
        """
            Interprets a received datagram and performs actions based on its
             values.
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
