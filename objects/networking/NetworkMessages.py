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
SYNC_RESPAWN = 8
SPAWN_ITEM = 9
WIN_STATE = 10

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

def createSpawnCharacterMessage (gameObject, objID, cName=None):
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

def createRespawnMessage (cID, newLocation):
    # Convert to generic tuple because network datagram doesn't support complex:
    simplifiedPos = (newLocation.getX(), newLocation.getY())
    newData = {'objID':cID, 'pos':simplifiedPos}
    newJson = json.dumps(newData)
    return createMessage(SYNC_RESPAWN, newJson)

def createRespawnRequest (cID):
    newData = {'objID':cID}
    newJson = json.dumps(newData)
    return createMessage(SYNC_RESPAWN, newJson)

def createSpawnItemMessage (item):
    newLocation = item.getGridPosition()
    simplifiedPos = (newLocation.getX(), newLocation.getY())
    newData = {'objID':item.getCID(), "itemType":item.getItemTypeEnum(),
               'pos':simplifiedPos}
    newJson = json.dumps(newData)
    return createMessage(SPAWN_ITEM, newJson)

def createWinMessage (winnerPlayerInfo):
    newData = winnerPlayerInfo.toJson()
    return createMessage(WIN_STATE, newData)
