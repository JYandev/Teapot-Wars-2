# This is a namespace containing all types of Network Messages.
from direct.distributed.PyDatagram import PyDatagram
import sys, json
from .PlayerInfo import PlayerInfo

DEBUG_MESSAGE = 1
MAP_MESSAGE = 2
UPDATE_PLAYER_INFO = 3
SPAWN_CHARACTER = 4
SYNC_ACTION = 5
SYNC_HEALTH = 6
SYNC_DEATH = 7

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
    return createMessage(UPDATE_PLAYER_INFO, newData)

def createSpawnCharacterMessage (gameObject, objID):
    """
        Character Type is a string representing the type of character "teapot",
         etc.; objID is a string representing the gameObject's ID - usually
         linked to connectionID (unless its the AI own by 'host') ; initPos is
         a tuple representing the row/col position of the object.
    """
    characterType = gameObject.getCharacterTypeEnum()
    posToParse = gameObject.getGridPosition()
    initPos = (posToParse.getX(), posToParse.getY())
    newData = {'charType':characterType, 'objID':objID, 'pos':initPos}
    newJson = json.dumps(newData)
    return createMessage(SPAWN_CHARACTER, newJson)

def createSyncActionMessage (objID, actionID, **kwargs):
    newData = {'objID':objID, "actionID":actionID, **kwargs}
    newJson = json.dumps(newData)
    return createMessage(SYNC_ACTION, newJson)

def createSyncHealthMessage (cID, newHealth):
    newData = {'objID':cID, "newHealth":newHealth}
    newJson = json.dumps(newData)
    return createMessage(SYNC_HEALTH, newJson)

def createSyncDeathMessage (cID):
    newData = {'objID':cID}
    newJson = json.dumps(newData)
    return createMessage(SYNC_DEATH, newJson)
