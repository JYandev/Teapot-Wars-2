# This is a namespace containing all types of Network Messages.
from direct.distributed.PyDatagram import PyDatagram
import sys
from .PlayerInfo import PlayerInfo

DEBUG_MESSAGE = 1
MAP_MESSAGE = 2
UPDATE_PLAYER_INFO = 3

def createMessage (msgType, command):
    """
        Returns a new string command of the given type.
    """
    newPyDatagram = PyDatagram()
    newPyDatagram.addUint8(msgType)
    newPyDatagram.addString(command)
    return newPyDatagram

def createMapMessage (command):
    """
        Returns a new map message of the given type.
    """
    newPyDatagram = PyDatagram()
    newPyDatagram.addUint8(MAP_MESSAGE)
    newPyDatagram.addString32(command)
    return newPyDatagram

def createPlayerInfoMessage (playerInfo):
    newData = playerInfo.toJson()
    print("Yahaha", newData)
    return createMessage(UPDATE_PLAYER_INFO, newData)
