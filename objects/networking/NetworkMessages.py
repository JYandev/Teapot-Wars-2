# This is a namespace containing all types of Network Messages.
from direct.distributed.PyDatagram import PyDatagram
import sys

DEBUG_MESSAGE = 1
MAP_MESSAGE = 2

def createMessage (msgType, command):
    """
        Returns a new string command of the given type.
    """
    newPyDatagram = PyDatagram()
    newPyDatagram.addUint8(msgType)
    newPyDatagram.addString(command)
    return newPyDatagram

def createLargeMessage (msgType, command):
    """
        Returns a new string command of the given type.
    """
    newPyDatagram = PyDatagram()
    newPyDatagram.addUint8(msgType)
    newPyDatagram.addString32(command)
    return newPyDatagram
